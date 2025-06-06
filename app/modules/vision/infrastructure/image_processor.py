from PIL import Image
import pytesseract
from app.modules.vision.infrastructure.interfaces import VisionProcessorInterface
from app.modules.vision.domain.entities import VisionInput, VisionResult

class DefaultVisionProcessor(VisionProcessorInterface):
    def process(self, data: VisionInput) -> VisionResult:
        if data.mode == "ocr":
            img = Image.open(data.image_path)
            text = pytesseract.image_to_string(img)
            return VisionResult(text=text)

        elif data.mode == "caption":
            return VisionResult(text="(captioning not yet implemented)")

        elif data.mode == "vqa":
            return VisionResult(text="(VQA not yet implemented)")

        return VisionResult(text="(invalid mode)")
