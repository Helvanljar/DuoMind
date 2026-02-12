import os
import sqlite3
import json
from pathlib import Path
from typing import Optional, Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel

from .routes_auth import get_current_user_optional
from .llm_orchestrator import run_dual_research, run_compare_reconcile
from .key_resolver import resolve_keys

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "duomind.db")

# Guest requests billed to server keys -> keep this low.
GUEST_MAX_PER_DAY = int(os.getenv("GUEST_MAX_PER_DAY", "5"))
# Logged-in users without BYOK (still using server keys) -> optional cap.
USER_SERVER_MAX_PER_DAY = int(os.getenv("USER_SERVER_MAX_PER_DAY", "20"))

router = APIRouter(prefix="/api", tags=["research"])


class ResearchRequest(BaseModel):
    query: str
    # UI passes full IDs like "openai:gpt-4o" / "gemini:1.5-pro"
    model_a: Optional[str] = "openai:gpt-4o-mini"
    model_b: Optional[str] = "gemini:1.5-flash"
    # Advanced: allow explicit overrides (e.g. for testing)
    openai_key: Optional[str] = None
    gemini_key: Optional[str] = None

    model_config = {"protected_namespaces": ()}


class CompareRequest(BaseModel):
    query: str
    answer_a: str
    answer_b: str
    lang: Optional[str] = "en"

    model_config = {"protected_namespaces": ()}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_history_table():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NULL,
            query TEXT NOT NULL,
            model_used TEXT,
            response TEXT,
            ip TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def _count_for_today(where_sql: str, params: tuple) -> int:
    ensure_history_table()
    conn = get_db()
    cur = conn.cursor()
    # created_at defaults to CURRENT_TIMESTAMP (UTC). Compare against UTC "now".
    cur.execute(
        f"SELECT COUNT(*) AS c FROM history WHERE {where_sql} AND DATE(created_at) = DATE('now')",
        params,
    )
    row = cur.fetchone()
    conn.close()
    return int(row["c"] if row else 0)


def count_guest_for_ip_today(ip: str) -> int:
    return _count_for_today("user_id IS NULL AND ip = ?", (ip,))


def count_user_for_today(user_id: int) -> int:
    return _count_for_today("user_id = ?", (user_id,))


def save_history(
    user_id: Optional[int],
    query: str,
    model_used: str,
    response: Dict[str, Any],
    ip: Optional[str],
):
    ensure_history_table()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (user_id, query, model_used, response, ip) VALUES (?, ?, ?, ?, ?)",
        (
            user_id,
            query,
            model_used,
            sqlite3.Binary(json.dumps(response, ensure_ascii=False).encode("utf-8")),
            ip,
        ),
    )
    conn.commit()
    conn.close()


def _needs_openai(model_id: str) -> bool:
    return (model_id or "").startswith("openai:")


def _needs_gemini(model_id: str) -> bool:
    return (model_id or "").startswith("gemini:")


def _missing_key_message(provider: str) -> str:
    # Clear CTA for A + graceful fallback
    if provider == "openai":
        return (
            "OpenAI is not configured for guest usage. "
            "If you're the admin, set OPENAI_API_KEY on the server. "
            "Otherwise, register/log in and add your own OpenAI key in Settings."
        )
    if provider == "gemini":
        return (
            "Gemini is not configured for guest usage. "
            "If you're the admin, set GEMINI_API_KEY on the server. "
            "Otherwise, register/log in and add your own Gemini key in Settings."
        )
    return "LLM provider is not configured. Please register/log in and add your own key."


@router.post("/research")
async def research(
    payload: ResearchRequest,
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    query = (payload.query or "").strip()
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="query is required")

    client_ip = request.client.host if request.client else "unknown"

    # Guests: fixed cheap models, strict daily cap.
    if not current_user:
        used = count_guest_for_ip_today(client_ip)
        if used >= GUEST_MAX_PER_DAY:
            return {
                "ok": False,
                "detail": (
                    f"Daily guest limit reached for this IP ({GUEST_MAX_PER_DAY} free research requests). "
                    "Please log in or register to continue."
                ),
            }
        payload.model_a = "openai:gpt-4o-mini"
        payload.model_b = "gemini:1.5-flash"

    # Resolve keys (BYOK for logged in, otherwise server env keys)
    resolved_openai = payload.openai_key
    resolved_gemini = payload.gemini_key
    key_mode = "guest"

    if current_user:
        from duomind_app.db import SessionLocal
        from duomind_app import models

        db = SessionLocal()
        try:
            orm_user = db.query(models.User).get(current_user["id"])
            keyset = resolve_keys(orm_user)
        finally:
            db.close()

        key_mode = keyset.get("mode", "guest")
        if resolved_openai is None:
            resolved_openai = keyset.get("openai")
        if resolved_gemini is None:
            resolved_gemini = keyset.get("gemini")

        # Optional safety: if user has no BYOK and is using server keys, cap usage too.
        if key_mode != "byok":
            used_u = count_user_for_today(int(current_user["id"]))
            if used_u >= USER_SERVER_MAX_PER_DAY:
                return {
                    "ok": False,
                    "detail": (
                        f"Daily limit reached ({USER_SERVER_MAX_PER_DAY} requests) for your account on the free tier. "
                        "Add your own API keys in Settings to continue."
                    ),
                }
    else:
        keyset = resolve_keys(None)
        if resolved_openai is None:
            resolved_openai = keyset.get("openai")
        if resolved_gemini is None:
            resolved_gemini = keyset.get("gemini")

    # Graceful fallback: if a needed provider key is missing, don't call provider (no MOCK).
    if _needs_openai(payload.model_a) and not (resolved_openai or "").strip():
        return {"ok": False, "detail": _missing_key_message("openai")}
    if _needs_gemini(payload.model_a) and not (resolved_gemini or "").strip():
        return {"ok": False, "detail": _missing_key_message("gemini")}
    if _needs_openai(payload.model_b) and not (resolved_openai or "").strip():
        return {"ok": False, "detail": _missing_key_message("openai")}
    if _needs_gemini(payload.model_b) and not (resolved_gemini or "").strip():
        return {"ok": False, "detail": _missing_key_message("gemini")}

    try:
        result = await run_dual_research(
            query=query,
            model_a=payload.model_a,
            model_b=payload.model_b,
            openai_key=resolved_openai,
            gemini_key=resolved_gemini,
            user=current_user,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        uid = int(current_user["id"]) if current_user else None
        save_history(uid, query, f"{payload.model_a}|{payload.model_b}", result, client_ip)
    except Exception:
        pass

    return {"ok": True, "data": result, "mode": key_mode}


@router.post("/compare")
async def compare(
    payload: CompareRequest,
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    query = (payload.query or "").strip()
    a = (payload.answer_a or "").strip()
    b = (payload.answer_b or "").strip()
    if not query or not a or not b:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="query, answer_a, and answer_b are required",
        )

    client_ip = request.client.host if request.client else "unknown"

    # Consume the same quotas as /research (this uses server keys unless BYOK)
    resolved_openai = None
    resolved_gemini = None
    key_mode = "guest"

    if not current_user:
        used = count_guest_for_ip_today(client_ip)
        if used >= GUEST_MAX_PER_DAY:
            return {
                "ok": False,
                "detail": (
                    f"Daily guest limit reached for this IP ({GUEST_MAX_PER_DAY} free research requests). "
                    "Please log in or register to continue."
                ),
            }
        keyset = resolve_keys(None)
        resolved_openai = keyset.get("openai")
        resolved_gemini = keyset.get("gemini")
    else:
        from duomind_app.db import SessionLocal
        from duomind_app import models

        db = SessionLocal()
        try:
            orm_user = db.query(models.User).get(current_user["id"])
            keyset = resolve_keys(orm_user)
        finally:
            db.close()

        key_mode = keyset.get("mode", "server")
        resolved_openai = keyset.get("openai")
        resolved_gemini = keyset.get("gemini")

        if key_mode != "byok":
            used_u = count_user_for_today(int(current_user["id"]))
            if used_u >= USER_SERVER_MAX_PER_DAY:
                return {
                    "ok": False,
                    "detail": (
                        f"Daily limit reached ({USER_SERVER_MAX_PER_DAY} requests) for your account on the free tier. "
                        "Add your own API keys in Settings to continue."
                    ),
                }

    if not (resolved_openai or "").strip() and not (resolved_gemini or "").strip():
        return {"ok": False, "detail": "Missing API key."}

    return await run_compare_reconcile(
        query=query,
        answer_a=a,
        answer_b=b,
        lang=(payload.lang or "en"),
        openai_key=resolved_openai,
        gemini_key=resolved_gemini,
    )
