import asyncio
import os
from pathlib import Path
import requests
import edge_tts

from .config import (
    EDGE_VOICES, ALIYUN_BASE_URL, ALIYUN_MODEL, ALIYUN_VOICE
)

def _run_async(coro):
    return asyncio.run(coro)

async def _edge_save(text: str, voice: str, output: Path, rate: str = "+0%"):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(output))

def synthesize_edge(text: str, output: Path, language: str = "zh", voice: str = "", rate: str = "+0%"):
    selected_voice = voice or EDGE_VOICES.get(language, EDGE_VOICES["zh"])
    _run_async(_edge_save(text, selected_voice, output, rate))
    return output

def synthesize_aliyun(text: str, output: Path, language: str = "zh", voice: str = ""):
    api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing DASHSCOPE_API_KEY. Configure it in your .env file.")

    # Qwen3-TTS-Flash non-streaming endpoint. The service returns a temporary audio URL.
    payload = {
        "model": ALIYUN_MODEL,
        "input": {
            "text": text,
            "voice": voice or ALIYUN_VOICE,
            "language_type": {"zh": "Chinese", "en": "English"}.get(language, "Auto"),
        },
    }
    response = requests.post(
        f"{ALIYUN_BASE_URL}/services/aigc/multimodal-generation/generation",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Alibaba TTS API error ({response.status_code}): {response.text[:1000]}"
        )
    data = response.json()
    audio_url = data.get("output", {}).get("audio", {}).get("url")
    if not audio_url:
        raise RuntimeError(f"Alibaba TTS returned no audio URL: {data}")
    audio_response = requests.get(audio_url, timeout=120)
    audio_response.raise_for_status()
    output.write_bytes(audio_response.content)
    return output

def synthesize(text: str, output: Path, provider: str = "edge",
               language: str = "zh", voice: str = "", rate: str = "+0%"):
    output.parent.mkdir(parents=True, exist_ok=True)
    if provider == "edge":
        return synthesize_edge(text, output, language, voice, rate)
    if provider == "aliyun":
        return synthesize_aliyun(text, output, language, voice)
    raise ValueError(f"Unknown provider: {provider}")
