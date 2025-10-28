
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from duomind_app.security import get_current_user
from duomind_app.db import SessionLocal
from duomind_app import models

templates = Jinja2Templates(directory="backend/duomind_app/templates")
router = APIRouter(tags=["history"])

@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request, user=Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse("history.html", {"request": request, "items": [], "guest": True})
    db = SessionLocal()
    try:
        rows = (
            db.query(models.UserQueryHistory)
            .filter(models.UserQueryHistory.user_id == user.id)
            .order_by(models.UserQueryHistory.created_at.desc())
            .limit(100)
            .all()
        )
        return templates.TemplateResponse("history.html", {"request": request, "items": rows, "guest": False, "email": user.email})
    finally:
        db.close()

@router.get("/api/history")
def history_api(user=Depends(get_current_user)):
    if not user:
        return {"items": []}
    db = SessionLocal()
    try:
        rows = (
            db.query(models.UserQueryHistory)
            .filter(models.UserQueryHistory.user_id == user.id)
            .order_by(models.UserQueryHistory.created_at.desc())
            .limit(100)
            .all()
        )
        return {"items": [
            {"id": r.id, "query": r.query, "model_used": r.model_used, "created_at": r.created_at.isoformat()} for r in rows
        ]}
    finally:
        db.close()
