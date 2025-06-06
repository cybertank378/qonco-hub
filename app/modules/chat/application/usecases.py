from typing import AsyncGenerator
from app.modules.chat.domain.entities import ChatMessage
from app.modules.chat.infrastructure.interfaces import ChatProviderInterface

class ChatService:
    def __init__(self, provider: ChatProviderInterface, prompt: str):
        self.provider = provider
        self.prompt = prompt

    def ask(self) -> ChatMessage:
        response = self.provider.get_response(self.prompt)
        return ChatMessage(prompt="user", response=response)

    async def stream(self) -> AsyncGenerator[str, None]:
        if not hasattr(self.provider, "stream_response") or not callable(getattr(self.provider, "stream_response")):
            raise NotImplementedError("Provider does not support streaming response.")

        async for chunk in self.provider.stream_response(self.prompt):
            yield chunk
