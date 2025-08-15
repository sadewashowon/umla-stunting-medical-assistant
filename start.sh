#!/bin/bash

# Stunting Medical Assistant Startup Script
# For Unix-like systems (Linux, macOS)

echo "🍼 Stunting Medical Assistant"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python version $PYTHON_VERSION is too old"
    echo "Please install Python $REQUIRED_VERSION or higher"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing/updating dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi

echo "✅ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    if [ -f "env_example.txt" ]; then
        echo "📝 Creating .env from template..."
        cp env_example.txt .env
        echo "✅ .env file created from template"
        echo "💡 Please edit .env file with your configuration"
    else
        echo "❌ env_example.txt not found"
        exit 1
    fi
fi

# Run tests (optional)
echo "🧪 Running quick tests..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo "✅ Tests passed"
else
    echo "⚠️  Some tests failed, but continuing..."
fi

# Start the application
echo ""
echo "🚀 Starting Stunting Medical Assistant..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"
echo "================================"

streamlit run app.py --server.port=8501 --server.address=localhost

