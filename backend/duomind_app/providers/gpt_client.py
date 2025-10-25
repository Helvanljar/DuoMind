
from typing import List, Dict
from duomind_app.config import OPENAI_API_KEY, GPT_MODEL

_client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        _client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        _client = None

def _mock_notes(query: str) -> List[Dict]:
    return [
        {"claim": f"[GPT-MOCK] Overview for '{query}'", "evidence":[{"url":"https://example.org","title":"Mock","quote":"..."}], "confidence":0.7},
        {"claim": "Model-only is quick; retrieval verifies.", "evidence":[{"url":"https://example.org/rag","title":"RAG","quote":"..."}], "confidence":0.8},
    ]

def _mock_report(query: str, notes: List[Dict], verified: bool) -> str:
    badge = "✅ VERIFIED" if verified else "⚠️ UNVERIFIED"
    lines = [f"# DuoMind Report — {badge}", "## Findings"]
    for i, n in enumerate(notes, 1):
        src = n.get("evidence",[{}])[0].get("url","-")
        lines.append(f"- ({i}) {n['claim']} [Source: {src}]")
    lines += ["", "## Limitations", "- Mock output (no real API call)."]
    return "\n".join(lines)

def researcher_notes(query: str, context: str) -> List[Dict]:
    """Use GPT as researcher (JSON list). Falls back to mock if no key/client."""
    if not _client:
        return _mock_notes(query)
    prompt = (
        "Return ONLY a JSON list of 3–6 objects with fields: "
        "claim (string), evidence (list of {url,title,quote}), confidence (0..1). "
        f"Query: {query}\nContext:\n{context}"
    )
    resp = _client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "system", "content": "Return only a valid JSON list."},
                  {"role": "user", "content": prompt}],
        temperature=0.2,
    )
    import json
    text = (resp.choices[0].message.content or "").strip()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return _mock_notes(query)

def editor_report(query: str, notes: List[Dict], verified: bool) -> str:
    """Use GPT as editor (Markdown). Falls back to mock if no key/client."""
    if not _client:
        return _mock_report(query, notes, verified)
    import json
    notes_json = json.dumps(notes, ensure_ascii=False)
    badge = "VERIFIED" if verified else "UNVERIFIED"
    prompt = (
        f"Create a clean Markdown report for '{query}'. Use only these notes (JSON): {notes_json}. "
        "Include: Executive Summary, Key Findings with inline source URLs, Limitations. "
        f"Add a top badge: {badge}."
    )
    resp = _client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "system", "content": "Output must be Markdown."},
                  {"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return (resp.choices[0].message.content or "").strip() or _mock_report(query, notes, verified)
