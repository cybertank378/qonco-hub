import requests
from app.modules.code.domain.entities import CodeSnippet, CodeExecutionResult
from app.modules.code.infrastructure.interfaces import CodeExecutionEngineInterface
from app.config import settings

JDoodleLangMap = {
    "python": "python3",
    "cpp": "cpp17",
    "java": "java",
    "c": "c",
    "go": "go",
    "javascript": "nodejs",
    "php": "php",
    "ruby": "ruby",
    "swift": "swift",
    "kotlin": "kotlin",

}

class JDoodleExecutor(CodeExecutionEngineInterface):
    def execute(self, snippet: CodeSnippet) -> CodeExecutionResult:
        lang = JDoodleLangMap.get(snippet.language.lower())
        if not lang:
            return CodeExecutionResult(output="", error="Unsupported language for JDoodle")

        data = {
            "clientId": settings.JDOODLE_CLIENT_ID,
            "clientSecret": settings.JDOODLE_CLIENT_SECRET,
            "script": snippet.source_code,
            "language": lang,
            "versionIndex": "0"
        }

        try:
            response = requests.post("https://api.jdoodle.com/v1/execute", json=data)
            result = response.json()
            return CodeExecutionResult(
                output=result.get("output", ""),
                error=result.get("error", result.get("statusCode") if result.get("statusCode") != 200 else None)
            )
        except Exception as e:
            return CodeExecutionResult(output="", error=str(e))
