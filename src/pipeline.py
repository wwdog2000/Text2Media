from pathlib import Path
import tempfile

from .text_utils import split_sentences
from .tts import synthesize
from .media import require_ffmpeg, audio_duration, combine_audio, make_video
from .subtitle import write_srt


def create_project(
    text: str,
    provider: str = "edge",
    language: str = "zh",
    output_base: str = "output/text2media",
    voice: str = "",
    rate: str = "+0%",
    make_video_file: bool = False,
    background: str = "",
    width: int = 1080,
    height: int = 1920,
    subtitle_font_size: int = 14,
    subtitle_max_chars: int = 18,
    subtitle_position: str = "bottom",
    subtitle_outline: bool = True,
    background_mode: str = "solid",
    background_image: str = "",
    background_video: str = "",
    wave_style: str = "wave",
    vinyl_speed: str = "normal",
    background_color: str = "#202020",
    image_fit: str = "cover",
    video_fit: str = "cover",
    vinyl_size: int = 68,
    vinyl_x: int = 50,
    vinyl_y: int = 50,
    wave_color: str = "#35D6C5",
    wave_height: int = 100,
    background_music: str = "",
    music_enabled: bool = False,
    music_volume: float = 0.15,
    music_loop: bool = True,
    music_fade_in: float = 1.5,
    music_fade_out: float = 2.0,
):
    require_ffmpeg()
    base = Path(output_base).expanduser()
    base.parent.mkdir(parents=True, exist_ok=True)
    audio_path = base.with_suffix(".mp3")
    srt_path = base.with_suffix(".srt")
    video_path = base.with_suffix(".mp4")

    sentences = split_sentences(text)
    if not sentences:
        raise ValueError("No valid text to synthesize.")

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
        write_srt(subtitle_items, srt_path, max_chars=subtitle_max_chars)

    result = {"audio": str(audio_path), "subtitle": str(srt_path)}
    if make_video_file:
        make_video(
            audio=audio_path,
            subtitle=srt_path,
            output=video_path,
            background=background,
            width=width,
            height=height,
            color=background_color,
            font_size=subtitle_font_size,
            position=subtitle_position,
            outline=subtitle_outline,
            background_mode=background_mode,
            background_image=background_image,
            background_video=background_video,
            wave_style=wave_style,
            vinyl_speed=vinyl_speed,
            image_fit=image_fit,
            video_fit=video_fit,
            vinyl_size=vinyl_size,
            vinyl_x=vinyl_x,
            vinyl_y=vinyl_y,
            wave_color=wave_color,
            wave_height=wave_height,
            background_music=background_music,
            music_enabled=music_enabled,
            music_volume=music_volume,
            music_loop=music_loop,
            music_fade_in=music_fade_in,
            music_fade_out=music_fade_out,
        )
        result["video"] = str(video_path)
    return result
