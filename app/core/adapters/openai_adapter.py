import uuid
import logging
from openai import OpenAI, OpenAIError, AsyncOpenAI
from app.core.builder.prompt_builder import LLMPromptBuilder
from typing import AsyncGenerator
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.client: AsyncOpenAI = OpenAI(api_key=api_key, timeout=15.0)  # ⏱ Timeout aktif

    def chat(self, prompt_builder: LLMPromptBuilder) -> str:
        messages = prompt_builder.build_openai()
        request_id = f"req-{uuid.uuid4()}"
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
            )
            logger.info(f"[{request_id}] Chat success")
            return response.choices[0].message.content
        except OpenAIError as e:
            logger.error(f"[{request_id}] OpenAI error: {str(e)}")
            return f"[ERROR] {str(e)}"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=10))
    async def stream_response(self, prompt_builder: LLMPromptBuilder) -> AsyncGenerator[str, None]:
        messages = prompt_builder.build_openai()
        request_id = f"req-{uuid.uuid4()}"

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                stream=True,
            )
            logger.info(f"[{request_id}] Streaming started")

            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except OpenAIError as e:
            logger.error(f"[{request_id}] Streaming failed: {str(e)}")
            yield f"[ERROR] {str(e)}"
