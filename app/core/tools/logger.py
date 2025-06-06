import datetime
import os

FALLBACK_LOG_PATH = "app/logs/fallback_log.txt"
USAGE_LOG_PATH = "app/logs/usage_log.txt"

def log_fallback(provider_name: str, reason: str):
    timestamp = datetime.datetime.now().isoformat()
    message = f"[{timestamp}] Fallback triggered on provider '{provider_name}': {reason}\n"
    _write_log(FALLBACK_LOG_PATH, message)

def log_usage(prompt: str, provider: str, model: str, tokens: int, response_time: float):
    timestamp = datetime.datetime.now().isoformat()
    message = (
        f"[{timestamp}] Provider: {provider}, Model: {model}, Tokens: {tokens}, "
        f"ResponseTime: {response_time:.2f}s\nPrompt: {prompt[:200]}...\n\n"
    )
    _write_log(USAGE_LOG_PATH, message)

def _write_log(path: str, message: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(message)
