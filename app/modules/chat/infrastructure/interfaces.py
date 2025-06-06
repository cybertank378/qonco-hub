from abc import ABC, abstractmethod

class ChatProviderInterface(ABC):
    @abstractmethod
    def get_response(self, prompt) -> str:
        pass

    def stream_response(self, prompt):
        pass
