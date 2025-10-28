
from fastapi import APIRouter, Depends
from duomind_app.auth import get_current_user

router = APIRouter(prefix="/api", tags=["models"])

AVAILABLE_MODELS = {
    "openai": ["gpt-4o-mini", "gpt-4o"],
    "gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
    "anthropic": ["claude-3-haiku", "claude-3-sonnet"]
}

MODEL_METADATA = {
    "gpt-4o-mini": {"recommended_for": ["speed","balanced"], "tag": "⚡ fast"},
    "gpt-4o": {"recommended_for": ["quality"], "tag": "💎 quality"},
    "gemini-1.5-flash": {"recommended_for": ["cost","fast"], "tag": "⚡ fast"},
    "gemini-1.5-pro": {"recommended_for": ["research"], "tag": "🧠 research"},
    "claude-3-haiku": {"recommended_for": ["speed","writing"], "tag": "📝 writing"},
    "claude-3-sonnet": {"recommended_for": ["editorial","precision"], "tag": "✍️ editor"}
}

@router.get("/models")
def list_models(user=Depends(get_current_user)):
    return {"available": AVAILABLE_MODELS, "meta": MODEL_METADATA, "user": ("guest" if not user else user.email)}
