from typing import Literal, Optional, List, Dict, Any

TONE_PROFILES = {
    "formal": "Gunakan bahasa formal dan sopan, seperti profesional di dunia kerja.",
    "santai": "Gunakan gaya bahasa santai dan bersahabat, seperti ngobrol dengan teman.",
    "business": "Gunakan kalimat singkat, profesional, dan langsung pada inti permasalahan.",
    "lucu": "Gunakan bahasa yang ringan, jenaka, dan menghibur.",
    "narator_horor": "Gunakan gaya penceritaan menyeramkan, gelap, dan membangun ketegangan.",
    "mentor_teknis": "Gunakan gaya seorang mentor berpengalaman: jelas, mendalam, dan edukatif.",
    "cs_sabar": "Bersikap ramah, sabar, dan tetap profesional dalam menangani keluhan.",
    "robot_nerd": "Jawab dengan gaya robot teknikal yang sangat informatif dan agak kaku.",
    "ceo_perfeksionis": "Gunakan gaya tegas, kritis, dan hasil-berorientasi, seperti CEO perfeksionis.",
}

STYLE_MAP = {
    "analisis": "Berikan penjelasan secara analitis, jelaskan penyebab, proses, dan dampaknya.",
    "instruksi": "Berikan langkah-langkah yang sistematis dan mudah diikuti.",
    "cerita": "Buat penjelasan dalam bentuk narasi yang mengalir.",
    "default": "Jawab pertanyaan dengan penjelasan lengkap dan terstruktur.",
}

LANGUAGE_MAP = {
    "id": "Jawab dalam Bahasa Indonesia.",
    "en": "Answer in English.",
}

FORMAT_MAP = {
    "markdown": "Gunakan format Markdown jika perlu.",
    "plain": "Hindari format khusus, cukup teks biasa.",
    "code": "Gunakan gaya teknis, cocok untuk dokumentasi atau developer.",
}


class LLMPromptBuilder:
    def __init__(
        self,
        prompt: str = "",
        tone: str = "formal",
        language: Literal["id", "en"] = "id",
        style: str = "analisis",
        output_format: str = "markdown",
        memory: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        project_structure: bool = False,
    ):
        self.prompt = prompt
        self.tone = tone
        self.language = language
        self.style = style
        self.output_format = output_format
        self.memory = memory or []
        self.tools = tools or []
        self.project_structure = project_structure

    def set_prompt(self, prompt: str):
        self.prompt = prompt
        return self

    def set_format(self, output_format: str):
        self.output_format = output_format
        return self

    def set_tone(self, tone: str):
        if tone not in TONE_PROFILES:
            raise ValueError(f"Tone '{tone}' tidak dikenali. Gunakan salah satu dari: {', '.join(TONE_PROFILES)}")
        self.tone = tone
        return self

    def set_style(self, style: str):
        self.style = style
        return self

    def set_language(self, lang: str):
        self.language = lang
        return self

    def set_tools(self, tools: List[Dict[str, Any]]):
        self.tools = tools
        return self

    def with_context(self, context: List[Dict[str, str]]):
        self.memory = context
        return self

    def with_project_structure_format(self):
        self.project_structure = True
        return self

    def auto_configure_from_prompt(self) -> "LLMPromptBuilder":
        p = self.prompt.lower()

        if any(word in p for word in ["how", "what", "please explain", "in english", "the reason"]):
            self.language = "en"
        elif any(word in p for word in ["jelaskan", "apa itu", "bagaimana", "mengapa", "tolong"]):
            self.language = "id"

        if any(word in p for word in ["step by step", "cara", "langkah", "how to", "panduan"]):
            self.style = "instruksi"
        elif any(word in p for word in ["ceritakan", "kisah", "cerpen", "narasi"]):
            self.style = "cerita"
        elif any(word in p for word in ["analisis", "analisa", "kenapa", "dampak", "penyebab"]):
            self.style = "analisis"
        else:
            self.style = "default"

        if any(word in p for word in ["as a mentor", "jelaskan secara teknis", "code review", "debug"]):
            self.tone = "mentor_teknis"
        elif any(word in p for word in ["joke", "funny", "ngakak", "bikin lucu"]):
            self.tone = "lucu"
        elif any(word in p for word in ["email bisnis", "pitch deck", "executive summary"]):
            self.tone = "business"
        elif any(word in p for word in ["cerita horor", "menyeramkan", "seram"]):
            self.tone = "narator_horor"
        else:
            self.tone = "formal"

        if any(word in p for word in ["html", "code", "python", "typescript", "sql", "function", "endpoint"]):
            self.output_format = "code"
        elif any(word in p for word in ["ringkasan", "markdown", "judul", "daftar"]):
            self.output_format = "markdown"
        else:
            self.output_format = "plain"

        if any(word in p for word in ["struktur proyek", "multi-file", "file terpisah", "@file:", "tree", "direktori"]):
            self.with_project_structure_format()

        return self

    def _get_instruction_text(self) -> str:
        base = " ".join(filter(None, [
            "Kamu adalah Qonco AI, asisten cerdas dan profesional.",
            LANGUAGE_MAP.get(self.language),
            TONE_PROFILES.get(self.tone),
            STYLE_MAP.get(self.style),
            FORMAT_MAP.get(self.output_format),
        ]))

        if self.project_structure:
            base += (
                "\n\nJika kamu diminta membuat struktur proyek atau beberapa file, "
                "jawablah dengan format:\n"
                "- Gunakan `@file: path/to/file.ext`\n"
                "- Sertakan isi file dalam blok kode\n"
                "- Jika perlu, tampilkan struktur folder dalam format `tree`.\n"
                "Contoh:\n"
                "@file: src/index.tsx\n```tsx\nconsole.log('hello');\n```"
            )

        return base.strip()

    def build_system_prompt(self) -> str:
        return self._get_instruction_text()

    def build_openai(self) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.build_system_prompt()},
            *self.memory,
            {"role": "user", "content": self.prompt or "Halo!"}
        ]

    def build_concatenated_prompt(self) -> str:
        history = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.memory
        )
        return f"{self.build_system_prompt()}\n\n{history}\nUser: {self.prompt or 'Halo!'}"

    def build_gemini(self) -> str:
        return self.build_concatenated_prompt()

    def build_ollama(self) -> str:
        return self.build_concatenated_prompt()

    def get_tools(self) -> Optional[List[Dict[str, Any]]]:
        return self.tools or None
