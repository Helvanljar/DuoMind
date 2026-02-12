from datetime import timedelta
from pathlib import Path
from typing import Optional

import sqlite3
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
)
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

from .security import (
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,         # still used for pure API auth if needed
    get_user_by_email,
    create_access_token,
    get_password_hash,
    verify_password,       # ✅ use this (argon2 + bcrypt verify)
)

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "duomind.db")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# =========================
# Pydantic models (JSON API)
# =========================

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


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
# Helpers
# =========================

def validate_password_strength(password: str) -> bool:
    """
    >= 8 chars, >= 2 digits, >= 1 special char, >= 1 uppercase.
    """
    import re
    pattern = re.compile(r"^(?=.*[A-Z])(?=(?:.*\d){2,})(?=.*[^\w\s]).{8,}$")
    return bool(pattern.match(password))


def build_cookie_login_response(token: str) -> RedirectResponse:
    """
    Redirect to home and set JWT cookie from form-based login/register.
    """
    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,        # set True behind HTTPS in production
        samesite="lax",
        max_age=int(timedelta(days=7).total_seconds()),
        path="/",
    )
    return response


# =========================
# Current user (used by main.py)
# =========================

def get_current_user_optional(
    request: Request,
    token_header: Optional[str] = Depends(oauth2_scheme),
):
    """
    Returns user dict or None.

    Priority:
    1. Bearer token from Authorization header (API usage)
    2. access_token cookie set by form-based login/register
    """
    token = None

    if token_header:
        token = token_header
    else:
        raw_cookie = request.cookies.get("access_token")
        if raw_cookie:
            token = raw_cookie

    if not token:
        return None

    if token.startswith("Bearer "):
        token = token[len("Bearer ") :]

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
# Registration (JSON + form)
# =========================

@router.post("/register")
async def register(request: Request):
    """
    Dual-mode /auth/register:

    1) Form:
       - Content-Type: application/x-www-form-urlencoded
       - Fields: username, email, password, confirm_password
       - Creates user, sets cookie, redirects to "/"

    2) JSON API:
       - Body: { "email", "password", "username" (optional) }
       - Returns: { "access_token", "token_type": "bearer" }
    """
    content_type = request.headers.get("content-type", "")

    # ---------- Form flow ----------
    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        email = str(form.get("email", "")).strip().lower()
        username = str(form.get("username", "")).strip()
        password = str(form.get("password", ""))
        confirm_password = str(form.get("confirm_password", ""))

        if not email or not password:
            return RedirectResponse(
                url="/?error=missing_fields",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        if password != confirm_password:
            return RedirectResponse(
                url="/?error=password_mismatch",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        if not validate_password_strength(password):
            return RedirectResponse(
                url="/?error=weak_password",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            conn.close()
            return RedirectResponse(
                url="/?error=email_exists",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        if not username:
            username = email.split("@")[0]

        cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            base = username
            idx = 1
            while True:
                candidate = f"{base}{idx}"
                cur.execute("SELECT 1 FROM users WHERE username = ?", (candidate,))
                if not cur.fetchone():
                    username = candidate
                    break
                idx += 1

        hashed = get_password_hash(password)  # ✅ argon2
        cur.execute(
            "INSERT INTO users (email, password_hash, username) VALUES (?, ?, ?)",
            (email, hashed, username),
        )
        conn.commit()
        conn.close()

        token = create_access_token({"sub": email})
        return build_cookie_login_response(token)

    # ---------- JSON flow ----------
    try:
        data = await request.json()
        req_model = RegisterRequest(**data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid registration payload.",
        )

    if not validate_password_strength(req_model.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be >=8 chars, >=2 digits, >=1 special, >=1 uppercase.",
        )

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM users WHERE email = ?", (req_model.email,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    username = req_model.username or req_model.email.split("@")[0]
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    hashed = get_password_hash(req_model.password)  # ✅ argon2
    cur.execute(
        "INSERT INTO users (email, password_hash, username) VALUES (?, ?, ?)",
        (req_model.email, hashed, username),
    )
    conn.commit()
    conn.close()

    token = create_access_token({"sub": req_model.email})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token, "token_type": "bearer"},
    )


# =========================
# Login (JSON + form)
# =========================

@router.post("/login")
async def login(request: Request):
    """
    Dual-mode /auth/login:

    1) Form:
       - email, password
       - On success: set cookie + redirect "/"

    2) JSON API:
       - { "email", "password" }
       - On success: JSON token
    """
    content_type = request.headers.get("content-type", "")

    # ---------- Form flow ----------
    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        email = str(form.get("email", "")).strip().lower()
        password = str(form.get("password", ""))

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if not user or not verify_password(password, user["password_hash"]):
            return RedirectResponse(
                url="/?error=invalid_credentials",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        token = create_access_token({"sub": email})
        return build_cookie_login_response(token)

    # ---------- JSON flow ----------
    try:
        data = await request.json()
        req_model = LoginRequest(**data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login payload.",
        )

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (req_model.email,))
    user = cur.fetchone()
    conn.close()

    if not user or not verify_password(req_model.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": req_model.email})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token, "token_type": "bearer"},
    )


# =========================
# Me
# =========================

@router.get("/me")
def read_me(current_user=Depends(get_current_user_optional)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user


# =========================
# Standalone HTML pages (optional)
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


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token", path="/")
    return response
