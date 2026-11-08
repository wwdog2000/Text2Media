# Text2Media

**Turn Text into Speech, Subtitles, and Captioned Videos with AI.**

**Text2Media** 是一个面向普通用户的本地优先文字转音视频工具。它可以将文字转换成语音，自动生成 SRT 字幕，并制作带字幕的视频。

项目支持 Edge-TTS 和阿里云百炼 TTS，提供命令行（CLI）和 Gradio 网页界面。

[中文说明](#中文说明) | [English Documentation](#english-documentation)

---

# 中文说明

## 1. 项目介绍

Text2Media 是一个简单易用的 AI 文字转音视频工具。

输入文字后，可以自动完成：

- 文字转语音
- 自动生成 SRT 字幕
- 生成 MP3 音频
- 制作带字幕的 MP4 视频
- 添加图片、视频、纯色、动态音波或黑胶唱片背景
- 为最终视频添加背景音乐

支持中文和英文，适合短视频制作、旁白配音、知识分享、故事视频及自媒体内容创作。

## 2. 功能特点

### 语音生成

- 支持 Edge-TTS（免费在线语音服务，无需 API Key）
- 支持阿里云百炼 TTS
- 支持中文和英文
- 支持音色及语速设置

### 自动字幕

- 自动生成 SRT 字幕文件
- 根据实际生成的语音片段计算字幕时间
- 支持调整每行最大字符数
- 支持调整字幕字号
- 支持字幕顶部、居中和底部位置
- 支持字幕描边

注意：字幕时间根据句子级语音片段计算，并非逐字或逐词强制对齐。

### 五种视频背景

| 背景模式 | 功能 |
|---|---|
| Solid | 纯色背景，可选择颜色 |
| Vinyl | 黑胶唱片背景，可调整尺寸、位置和旋转速度 |
| Wave | 动态音波背景 |
| Image | 使用本地图片作为背景 |
| Video | 使用本地视频作为动态背景 |

其他背景设置：

- 图片适配：Cover / Contain
- 视频适配：Cover / Contain
- 音波样式：Waveform / Spectrum
- 音波颜色及显示高度
- 黑胶唱片尺寸、位置及旋转速度

### 背景音乐

支持在最终 MP4 视频中添加背景音乐：

- 上传本地背景音乐
- 开启或关闭背景音乐
- 调节背景音乐音量
- 设置音乐循环
- 设置淡入和淡出时间

**重要：背景音乐只混入最终 MP4 视频，单独生成的 MP3 文件始终保留纯旁白。**

关闭背景音乐时，视频仍按原有方式生成。

### 输出文件

| 文件 | 说明 |
|---|---|
| MP3 | 生成的旁白音频 |
| SRT | 自动生成的字幕文件 |
| MP4 | 带字幕和背景的视频 |

## 3. 系统要求

- macOS、Windows 或 Linux
- Python 3.10+
- FFmpeg
- 网络连接（使用在线 TTS 服务时）

## 4. 安装

### macOS

首先安装 FFmpeg：

```bash
brew install ffmpeg
```

克隆项目：

```bash
git clone https://github.com/wwdog2000/Text2Media.git
cd Text2Media
```

运行安装脚本：

```bash
bash install.sh
```

安装脚本会创建 Python 虚拟环境并安装项目依赖。

### 启动网页界面

```bash
source .venv/bin/activate
python app.py
```

打开浏览器：

```text
http://127.0.0.1:7860
```

## 5. 网页界面使用方法

### 第一步：输入文字

在文本输入框中粘贴需要转换的文章、旁白或脚本。

### 第二步：选择语音服务

选择：

- Edge-TTS
- Alibaba Cloud Bailian

设置语言、音色和语速。

### 第三步：选择输出类型

可以选择：

- Audio Only：仅生成音频
- Audio + Video：生成音频和视频

### 第四步：选择视频背景

支持五种背景：

- 纯色背景
- 黑胶唱片
- 动态音波
- 本地图片
- 本地视频

根据所选背景调整对应参数。

使用图片或视频背景时，需要上传相应素材。

### 第五步：设置字幕

可以调整：

- 字幕字号
- 每行最大字符数
- 字幕位置
- 字幕描边

### 第六步：添加背景音乐

如果需要背景音乐：

1. 开启背景音乐功能。
2. 上传本地音乐文件。
3. 设置音乐音量。
4. 根据需要设置循环、淡入和淡出。

### 第七步：生成项目

点击 Generate Project。

生成完成后，可以在网页界面查看和下载音频、字幕及视频文件。

## 6. CLI 命令行使用

激活虚拟环境：

```bash
source .venv/bin/activate
```

生成音频和字幕：

```bash
python main.py audio --text-file examples/example.txt --provider edge --language zh --output output/demo
```

生成带图片背景的视频：

```bash
python main.py video --text-file examples/example.txt --provider edge --language zh \
  --background assets/backgrounds/sample.png --output output/demo-video --width 1080 --height 1920
```

使用阿里云 TTS：

```bash
python main.py audio --text-file examples/example.txt --provider aliyun --language zh --output output/aliyun-demo
```

## 7. 阿里云百炼配置

### 获取 API Key

在阿里云百炼 Model Studio 控制台创建 API Key。

复制配置文件：

```bash
cp .env.example .env
```

使用 TextEdit 编辑：

```bash
open -e .env
```

配置示例：

```dotenv
DASHSCOPE_API_KEY=your_api_key_here

DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1

DASHSCOPE_MODEL=qwen3-tts-flash

DASHSCOPE_VOICE=Cherry
```

注意：

- 上述地址为国际服务区域示例。
- 如果使用中国内地（北京）区域，需要使用对应区域的服务地址和 API Key。
- API Key 与服务区域有关。
- `.env` 文件包含敏感信息，不要上传到 GitHub。

## 8. 常见问题

### FFmpeg not found

安装 FFmpeg：

```bash
brew install ffmpeg
```

检查：

```bash
ffmpeg -version
```

### Edge-TTS 网络错误

- 检查网络连接。
- 稍后重新尝试。
- 检查所选语音是否仍然可用。
- 必要时切换到阿里云 TTS。

### Alibaba 401 / Unauthorized

- 检查 API Key 是否正确。
- 检查 API Key 所属区域。
- 确认账号是否具有对应模型的调用权限。

### Alibaba 400 / Invalid voice or model

检查 `.env` 中的模型和音色设置，确认它们在当前百炼服务区域可用。

### 中文字幕显示方框

安装或指定支持中文的字体。

macOS 示例：

```text
/System/Library/Fonts/PingFang.ttc
```

必要时通过 `TEXT2MEDIA_FONT` 设置字体文件路径。

### 视频生成失败

- 检查 FFmpeg 是否正常安装。
- 检查背景图片或视频是否可以正常读取。
- 检查输出目录是否具有写入权限。
- 查看终端中的 FFmpeg 错误信息。

## 9. 项目结构

```text
Text2Media/
├── app.py
├── main.py
├── src/
│   ├── config.py
│   ├── text_utils.py
│   ├── tts.py
│   ├── subtitle.py
│   ├── media.py
│   └── pipeline.py
├── examples/
├── assets/
│   └── backgrounds/
├── output/
├── tests/
├── .env.example
├── requirements.txt
└── install.sh
```

## 10. 安全说明

- 不要将 `.env` 上传到 GitHub。
- 不要在代码中硬编码 API Key。
- 不要公开分享个人 API Key。
- Edge-TTS 和阿里云 TTS 均依赖在线服务。
- 阿里云服务可能产生费用，具体以百炼控制台的价格和配额为准。

## 11. 版本信息

**Current Version: v1.1.0**

本版本主要更新：

- Modern 双语 Gradio 网页界面
- 五种视频背景模式
- 背景参数自定义
- 背景音乐混音
- 字幕设置优化
- 视频生成流程优化

## 12. License

MIT License.

第三方服务和依赖库遵循各自的许可协议。

---

# English Documentation

## 1. Introduction

Text2Media is a beginner-friendly, local-first AI media generation tool.

It converts text into speech, generates SRT subtitles, and creates captioned MP4 videos.

Supported TTS providers:

- Edge-TTS
- Alibaba Cloud Model Studio / DashScope Qwen TTS

The project provides both a command-line interface (CLI) and a Gradio web interface.

## 2. Features

### Text-to-Speech

- Edge-TTS (free online service, no API key required)
- Alibaba Cloud Bailian TTS
- Chinese and English
- Voice and speech rate settings

### Automatic Subtitles

- Automatic SRT generation
- Sentence-level subtitle timing based on generated audio clips
- Adjustable font size
- Adjustable maximum characters per line
- Top, center, and bottom subtitle positions
- Optional subtitle outline

Note: Subtitle timing is sentence-level, not forced word-level alignment.

### Five Video Background Modes

| Mode | Description |
|---|---|
| Solid | Custom solid-color background |
| Vinyl | Animated vinyl record |
| Wave | Animated audio visualizer |
| Image | Local image background |
| Video | Local video background |

Additional settings:

- Image and video fitting: Cover / Contain
- Waveform and Spectrum styles
- Custom visualizer color and height
- Vinyl size, position, and rotation speed

### Background Music

Add background music to the final MP4 video.

- Upload local audio files
- Enable or disable background music
- Adjust music volume
- Loop music
- Configure fade-in and fade-out

**Important: Background music is mixed into the final MP4 only. The separately generated MP3 always contains narration only.**

### Output Files

| File | Description |
|---|---|
| MP3 | Generated narration |
| SRT | Subtitle file |
| MP4 | Captioned video with background |

## 3. Requirements

- macOS, Windows, or Linux
- Python 3.10+
- FFmpeg installed and available in PATH
- Internet connection for online TTS providers

## 4. Installation

### macOS

Install FFmpeg:

```bash
brew install ffmpeg
```

Clone the repository:

```bash
git clone https://github.com/wwdog2000/Text2Media.git
cd Text2Media
```

Run the installer:

```bash
bash install.sh
```

The installer creates a Python virtual environment and installs the required packages.

### Windows 10 / 11 Installation

#### Requirements

- Windows 10 or Windows 11
- Python 3.11 or later
- Git
- FFmpeg

#### Step 1. Install Python, Git and FFmpeg

Open PowerShell and run:

```powershell
winget install --id Python.Python.3.11 --exact
winget install --id Git.Git --exact
winget install --id Gyan.FFmpeg --exact
```

Restart PowerShell after installation.

Verify the installations:

```powershell
py --version
git --version
ffmpeg -version
```

#### Step 2. Download Text2Media

```powershell
git clone https://github.com/wwdog2000/Text2Media.git
cd Text2Media
```

#### Step 3. Install Python Dependencies

Run the Windows installation script:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

#### Step 4. Configure Alibaba Cloud TTS (Optional)

Open `.env` and configure your Alibaba Cloud API key if you want to use Qwen TTS.

Edge-TTS does not require an API key.

#### Step 5. Start Text2Media

```powershell
.\.venv\Scripts\python.exe app.py
```

Open your browser and visit:

```text
http://127.0.0.1:7860
```

#### Troubleshooting

**FFmpeg not found**

Make sure FFmpeg is installed and available in the Windows PATH environment variable. Restart PowerShell and run:

```powershell
ffmpeg -version
```

**Python virtual environment issues**

Use the Python executable inside `.venv` directly:

```powershell
.\.venv\Scripts\python.exe app.py
```

This avoids PowerShell activation policy issues.

### Start the Web Interface

```bash
source .venv/bin/activate
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

## 5. Web Interface Workflow

1. Enter your text or script.
2. Select Edge-TTS or Alibaba Cloud Bailian.
3. Choose the language, voice, and speech rate.
4. Select Audio Only or Audio + Video.
5. Choose one of the five background modes.
6. Configure video and subtitle settings.
7. Optionally upload background music and configure its volume, looping, and fade effects.
8. Click Generate Project.

After generation, you can access the MP3, SRT, and MP4 files through the interface.

## 6. CLI Examples

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Generate audio and subtitles:

```bash
python main.py audio --text-file examples/example.txt --provider edge --language zh --output output/demo
```

Generate a video with an image background:

```bash
python main.py video --text-file examples/example.txt --provider edge --language zh \
  --background assets/backgrounds/sample.png --output output/demo-video --width 1080 --height 1920
```

Use Alibaba TTS:

```bash
python main.py audio --text-file examples/example.txt --provider aliyun --language zh --output output/aliyun-demo
```

## 7. Alibaba Cloud Configuration

Create an API key in Alibaba Cloud Model Studio.

Copy the example environment file:

```bash
cp .env.example .env
```

Edit it:

```bash
open -e .env
```

Example:

```dotenv
DASHSCOPE_API_KEY=your_api_key_here

DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1

DASHSCOPE_MODEL=qwen3-tts-flash

DASHSCOPE_VOICE=Cherry
```

The endpoint above is an example for the international service.

For the China (Beijing) region, use the matching endpoint and API key from your Model Studio console.

API keys are region-specific.

Never commit your `.env` file or expose your API key.

## 8. Troubleshooting

**FFmpeg not found**

```bash
brew install ffmpeg
```

**Edge-TTS network errors**

- Check your internet connection.
- Retry later.
- Check whether the selected voice is still available.
- Switch to Alibaba TTS if necessary.

**Alibaba 401 / Unauthorized**

- Verify your API key.
- Check the key's service region.
- Confirm access to the selected model.

**Alibaba 400 / Invalid voice or model**

Check the model and voice settings in your `.env` file and confirm availability in your Model Studio region.

**Chinese subtitles appear as boxes**

Install a Chinese font or configure `TEXT2MEDIA_FONT`.

macOS example:

```text
/System/Library/Fonts/PingFang.ttc
```

**Video generation errors**

- Check your FFmpeg installation.
- Verify that the selected background files can be read.
- Check output directory permissions.
- Review FFmpeg error messages in Terminal.

## 9. Project Structure

```text
Text2Media/
├── app.py
├── main.py
├── src/
│   ├── config.py
│   ├── text_utils.py
│   ├── tts.py
│   ├── subtitle.py
│   ├── media.py
│   └── pipeline.py
├── examples/
├── assets/
│   └── backgrounds/
├── output/
├── tests/
├── .env.example
├── requirements.txt
└── install.sh
```

## 10. Security

- Never commit `.env` files.
- Never hard-code API keys.
- Do not share API keys publicly.
- Online TTS providers require an internet connection.
- Alibaba Cloud services may incur usage charges.

## 11. Version

**Current Version: v1.1.0**

Highlights:

- Modern bilingual Gradio interface
- Five video background modes
- Customizable background parameters
- Background music mixing
- Improved subtitle controls
- Improved video generation workflow

## 12. License

MIT License.

Third-party services and dependencies are subject to their respective licenses.
