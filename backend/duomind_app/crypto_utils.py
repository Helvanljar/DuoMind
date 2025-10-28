
import base64, os
from cryptography.fernet import Fernet, InvalidToken

def _mk_fernet() -> Fernet:
    key = os.getenv("DUOMIND_KMS_KEY", "change-me-32-bytes-min").encode()
    if len(key) < 32:
        key = key.ljust(32, b"_")
    b64 = base64.urlsafe_b64encode(key[:32])
    return Fernet(b64)

_fernet = _mk_fernet()

def encrypt_str(s: str) -> bytes:
    return _fernet.encrypt(s.encode())

def decrypt_to_str(b: bytes) -> str:
    try:
        return _fernet.decrypt(b).decode()
    except InvalidToken:
        return ""
