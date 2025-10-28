
# Day 4 – Dual‑LLM Integration (Gemini + GPT)
1) Copy backend/.env.example -> backend/.env and add your keys.
2) Append backend/duomind_app/main.py.add to your main.py.
3) Install extra deps:
   .\.venv\Scripts\pip.exe install google-generativeai openai python-dotenv
4) Run:
   .\.venv\Scripts\python.exe -m uvicorn duomind_app.main:app --reload --app-dir backend
5) Test with /api/session -> /api/session/{id}/run (mode=dual) -> /report/{id}
