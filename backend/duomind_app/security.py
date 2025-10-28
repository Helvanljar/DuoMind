
import os
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt, JWTError
from fastapi import Header

from duomind_app.db import SessionLocal
from duomind_app import models

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-dev")
ALGO = "HS256"
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN", "60"))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False

def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TTL_MIN)}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def decode_token(token: str) -> Optional[int]:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
        return int(data.get("sub"))
    except JWTError:
        return None

def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[models.User]:
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
