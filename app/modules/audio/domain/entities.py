from dataclasses import dataclass

@dataclass
class AudioRequest:
    text: str
    voice: str = "default"  # Bisa "male", "female", "narrator", dll

@dataclass
class AudioResponse:
    audio_path: str  # Lokasi file hasil
