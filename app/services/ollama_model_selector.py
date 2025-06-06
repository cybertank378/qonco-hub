def pick_ollama_model(prompt: str) -> str:
    """
    Pilih model Ollama berdasarkan jenis prompt.
    """
    lower = prompt.lower()

    # 👨‍💻 Deteksi kebutuhan coding
    if any(kw in lower for kw in ["python", "debug", "script", "kode", "program"]):
        return "codellama:latest"

    # 🧠 Deteksi reasoning atau instruction-based prompt
    if any(kw in lower for kw in ["penjelasan", "analisa", "jelaskan", "mengapa", "bagaimana"]):
        return "llama3:instruct"

    # ✍️ Deteksi pembuatan konten naratif atau kreatif
    if any(kw in lower for kw in ["cerita", "narasi", "konten", "blog", "tulisan"]):
        return "llama3:latest"

    # 🖼️ Deteksi jika terkait file atau multimodal (opsional)
    if any(kw in lower for kw in ["gambar", "visual", "pdf", "dokumen"]):
        return "llava:7b"

    # 🌐 Default model general purpose
    return "llama3:latest"
