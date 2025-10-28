
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from argon2 import PasswordHasher
from duomind_app.db import SessionLocal
from duomind_app import models

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-dev")
ALGO = "HS256"
ph = PasswordHasher()

def hash_password(pw: str) -> str:
    return ph.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, pw)
        return True
    except Exception:
        return False

def make_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def decode_token(token: str) -> Optional[int]:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
        return int(data.get("sub"))
    except JWTError:
        return None

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    uid = decode_token(token)
    if not uid:
        return None
    db = SessionLocal()
    try:
        return db.query(models.User).get(uid)
    finally:
        db.close()
