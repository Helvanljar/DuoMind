from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes_auth import router as auth_router, get_current_user_optional
from .routes_history import router as history_router
from . import routes_research
from . import routes_settings
from . import routes_models
from . import routes_debate

app = FastAPI(title="DuoMind")

# MCP (Model Context Protocol) endpoint
from .mcp_server import mcp
app.mount("/mcp", mcp.streamable_http_app())

from .db import init_db

@app.on_event("startup")
def _startup_init_db():
    init_db()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))



app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(history_router, prefix="/api", tags=["history"])
app.include_router(routes_research.router)
app.include_router(routes_settings.router)
app.include_router(routes_models.router)
app.include_router(routes_debate.router)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})


@app.get("/research", response_class=HTMLResponse)
async def research_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("research.html", {"request": request, "current_user": current_user})


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("history.html", {"request": request, "current_user": current_user})
