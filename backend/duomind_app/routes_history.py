from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from .routes_auth import get_current_user_optional

router = APIRouter(tags=["history"])

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "duomind.db")


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    """Keep history storage compatible with routes_research.py."""
    conn = _db()
    cur = conn.cursor()
    # routes_research stores the full response JSON in `response`.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            response BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


_init_db()


@router.get("/history")
async def list_history(
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    """Return the current user's research history.

    Auth: cookie or Authorization bearer (via get_current_user_optional).
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        uid = int(current_user["id"])  # type: ignore[index]
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")

    conn = _db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, query, created_at
        FROM history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 200
        """,
        (uid,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return {"items": rows}
