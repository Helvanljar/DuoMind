
# DuoMind · Day 4.5 — Auth + BYOK + Model List API

## Apply
1) Append models:
   - Open `backend/duomind_app/models.py`
   - Paste content from `backend/duomind_app/models.py.add` at the end.

2) Wire routes:
   - Open `backend/duomind_app/main.py`
   - Append from `backend/duomind_app/main.py.add2`

3) Env:
   - Copy `backend/.env.example` → `backend/.env` and set JWT_SECRET, DUOMIND_KMS_KEY.

4) Deps:
   - Append `backend_requirements_append.txt` to `backend/requirements.txt`
   - Install: `.\.venv\Scripts\pip.exe install -r backend\requirements.txt`

5) Run:
   - `.\.venv\Scripts\python.exe -m uvicorn duomind_app.main:app --reload --app-dir backend`

## Test (PowerShell)
$base = "http://127.0.0.1:8000"
$u = Invoke-RestMethod -Method Post -Uri "$base/auth/signup" -ContentType "application/json" -Body '{"email":"a@b.com","password":"pass12345"}'
$token = $u.token
Invoke-RestMethod -Method Get -Uri "$base/me/keys" -Headers @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Method Post -Uri "$base/me/keys" -Headers @{ Authorization = "Bearer $token" } -ContentType "application/json" -Body '{"provider":"openai","api_key":"sk-..."}'
Invoke-RestMethod -Method Get -Uri "$base/api/models"

# In /api/session/{id}/run use keys via resolve_keys(user) as shown in main.py.add2
