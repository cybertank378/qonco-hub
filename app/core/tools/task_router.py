from typing import Optional

# Simulasi deteksi berdasarkan file type dan prompt
def detect_task_type(prompt: str, file_type: Optional[str] = None) -> str:
    if file_type:
        # 🔍 Deteksi berdasarkan tipe file (gambar, dokumen, excel)
        if file_type.startswith("image/"):
            return "vision"
        if file_type in [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ]:
            return "vision"

    # 🤖 Deteksi berdasarkan kata kunci dalam prompt
    lower_prompt = prompt.lower()
    if any(kw in lower_prompt for kw in ["kode", "program", "debug", "jalankan kode", "refactor"]):
        return "code"
    if any(kw in lower_prompt for kw in ["ubah jadi suara", "bacakan", "tts", "voiceover", "narasi"]):
        return "audio"
    if any(kw in lower_prompt for kw in ["buat konten", "skrip video", "caption", "desain poster", "konten audio", "generator konten"]):
        return "content"
    if any(kw in lower_prompt for kw in ["analisa", "ringkas", "resume", "tinjau", "gambaran", "visualisasi"]):
        return "vision"

    return "chat"

# Contoh test prompt dan file type
tests = [
    {"prompt": "Tolong ubah ini jadi suara narasi", "file_type": None},
    {"prompt": "Buat kode python untuk baca file excel ini", "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
    {"prompt": "Berikan ringkasan dari dokumen berikut", "file_type": "application/pdf"},
    {"prompt": "Jelaskan tentang perubahan iklim", "file_type": None},
    {"prompt": "Debug script ini", "file_type": None}
]

results = [(t["prompt"], detect_task_type(t["prompt"], t["file_type"])) for t in tests]
import pandas as pd
import ace_tools as tools; tools.display_dataframe_to_user(name="Deteksi Task Type", dataframe=pd.DataFrame(results, columns=["Prompt", "TaskType"]))
