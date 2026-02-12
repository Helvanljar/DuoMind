from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends

from .routes_auth import get_current_user_optional
from .key_resolver import resolve_keys

router = APIRouter(prefix="/api", tags=["models"])

# Keep these conservative; only include providers you actually support in llm_orchestrator.
GUEST_MODELS = {
    "model_a": ["openai:gpt-4o-mini"],
    "model_b": ["gemini:1.5-flash"],
}

REGISTERED_MODELS = {
    "model_a": ["openai:gpt-4o-mini", "openai:gpt-4o"],
    "model_b": ["gemini:1.5-flash", "gemini:1.5-pro"],
}


@router.get("/models")
def list_models(current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)):
    if not current_user:
        return {"ok": True, "mode": "guest", "models": GUEST_MODELS}

    # Determine whether user has BYOK; if not, still allow selection but you'll cap in /api/research.
    key_mode = "guest"
    try:
        from duomind_app.db import SessionLocal
        from duomind_app import models as orm_models

        db = SessionLocal()
        try:
            orm_user = db.query(orm_models.User).get(int(current_user["id"]))
            keyset = resolve_keys(orm_user)
            key_mode = keyset.get("mode", "guest")
        finally:
            db.close()
    except Exception:
        pass

    return {"ok": True, "mode": key_mode, "models": REGISTERED_MODELS}
