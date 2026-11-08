
from pathlib import Path
import textwrap


def format_srt_time(seconds: float) -> str:
    milliseconds = max(0, int(round(seconds * 1000)))

    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def wrap_subtitle_text(
    text: str,
    max_chars: int = 18,
) -> str:
    if max_chars < 1:
        raise ValueError("max_chars must be greater than zero.")

    result = []

    for paragraph in text.splitlines():
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        wrapped = textwrap.wrap(
            paragraph,
            width=max_chars,
            break_long_words=True,
            break_on_hyphens=False,
        )

        result.extend(wrapped or [paragraph])

    return "\n".join(result)


def write_srt(
    items: list[dict],
    output: Path,
    max_chars: int = 18,
):
    lines = []

    for index, item in enumerate(items, 1):
        subtitle_text = wrap_subtitle_text(
            item["text"],
            max_chars=max_chars,
        )

        lines.extend([
            str(index),
            (
                f"{format_srt_time(item['start'])} --> "
                f"{format_srt_time(item['end'])}"
            ),
            subtitle_text,
            "",
        ])

    output.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output
