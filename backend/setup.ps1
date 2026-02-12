$ErrorActionPreference = "Stop"

if (!(Test-Path ".\.venv")) {
  python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

if (Test-Path ".\requirements.txt") {
  python -m pip install -r .\requirements.txt
} else {
  python -m pip install fastapi "uvicorn[standard]" jinja2 python-multipart "passlib[bcrypt]" sqlalchemy "python-jose[cryptography]" httpx python-dotenv pyyaml
  python -m pip freeze > requirements.txt
}

Write-Host "✅ Setup complete"
Write-Host "Run: python -m uvicorn duomind_app.main:app --reload"
