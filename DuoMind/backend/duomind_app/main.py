
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session as OrmSession
from .db import Base, engine, get_db
from . import models

# Create DB schema on start
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DuoMind API (Tag 1)", version="0.0.1")

class SessionCreate(BaseModel):
    user_query: str

class SessionOut(BaseModel):
    id: str
    user_query: str
    status: str

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
