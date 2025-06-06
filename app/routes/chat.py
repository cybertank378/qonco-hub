from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional

from app.schemas.chat import ChatResponse, SafetyRating
from app.core.tools.task_router import detect_task_type
from app.modules.chat.infrastructure.chat_provider_selector import get_resilient_provider
from app.modules.chat.application.usecases import ChatService
from app.core.tools.safety_rating import generate_default_safety_ratings

# Import semua service module
from app.modules.vision.application.usecases import process_vision
from app.modules.code.application.usecases import run_code
from app.modules.audio.application.usecases import generate_audio
from app.modules.content.application.usecases import generate_content

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def unified_chat(
    request: Request,
    prompt: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    # Deteksi file type jika ada
    file_type = file.content_type if file else None

    # 🔍 Deteksi task secara otomatis
    task = detect_task_type(prompt, file_type)

    # 🚀 Jalankan usecase sesuai task
    if task == "vision":
        result = await process_vision(prompt, file)
    elif task == "code":
        result = run_code(prompt, file)
    elif task == "audio":
        result = generate_audio(prompt)
    elif task == "content":
        result = generate_content(prompt)
    else:
        # Default ke chat: pakai fallback provider
        provider, built_prompt = get_resilient_provider(prompt)
        service = ChatService(provider, built_prompt)
        message = service.ask()
        result = message.response

    # Tambahkan dummy safety rating (bisa diganti dengan evaluasi aktual)
    safety_ratings = [SafetyRating(**s) for s in generate_default_safety_ratings()]

    return ChatResponse(
        response=result,
        safetyRatings=safety_ratings
    )
