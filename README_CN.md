# Text2Media：文字一键生成音频和字幕视频

把一段文字转换成配音、SRT 字幕和 MP4 字幕视频。支持 Edge-TTS 与阿里云百炼双引擎，提供命令行和网页界面。

## V1.0 功能
- 中文、英文文字转语音
- Edge-TTS：无需 API Key，但需要联网
- 阿里云百炼 Qwen TTS：需要 API Key，按云服务规则计费
- 导出 MP3、WAV、SRT
- 图片背景或纯色背景生成 MP4
- 自动逐句生成配音，并根据每句实际音频时长生成字幕时间轴
- Gradio 网页界面 + CLI 命令行

## 一、Mac 安装

先打开“终端”，逐行复制执行：

```bash
brew install ffmpeg
```

检查 FFmpeg：
```bash
ffmpeg -version
```

下载项目（正式发布到 GitHub 后执行；把 YOUR_GITHUB_NAME 换成自己的 GitHub 用户名）：
```bash
cd ~
git clone https://github.com/YOUR_GITHUB_NAME/Text2Media.git
cd Text2Media
```

如果你已经下载了项目 ZIP 并解压，则在终端输入 `cd `（注意 cd 后有空格），把 Text2Media 文件夹拖进终端，再按回车。

运行安装脚本：
```bash
bash install.sh
```

安装完成后，启动网页：
```bash
source .venv/bin/activate
python app.py
```

终端出现本地网址后，按住 Command 点击网址，或复制到浏览器打开。通常是：
`http://127.0.0.1:7860`

## 二、先做一次音频测试

项目自带测试文字 `examples/example.txt`。运行：

```bash
source .venv/bin/activate
python main.py audio --text-file examples/example.txt --provider edge --language zh --output output/my-first-audio
```

成功后检查 `output` 文件夹，应该有：
- `my-first-audio.mp3`
- `my-first-audio.srt`

## 三、生成带字幕视频

项目提供示例背景图 `assets/backgrounds/sample.png`：

```bash
python main.py video --text-file examples/example.txt --provider edge --language zh --background assets/backgrounds/sample.png --output output/my-first-video --width 1080 --height 1920
```

生成：
- `my-first-video.mp3`
- `my-first-video.srt`
- `my-first-video.mp4`

## 四、使用阿里云百炼

1. 登录阿里云百炼 / Model Studio 控制台。
2. 创建对应地域的 API Key，并确认开通了可用的语音合成模型。
3. 在项目文件夹中复制配置模板：

```bash
cp .env.example .env
open -e .env
```

4. 在 `.env` 中填写自己的 Key：

```dotenv
DASHSCOPE_API_KEY=替换成自己的API_KEY
DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/api/v1
DASHSCOPE_MODEL=qwen3-tts-flash
DASHSCOPE_VOICE=Cherry
```

国际站和中国地域的 API Key、服务地址可能不同，必须按控制台显示配置，不能混用。保存后测试：

```bash
python main.py audio --text-file examples/example.txt --provider aliyun --language zh --output output/aliyun-test
```

**安全提醒：绝对不要把 `.env` 上传到 GitHub，也不要把 API Key 写在代码里。** `.gitignore` 已经排除了 `.env`。

## 五、常用命令

音频：
```bash
python main.py audio --text-file examples/example.txt --provider edge --language zh --output output/demo
```

视频：
```bash
python main.py video --text-file examples/example.txt --provider edge --language zh --background assets/backgrounds/sample.png --output output/demo-video
```

英文配音：
```bash
python main.py audio --text-file examples/example.txt --provider edge --language en --output output/english-demo
```

## 六、常见问题

**1. 提示 ffmpeg not found**
```bash
brew install ffmpeg
ffmpeg -version
```

**2. Edge-TTS 连接失败**
检查网络，稍后重试，或者切换到阿里云引擎。

**3. 阿里云 401**
检查 API Key、地域、模型权限。中国地域和国际地域的 Key 不一定通用。

**4. 视频字幕中文乱码**
可在 `.env` 中设置字体路径，例如：
```dotenv
TEXT2MEDIA_FONT=/System/Library/Fonts/PingFang.ttc
```

**5. 想重新安装**
```bash
cd ~/Text2Media
rm -rf .venv
bash install.sh
```

## 当前版本说明
V1.0 的字幕是逐句时间轴，不是逐字卡点。阿里云接口的模型、音色和地域能力可能调整，需以控制台和官方文档为准。
