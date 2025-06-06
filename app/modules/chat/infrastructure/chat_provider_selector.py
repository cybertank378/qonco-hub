from app.core.adapters.openai_adapter import OpenAIAdapter
from app.core.adapters.vertex_adapter import VertexAIAdapter
from app.core.adapters.ollama_adapter import OllamaAdapter
from app.core.builder.prompt_builder import LLMPromptBuilder

def get_resilient_provider(prompt: str):
    builder = LLMPromptBuilder().set_prompt(prompt).auto_configure_from_prompt()
    try: return OpenAIAdapter(), builder.build_openai()
    except: pass
    try: return VertexAIAdapter(), builder.build_gemini()
    except: pass
    try: return OllamaAdapter(), builder.build_ollama()
    except: pass
    raise RuntimeError("All LLM providers failed.")
