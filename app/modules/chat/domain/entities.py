from dataclasses import dataclass

@dataclass
class ChatMessage:
    prompt: str
    response: str
