
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from duomind_app.security import get_current_user
from duomind_app.db import SessionLocal
from duomind_app import models

templates = Jinja2Templates(directory="backend/duomind_app/templates")
router = APIRouter(tags=["settings"])

@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

class SettingsPayload(BaseModel):
    openai_key: str | None = None
    gemini_key: str | None = None
    preferred_llm: str | None = None

@router.get("/api/settings")
def get_settings(user=Depends(get_current_user)):
    if not user:
        return {"email": None, "openai_key": None, "gemini_key": None, "preferred_llm": None, "mode": "guest"}
    db = SessionLocal()
    try:
        s = db.query(models.UserSettings).filter(models.UserSettings.user_id == user.id).first()
        if not s:
            s = models.UserSettings(user_id=user.id)
            db.add(s); db.commit(); db.refresh(s)
        def mask(k):
            if not k: return None
            return k[:4] + "****" + k[-4:] if len(k) > 8 else "***"
        return {"email": user.email, "openai_key": mask(s.openai_key), "gemini_key": mask(s.gemini_key), "preferred_llm": s.preferred_llm, "mode": "byok"}
    finally:
        db.close()

@router.post("/api/settings")
def save_settings(p: SettingsPayload, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(401, "Login required")
    db = SessionLocal()
    try:
        s = db.query(models.UserSettings).filter(models.UserSettings.user_id == user.id).first()
        if not s:
            s = models.UserSettings(user_id=user.id)
            db.add(s)
        if p.openai_key is not None:
            s.openai_key = p.openai_key.strip() or None
        if p.gemini_key is not None:
            s.gemini_key = p.gemini_key.strip() or None
        if p.preferred_llm is not None:
            s.preferred_llm = p.preferred_llm
        db.commit()
        return {"ok": True}
    finally:
        db.close()
