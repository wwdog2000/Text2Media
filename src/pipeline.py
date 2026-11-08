from pathlib import Path
import shutil
import tempfile

from .text_utils import split_sentences
from .tts import synthesize
from .media import require_ffmpeg, audio_duration, combine_audio, make_video
from .subtitle import write_srt

def create_project(text: str, provider: str = "edge", language: str = "zh",
                   output_base: str = "output/text2media", voice: str = "",
                   rate: str = "+0%", make_video_file: bool = False,
                   background: str = "", width: int = 1080, height: int = 1920):
    require_ffmpeg()
    base = Path(output_base).expanduser()
    base.parent.mkdir(parents=True, exist_ok=True)
    audio_path = base.with_suffix(".mp3")
    srt_path = base.with_suffix(".srt")
    video_path = base.with_suffix(".mp4")

    sentences = split_sentences(text)
    subtitle_items = []
    clips = []
    current_time = 0.0

    with tempfile.TemporaryDirectory(prefix="text2media_") as temp_dir:
        temp = Path(temp_dir)
        for index, sentence in enumerate(sentences, 1):
            clip = temp / f"clip_{index:04d}.mp3"
            synthesize(sentence, clip, provider, language, voice, rate)
            duration = audio_duration(clip)
            if duration <= 0:
                raise RuntimeError(f"Generated audio clip {index} has zero duration.")
            subtitle_items.append({
                "start": current_time,
                "end": current_time + duration,
                "text": sentence,
            })
            current_time += duration
            clips.append(clip)

        combine_audio(clips, audio_path)
        write_srt(subtitle_items, srt_path)

    result = {"audio": str(audio_path), "subtitle": str(srt_path)}
    if make_video_file:
        make_video(audio_path, srt_path, video_path, background, width, height)
        result["video"] = str(video_path)
    return result
