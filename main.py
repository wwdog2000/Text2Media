import argparse
from pathlib import Path
from src.pipeline import create_project

def main():
    parser = argparse.ArgumentParser(description="Text2Media: text to speech and captioned video")
    sub = parser.add_subparsers(dest="command", required=True)

    for command in ("audio", "video"):
        p = sub.add_parser(command)
        source = p.add_mutually_exclusive_group(required=True)
        source.add_argument("--text", help="Text to synthesize")
        source.add_argument("--text-file", help="UTF-8 text file")
        p.add_argument("--provider", choices=["edge", "aliyun"], default="edge")
        p.add_argument("--language", choices=["zh", "en"], default="zh")
        p.add_argument("--voice", default="")
        p.add_argument("--rate", default="+0%")
        p.add_argument("--output", default="output/text2media")
        p.add_argument("--background", default="")
        p.add_argument("--width", type=int, default=1080)
        p.add_argument("--height", type=int, default=1920)

    args = parser.parse_args()
    text = args.text if args.text is not None else Path(args.text_file).read_text(encoding="utf-8")
    result = create_project(
        text=text, provider=args.provider, language=args.language,
        output_base=args.output, voice=args.voice, rate=args.rate,
        make_video_file=args.command == "video",
        background=args.background, width=args.width, height=args.height,
    )
    print("\n[OK] Files generated:")
    for key, value in result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
