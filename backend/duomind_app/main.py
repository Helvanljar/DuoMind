
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from duomind_app.db import init_db
from duomind_app.routes_auth import router as auth_router
from duomind_app.routes_settings import router as settings_router
from duomind_app.routes_history import router as history_router

app = FastAPI(title="DuoMind – AI Research Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/duomind_app/static"), name="static")
templates = Jinja2Templates(directory="backend/duomind_app/templates")

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(history_router)
