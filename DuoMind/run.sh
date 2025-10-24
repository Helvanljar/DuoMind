
#!/usr/bin/env bash
# Runs the backend on macOS/Linux
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn duomind_app.main:app --reload
