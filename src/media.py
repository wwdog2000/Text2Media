import subprocess
import tempfile
from pathlib import Path

from pydub import AudioSegment
from .config import FONT_PATH


def require_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError(
            "FFmpeg was not found. Install it with: brew install ffmpeg"
        )


def audio_duration(path: Path) -> float:
    audio = AudioSegment.from_file(path)
    return len(audio) / 1000.0


def combine_audio(clips: list[Path], output: Path):
    combined = AudioSegment.empty()
    for clip in clips:
        combined += AudioSegment.from_file(clip)

    output.parent.mkdir(parents=True, exist_ok=True)
    combined.export(output, format=output.suffix.lstrip(".") or "mp3")
    return output


def _ffmpeg_color(value: str) -> str:
    """Convert UI hex colors (#RRGGBB) to FFmpeg's 0xRRGGBB form."""
    value = str(value or "#202020").strip()
    if value.startswith("#") and len(value) == 7:
        return "0x" + value[1:]
    if value.startswith("0x") and len(value) == 8:
        return value
    raise ValueError("Color must be a hex color such as #202020.")


def _make_vinyl_image(output: Path, size: int = 800):
    """Generate a transparent vinyl record PNG with visible rotation markers."""
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required for vinyl backgrounds. Run: pip install Pillow"
        ) from exc

    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    center = size // 2
    outer = int(size * 0.48)
    draw.ellipse(
        (center - outer, center - outer, center + outer, center + outer),
        fill=(15, 15, 18, 255), outline=(85, 85, 90, 255), width=5,
    )
    for radius in range(int(size * 0.18), int(size * 0.45), 9):
        draw.ellipse(
            (center - radius, center - radius, center + radius, center + radius),
            outline=(65, 65, 72, 255), width=2,
        )

    label_radius = int(size * 0.16)
    draw.ellipse(
        (center - label_radius, center - label_radius,
         center + label_radius, center + label_radius),
        fill=(155, 45, 45, 255), outline=(230, 185, 135, 255), width=5,
    )
    draw.line(
        (center, center - label_radius + 18, center, center - 35),
        fill=(255, 225, 170, 255), width=12,
    )
    marker_radius = int(size * 0.025)
    marker_x = center + int(label_radius * 0.65)
    marker_y = center - int(label_radius * 0.45)
    draw.ellipse(
        (marker_x - marker_radius, marker_y - marker_radius,
         marker_x + marker_radius, marker_y + marker_radius),
        fill=(255, 235, 190, 255),
    )
    hole_radius = int(size * 0.018)
    draw.ellipse(
        (center - hole_radius, center - hole_radius,
         center + hole_radius, center + hole_radius),
        fill=(5, 5, 5, 255),
    )
    image.save(output, "PNG")


def _subtitle_filter(
    subtitle: Path, font_size: int, position: str, outline: bool,
    width: int, height: int,
) -> str:
    subtitle_path = (
        subtitle.resolve().as_posix()
        .replace("\\", r"\\").replace(":", r"\:").replace("'", r"\'")
    )
    scale = width / 720
    actual_font_size = max(1, round(font_size * scale))
    margin_lr = round(50 * scale)
    margin_v = round(55 * height / 1080)
    outline_size = max(1, round(1.5 * scale)) if outline else 0
    alignment = {"bottom": 2, "center": 5, "top": 8}[position]
    style = (
        "FontName=PingFang SC,"
        f"FontSize={actual_font_size},"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,"
        f"Outline={outline_size},Shadow=1,Alignment={alignment},"
        f"MarginL={margin_lr},MarginR={margin_lr},MarginV={margin_v},WrapStyle=0"
    )
    if FONT_PATH:
        font_dir = Path(FONT_PATH).expanduser().resolve().parent.as_posix()
        return f"subtitles='{subtitle_path}':fontsdir='{font_dir}':force_style='{style}'"
    return f"subtitles='{subtitle_path}':force_style='{style}'"


def _fit_filter(width: int, height: int, fit_mode: str) -> str:
    if fit_mode == "cover":
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height}"
        )
    if fit_mode == "contain":
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black"
        )
    raise ValueError("Fit mode must be 'cover' or 'contain'.")


def _mix_background_music(
    video_path: Path,
    music_path: str,
    duration: float,
    volume: float,
    loop: bool,
    fade_in: float,
    fade_out: float,
):
    """Mix music into the MP4 only; the separate narration MP3 is untouched."""
    music = Path(music_path).expanduser().resolve()
    if not music.is_file():
        raise ValueError("Please upload a valid background music file.")
    if not 0 <= float(volume) <= 0.5:
        raise ValueError("Background music volume must be between 0 and 0.5.")
    if not 0 <= float(fade_in) <= 10 or not 0 <= float(fade_out) <= 10:
        raise ValueError("Music fade durations must be between 0 and 10 seconds.")

    temp_output = video_path.with_name(video_path.stem + ".music-mix" + video_path.suffix)
    if temp_output.exists():
        temp_output.unlink()

    music_input = []
    if loop:
        music_input = ["-stream_loop", "-1"]

    filters = [f"volume={float(volume):.4f}"]
    if fade_in > 0:
        filters.append(f"afade=t=in:st=0:d={float(fade_in):.3f}")
    if fade_out > 0:
        music_end = duration if loop else min(duration, audio_duration(music))
        effective_fade = min(float(fade_out), music_end)
        fade_start = max(0.0, music_end - effective_fade)
        filters.append(f"afade=t=out:st={fade_start:.3f}:d={effective_fade:.3f}")
    music_filter = ",".join(filters)
    filter_complex = (
        f"[1:a:0]{music_filter}[music];"
        "[0:a:0][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path), *music_input, "-i", str(music),
        "-filter_complex", filter_complex,
        "-map", "0:v:0", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", str(temp_output),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if temp_output.exists():
            temp_output.unlink()
        raise RuntimeError("Background music mixing failed:\n" + result.stderr[-3000:])
    temp_output.replace(video_path)


def make_video(
    audio: Path,
    subtitle: Path,
    output: Path,
    background: str = "",
    width: int = 1080,
    height: int = 1920,
    color: str = "#202020",
    font_size: int = 14,
    position: str = "bottom",
    outline: bool = True,
    background_mode: str = "solid",
    background_image: str = "",
    background_video: str = "",
    wave_style: str = "wave",
    vinyl_speed: str = "normal",
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
    audio = Path(audio).expanduser().resolve()
    subtitle = Path(subtitle).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    if position not in ("top", "center", "bottom"):
        raise ValueError("Invalid subtitle position.")
    if not 1 <= int(font_size) <= 100:
        raise ValueError("Invalid subtitle font size.")
    width, height = int(width), int(height)
    if width <= 0 or height <= 0:
        raise ValueError("Video width and height must be positive.")
    if background and background_mode == "solid":
        background_mode, background_image = "image", background
    if background_mode not in ("solid", "vinyl", "wave", "image", "video"):
        raise ValueError("Invalid background mode.")
    if wave_style not in ("wave", "spectrum"):
        raise ValueError("Invalid waveform style.")
    if vinyl_speed not in ("slow", "normal", "fast"):
        raise ValueError("Invalid vinyl rotation speed.")
    if not 40 <= int(vinyl_size) <= 90:
        raise ValueError("Vinyl size must be between 40 and 90 percent.")
    if not 0 <= int(vinyl_x) <= 100 or not 0 <= int(vinyl_y) <= 100:
        raise ValueError("Vinyl position values must be between 0 and 100.")
    if not 50 <= int(wave_height) <= 100:
        raise ValueError("Wave height must be between 50 and 100 percent.")
    if music_enabled:
        if not background_music or not Path(background_music).expanduser().is_file():
            raise ValueError("Please upload a valid background music file.")
        if not 0 <= float(music_volume) <= 0.5:
            raise ValueError("Background music volume must be between 0 and 0.5.")
        if not 0 <= float(music_fade_in) <= 10 or not 0 <= float(music_fade_out) <= 10:
            raise ValueError("Music fade durations must be between 0 and 10 seconds.")

    bg_color = _ffmpeg_color(color)
    visual_color = _ffmpeg_color(wave_color)
    subtitle_filter = _subtitle_filter(subtitle, int(font_size), position, outline, width, height)
    duration = max(0.1, audio_duration(audio))

    common_output_args = [
        "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "23", "-threads", "2", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest", str(output),
    ]

    if background_mode == "solid":
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"color=c={bg_color}:s={width}x{height}:r=25:d={duration}",
            "-i", str(audio), "-vf", subtitle_filter, "-map", "0:v:0",
            *common_output_args,
        ]

    elif background_mode in ("image", "video"):
        source = background_image if background_mode == "image" else background_video
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            label = "image" if background_mode == "image" else "video"
            raise ValueError(f"Please upload a valid background {label}.")
        fit = image_fit if background_mode == "image" else video_fit
        fit_chain = _fit_filter(width, height, fit)
        if background_mode == "image":
            input_args = ["-loop", "1", "-i", str(source_path)]
        else:
            input_args = ["-stream_loop", "-1", "-i", str(source_path)]
        cmd = [
            "ffmpeg", "-y", *input_args, "-i", str(audio),
            "-vf", f"{fit_chain},{subtitle_filter}", "-map", "0:v:0",
            *common_output_args,
        ]

    elif background_mode == "wave":
        visual_height = max(100, round(height * int(wave_height) / 100))
        if wave_style == "wave":
            visualizer = (
                f"showwaves=s={width}x{visual_height}:mode=line:rate=25:"
                f"colors={visual_color}"
            )
        else:
            visualizer = (
                f"showspectrum=s={width}x{visual_height}:mode=combined:"
                "color=intensity:scale=log:slide=scroll:fps=25"
            )
        filter_complex = (
            f"[0:a]{visualizer},"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color={bg_color},"
            f"{subtitle_filter}[v]"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(audio), "-filter_complex", filter_complex,
            "-map", "[v]", "-map", "0:a:0", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "23", "-threads", "2",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            "-shortest", str(output),
        ]

    else:  # vinyl
        speed_seconds = {"slow": 12, "normal": 6, "fast": 3}[vinyl_speed]
        with tempfile.TemporaryDirectory(prefix="text2media_vinyl_") as temp_dir:
            vinyl_path = Path(temp_dir) / "vinyl.png"
            _make_vinyl_image(vinyl_path)
            record_size = max(160, int(min(width, height) * int(vinyl_size) / 100))
            x_expr = f"(W-w)*{int(vinyl_x)}/100"
            y_expr = f"(H-h)*{int(vinyl_y)}/100"
            filter_complex = (
                "[1:v]fps=25,"
                f"scale={record_size}:{record_size},format=rgba,"
                f"rotate=2*PI*t/{speed_seconds}:c=none:ow=rotw(iw):oh=roth(ih):bilinear=1[record];"
                f"[0:v][record]overlay={x_expr}:{y_expr}:shortest=1,"
                f"{subtitle_filter}[v]"
            )
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i",
                f"color=c={bg_color}:s={width}x{height}:r=25:d={duration}",
                "-loop", "1", "-i", str(vinyl_path), "-i", str(audio),
                "-filter_complex", filter_complex, "-map", "[v]", "-map", "2:a:0",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-threads", "2", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-shortest", str(output),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError("FFmpeg video rendering failed:\n" + result.stderr[-3000:])

    if background_mode != "vinyl":
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("FFmpeg video rendering failed:\n" + result.stderr[-3000:])

    if music_enabled:
        if not background_music:
            raise ValueError("Please upload a background music file or turn music off.")
        _mix_background_music(
            output, background_music, duration, music_volume, music_loop,
            music_fade_in, music_fade_out,
        )
    return output
