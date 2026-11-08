# Text2Media

**Turn text into speech, subtitles, and captioned videos.**

Text2Media is a beginner-friendly, local-first Python project with two TTS providers:
- Edge-TTS (online, no API key)
- Alibaba Cloud Model Studio / DashScope Qwen TTS (API key required)

It can export MP3/WAV audio, SRT subtitles, and MP4 videos with burned-in subtitles.

## Features (v1.0)
- Chinese and English text-to-speech
- Select Edge-TTS or Alibaba TTS
- Generate audio and sentence-level SRT subtitles
- Create MP4 from a still-image background or a solid-color background
- CLI and Gradio web interface
- API keys are read from environment variables / `.env`, never hard-coded

## Requirements
- macOS, Windows, or Linux
- Python 3.10+
- FFmpeg installed and available in PATH
- Internet connection for either online TTS provider

## Quick start (macOS)
```bash
brew install ffmpeg
git clone https://github.com/wwdog2000/Text2Media.git
cd Text2Media
bash install.sh
```
The installer creates `.venv`, installs Python packages, and opens `.env` in TextEdit if it exists.

Start the web UI:
```bash
source .venv/bin/activate
python app.py
```
Open the local URL printed in Terminal (usually http://127.0.0.1:7860).

## CLI examples
Generate audio and SRT:
```bash
python main.py audio --text-file examples/example.txt --provider edge --language zh --output output/demo
```

Generate a video with an image background:
```bash
python main.py video --text-file examples/example.txt --provider edge --language zh \
  --background assets/backgrounds/sample.png --output output/demo-video --width 1080 --height 1920
```

Use Alibaba TTS:
```bash
python main.py audio --text-file examples/example.txt --provider aliyun --language zh --output output/aliyun-demo
```

## Alibaba Cloud configuration
1. Create an API key in Alibaba Cloud Model Studio.
2. Copy `.env.example` to `.env`.
3. Put the key in `DASHSCOPE_API_KEY`.
4. Keep `.env` private. It is excluded by `.gitignore`.

Example:
```dotenv
DASHSCOPE_API_KEY=your_api_key_here
DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1
DASHSCOPE_MODEL=qwen3-tts-flash
DASHSCOPE_VOICE=Cherry
```
The default endpoint above is for the international service. If your API key belongs to the China (Beijing) region, use the matching regional endpoint and key shown in your Model Studio console. API keys are region-specific.

## Important notes
- Edge-TTS uses Microsoft's online speech service; it is not offline TTS and availability can change.
- Alibaba TTS is a paid cloud service subject to your account's model availability, pricing, quotas, region, and voice support.
- The first version creates sentence-level subtitle timing by measuring each generated sentence audio clip. Timing is more reliable than estimating from character count, but it is not forced word-level alignment.
- Text is split into sentences/chunks before synthesis. Provider voice names and supported languages can change; check the provider's current documentation.
- Do not commit `.env`, API keys, generated audio, or videos.

## Project layout
```text
Text2Media/
├── app.py
├── main.py
├── src/
│   ├── config.py
│   ├── text_utils.py
│   ├── tts.py
│   ├── subtitle.py
│   ├── media.py
│   └── pipeline.py
├── examples/
├── assets/backgrounds/
├── output/
├── tests/
├── .env.example
├── requirements.txt
└── install.sh
```

## Troubleshooting
**FFmpeg not found**
```bash
brew install ffmpeg
ffmpeg -version
```

**Edge-TTS network error**
- Check the internet connection.
- Try again later or switch to Alibaba TTS.
- Confirm the selected voice exists in the current Edge-TTS voice list.

**Alibaba 401 / unauthorized**
- Confirm the API key is correct and belongs to the selected region.
- Confirm the key has access to the selected TTS model.
- Do not paste the key into GitHub issues or chat.

**Alibaba 400 / invalid voice or model**
- Check the model and voice available in your Model Studio console.
- Update `DASHSCOPE_MODEL` and `DASHSCOPE_VOICE` in `.env`.

**Video has no subtitles / Chinese text appears as boxes**
- Install a Chinese font such as Noto Sans CJK.
- On macOS, set `TEXT2MEDIA_FONT` to a font file path if needed.
- Example: `/System/Library/Fonts/PingFang.ttc`

## License
MIT. Third-party services and dependencies retain their own terms.
