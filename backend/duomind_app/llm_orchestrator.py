from typing import List, Dict, Tuple, Optional, Any
import asyncio

from duomind_app.config import RESEARCHER_PROVIDER, EDITOR_PROVIDER
from duomind_app.providers import gpt_client, gemini_client

def researcher_generate_notes(query: str, context: str) -> List[Dict]:
    if RESEARCHER_PROVIDER == "gemini":
        return gemini_client.researcher_notes(query, context)
    if RESEARCHER_PROVIDER == "gpt":
        return gpt_client.researcher_notes(query, context)
    return gemini_client.researcher_notes(query, context)

def editor_generate_report(query: str, notes: List[Dict], verified: bool) -> str:
    if EDITOR_PROVIDER == "gpt":
        return gpt_client.editor_report(query, notes, verified)
    if EDITOR_PROVIDER == "gemini":
        return gemini_client.editor_report(query, notes, verified)
    return gpt_client.editor_report(query, notes, verified)

def dual_run(query: str, context: str, verified: bool = True) -> Tuple[List[Dict], str]:
    notes = researcher_generate_notes(query, context)
    report_md = editor_generate_report(query, notes, verified)
    return notes, report_md

# Day 8 compare
from duomind_app.providers import openai_provider, gemini_provider

async def run_dual_research(
    query: str,
    model_a: str = "openai:gpt-4o-mini",
    model_b: str = "gemini:1.5-flash",
    openai_key: Optional[str] = None,
    gemini_key: Optional[str] = None,
    user: Optional[Dict[str, Any]] = None,
):
    async def run_model(tag: str, model_id: str, key_override: Optional[str]):
        if model_id.startswith("openai:"):
            mn = model_id.split(":", 1)[1]
            content = await openai_provider.call_openai_model(query, mn, key_override)
            return {"provider": "openai", "model": mn, "tag": tag, "content": content}
        if model_id.startswith("gemini:"):
            mn = model_id.split(":", 1)[1]
            content = await gemini_provider.call_gemini_model(query, mn, key_override)
            return {"provider": "gemini", "model": mn, "tag": tag, "content": content}
        return {"provider": "unknown", "model": model_id, "tag": tag, "content": f"Unsupported model {model_id}"}

    res_a, res_b = await asyncio.gather(
        run_model("A", model_a, openai_key if model_a.startswith("openai:") else None),
        run_model("B", model_b, gemini_key if model_b.startswith("gemini:") else None),
    )

    synthesis = build_synthesis(query, res_a.get("content", ""), res_b.get("content", ""))

    return {"query": query, "model_a": res_a, "model_b": res_b, "synthesis": synthesis}

def build_synthesis(query: str, a: str, b: str) -> Dict[str, Any]:
    agreements: List[str] = []
    disagreements: List[Dict[str, str]] = []

    if a and b:
        a_lines = [ln.strip() for ln in a.split("\n") if ln.strip()]
        b_lines = [ln.strip() for ln in b.split("\n") if ln.strip()]
        overlap = set(a_lines) & set(b_lines)
        for item in list(overlap)[:3]:
            agreements.append(item)
        diff_a = [ln for ln in a_lines if ln not in overlap][:3]
        diff_b = [ln for ln in b_lines if ln not in overlap][:3]
        for item in diff_a:
            disagreements.append({"from": "A", "text": item})
        for item in diff_b:
            disagreements.append({"from": "B", "text": item})

    return {
        "title": "Vergleich / Synthese",
        "summary": "Both models responded. Agreements show overlap; disagreements show nuance.",
        "agreements": agreements,
        "disagreements": disagreements,
    }
