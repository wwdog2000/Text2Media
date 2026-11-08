from pathlib import Path
import gradio as gr
from src.pipeline import create_project

def generate(text, provider, language, voice, rate, mode, background, width, height):
    if not text or not text.strip():
        raise gr.Error("Please enter some text first.")
    try:
        result = create_project(
            text=text, provider=provider, language=language,
            output_base="output/web-created",
            voice=voice.strip(), rate=rate,
            make_video_file=(mode == "Audio + video"),
            background=background.strip(),
            width=int(width), height=int(height),
        )
    except Exception as exc:
        raise gr.Error(str(exc))
    audio = result.get("audio")
    subtitle = result.get("subtitle")
    video = result.get("video")
    return audio, subtitle, video, "\n".join(f"{k}: {v}" for k, v in result.items())

with gr.Blocks(title="Text2Media") as demo:
    gr.Markdown("# Text2Media\n### Turn text into speech, subtitles, and captioned videos")
    text = gr.Textbox(label="Text", lines=10, placeholder="Paste Chinese or English text here...")
    with gr.Row():
        provider = gr.Dropdown(["edge", "aliyun"], value="edge", label="TTS provider")
        language = gr.Dropdown(["zh", "en"], value="zh", label="Language")
        mode = gr.Dropdown(["Audio only", "Audio + video"], value="Audio + video", label="Output")
    with gr.Row():
        voice = gr.Textbox(label="Voice (optional)", placeholder="Leave blank for default")
        rate = gr.Textbox(label="Edge rate", value="+0%", placeholder="+0%")
    background = gr.Textbox(label="Background image path (optional)", placeholder="Leave blank for a solid background")
    with gr.Row():
        width = gr.Number(value=1080, label="Video width", precision=0)
        height = gr.Number(value=1920, label="Video height", precision=0)
    run = gr.Button("Generate", variant="primary")
    audio_out = gr.Audio(label="Generated audio", type="filepath")
    subtitle_out = gr.File(label="SRT subtitles")
    video_out = gr.Video(label="Generated video")
    files_out = gr.Textbox(label="Output files", lines=3)
    run.click(
        generate,
        inputs=[text, provider, language, voice, rate, mode, background, width, height],
        outputs=[audio_out, subtitle_out, video_out, files_out],
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
