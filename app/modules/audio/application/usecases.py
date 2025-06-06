from app.modules.audio.domain.entities import AudioRequest, AudioResponse
from app.modules.audio.infrastructure.interfaces import TextToSpeechInterface

class AudioService:
    def __init__(self, engine: TextToSpeechInterface):
        self.engine = engine

    def generate(self, text: str, voice: str = "default") -> AudioResponse:
        return self.engine.synthesize(AudioRequest(text=text, voice=voice))
