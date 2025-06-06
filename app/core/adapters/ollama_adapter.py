import aiohttp
import json
from typing import AsyncGenerator
from app.core.builder.prompt_builder import LLMPromptBuilder
from app.services.ollama_model_selector import pick_ollama_model

class OllamaAdapter:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"

    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        builder = LLMPromptBuilder(prompt)
        model = pick_ollama_model(prompt)
        built_prompt = builder.build_ollama()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                json={"model": model, "prompt": built_prompt, "stream": True},
            ) as resp:
                async for line in resp.content:
                    if not line:
                        continue
                    try:
                        data = json.loads(line.decode("utf-8").strip().removeprefix("data: "))
                        content = data.get("response", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
