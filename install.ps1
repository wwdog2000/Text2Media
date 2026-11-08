
$ErrorActionPreference = "Stop"

Write-Host "======================================"
Write-Host " Text2Media Windows Installer"
Write-Host "======================================"

# Check Python
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python was not found."
    Write-Host "Please install Python 3.11 or later."
    exit 1
}

# Check FFmpeg
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] FFmpeg was not found."
    Write-Host "Please install FFmpeg and add it to PATH."
    exit 1
}

# Create virtual environment
if (-not (Test-Path ".venv")) {
    py -3 -m venv .venv
}

$Python = ".\.venv\Scripts\python.exe"

# Install dependencies
& $Python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upgrade pip."
}

& $Python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install requirements."
}

# Create .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

# Create output directory
New-Item -ItemType Directory -Force -Path "output" | Out-Null

Write-Host ""
Write-Host "[OK] Installation completed."
Write-Host "Start the application with:"
Write-Host "  .\.venv\Scripts\python.exe app.py"
