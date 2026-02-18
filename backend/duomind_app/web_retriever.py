from __future__ import annotations

from typing import Any, Dict, List, Optional
import re
import urllib.parse

import httpx

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_REST_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/"

USER_AGENT = "DuoMind/1.0 (RAG-lite via Wikipedia; contact: none)"


async def wikipedia_search(query: str, *, limit: int = 5, lang: str = "en") -> List[Dict[str, Any]]:
    """Search Wikipedia for a query and return top results (title + url)."""
    q = (query or "").strip()
    if not q:
        return []
    api = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": q,
        "srlimit": str(max(1, min(limit, 10))),
        "format": "json",
    }
    async with httpx.AsyncClient(timeout=12.0, headers={"User-Agent": USER_AGENT}) as client:
        r = await client.get(api, params=params)
        r.raise_for_status()
        data = r.json()

    out: List[Dict[str, Any]] = []
    for item in (data.get("query", {}) or {}).get("search", [])[:limit]:
        title = item.get("title") or ""
        if not title:
            continue
        url_title = urllib.parse.quote(title.replace(" ", "_"))
        url = f"https://{lang}.wikipedia.org/wiki/{url_title}"
        out.append({"title": title, "url": url, "snippet_html": item.get("snippet", "")})
    return out


async def wikipedia_summary(title: str, *, lang: str = "en") -> Optional[Dict[str, Any]]:
    """Fetch Wikipedia REST summary (plain text extract + canonical url)."""
    t = (title or "").strip()
    if not t:
        return None
    url_title = urllib.parse.quote(t.replace(" ", "_"))
    rest = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{url_title}"
    async with httpx.AsyncClient(timeout=12.0, headers={"User-Agent": USER_AGENT}) as client:
        r = await client.get(rest)
        if r.status_code != 200:
            return None
        data = r.json()
    extract = (data.get("extract") or "").strip()
    if not extract:
        return None
    canonical = None
    content_urls = data.get("content_urls") or {}
    if isinstance(content_urls, dict):
        canonical = (content_urls.get("desktop") or {}).get("page") or (content_urls.get("mobile") or {}).get("page")
    return {
        "title": data.get("title") or t,
        "url": canonical or f"https://{lang}.wikipedia.org/wiki/{url_title}",
        "extract": extract,
    }


def _strip_html(text: str) -> str:
    # Wikipedia search 'snippet' contains <span class="searchmatch">...</span>
    t = re.sub(r"<[^>]+>", "", text or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


async def retrieve_evidence(query: str, *, lang: str = "en", max_pages: int = 3, max_chars: int = 1400) -> List[Dict[str, Any]]:
    """RAG-lite retrieval: Wikipedia search + summaries (no local DB).

    Returns a list of evidence items:
      {source: 'wikipedia', title, url, snippet}
    """
    results = await wikipedia_search(query, limit=max_pages, lang=lang)
    evidence: List[Dict[str, Any]] = []
    for r in results[:max_pages]:
        summ = await wikipedia_summary(r["title"], lang=lang)
        if not summ:
            # fallback: at least keep search snippet
            snip = _strip_html(r.get("snippet_html", ""))[:max_chars]
            if snip:
                evidence.append({"source": "wikipedia", "title": r["title"], "url": r["url"], "snippet": snip})
            continue
        snip = summ["extract"][:max_chars]
        evidence.append({"source": "wikipedia", "title": summ["title"], "url": summ["url"], "snippet": snip})
    return evidence
