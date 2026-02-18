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

import json
import re

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
        # UI localizes the section title. Keep content language-neutral.
        "title": "Comparison / Synthesis",
        "summary": "",
        "agreements": agreements,
        "disagreements": disagreements,
    }


def _extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Best-effort JSON extraction for LLM output.

    Accepts raw JSON or JSON wrapped in Markdown fences.
    """
    if not text:
        return None
    t = text.strip()
    # Strip ```json ... ``` fences
    t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*```$", "", t)

    # Fast path
    try:
        obj = json.loads(t)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # Find first {...} block
    m = re.search(r"\{.*\}", t, flags=re.DOTALL)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


async def run_compare_reconcile(
    *,
    query: str,
    answer_a: str,
    answer_b: str,
    lang: str = "en",
    openai_key: Optional[str] = None,
    gemini_key: Optional[str] = None,
) -> Dict[str, Any]:
    """LLM-powered comparison (opt-in).

    Uses OpenAI if an OpenAI key is available, otherwise Gemini.
    """

    lang_map = {
        "en": "English",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "pt": "Portuguese",
        "tr": "Turkish",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "th": "Thai",
        "id": "Indonesian",
        "vi": "Vietnamese",
        "ar": "Arabic",
    }
    lang_name = lang_map.get((lang or "en").lower(), "English")

    prompt = (
        "You are a neutral analyst. Compare two independent answers to the same user query. "
        "Produce a helpful reconciliation and highlight where they differ.\n\n"
        "Return STRICT JSON (no markdown) with keys:\n"
        "- summary: string (2–4 sentences)\n"
        "- agreements: array of 3–6 short bullet strings\n"
        "- disagreements: array of 3–6 short bullet strings\n"
        "- recommendation: string (best combined answer or guidance, 4–10 sentences)\n"
        "- open_questions: array of 0–5 short bullet strings (only if needed)\n\n"
        f"Write in {lang_name}.\n\n"
        f"USER QUERY:\n{query}\n\n"
        f"ANSWER A:\n{answer_a}\n\n"
        f"ANSWER B:\n{answer_b}\n"
    )

    used_provider = None
    used_model = None
    raw = ""

    if (openai_key or "").strip():
        used_provider = "openai"
        used_model = "gpt-4o-mini"
        raw = await openai_provider.call_openai_model(prompt, used_model, openai_key)
    elif (gemini_key or "").strip():
        used_provider = "gemini"
        used_model = "1.5-flash"
        raw = await gemini_provider.call_gemini_model(prompt, used_model, gemini_key)
    else:
        return {"ok": False, "detail": "Missing API key."}

    obj = _extract_first_json_object(raw) or {}

    data = {
        "provider": used_provider,
        "model": used_model,
        "summary": str(obj.get("summary", "")).strip(),
        "agreements": obj.get("agreements", []) if isinstance(obj.get("agreements", []), list) else [],
        "disagreements": obj.get("disagreements", []) if isinstance(obj.get("disagreements", []), list) else [],
        "recommendation": str(obj.get("recommendation", "")).strip(),
        "open_questions": obj.get("open_questions", []) if isinstance(obj.get("open_questions", []), list) else [],
        "raw": raw,
    }
    return {"ok": True, "data": data}


async def run_debate_and_converge(
    *,
    query: str,
    model_a: str = "openai:gpt-4o-mini",
    model_b: str = "gemini:1.5-flash",
    lang: str = "en",
    openai_key: Optional[str] = None,
    gemini_key: Optional[str] = None,
    evidence_lang: Optional[str] = None,
) -> Dict[str, Any]:
    """Two-LLM debate + web retrieval (Wikipedia) + evidence-gated judge.

    This is "RAG-lite": retrieval comes from public sources (Wikipedia) so we don't need a custom vector DB.
    """
    from duomind_app.web_retriever import retrieve_evidence

    q = (query or "").strip()
    if not q:
        return {"ok": False, "detail": "query is required"}

    # 1) Get initial answers from both models
    base_prompt = (
        "Answer the user question.\n"
        "Then list your key claims as bullet points.\n"
        "Be concise.\n\n"
        f"QUESTION:\n{q}\n"
    )

    async def run_model_answer(model_id: str) -> str:
        if model_id.startswith("openai:"):
            mn = model_id.split(":", 1)[1]
            return await openai_provider.call_openai_model(base_prompt, mn, openai_key)
        if model_id.startswith("gemini:"):
            mn = model_id.split(":", 1)[1]
            return await gemini_provider.call_gemini_model(base_prompt, mn, gemini_key)
        return f"Unsupported model: {model_id}"

    answer_a, answer_b = await asyncio.gather(
        run_model_answer(model_a),
        run_model_answer(model_b),
    )

    # 2) Retrieve evidence (Wikipedia)
    ev_lang = (evidence_lang or lang or "en").lower()
    if ev_lang not in {"en", "de", "fr", "es", "pt", "it", "nl"}:
        ev_lang = "en"
    evidence = await retrieve_evidence(q, lang=ev_lang, max_pages=3)

    evidence_block = ""
    if evidence:
        parts = []
        for i, item in enumerate(evidence, start=1):
            parts.append(
                f"[E{i}] {item.get('title','')}\nURL: {item.get('url','')}\nSNIPPET: {item.get('snippet','')}\n"
            )
        evidence_block = "\n\n".join(parts)

    # 3) Evidence-gated judge: decide what's true based on evidence
    lang_map = {
        "en": "English",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "pt": "Portuguese",
        "tr": "Turkish",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "th": "Thai",
        "id": "Indonesian",
        "vi": "Vietnamese",
        "ar": "Arabic",
    }
    lang_name = lang_map.get((lang or "en").lower(), "English")

    judge_prompt = (
        "You are a strict fact-checking judge. Your job: reconcile two answers using ONLY the provided EVIDENCE.\n"
        "Rules:\n"
        "1) If a claim is not supported by EVIDENCE, mark it as unsupported (even if it sounds plausible).\n"
        "2) Prefer the most directly supported statements.\n"
        "3) If evidence is insufficient, say so clearly and suggest what to look up next.\n\n"
        "Return STRICT JSON (no markdown) with keys:\n"
        "- final_answer: string (4–10 sentences)\n"
        "- supported_facts: array of 3–8 short bullet strings\n"
        "- rejected_claims: array of objects {claim: string, reason: string}\n"
        "- sources: array of objects {label: string, url: string}\n"
        "- confidence: string (one of: low, medium, high)\n\n"
        f"Write in {lang_name}.\n\n"
        f"QUESTION:\n{q}\n\n"
        f"ANSWER A:\n{answer_a}\n\n"
        f"ANSWER B:\n{answer_b}\n\n"
        f"EVIDENCE:\n{evidence_block if evidence_block else 'No evidence retrieved.'}\n"
    )

    used_provider = None
    used_model = None
    raw = ""

    if (openai_key or "").strip():
        used_provider = "openai"
        used_model = "gpt-4o-mini"
        raw = await openai_provider.call_openai_model(judge_prompt, used_model, openai_key)
    elif (gemini_key or "").strip():
        used_provider = "gemini"
        used_model = "1.5-flash"
        raw = await gemini_provider.call_gemini_model(judge_prompt, used_model, gemini_key)
    else:
        return {"ok": False, "detail": "Missing API key."}

    obj = _extract_first_json_object(raw) or {}

    # Normalize sources based on evidence labels
    sources = obj.get("sources", [])
    if not isinstance(sources, list):
        sources = []
    norm_sources = []
    for s in sources:
        if isinstance(s, dict):
            lbl = str(s.get("label", "")).strip()
            url = str(s.get("url", "")).strip()
            if lbl and url:
                norm_sources.append({"label": lbl, "url": url})
    # If model didn't include sources, add evidence urls
    if not norm_sources and evidence:
        for i, item in enumerate(evidence, start=1):
            u = str(item.get("url", "")).strip()
            if u:
                norm_sources.append({"label": f"E{i}", "url": u})

    data = {
        "judge_provider": used_provider,
        "judge_model": used_model,
        "answer_a": answer_a,
        "answer_b": answer_b,
        "evidence": evidence,
        "final_answer": str(obj.get("final_answer", "")).strip(),
        "supported_facts": obj.get("supported_facts", []) if isinstance(obj.get("supported_facts", []), list) else [],
        "rejected_claims": obj.get("rejected_claims", []) if isinstance(obj.get("rejected_claims", []), list) else [],
        "sources": norm_sources,
        "confidence": str(obj.get("confidence", "")).strip() or "medium",
        "raw": raw,
    }
    return {"ok": True, "data": data}
