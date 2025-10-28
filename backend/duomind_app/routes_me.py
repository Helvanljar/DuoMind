
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from duomind_app.db import SessionLocal
from duomind_app import models
from duomind_app.auth import get_current_user
from duomind_app.crypto_utils import encrypt_str

router = APIRouter(prefix="/me", tags=["me"])

class KeyPayload(BaseModel):
    provider: str
    api_key: str

@router.get("/keys")
def list_keys(user=Depends(get_current_user)):
    if not user:
        return {"mode": "guest", "keys": []}
    db = SessionLocal()
    try:
        rows = db.query(models.ApiCredential).filter(models.ApiCredential.user_id == user.id).all()
        items = [{"provider": r.provider, "masked": "***", "last_used_at": r.last_used_at} for r in rows]
        return {"mode": "byok" if rows else "guest", "keys": items}
    finally:
        db.close()

@router.post("/keys")
def add_key(p: KeyPayload, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(401, "Login required")
    db = SessionLocal()
    try:
        enc = encrypt_str(p.api_key)
        cred = db.query(models.ApiCredential).filter_by(user_id=user.id, provider=p.provider).first()
        if cred:
            cred.key_encrypted = enc
        else:
            db.add(models.ApiCredential(user_id=user.id, provider=p.provider, key_encrypted=enc))
        db.commit()
        return {"ok": True}
    finally:
        db.close()
