import gradio as gr
from src.pipeline import create_project


CSS = """
.gradio-container { max-width: 1180px !important; margin: 0 auto !important; }
#main-title { text-align: center; padding: 24px 0 8px; }
#main-title h1 { font-size: 34px; font-weight: 700; letter-spacing: -0.8px; }
#main-title p { color: var(--body-text-color-subdued); font-size: 14px; }
.generate-btn { min-height: 48px !important; font-size: 16px !important; font-weight: 650 !important; }
footer { display: none !important; }
"""


def generate(
    text, provider, language, voice, rate, mode,
    background_mode, background_image, background_video,
    wave_style, vinyl_speed, background_color, image_fit, video_fit,
    vinyl_size, vinyl_x, vinyl_y, wave_color, wave_height,
    music_enabled, background_music, music_volume, music_loop,
    music_fade_in, music_fade_out,
    width, height, subtitle_font_size, subtitle_max_chars,
    subtitle_position, subtitle_outline,
):
    if not text or not text.strip():
        raise gr.Error("请输入需要转换的文字 / Please enter some text.")

    if mode == "Audio + video":
        if background_mode == "image" and not background_image:
            raise gr.Error("请上传背景图片 / Please upload a background image.")
        if background_mode == "video" and not background_video:
            raise gr.Error("请上传背景视频 / Please upload a background video.")
        if music_enabled and not background_music:
            raise gr.Error("请上传背景音乐 / Please upload background music.")
    elif music_enabled:
        raise gr.Error("背景音乐仅用于视频输出 / Background music is available for video output only.")

    try:
        result = create_project(
            text=text,
            provider=provider,
            language=language,
            output_base="output/web-created",
            voice=(voice or "").strip(),
            rate=rate,
            make_video_file=(mode == "Audio + video"),
            width=int(width),
            height=int(height),
            subtitle_font_size=int(subtitle_font_size),
            subtitle_max_chars=int(subtitle_max_chars),
            subtitle_position=subtitle_position,
            subtitle_outline=subtitle_outline,
            background_mode=background_mode,
            background_image=background_image or "",
            background_video=background_video or "",
            wave_style=wave_style,
            vinyl_speed=vinyl_speed,
            background_color=background_color,
            image_fit=image_fit,
            video_fit=video_fit,
            vinyl_size=int(vinyl_size),
            vinyl_x=int(vinyl_x),
            vinyl_y=int(vinyl_y),
            wave_color=wave_color,
            wave_height=int(wave_height),
            background_music=background_music or "",
            music_enabled=music_enabled,
            music_volume=float(music_volume),
            music_loop=music_loop,
            music_fade_in=float(music_fade_in),
            music_fade_out=float(music_fade_out),
        )
    except Exception as exc:
        raise gr.Error(str(exc)) from exc

    return (
        result.get("audio"),
        result.get("subtitle"),
        result.get("video"),
        "\n".join(f"{key}: {value}" for key, value in result.items()),
    )


with gr.Blocks(
    title="Text2Media | AI Media Studio",
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate", neutral_hue="slate"),
    css=CSS,
) as demo:
    gr.Markdown(
        """
        <div id="main-title">
            <h1>Text2Media</h1>
            <p>AI Media Studio · 文字转语音 · 自动字幕 · 视频生成</p>
            <p>Turn Text into Audio and Video with AI</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=7):
            gr.Markdown("### 01 · 文本内容 / Text Input")
            text = gr.Textbox(
                label="输入文字 / Enter Your Text",
                placeholder="在这里粘贴需要转换的文字……\nPaste your script here...",
                lines=9,
                max_lines=20,
            )
            gr.Markdown("### 02 · 语音设置 / Voice Settings")
            with gr.Row():
                provider = gr.Dropdown(
                    choices=[("Edge TTS（免费）/ Edge TTS (Free)", "edge"),
                             ("阿里云百炼 / Alibaba Cloud Bailian", "aliyun")],
                    value="edge", label="语音服务 / TTS Provider",
                )
                language = gr.Dropdown(
                    choices=[("中文 / Chinese", "zh"), ("英文 / English", "en")],
                    value="zh", label="语言 / Language",
                )
            with gr.Row():
                voice = gr.Textbox(
                    label="音色 / Voice",
                    placeholder="留空使用默认音色 / Leave blank for default",
                )
                rate = gr.Textbox(
                    label="语速 / Speech Rate", value="+0%",
                    placeholder="例如：+10% / -10%",
                )
            mode = gr.Radio(
                choices=[("仅生成音频 / Audio Only", "Audio only"),
                         ("生成音频和视频 / Audio + Video", "Audio + video")],
                value="Audio + video", label="输出类型 / Output Type",
            )

        with gr.Column(scale=5):
            gr.Markdown("### 03 · 视频背景 / Video Background")
            background_mode = gr.Radio(
                choices=[
                    ("纯色背景 / Solid Color", "solid"),
                    ("黑胶唱片 / Vinyl Record", "vinyl"),
                    ("动态音波 / Audio Visualizer", "wave"),
                    ("本地图片 / Local Image", "image"),
                    ("本地视频 / Local Video", "video"),
                ],
                value="vinyl", label="背景类型 / Background Type",
            )
            background_color = gr.ColorPicker(
                label="背景颜色 / Background Color", value="#202020"
            )
            background_image = gr.File(
                label="上传背景图片 / Upload Image", file_types=["image"], type="filepath"
            )
            image_fit = gr.Radio(
                choices=[("铺满裁切 / Cover", "cover"), ("完整显示 / Contain", "contain")],
                value="cover", label="图片适配 / Image Fit",
            )
            background_video = gr.File(
                label="上传背景视频 / Upload Video", file_types=["video"], type="filepath"
            )
            video_fit = gr.Radio(
                choices=[("铺满裁切 / Cover", "cover"), ("完整显示 / Contain", "contain")],
                value="cover", label="视频适配 / Video Fit",
            )
            gr.Markdown("#### 音波设置 / Audio Visualizer")
            wave_style = gr.Radio(
                choices=[("横向波形 / Waveform", "wave"), ("动态频谱 / Spectrum", "spectrum")],
                value="wave", label="音波样式 / Wave Style",
            )
            wave_color = gr.ColorPicker(
                label="Waveform 颜色 / Waveform Color", value="#35D6C5"
            )
            wave_height = gr.Slider(
                minimum=50, maximum=100, value=100, step=5,
                label="音波显示高度 / Visualizer Height (%)",
            )
            gr.Markdown("#### 黑胶设置 / Vinyl Settings")
            vinyl_speed = gr.Dropdown(
                choices=[("慢速 / Slow", "slow"), ("标准 / Normal", "normal"), ("快速 / Fast", "fast")],
                value="normal", label="旋转速度 / Rotation Speed",
            )
            vinyl_size = gr.Slider(
                minimum=40, maximum=90, value=68, step=1,
                label="唱片尺寸 / Record Size (%)",
            )
            with gr.Row():
                vinyl_x = gr.Slider(minimum=0, maximum=100, value=50, step=1,
                                    label="水平位置 / Horizontal Position (%)")
                vinyl_y = gr.Slider(minimum=0, maximum=100, value=50, step=1,
                                    label="垂直位置 / Vertical Position (%)")

    with gr.Accordion("04 · 背景音乐 / Background Music", open=True):
        gr.Markdown(
            "背景音乐只混入最终 MP4；独立 MP3 始终保留纯旁白。\n"
            "Music is mixed into the final MP4 only. The separate MP3 remains narration-only."
        )
        music_enabled = gr.Checkbox(value=False, label="启用背景音乐 / Enable Background Music")
        background_music = gr.File(
            label="上传音乐文件 / Upload Music (MP3, WAV, M4A)",
            file_types=["audio"], type="filepath",
        )
        with gr.Row():
            music_volume = gr.Slider(
                minimum=0, maximum=0.5, value=0.15, step=0.01,
                label="音乐音量 / Music Volume (default 15%)",
            )
            music_loop = gr.Checkbox(value=True, label="循环播放 / Loop Music")
        with gr.Row():
            music_fade_in = gr.Slider(
                minimum=0, maximum=5, value=1.5, step=0.5,
                label="淡入时间 / Fade In (seconds)",
            )
            music_fade_out = gr.Slider(
                minimum=0, maximum=5, value=2, step=0.5,
                label="淡出时间 / Fade Out (seconds)",
            )

    with gr.Accordion("05 · 视频参数 / Video Settings", open=False):
        with gr.Row():
            width = gr.Number(label="视频宽度 / Width", value=720, precision=0)
            height = gr.Number(label="视频高度 / Height", value=1080, precision=0)

    with gr.Accordion("06 · 字幕设置 / Subtitle Settings", open=True):
        with gr.Row():
            subtitle_font_size = gr.Slider(
                minimum=10, maximum=36, value=14, step=1,
                label="字幕字号 / Font Size",
            )
            subtitle_max_chars = gr.Slider(
                minimum=8, maximum=30, value=18, step=1,
                label="每行最大字数 / Max Characters per Line",
            )
        with gr.Row():
            subtitle_position = gr.Radio(
                choices=[("底部 / Bottom", "bottom"), ("居中 / Center", "center"), ("顶部 / Top", "top")],
                value="bottom", label="字幕位置 / Subtitle Position",
            )
            subtitle_outline = gr.Checkbox(value=True, label="字幕描边 / Subtitle Outline")

    gr.Markdown("---")
    run = gr.Button("生成项目 / Generate Project", variant="primary", elem_classes=["generate-btn"])
    gr.Markdown("### 07 · 生成结果 / Generated Results")
    with gr.Row():
        with gr.Column():
            audio_out = gr.Audio(label="生成音频 / Generated Audio")
            subtitle_out = gr.File(label="字幕文件 / Subtitle File")
        with gr.Column():
            video_out = gr.Video(label="生成视频 / Generated Video")
    files_out = gr.Textbox(label="项目文件信息 / Project Information", lines=5, interactive=False)

    run.click(
        fn=generate,
        inputs=[
            text, provider, language, voice, rate, mode,
            background_mode, background_image, background_video,
            wave_style, vinyl_speed, background_color, image_fit, video_fit,
            vinyl_size, vinyl_x, vinyl_y, wave_color, wave_height,
            music_enabled, background_music, music_volume, music_loop,
            music_fade_in, music_fade_out,
            width, height, subtitle_font_size, subtitle_max_chars,
            subtitle_position, subtitle_outline,
        ],
        outputs=[audio_out, subtitle_out, video_out, files_out],
    )

    gr.Markdown(
        """<div style="text-align:center; padding:20px; color:var(--body-text-color-subdued);">
        Text2Media · AI Media Studio · v1.1.0</div>"""
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
