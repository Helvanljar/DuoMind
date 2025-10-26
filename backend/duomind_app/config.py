
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

RESEARCHER_PROVIDER = os.getenv("RESEARCHER_PROVIDER", "gemini").strip().lower()
EDITOR_PROVIDER = os.getenv("EDITOR_PROVIDER", "gpt").strip().lower()

GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///duomind.db").strip()
