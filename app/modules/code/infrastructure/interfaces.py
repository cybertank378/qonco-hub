from abc import ABC, abstractmethod
from app.modules.code.domain.entities import CodeSnippet, CodeExecutionResult

class CodeExecutionEngineInterface(ABC):
    @abstractmethod
    def execute(self, snippet: CodeSnippet) -> CodeExecutionResult:
        pass
