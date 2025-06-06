from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional

from app.schemas.chat import ChatResponse, SafetyRating
from app.core.tools.task_router import detect_task_type
from app.modules.chat.infrastructure.chat_provider_selector import get_resilient_provider
from app.modules.chat.application.usecases import ChatService
from app.core.tools.safety_rating import generate_default_safety_ratings

# Import service classes
from app.modules.vision.application.usecases import VisionService
from app.modules.vision.infrastructure.image_processor import DefaultVisionProcessor
from app.modules.code.application.usecases import CodeService
from app.modules.code.domain.entities import CodeSnippet
from app.modules.audio.application.usecases import AudioService
from app.modules.audio.infrastructure.tts_engine import GoogleTextToSpeech
from app.modules.content.application.usecases import ContentService
from app.modules.content.domain.entities import ContentPrompt
from app.modules.content.infrastructure.content_generator import DummyContentGenerator
import tempfile

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

    # 🚀 Jalankan service sesuai task
    if task == "vision" and file:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(await file.read())
        tmp.flush()
        vision_service = VisionService(DefaultVisionProcessor())
        result_obj = vision_service.analyze(tmp.name)
        result = result_obj.text
        tmp.close()
    elif task == "code":
        code_text = (await file.read()).decode() if file else prompt
        snippet = CodeSnippet(language="python", source_code=code_text)
        code_service = CodeService()
        result_obj = code_service.run(snippet)
        result = result_obj.output if not result_obj.error else result_obj.error
    elif task == "audio":
        audio_service = AudioService(GoogleTextToSpeech())
        audio_resp = audio_service.generate(prompt)
        result = audio_resp.audio_path
    elif task == "content":
        content_service = ContentService(DummyContentGenerator())
        cp = ContentPrompt(topic=prompt, content_type="script")
        result = content_service.generate(cp)
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
