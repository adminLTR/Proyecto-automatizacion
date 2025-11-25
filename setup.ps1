# Setup script for Windows
# Run this with: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "🚀 Telegram Automation Bot - Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created. Please edit it with your credentials." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✅ .env file already exists." -ForegroundColor Green
    Write-Host ""
}

# Check if credentials.json exists
if (-not (Test-Path credentials.json)) {
    Write-Host "⚠️  WARNING: credentials.json not found!" -ForegroundColor Red
    Write-Host "📥 Please download it from Google Cloud Console and place it in the project root." -ForegroundColor Yellow
    Write-Host "   Instructions: https://console.cloud.google.com/" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✅ credentials.json found." -ForegroundColor Green
    Write-Host ""
}

# Create virtual environment
if (-not (Test-Path venv)) {
    Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✅ Virtual environment already exists." -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment and install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "✅ Dependencies installed." -ForegroundColor Green
Write-Host ""

# Check if token.json exists
if (-not (Test-Path token.json)) {
    Write-Host "🔐 Google authentication required..." -ForegroundColor Yellow
    Write-Host "⚡ Starting app for first-time authentication..." -ForegroundColor Yellow
    Write-Host "   A browser window will open. Please authorize the application." -ForegroundColor Yellow
    Write-Host ""
    
    $response = Read-Host "Press ENTER to start authentication or Ctrl+C to cancel"
    python run.py
} else {
    Write-Host "✅ Google token already exists." -ForegroundColor Green
    Write-Host ""
}

Write-Host ""
Write-Host "✨ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env with your Telegram bot token and email" -ForegroundColor White
Write-Host "2. Run: docker-compose up -d" -ForegroundColor White
Write-Host "3. Start chatting with your bot!" -ForegroundColor White
Write-Host ""
