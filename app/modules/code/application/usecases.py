from app.modules.code.domain.entities import CodeSnippet, CodeExecutionResult
from app.modules.code.infrastructure.code_executor import LocalPythonExecutor
from app.modules.code.infrastructure.jdoodle_executor import JDoodleExecutor

class CodeService:
    def __init__(self):
        self.local_executor = LocalPythonExecutor()
        self.remote_executor = JDoodleExecutor()

    def run(self, snippet: CodeSnippet) -> CodeExecutionResult:
        if snippet.language.lower() == "python":
            return self.local_executor.execute(snippet)
        return self.remote_executor.execute(snippet)
