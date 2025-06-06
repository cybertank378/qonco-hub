from abc import ABC, abstractmethod
from app.modules.audio.domain.entities import AudioRequest, AudioResponse

class TextToSpeechInterface(ABC):
    @abstractmethod
    def synthesize(self, request: AudioRequest) -> AudioResponse:
        pass
