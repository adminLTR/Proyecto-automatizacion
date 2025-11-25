#!/bin/bash
# Setup script for first-time configuration

echo "🚀 Telegram Automation Bot - Setup Script"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your credentials."
    echo ""
else
    echo "✅ .env file already exists."
    echo ""
fi

# Check if credentials.json exists
if [ ! -f credentials.json ]; then
    echo "⚠️  WARNING: credentials.json not found!"
    echo "📥 Please download it from Google Cloud Console and place it in the project root."
    echo "   Instructions: https://console.cloud.google.com/"
    echo ""
else
    echo "✅ credentials.json found."
    echo ""
fi

# Create virtual environment
if [ ! -d venv ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
    echo ""
else
    echo "✅ Virtual environment already exists."
    echo ""
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Dependencies installed."
echo ""

# Check if token.json exists
if [ ! -f token.json ]; then
    echo "🔐 Google authentication required..."
    echo "⚡ Starting app for first-time authentication..."
    echo "   A browser window will open. Please authorize the application."
    echo ""
    python run.py
else
    echo "✅ Google token already exists."
    echo ""
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Telegram bot token and email"
echo "2. Run: docker-compose up -d"
echo "3. Start chatting with your bot!"
echo ""
