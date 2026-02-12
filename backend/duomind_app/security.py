from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# =========================
# Config
# =========================

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_DEV_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080")  # 7 days
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "duomind.db")

# =========================
# Password hashing
# =========================
# ✅ Argon2 is primary
# ✅ bcrypt allowed for legacy hashes
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
)

def get_password_hash(password: str) -> str:
    """
    Hash password using Argon2 (default).
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against stored hash.
    Supports argon2 + legacy bcrypt.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# =========================
# JWT helpers
# =========================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =========================
# OAuth2 (used by FastAPI deps)
# =========================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

# =========================
# Database helpers
# =========================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    email = (email or "").strip().lower()
    if not email:
        return None

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None

# =========================
# Token → user helpers
# =========================

def get_current_user_from_token(token: str):
    """
    Legacy helper used by routes_history.py and others.

    Accepts:
      - raw JWT
      - "Bearer <JWT>"

    Returns:
      - user dict or None
    """
    if not token:
        return None

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            return None
        return get_user_by_email(email)
    except JWTError:
        return None
