from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeSnippet:
    language: str
    source_code: str

@dataclass
class CodeExecutionResult:
    output: str
    error: Optional[str] = None
