from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import sqlite3

SECRET_KEY = "super-secret-duomind"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 4

# ✅ make bearer optional for guest pages
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_PATH = "duomind.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(email: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, username, password_hash, openai_key, gemini_key FROM users WHERE email = ?",
        (email,),
    )
    row = cur.fetchone()
    if row:
        return dict(row)
    return None

def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    # this one is for endpoints that MUST be protected (/auth/me, /api/history, ...)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user