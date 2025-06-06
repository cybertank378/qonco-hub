from app.modules.content.domain.entities import ContentPrompt
from app.modules.content.infrastructure.interfaces import ContentGenerationInterface

class DummyContentGenerator(ContentGenerationInterface):
    def generate(self, prompt: ContentPrompt) -> str:
        return (
            f"[Generated {prompt.content_type}]\n"
            f"Topic: {prompt.topic}\n"
            f"Audience: {prompt.audience}\n"
            f"Tone: {prompt.tone}\n"
            f"Style: {prompt.style}\n"
        )
