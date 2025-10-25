
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from sqlalchemy.orm import Session as OrmSession

from .db import Base, engine, get_db
from . import models
from duomind_app import llm_orchestrator
from duomind_app.config import RESEARCHER_PROVIDER, EDITOR_PROVIDER

# Create DB schema on start
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DuoMind API (Tag 2: Dual LLM)", version="0.2.0")

class SessionCreate(BaseModel):
    user_query: str

class SessionOut(BaseModel):
    id: str
    user_query: str
    status: str

class RunRequest(BaseModel):
    mode: Optional[str] = "auto"  # 'model_only' | 'web_rag' | 'auto'

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/session", response_model=SessionOut)
def create_session(payload: SessionCreate, db: OrmSession = Depends(get_db)):
    s = models.Session(user_query=payload.user_query, status="draft")
    db.add(s)
    db.commit()
    db.refresh(s)
    return SessionOut(id=s.id, user_query=s.user_query, status=s.status)

@app.get("/api/session/{session_id}", response_model=SessionOut)
def get_session(session_id: str, db: OrmSession = Depends(get_db)):
    s = db.get(models.Session, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionOut(id=s.id, user_query=s.user_query, status=s.status)

@app.post("/api/session/{session_id}/run")
def run_pipeline(session_id: str, body: RunRequest, db: OrmSession = Depends(get_db)):
    s = db.get(models.Session, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")

    mode = body.mode or "auto"
    verified = (mode != "model_only")
    context = "Stub context (RAG later)."

    notes: List[Dict] = llm_orchestrator.researcher_generate_notes(s.user_query, context)
    report_md: str = llm_orchestrator.editor_generate_report(s.user_query, notes, verified)

    s.status = "complete"
    db.commit()

    return {
        "ok": True,
        "providers": {"researcher": RESEARCHER_PROVIDER, "editor": EDITOR_PROVIDER},
        "verified": verified,
        "notes": notes,
        "report_markdown": report_md,
    }
