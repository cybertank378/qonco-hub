from pydantic import BaseModel, Field
from typing import List, Literal


class SafetyRating(BaseModel):
    """
    ✅ Safety rating berdasarkan kategori konten berbahaya menurut AI provider.
    """
    category: Literal[
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_DANGEROUS_CONTENT"
    ] = Field(..., description="Kategori potensi bahaya pada respons AI.")

    probability: Literal["NEGLIGIBLE", "LOW", "MEDIUM", "HIGH"] = Field(
        ..., description="Tingkat kemungkinan konten berbahaya muncul."
    )


class ChatRequest(BaseModel):
    """
    📨 Permintaan user ke AI.
    """
    prompt: str = Field(..., example="Jelaskan apa itu perubahan iklim")


class ChatResponse(BaseModel):
    """
    📬 Respons dari AI lengkap dengan rating keamanan.
    """
    response: str = Field(..., description="Respons dari AI dalam bentuk teks.")
    safetyRatings: List[SafetyRating] = Field(
        ..., description="Daftar rating keamanan konten AI."
    )
