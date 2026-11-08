#!/bin/bash
set -e

echo "======================================"
echo " Text2Media installer"
echo "======================================"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] Python 3 was not found. Install Python 3.11 first."
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[ERROR] FFmpeg was not found."
  echo "Run: brew install ffmpeg"
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
fi

mkdir -p output
echo ""
echo "[OK] Installation completed."
echo "Start the web app with:"
echo "  source .venv/bin/activate"
echo "  python app.py"
echo ""
if command -v open >/dev/null 2>&1; then
  open -e .env
fi
