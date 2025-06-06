from fastapi.responses import StreamingResponse
from typing import Optional
import json

from app.modules.chat.infrastructure.chat_provider_selector import get_resilient_provider
from app.modules.chat.application.usecases import ChatService
from app.core.tools.safety_rating import generate_default_safety_ratings
from app.modules.vision.application.usecases import VisionService
from app.modules.code.application.usecases import CodeService
from app.modules.audio.application.usecases import AudioService
from app.modules.content.application.usecases import ContentService
from app.core.tools.task_router import detect_task_type


def stream_chat_response(prompt: str) -> StreamingResponse:
    provider, built_prompt = get_resilient_provider(prompt)
    service = ChatService(provider, built_prompt)

    async def event_stream():
        async for chunk in service.stream():  # ✅ ensure ChatService has .stream()
            yield f"data: {chunk}\\n\\n"
        yield _safety_event()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def stream_vision_response(prompt: str, file: Optional[bytes] = None) -> StreamingResponse:
    service = VisionService()

    async def event_stream():
        async for chunk in service.stream(prompt=prompt, file=file):
            yield f"data: {chunk}\\n\\n"
        yield _safety_event()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def stream_code_response(prompt: str) -> StreamingResponse:
    service = CodeService()

    async def event_stream():
        async for chunk in service.stream(prompt=prompt):
            yield f"data: {chunk}\\n\\n"
        yield _safety_event()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def stream_audio_response(prompt: str) -> StreamingResponse:
    service = AudioService()

    async def event_stream():
        async for chunk in service.stream(prompt=prompt):
            yield f"data: {chunk}\\n\\n"
        yield _safety_event()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def stream_content_response(prompt: str) -> StreamingResponse:
    service = ContentService()

    async def event_stream():
        async for chunk in service.stream(prompt=prompt):
            yield f"data: {chunk}\\n\\n"
        yield _safety_event()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def stream_auto_response(prompt: str, file_type: Optional[str] = None, file: Optional[bytes] = None) -> StreamingResponse:
    task = detect_task_type(prompt, file_type)

    if task == "vision":
        return stream_vision_response(prompt, file)
    elif task == "code":
        return stream_code_response(prompt)
    elif task == "audio":
        return stream_audio_response(prompt)
    elif task == "content":
        return stream_content_response(prompt)
    else:
        return stream_chat_response(prompt)


def _safety_event():
    payload = {
        "type": "safety",
        "ratings": [r.dict() for r in generate_default_safety_ratings()]
    }
    return f"data: {json.dumps(payload)}\\n\\n"