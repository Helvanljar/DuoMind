from pathlib import Path
from typing import Optional, Dict, Any, Tuple

import httpx

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .routes_auth import get_current_user_optional
from .db import SessionLocal
from . import models
from .crypto_utils import encrypt_str

router = APIRouter(tags=["settings"])

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    preferred_llm = None
    if current_user:
        db = SessionLocal()
        try:
            uid = int(current_user["id"])
            us = db.query(models.UserSettings).filter(models.UserSettings.user_id == uid).first()
            preferred_llm = us.preferred_llm if us else None
        finally:
            db.close()
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "current_user": current_user,
            "preferred_llm": preferred_llm,
        },
    )


def _upsert_credential(db, user_id: int, provider: str, raw_key: str):
    raw_key = (raw_key or "").strip()
    if not raw_key:
        return
    enc = encrypt_str(raw_key)
    row = (
        db.query(models.ApiCredential)
        .filter(models.ApiCredential.user_id == user_id, models.ApiCredential.provider == provider)
        .first()
    )
    if row:
        row.key_encrypted = enc
    else:
        db.add(models.ApiCredential(user_id=user_id, provider=provider, key_encrypted=enc))


async def _validate_key(provider: str, raw_key: str) -> Tuple[bool, int, str]:
    """Lightweight key validation.

    Returns (is_valid, status_code, message).
    """
    raw_key = (raw_key or "").strip()
    if not raw_key:
        return True, 0, "skipped"

    timeout = httpx.Timeout(8.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            if provider == "openai":
                r = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {raw_key}"},
                )
            elif provider == "gemini":
                # Generative Language API
                r = await client.get(
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    params={"key": raw_key},
                )
            elif provider == "anthropic":
                r = await client.get(
                    "https://api.anthropic.com/v1/models",
                    headers={
                        "x-api-key": raw_key,
                        "anthropic-version": "2023-06-01",
                    },
                )
            elif provider == "openrouter":
                r = await client.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={"Authorization": f"Bearer {raw_key}"},
                )
            elif provider == "mistral":
                r = await client.get(
                    "https://api.mistral.ai/v1/models",
                    headers={"Authorization": f"Bearer {raw_key}"},
                )
            else:
                return False, 0, "unknown provider"
        except Exception as e:
            return False, 0, str(e)

    ok = 200 <= r.status_code < 300
    msg = "valid" if ok else (r.text[:200] if r.text else "invalid")
    return ok, int(r.status_code), msg


@router.post("/api/settings/save")
async def api_save_settings(
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    """Save BYOK keys with optional validation.

    Rules:
    - Empty field: do not touch existing key.
    - Non-empty: validate; only overwrite if valid.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Please log in to update settings.")

    payload = await request.json()
    preferred_llm = str(payload.get("preferred_llm") or "").strip() or None

    raw_keys = {
        "openai": str(payload.get("openai_key") or "").strip(),
        "gemini": str(payload.get("gemini_key") or "").strip(),
        "anthropic": str(payload.get("anthropic_key") or "").strip(),
        "openrouter": str(payload.get("openrouter_key") or "").strip(),
        "mistral": str(payload.get("mistral_key") or "").strip(),
    }

    results: Dict[str, Any] = {}
    # Validate only fields that were provided (non-empty). Empty -> skipped.
    for prov, val in raw_keys.items():
        if not val:
            results[prov] = {"ok": True, "status": "skipped"}
            continue
        ok, code, msg = await _validate_key(prov, val)
        results[prov] = {"ok": ok, "status": "valid" if ok else "invalid", "code": code, "message": msg}

    db = SessionLocal()
    saved = []
    try:
        uid = int(current_user["id"])

        # Only persist keys that validated.
        for prov, val in raw_keys.items():
            if not val:
                continue
            if results.get(prov, {}).get("status") == "valid":
                _upsert_credential(db, uid, prov, val)
                saved.append(prov)

        # Preferred model setting
        us = db.query(models.UserSettings).filter(models.UserSettings.user_id == uid).first()
        if not us:
            us = models.UserSettings(user_id=uid)
            db.add(us)
        us.preferred_llm = preferred_llm

        db.commit()
    finally:
        db.close()

    return {"ok": True, "saved": saved, "results": results}


@router.post("/settings")
async def save_settings(
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    if not current_user:
        # Settings are for BYOK; prompt login.
        raise HTTPException(status_code=401, detail="Please log in to update settings.")

    form = await request.form()
    openai_key = str(form.get("openai_key") or "")
    gemini_key = str(form.get("gemini_key") or "")
    anthropic_key = str(form.get("anthropic_key") or "")
    openrouter_key = str(form.get("openrouter_key") or "")
    mistral_key = str(form.get("mistral_key") or "")
    preferred_llm = str(form.get("preferred_llm") or "").strip() or None

    db = SessionLocal()
    try:
        uid = int(current_user["id"])
        _upsert_credential(db, uid, "openai", openai_key)
        _upsert_credential(db, uid, "gemini", gemini_key)
        _upsert_credential(db, uid, "anthropic", anthropic_key)
        _upsert_credential(db, uid, "openrouter", openrouter_key)
        _upsert_credential(db, uid, "mistral", mistral_key)

        us = db.query(models.UserSettings).filter(models.UserSettings.user_id == uid).first()
        if not us:
            us = models.UserSettings(user_id=uid)
            db.add(us)
        us.preferred_llm = preferred_llm

        db.commit()
    finally:
        db.close()

    return RedirectResponse(url="/settings", status_code=303)
