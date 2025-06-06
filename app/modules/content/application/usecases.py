from app.modules.content.domain.entities import ContentPrompt
from app.modules.content.infrastructure.interfaces import ContentGenerationInterface

class ContentService:
    def __init__(self, generator: ContentGenerationInterface):
        self.generator = generator

    def generate(self, prompt: ContentPrompt) -> str:
        return self.generator.generate(prompt)