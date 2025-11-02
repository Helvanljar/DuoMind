from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from typing import Optional
import sqlite3
from passlib.context import CryptContext
from pathlib import Path
from fastapi.templating import Jinja2Templates

from .security import (
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,
    get_user_by_email,
    create_access_token,
    get_password_hash,
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB
DB_PATH = "duomind.db"

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# =========================
# Pydantic models
# =========================
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# DB helpers
# =========================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


# =========================
# optional user
# =========================
def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme)):
    """
    Returns user dict or None (guest).
    """
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            return None
        user = get_user_by_email(email)
        return user
    except JWTError:
        return None


# =========================
# API endpoints (JSON)
# =========================
@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest):
    conn = get_db()
    cur = conn.cursor()

    # email unique
    cur.execute("SELECT 1 FROM users WHERE email = ?", (req.email,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    # username unique
    desired_username = req.username or req.email.split("@")[0]
    cur.execute("SELECT 1 FROM users WHERE username = ?", (desired_username,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Username already taken")

    # password policy (>=8, >=2 digits, >=1 special, >=1 uppercase)
    import re
    strong = re.compile(r"^(?=.*[A-Z])(?=(?:.*\d){2,})(?=.*[^\w\s]).{8,}$")
    if not strong.match(req.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be >=8 chars, >=2 digits, >=1 special, >=1 uppercase.",
        )

    hashed = get_password_hash(req.password)
    cur.execute(
        "INSERT INTO users (email, password_hash, username) VALUES (?, ?, ?)",
        (req.email, hashed, desired_username),
    )
    conn.commit()

    token = create_access_token({"sub": req.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (req.email,))
    user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": req.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def read_me(current_user=Depends(get_current_user_optional)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user


# =========================
# HTML routes for modals
# =========================
@router.get("/login-page", response_class=HTMLResponse)
async def login_page_html(
    request: Request,
    current_user=Depends(get_current_user_optional),
):
    ctx = {"request": request, "current_user": current_user}
    return templates.TemplateResponse("login.html", ctx)


@router.get("/register-page", response_class=HTMLResponse)
async def register_page_html(
    request: Request,
    current_user=Depends(get_current_user_optional),
):
    ctx = {"request": request, "current_user": current_user}
    return templates.TemplateResponse("register.html", ctx)
