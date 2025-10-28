
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from duomind_app.db import SessionLocal
from duomind_app import models
from duomind_app.auth import hash_password, verify_password, make_token

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupPayload(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(p: SignupPayload):
    db = SessionLocal()
    try:
        if db.query(models.User).filter(models.User.email == p.email).first():
            raise HTTPException(409, "Email already registered")
        u = models.User(email=p.email, password_hash=hash_password(p.password))
        db.add(u); db.commit(); db.refresh(u)
        return {"token": make_token(u.id), "user_id": u.id, "email": u.email}
    finally:
        db.close()

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(p: LoginPayload):
    db = SessionLocal()
    try:
        u = db.query(models.User).filter(models.User.email == p.email).first()
        if not u or not verify_password(p.password, u.password_hash):
            raise HTTPException(401, "Invalid credentials")
        return {"token": make_token(u.id), "user_id": u.id, "email": u.email}
    finally:
        db.close()
