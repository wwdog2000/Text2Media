from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

EDGE_VOICES = {
    "zh": "zh-CN-XiaoxiaoNeural",
    "en": "en-US-AriaNeural",
}
ALIYUN_VOICE = os.getenv("DASHSCOPE_VOICE", "Cherry")
ALIYUN_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen3-tts-flash")
ALIYUN_BASE_URL = os.getenv(
    "DASHSCOPE_BASE_URL",
    "https://dashscope-intl.aliyuncs.com/api/v1"
).rstrip("/")
FONT_PATH = os.getenv("TEXT2MEDIA_FONT", "")
