from abc import ABC, abstractmethod
from app.modules.vision.domain.entities import VisionInput, VisionResult

class VisionProcessorInterface(ABC):
    @abstractmethod
    def process(self, data: VisionInput) -> VisionResult:
        pass
