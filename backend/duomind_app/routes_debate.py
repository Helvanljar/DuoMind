import os
from typing import Optional, Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel

from .routes_auth import get_current_user_optional
from .llm_orchestrator import run_debate_and_converge
from .key_resolver import resolve_keys

# Reuse quota + history helpers from routes_research
from .routes_research import (
    count_guest_for_ip_today,
    count_user_for_today,
    save_history,
    _missing_key_message,
    _needs_openai,
    _needs_gemini,
    GUEST_MAX_PER_DAY,
    USER_SERVER_MAX_PER_DAY,
)

router = APIRouter(prefix="/api", tags=["debate"])


class DebateRequest(BaseModel):
    query: str
    model_a: Optional[str] = "openai:gpt-4o-mini"
    model_b: Optional[str] = "gemini:1.5-flash"
    lang: Optional[str] = "en"
    # Advanced: allow explicit overrides (testing)
    openai_key: Optional[str] = None
    gemini_key: Optional[str] = None

    model_config = {"protected_namespaces": ()}


@router.post("/debate")
async def debate(
    payload: DebateRequest,
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    query = (payload.query or "").strip()
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="query is required")

    client_ip = request.client.host if request.client else "unknown"

    # Guests: strict daily cap + fixed cheap models.
    if not current_user:
        used = count_guest_for_ip_today(client_ip)
        if used >= GUEST_MAX_PER_DAY:
            return {
                "ok": False,
                "detail": (
                    f"Daily guest limit reached for this IP ({GUEST_MAX_PER_DAY} free requests). "
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

    # Ensure needed provider keys exist
    if _needs_openai(payload.model_a) and not (resolved_openai or "").strip():
        return {"ok": False, "detail": _missing_key_message("openai")}
    if _needs_gemini(payload.model_a) and not (resolved_gemini or "").strip():
        return {"ok": False, "detail": _missing_key_message("gemini")}
    if _needs_openai(payload.model_b) and not (resolved_openai or "").strip():
        return {"ok": False, "detail": _missing_key_message("openai")}
    if _needs_gemini(payload.model_b) and not (resolved_gemini or "").strip():
        return {"ok": False, "detail": _missing_key_message("gemini")}

    result = await run_debate_and_converge(
        query=query,
        model_a=payload.model_a,
        model_b=payload.model_b,
        lang=(payload.lang or "en"),
        openai_key=resolved_openai,
        gemini_key=resolved_gemini,
    )

    # save to history (reuse existing table)
    try:
        uid = int(current_user["id"]) if current_user else None
        save_history(uid, query, f"debate:{payload.model_a}|{payload.model_b}", result, client_ip)
    except Exception:
        pass

    return {"ok": True, "data": result.get("data") if result.get("ok") else result, "mode": key_mode}
