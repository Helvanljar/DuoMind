
from typing import List, Dict, Tuple
from duomind_app.config import RESEARCHER_PROVIDER, EDITOR_PROVIDER
from duomind_app.providers import gpt_client, gemini_client
def researcher_generate_notes(query: str, context: str) -> List[Dict]:
    if RESEARCHER_PROVIDER == "gemini": return gemini_client.researcher_notes(query, context)
    if RESEARCHER_PROVIDER == "gpt": return gpt_client.researcher_notes(query, context)
    return gemini_client.researcher_notes(query, context)
def editor_generate_report(query: str, notes: List[Dict], verified: bool) -> str:
    if EDITOR_PROVIDER == "gpt": return gpt_client.editor_report(query, notes, verified)
    if EDITOR_PROVIDER == "gemini": return gemini_client.editor_report(query, notes, verified)
    return gpt_client.editor_report(query, notes, verified)
def dual_run(query: str, context: str, verified: bool = True) -> Tuple[List[Dict], str]:
    notes = researcher_generate_notes(query, context)
    report_md = editor_generate_report(query, notes, verified)
    return notes, report_md
