from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional
import json
import time

from app.core.tools.task_router import detect_task_type
from app.core.tools.safety_rating import generate_default_safety_ratings
from app.modules.chat.infrastructure.chat_provider_selector import get_resilient_provider
from app.modules.chat.application.usecases import ChatService

# Optional streaming modules
from app.modules.vision.application.usecases import stream_vision_response
from app.modules.audio.application.usecases import stream_audio_response
from app.modules.content.application.usecases import stream_content_response
from app.modules.code.application.usecases import stream_code_response

router = APIRouter()


@router.post("/chat/stream/auto")
async def stream_auto_chat(
    request: Request,
    prompt: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_type = file.content_type if file else None
    task = detect_task_type(prompt, file_type)

    # 🧠 Dispatcher streaming berdasarkan task
    async def stream_generator():
        start = time.time()

        try:
            if task == "vision":
                async for chunk in stream_vision_response(prompt, file):
                    yield f"data: {chunk}\n\n"

            elif task == "code":
                async for chunk in stream_code_response(prompt, file):
                    yield f"data: {chunk}\n\n"

            elif task == "audio":
                async for chunk in stream_audio_response(prompt):
                    yield f"data: {chunk}\n\n"

            elif task == "content":
                async for chunk in stream_content_response(prompt):
                    yield f"data: {chunk}\n\n"

            else:
                provider, built_prompt = get_resilient_provider(prompt)
                service = ChatService(provider, built_prompt)
                async for chunk in service.stream():  # pastikan ChatService mendukung stream()
                    yield f"data: {chunk}\n\n"

        finally:
            # 🛡️ Tambahkan safety rating di akhir
            ratings = generate_default_safety_ratings()
            yield f"data: {json.dumps({'type': 'safety', 'ratings': ratings})}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
