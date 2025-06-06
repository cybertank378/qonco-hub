from abc import ABC, abstractmethod
from app.modules.content.domain.entities import ContentPrompt

class ContentGenerationInterface(ABC):
    @abstractmethod
    def generate(self, prompt: ContentPrompt) -> str:
        pass
