from pathlib import Path

def format_srt_time(seconds: float) -> str:
    milliseconds = max(0, int(round(seconds * 1000)))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def write_srt(items: list[dict], output: Path):
    lines = []
    for index, item in enumerate(items, 1):
        lines.extend([
            str(index),
            f"{format_srt_time(item['start'])} --> {format_srt_time(item['end'])}",
            item["text"],
            "",
        ])
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
