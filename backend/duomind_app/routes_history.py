from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import sqlite3
from .security import get_current_user_from_token

DB_PATH = "duomind.db"
router = APIRouter()

class HistoryCreate(BaseModel):
    query: str
    llm_used: Optional[str] = None  # was model_used

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/history")
def create_history(payload: HistoryCreate, current_user=Depends(get_current_user_from_token)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (user_id, query, model_used) VALUES (?, ?, ?)",
        (current_user["id"], payload.query, payload.llm_used),
    )
    conn.commit()
    return {"status": "ok"}

@router.get("/history")
def list_history(current_user=Depends(get_current_user_from_token)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, query, model_used, created_at FROM history WHERE user_id = ? ORDER BY created_at DESC",
        (current_user["id"],),
    )
    rows = cur.fetchall()
    return [dict(r) for r in rows]