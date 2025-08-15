#!/bin/bash

echo "🔧 Installing dependencies for Stunting Medical Assistant..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Uninstall potentially conflicting packages
echo "🧹 Cleaning up potentially conflicting packages..."
pip uninstall -y openai openai-whisper openai-cli 2>/dev/null || true

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
python3 check_versions.py

echo ""
echo "✅ Installation completed!"
echo "🚀 To run the application:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "🔑 Don't forget to set up your OpenAI API key in .env file!"

