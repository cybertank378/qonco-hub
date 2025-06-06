from app.modules.chat.infrastructure.chat_provider_selector import get_resilient_provider
from app.modules.chat.application.usecases import ChatService
from app.modules.chat.domain.entities import ChatMessage
from app.core.tools.logger import log_usage, log_fallback
import time


def get_ai_response(prompt: str) -> ChatMessage:
    # ⏱ Mulai timer untuk logging durasi respons
    start_time = time.time()

    # 🧠 Bangun prompt dan pilih provider dengan fallback
    try:
        provider, built_prompt = get_resilient_provider(prompt)
    except Exception as e:
        log_fallback("ALL", str(e))
        raise RuntimeError("Semua provider LLM gagal dijalankan.")

    # 🤖 Proses prompt menggunakan ChatService
    service = ChatService(provider, built_prompt)
    result = service.ask()

    # 🕒 Log penggunaan dan durasi respons
    response_time = time.time() - start_time
    log_usage(prompt, provider.__class__.__name__, getattr(provider, "model", "unknown"), tokens=len(prompt.split()), response_time=response_time)

    return result
