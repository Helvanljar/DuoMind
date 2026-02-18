from typing import Optional

import httpx


MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


async def call_mistral_model(prompt: str, model: str, api_key_override: Optional[str] = None) -> str:
    """Call the Mistral chat completions API and return the assistant text."""

    api_key = (api_key_override or "").strip()
    if not api_key:
        raise RuntimeError("Mistral API key missing")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(MISTRAL_URL, headers=headers, json=payload)

    if resp.status_code >= 400:
        raise RuntimeError(f"Mistral error {resp.status_code}: {resp.text}")

    data = resp.json() or {}
    try:
        return (data.get("choices", [])[0].get("message", {}).get("content") or "").strip()
    except Exception:
        raise RuntimeError("Mistral response contained no text output")
