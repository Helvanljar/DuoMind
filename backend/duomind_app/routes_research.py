import json
import sqlite3
from typing import Optional, Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Request

from .routes_auth import get_current_user_optional
from .llm_orchestrator import run_dual_research
from .key_resolver import resolve_keys

DB_PATH = "duomind.db"
GUEST_MAX_PER_DAY = 5

router = APIRouter(prefix="/api", tags=["research"])


from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str
    model_a: Optional[str] = "openai:gpt-4o-mini"
    model_b: Optional[str] = "gemini:1.5-flash"
    openai_key: Optional[str] = None
    gemini_key: Optional[str] = None

    model_config = {
        "protected_namespaces": ()
    }


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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    try:
        cur.execute("ALTER TABLE history ADD COLUMN ip TEXT")
    except Exception:
        pass
    conn.commit()
    conn.close()


def count_guest_for_ip(ip: str) -> int:
    ensure_history_table()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM history WHERE user_id IS NULL AND ip = ?", (ip,))
    row = cur.fetchone()
    conn.close()
    return int(row["c"] if row else 0)


def save_history(user_id: Optional[int], query: str, model_used: str, response: Dict[str, Any], ip: Optional[str]):
    ensure_history_table()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (user_id, query, model_used, response, ip) VALUES (?, ?, ?, ?, ?)",
        (user_id, query, model_used, json.dumps(response, ensure_ascii=False), ip),
    )
    conn.commit()
    conn.close()


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

    if not current_user:
        used = count_guest_for_ip(client_ip)
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

    resolved_openai = payload.openai_key
    resolved_gemini = payload.gemini_key

    if current_user and (resolved_openai is None or resolved_gemini is None):
        from duomind_app.db import SessionLocal
        from duomind_app import models

        db = SessionLocal()
        try:
            orm_user = db.query(models.User).get(current_user["id"])
            keyset = resolve_keys(orm_user)
            if resolved_openai is None:
                resolved_openai = keyset.get("openai")
            if resolved_gemini is None:
                resolved_gemini = keyset.get("gemini")
        finally:
            db.close()
    elif not current_user:
        keyset = resolve_keys(None)
        if resolved_openai is None:
            resolved_openai = keyset.get("openai")
        if resolved_gemini is None:
            resolved_gemini = keyset.get("gemini")

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
        uid = current_user["id"] if current_user else None
        save_history(uid, query, f"{payload.model_a}|{payload.model_b}", result, client_ip)
    except Exception:
        pass

    return {"ok": True, "data": result}
