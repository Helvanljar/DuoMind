from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .routes_auth import router as auth_router, get_current_user_optional
from .routes_history import router as history_router

app = FastAPI(title="DuoMind")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# static
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

# routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(history_router, prefix="/api", tags=["history"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_user": current_user},
    )


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse(
        "settings.html",
        {"request": request, "current_user": current_user},
    )


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse(
        "history.html",
        {"request": request, "current_user": current_user},
    )


@app.get("/ping")
async def ping():
    return {"status": "ok"}
