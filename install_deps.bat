@echo off
echo 🔧 Installing dependencies for Stunting Medical Assistant...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Uninstall potentially conflicting packages
echo 🧹 Cleaning up potentially conflicting packages...
pip uninstall -y openai openai-whisper openai-cli 2>nul

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Verify installation
echo 🔍 Verifying installation...
python check_versions.py

echo.
echo ✅ Installation completed!
echo 🚀 To run the application:
echo    venv\Scripts\activate.bat
echo    streamlit run app.py
echo.
echo 🔑 Don't forget to set up your OpenAI API key in .env file!
pause

