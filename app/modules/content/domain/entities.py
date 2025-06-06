from pydantic import BaseModel
from typing import Literal

class ContentPrompt(BaseModel):
    topic: str
    content_type: Literal["audio", "video", "image", "script"]
    audience: str = "general"
    tone: str = "informative"
    style: str = "default"