import os
from gtts import gTTS
from uuid import uuid4
from app.modules.audio.domain.entities import AudioRequest, AudioResponse
from app.modules.audio.infrastructure.interfaces import TextToSpeechInterface

class GoogleTextToSpeech(TextToSpeechInterface):
    def synthesize(self, request: AudioRequest) -> AudioResponse:
        tts = gTTS(text=request.text, lang="id" if "indonesia" in request.text.lower() else "en")
        filename = f"/tmp/tts_{uuid4().hex}.mp3"
        tts.save(filename)
        return AudioResponse(audio_path=filename)
