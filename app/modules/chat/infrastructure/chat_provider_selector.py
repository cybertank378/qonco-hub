import os

from app.core.adapters.openai_adapter import OpenAIAdapter
from app.core.adapters.vertex_adapter import VertexAIAdapter
from app.core.adapters.ollama_adapter import OllamaAdapter
from app.core.builder.prompt_builder import LLMPromptBuilder
from app.core.loader import load_config

def get_resilient_provider(prompt: str):
    builder = LLMPromptBuilder().set_prompt(prompt).auto_configure_from_prompt()

    api_key = os.getenv("OPENAI_API_KEY") or load_config().get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")

    try:
        return OpenAIAdapter(api_key), builder.build_openai()
    except Exception:
        pass
    try:
        return VertexAIAdapter(), builder.build_gemini()
    except Exception:
        pass
    try:
        return OllamaAdapter(), builder.build_ollama()
    except Exception:
        pass

    raise RuntimeError("All LLM providers failed.")
