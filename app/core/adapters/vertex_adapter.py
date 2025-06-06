from vertexai.language_models import ChatModel
from app.core.builder.prompt_builder import LLMPromptBuilder
from typing import AsyncGenerator
import asyncio

class VertexAIAdapter:
    def __init__(self):
        self.model = ChatModel.from_pretrained("chat-bison")

    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        builder = LLMPromptBuilder(prompt)
        built_prompt = builder.build_gemini()

        # Vertex AI SDK belum mendukung streaming async → disimulasikan
        chat = self.model.start_chat()
        response = chat.send_message(built_prompt).text

        for token in response.split():
            await asyncio.sleep(0.02)  # simulasi streaming
            yield token + " "
