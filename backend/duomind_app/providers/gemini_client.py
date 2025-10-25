
from typing import List, Dict
from duomind_app.config import GEMINI_API_KEY, GEMINI_MODEL

_model = None
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(GEMINI_MODEL)
    except Exception:
        _model = None

def _mock_notes(query: str) -> List[Dict]:
    return [
        {"claim": f"[Gemini-MOCK] Broad context collected for '{query}'", "evidence":[{"url":"https://example.org/intro","title":"Intro","quote":"..."}], "confidence":0.7},
        {"claim": "Critic agents improve factuality.", "evidence":[{"url":"https://example.org/quality","title":"Quality","quote":"..."}], "confidence":0.75},
    ]

def _mock_report(query: str, notes: List[Dict], verified: bool) -> str:
    badge = "✅ VERIFIED" if verified else "⚠️ UNVERIFIED"
    items = "\n".join([f"- ({i+1}) {n['claim']}" for i, n in enumerate(notes)])
    return f"# DuoMind Report — {badge}\n\n## Findings\n{items}\n\n## Limitations\n- Mock output."

def researcher_notes(query: str, context: str) -> List[Dict]:
    """Use Gemini as researcher (JSON list). Falls back to mock."""
    if not _model:
        return _mock_notes(query)
    prompt = (
        "Return ONLY a JSON list of 3–6 objects with fields: "
        "claim (string), evidence (list of {url,title,quote}), confidence (0..1). "
        f"Query: {query}\nContext:\n{context}"
    )
    resp = _model.generate_content(prompt)
    text = (getattr(resp, 'text', '') or '').strip()
    import json
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return _mock_notes(query)

def editor_report(query: str, notes: List[Dict], verified: bool) -> str:
    """Use Gemini as editor (Markdown). Falls back to mock."""
    if not _model:
        return _mock_report(query, notes, verified)
    import json
    notes_json = json.dumps(notes, ensure_ascii=False)
    badge = "VERIFIED" if verified else "UNVERIFIED"
    prompt = (
        f"Create a clean Markdown report for '{query}'. Use only these notes (JSON): {notes_json}. "
        "Include: Executive Summary, Key Findings with inline source URLs, Limitations. "
        f"Add a top badge: {badge}."
    )
    resp = _model.generate_content(prompt)
    return (getattr(resp, 'text', '') or '').strip() or _mock_report(query, notes, verified)
