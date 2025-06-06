from app.modules.vision.domain.entities import VisionInput, VisionResult
from app.modules.vision.infrastructure.interfaces import VisionProcessorInterface

class VisionService:
    def __init__(self, processor: VisionProcessorInterface):
        self.processor = processor

    def analyze(self, image_path: str, mode: str = "ocr") -> VisionResult:
        request = VisionInput(image_path=image_path, mode=mode)
        return self.processor.process(request)
