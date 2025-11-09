import os, httpx

async def call_openai_model(prompt: str, model: str, api_key_override=None) -> str:
    api_key = api_key_override or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return f"[OpenAI MOCK] {prompt}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a precise research assistant."},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
