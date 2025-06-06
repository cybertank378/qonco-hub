from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, stream
from app.core.loader import download_ollama_models

app = FastAPI(
    title="KoncoAI Backend",
    description="AI Chat API with OpenAI provider using Hexagonal Architecture",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(stream.router, prefix="/api/chat", tags=["Stream"])

@app.on_event("startup")
def startup_event():
    download_ollama_models()

@app.get("/")
def root():
    return {"message": "KoncoAI Backend is running"}


