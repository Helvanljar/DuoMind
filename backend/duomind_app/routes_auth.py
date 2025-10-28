
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator

from duomind_app.db import SessionLocal
from duomind_app import models
from duomind_app.security import get_password_hash, verify_password, create_access_token

templates = Jinja2Templates(directory="backend/duomind_app/templates")
router = APIRouter(tags=["auth"])

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

class RegisterPayload(BaseModel):
    email: EmailStr
    password: str
    @field_validator("password")
    @classmethod
    def strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

@router.post("/auth/register")
def register(p: RegisterPayload):
    db = SessionLocal()
    try:
        if db.query(models.User).filter(models.User.email == p.email).first():
            raise HTTPException(409, "Email already registered")
        u = models.User(email=p.email, password_hash=get_password_hash(p.password))
        db.add(u); db.commit(); db.refresh(u)
        s = models.UserSettings(user_id=u.id)
        db.add(s); db.commit()
        token = create_access_token(u.id)
        return {"token": token, "user_id": u.id, "email": u.email}
    finally:
        db.close()

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

@router.post("/auth/login")
def login(p: LoginPayload):
    db = SessionLocal()
    try:
        u = db.query(models.User).filter(models.User.email == p.email).first()
        if not u or not verify_password(p.password, u.password_hash):
            raise HTTPException(401, "Invalid credentials")
        token = create_access_token(u.id)
        return {"token": token, "user_id": u.id, "email": u.email}
    finally:
        db.close()

@router.post("/auth/logout")
def logout():
    return {"ok": True}
