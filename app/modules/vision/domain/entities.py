from dataclasses import dataclass

@dataclass
class VisionInput:
    image_path: str
    mode: str  # "ocr", "caption", "vqa"

@dataclass
class VisionResult:
    text: str
