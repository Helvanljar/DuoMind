
import os
from typing import Optional, Dict
from duomind_app.db import SessionLocal
from duomind_app import models
from duomind_app.crypto_utils import decrypt_to_str

def resolve_keys(user: Optional[models.User]) -> Dict[str, str | None]:
    # mode:
    # - "guest": not logged in
    # - "server": logged in but no BYOK keys saved (uses server env keys)
    # - "byok": at least one BYOK key saved
    keys = {"openai": None, "gemini": None, "mode": "guest"}
    if user:
        db = SessionLocal()
        try:
            rows = db.query(models.ApiCredential).filter(models.ApiCredential.user_id == user.id).all()
            for r in rows:
                if r.provider == "openai":
                    keys["openai"] = decrypt_to_str(r.key_encrypted)
                elif r.provider == "gemini":
                    keys["gemini"] = decrypt_to_str(r.key_encrypted)
        finally:
            db.close()
    if keys["openai"] or keys["gemini"]:
        keys["mode"] = "byok"
        return keys
    keys["openai"] = os.getenv("OPENAI_PROJECT_KEY", os.getenv("OPENAI_API_KEY"))
    keys["gemini"] = os.getenv("GEMINI_PROJECT_KEY", os.getenv("GEMINI_API_KEY"))
    keys["mode"] = "server" if user else "guest"
    return keys
