
import os, json
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()
try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    _client = None
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")
def _mock_notes(query: str) -> List[Dict]:
    return [{"claim": f"GPT mock insight about: {query}", "evidence": [], "confidence": 0.5}]
def _mock_report(query: str, notes: List[Dict], verified: bool) -> str:
    bullets = "\n".join([f"- {n['claim']}" for n in notes])
    tag = "VERIFIED" if verified else "UNVERIFIED"
    return f"# DuoMind Report ({tag})\n**Topic:** {query}\n\n## Key Points (GPT Mock)\n{bullets}\n"
def researcher_notes(query: str, context: str):
    if _client is None: return _mock_notes(query)
    prompt = f"Give 3 short claims with simple JSON list (claim, evidence[], confidence) about: {query}"
    resp = _client.chat.completions.create(model=GPT_MODEL, messages=[{"role":"user","content":prompt}])
    text = resp.choices[0].message.content.strip()
    try: data = json.loads(text); 
    except Exception: return _mock_notes(query)
    return data if isinstance(data, list) else _mock_notes(query)
def editor_report(query: str, notes: List[Dict], verified: bool) -> str:
    if _client is None: return _mock_report(query, notes, verified)
    tag = "VERIFIED" if verified else "UNVERIFIED"
    prompt = f"Synthesize to Markdown. Badge {tag}. Notes JSON: {json.dumps(notes, ensure_ascii=False)} Topic: {query}"
    resp = _client.chat.completions.create(model=GPT_MODEL, messages=[{"role":"user","content":prompt}])
    return resp.choices[0].message.content.strip()
