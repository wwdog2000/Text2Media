import re

def split_sentences(text: str, max_chars: int = 450) -> list[str]:
    """Split text into readable sentence chunks, keeping provider limits in mind."""
    text = re.sub(r"\r\n?", "\n", text).strip()
    if not text:
        raise ValueError("Text is empty.")

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    output = []
    for paragraph in paragraphs:
        parts = re.split(r"(?<=[。！？.!?；;])\s*", paragraph)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            while len(part) > max_chars:
                cut = part.rfind("，", 0, max_chars)
                if cut < max_chars // 2:
                    cut = part.rfind(" ", 0, max_chars)
                if cut < max_chars // 2:
                    cut = max_chars
                output.append(part[:cut].strip())
                part = part[cut:].strip()
            if part:
                output.append(part)
    return output
