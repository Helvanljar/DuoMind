from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes_auth import router as auth_router, get_current_user_optional
from .routes_history import router as history_router
from . import routes_research

app = FastAPI(title="DuoMind")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(history_router, prefix="/api", tags=["history"])
app.include_router(routes_research.router)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})


@app.get("/research", response_class=HTMLResponse)
async def research_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("research.html", {"request": request, "current_user": current_user})
