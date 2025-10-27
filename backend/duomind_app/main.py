
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session as OrmSession

from .db import Base, engine, get_db
from . import models
from duomind_app import llm_orchestrator
from duomind_app.config import RESEARCHER_PROVIDER, EDITOR_PROVIDER

import json
import os
import markdown2

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DuoMind API (Tag 3: Persistence + Viewer)", version="0.3.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class SessionCreate(BaseModel):
    user_query: str

class SessionOut(BaseModel):
    id: str
    user_query: str
    status: str

class NoteOut(BaseModel):
    id: str
    claim: str
    evidence: Optional[List[Dict[str, Any]]] = None
    confidence: Optional[float] = None
    created_at: Optional[str] = None

class ReportOut(BaseModel):
    id: str
    markdown: str
    verified: bool
    created_at: Optional[str] = None

class RunRequest(BaseModel):
    mode: Optional[str] = "auto"

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

    # persist notes
    for n in notes:
        evidence_json = json.dumps(n.get("evidence") or [], ensure_ascii=False)
        db.add(models.Note(session_id=s.id, claim=n.get("claim") or "", evidence_json=evidence_json, confidence=n.get("confidence")))

    # persist report
    report = models.Report(session_id=s.id, markdown=report_md, verified=verified)
    db.add(report)

    s.status = "complete"
    db.commit()

    return {"ok": True, "providers": {"researcher": RESEARCHER_PROVIDER, "editor": EDITOR_PROVIDER}, "verified": verified, "notes_saved": len(notes), "report_id": report.id}

@app.get("/api/session/{session_id}/notes")
def get_notes(session_id: str, db: OrmSession = Depends(get_db)):
    s = db.get(models.Session, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    rows = db.query(models.Note).filter(models.Note.session_id == session_id).order_by(models.Note.created_at.asc()).all()
    out = []
    for r in rows:
        try:
            ev = json.loads(r.evidence_json or "[]")
        except Exception:
            ev = []
        out.append({"id": r.id, "claim": r.claim, "evidence": ev, "confidence": r.confidence, "created_at": str(r.created_at)})
    return out

@app.get("/api/session/{session_id}/report")
def get_report(session_id: str, db: OrmSession = Depends(get_db)):
    s = db.get(models.Session, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    r = db.query(models.Report).filter(models.Report.session_id == session_id).order_by(models.Report.created_at.desc()).first()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"id": r.id, "markdown": r.markdown, "verified": bool(r.verified), "created_at": str(r.created_at)}

@app.get("/report/{session_id}", response_class=HTMLResponse)
def render_report(session_id: str, request: Request, db: OrmSession = Depends(get_db)):
    s = db.get(models.Session, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    r = db.query(models.Report).filter(models.Report.session_id == session_id).order_by(models.Report.created_at.desc()).first()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")

    html_body = markdown2.markdown(r.markdown or "", extras=["fenced-code-blocks", "tables", "strike", "task_list", "header-ids"])
    return templates.TemplateResponse("report.html", {"request": request, "session_id": session_id, "user_query": s.user_query, "verified": r.verified, "report_html": html_body})

# --- Tag 3.1 additions (append to your existing main.py) ---
from fastapi.responses import RedirectResponse, HTMLResponse

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: OrmSession = Depends(get_db)):
    rows = db.query(models.Session).order_by(models.Session.created_at.desc()).all()
    if not rows:
        return RedirectResponse(url="/docs", status_code=302)

    data = []
    for s in rows:
        has_report = db.query(models.Report).filter(models.Report.session_id == s.id).first() is not None
        data.append({
            "id": s.id,
            "user_query": s.user_query,
            "status": s.status,
            "created_at": s.created_at,
            "has_report": has_report
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "sessions": data
    })
