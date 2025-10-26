# 🧠 DuoMind – AI Research Copilot MVP  
> A lightweight, dual-LLM powered research assistant for generating and verifying scientific-style summaries.

## 🚀 Overview  
**DuoMind** is an AI-driven research copilot that uses two specialized LLMs in collaboration:
- 🧩 **Researcher LLM** – gathers claims, notes, and evidence  
- 🧠 **Editor LLM** – verifies and structures these insights into clean, human-readable reports  

All interactions are stored in a local database for persistence, and results can be viewed directly in a beautiful, responsive HTML report page.

## ✨ Features  
- **Dual LLM workflow:** combines two models (e.g. GPT-4 + Gemini) for diverse reasoning  
- **Research pipeline:** generate structured notes → compile into final report  
- **Persistence layer:** every query, note, and report stored via SQLite  
- **FastAPI backend:** clean REST API design + Swagger docs (`/docs`)  
- **Elegant report viewer:** light/dark friendly HTML summaries for easy sharing  
- **Zero-setup:** runs locally with SQLite, no Docker required  

## 🧩 Architecture  
```
backend/
 ├── duomind_app/
 │   ├── main.py          # FastAPI app entrypoint
 │   ├── models.py        # SQLAlchemy ORM models
 │   ├── llm_orchestrator.py  # Dual LLM coordination
 │   ├── templates/
 │   │   └── report.html  # HTML report viewer
 │   └── db.py, config.py, ...
 ├── requirements.txt
 └── ...
```

## ⚙️ Setup & Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Helvanljar/DuoMind.git
cd DuoMind/backend
```

### 2️⃣ Create virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows PowerShell
# or source .venv/bin/activate   # macOS/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run FastAPI server
```bash
python -m uvicorn duomind_app.main:app --reload
```

Server runs on → [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Swagger docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧠 Example API Flow

```bash
# Create session
POST /api/session
{
  "user_query": "Explain agentic RAG simply."
}

# Run the research pipeline
POST /api/session/{session_id}/run

# View notes
GET /api/session/{session_id}/notes

# View formatted HTML report
GET /report/{session_id}
```

## 🪄 Tech Stack
- **Backend:** FastAPI + SQLAlchemy + Jinja2  
- **Database:** SQLite (easily switchable to PostgreSQL)  
- **LLMs:** OpenAI GPT-4, Google Gemini (planned dual-integration)  
- **Frontend (light):** Jinja2 + Markdown2 for clean HTML rendering  

## 📈 Roadmap
| Tag | Milestone | Status |
|-----|------------|--------|
| 1 | Base FastAPI skeleton | ✅ |
| 2 | Dual-LLM orchestration | ✅ |
| 3 | Persistence + Report viewer | ✅ |
| 3.1 | Dashboard & session list | 🔜 |
| 4 | Full LLM integration (OpenAI + Gemini) | 🔜 |
| 5 | Frontend polish & hosting (Render / Hugging Face) | 🔜 |

## 👤 Author
**Helvanljar**  
AI Engineer Trainee · Building intelligent research tools  

[🔗 GitHub Profile](https://github.com/Helvanljar)

## 🧾 License
MIT License © 2025 Helvanljar
