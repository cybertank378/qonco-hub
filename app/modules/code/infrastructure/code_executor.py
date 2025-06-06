import contextlib
import io
from app.modules.code.domain.entities import CodeSnippet, CodeExecutionResult
from app.modules.code.infrastructure.interfaces import CodeExecutionEngineInterface

class LocalPythonExecutor(CodeExecutionEngineInterface):
    def execute(self, snippet: CodeSnippet) -> CodeExecutionResult:
        if snippet.language != "python":
            return CodeExecutionResult(output="", error="Only Python is supported.")

        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(snippet.source_code, {})
            return CodeExecutionResult(output=stdout.getvalue())
        except Exception as e:
            return CodeExecutionResult(output=stdout.getvalue(), error=str(e))
