import os, httpx

async def call_gemini_model(prompt: str, model: str, api_key_override=None) -> str:
    api_key = api_key_override or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return f"[Gemini MOCK] {prompt}"
    base = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{base}/models/{model}:generateContent?key={api_key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        r.raise_for_status()
        data = r.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return str(data)
