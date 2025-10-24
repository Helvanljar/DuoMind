
# DuoMind — Tag 1 (Backend & DB, zero-docker)

Minimal startbares Backend mit FastAPI + SQLite.
Später erweitern wir schrittweise (LLM‑Pipeline, RAG, Frontend).

## Quickstart (Windows PowerShell)
```powershell
cd DuoMind\backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; uvicorn duomind_app.main:app --reload
```

## Quickstart (macOS/Linux)
```bash
cd DuoMind/backend
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn duomind_app.main:app --reload
```

### Test
- Health: http://127.0.0.1:8000/api/health → {"ok": true}
- Session anlegen (z. B. mit curl/Postman):
```bash
curl -X POST http://127.0.0.1:8000/api/session -H "Content-Type: application/json" -d '{"user_query":"Was ist agentic RAG?"}'
```

## Struktur
```
DuoMind/
├─ backend/
│  ├─ requirements.txt
│  └─ duomind_app/
│     ├─ __init__.py
│     ├─ db.py
│     ├─ models.py
│     └─ main.py
└─ (später) frontend/, scripts/, etc.
```
