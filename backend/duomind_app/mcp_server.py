from __future__ import annotations

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from .llm_orchestrator import run_dual_research, run_compare_reconcile, run_debate_and_converge

mcp = FastMCP("DuoMind", json_response=True)


@mcp.tool()
async def duomind_dual_research(
    query: str,
    model_a: str = "openai:gpt-4o-mini",
    model_b: str = "gemini:1.5-flash",
    openai_key: Optional[str] = None,
    gemini_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Run DuoMind dual research (two models + lightweight synthesis)."""
    return await run_dual_research(
        query=query,
        model_a=model_a,
        model_b=model_b,
        openai_key=openai_key,
        gemini_key=gemini_key,
    )


@mcp.tool()
async def duomind_compare_reconcile_tool(
    query: str,
    answer_a: str,
    answer_b: str,
    lang: str = "en",
    openai_key: Optional[str] = None,
    gemini_key: Optional[str] = None,
) -> Dict[str, Any]:
    """LLM-powered comparison/reconciliation (returns JSON)."""
    return await run_compare_reconcile(
        query=query,
        answer_a=answer_a,
        answer_b=answer_b,
        lang=lang,
        openai_key=openai_key,
        gemini_key=gemini_key,
    )


@mcp.tool()
async def duomind_debate_and_converge(
    query: str,
    model_a: str = "openai:gpt-4o-mini",
    model_b: str = "gemini:1.5-flash",
    lang: str = "en",
    openai_key: Optional[str] = None,
    gemini_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Two-LLM debate + public retrieval (Wikipedia) + evidence-gated final answer."""
    return await run_debate_and_converge(
        query=query,
        model_a=model_a,
        model_b=model_b,
        lang=lang,
        openai_key=openai_key,
        gemini_key=gemini_key,
    )
