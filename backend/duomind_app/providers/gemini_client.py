
import os, json
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    _model = genai.GenerativeModel(os.getenv("GEMINI_MODEL","gemini-1.5-flash"))
except Exception:
    _model = None
def _mock_notes(query: str) -> List[Dict]:
    return [{"claim": f"Gemini mock perspective on: {query}", "evidence": [], "confidence": 0.55}]
def _mock_report(query: str, notes: List[Dict], verified: bool) -> str:
    bullets = "\n".join([f"- {n['claim']}" for n in notes])
    tag = "VERIFIED" if verified else "UNVERIFIED"
    return f"# DuoMind Report ({tag})\n**Topic:** {query}\n\n## Gemini Mock Editor Notes\n{bullets}\n"
def researcher_notes(query: str, context: str):
    if _model is None: return _mock_notes(query)
    prompt = f"Return JSON list of claims (claim,evidence[],confidence) about: {query}"
    resp = _model.generate_content(prompt)
    text = (getattr(resp, "text", "") or "").strip()
    try: data = json.loads(text)
    except Exception: return _mock_notes(query)
    return data if isinstance(data, list) else _mock_notes(query)
def editor_report(query: str, notes: List[Dict], verified: bool) -> str:
    if _model is None: return _mock_report(query, notes, verified)
    tag = "VERIFIED" if verified else "UNVERIFIED"
    prompt = f"Synthesize Markdown with sections (Summary, Findings, Limits). Badge {tag}. Notes: {json.dumps(notes, ensure_ascii=False)} Topic: {query}"
    resp = _model.generate_content(prompt)
    return (getattr(resp, "text","") or _mock_report(query, notes, verified)).strip()
