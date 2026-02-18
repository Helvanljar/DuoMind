from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Request

from .routes_auth import get_current_user_optional
from .routes_research import GUEST_MAX_PER_DAY, count_guest_for_ip_today
from .key_resolver import resolve_keys


router = APIRouter(prefix="/api", tags=["quota"])


def _get_client_ip(request: Request) -> str:
    # Prefer X-Forwarded-For if behind a proxy/load balancer.
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip() or "unknown"
    return request.client.host if request.client else "unknown"


def _next_utc_midnight_iso() -> str:
    now = datetime.now(timezone.utc)
    next_midnight = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) + timedelta(days=1)
    return next_midnight.isoformat().replace("+00:00", "Z")


@router.get("/quota")
async def quota(
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional),
):
    """Return remaining free requests for guest-like users.

    Guest-like = true guests OR logged-in users without BYOK keys.
    BYOK users are unlimited.
    """

    client_ip = _get_client_ip(request)

    # Determine key mode (guest vs byok)
    key_mode = "guest"
    if current_user:
        from duomind_app.db import SessionLocal
        from duomind_app import models

        db = SessionLocal()
        try:
            orm_user = db.query(models.User).get(current_user["id"])
            keyset = resolve_keys(orm_user)
        finally:
            db.close()
        key_mode = keyset.get("mode", "guest")

    if key_mode == "byok":
        return {"mode": "byok", "limit": None, "used": None, "remaining": None, "reset_at_utc": None}

    used = count_guest_for_ip_today(client_ip)
    limit = int(GUEST_MAX_PER_DAY)
    remaining = max(0, limit - used)
    return {
        "mode": "guest",
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "reset_at_utc": _next_utc_midnight_iso(),
    }
