import subprocess
from pathlib import Path
from pydub import AudioSegment
from .config import FONT_PATH

def require_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError("FFmpeg was not found. Install it with: brew install ffmpeg")

def audio_duration(path: Path) -> float:
    audio = AudioSegment.from_file(path)
    return len(audio) / 1000.0

def combine_audio(clips: list[Path], output: Path):
    combined = AudioSegment.empty()
    for clip in clips:
        combined += AudioSegment.from_file(clip)
    combined.export(output, format=output.suffix.lstrip(".") or "mp3")
    return output

def make_video(audio: Path, subtitle: Path, output: Path, background: str = "",
               width: int = 1080, height: int = 1920, color: str = "0x202020"):
    require_ffmpeg()
    subtitle_path = subtitle.resolve().as_posix().replace(":", r"\:").replace("'", r"\'")
    style = "FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=100"
    if FONT_PATH:
        font_dir = Path(FONT_PATH).expanduser().resolve().parent
        style += ",FontName=PingFang SC"
        force_style = style
        vf = f"subtitles='{subtitle_path}':fontsdir='{font_dir.as_posix()}':force_style='{force_style}'"
    else:
        vf = f"subtitles='{subtitle_path}':force_style='{style}'"

    if background:
        input_args = ["-loop", "1", "-i", str(Path(background).resolve()), "-i", str(audio)]
        video_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},{vf}"
        )
        cmd = ["ffmpeg", "-y", *input_args, "-vf", video_filter,
               "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
               "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
               "-pix_fmt", "yuv420p", "-shortest", str(output)]
    else:
        cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i",
               f"color=c={color}:s={width}x{height}:r=25", "-i", str(audio),
               "-vf", vf, "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
               "-pix_fmt", "yuv420p", "-shortest", str(output)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("FFmpeg video rendering failed:\n" + result.stderr[-2500:])
    return output
