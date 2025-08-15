@echo off
REM Stunting Medical Assistant Startup Script
REM For Windows systems

echo 🍼 Stunting Medical Assistant
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2^>nul') do set PYTHON_VERSION=%%i

if %PYTHON_VERSION% LSS 3.8 (
    echo ❌ Python version %PYTHON_VERSION% is too old
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo ✅ Python %PYTHON_VERSION% found

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo 📥 Installing/updating dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo ✅ Dependencies installed

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    if exist "env_example.txt" (
        echo 📝 Creating .env from template...
        copy env_example.txt .env
        echo ✅ .env file created from template
        echo 💡 Please edit .env file with your configuration
    ) else (
        echo ❌ env_example.txt not found
        pause
        exit /b 1
    )
)

REM Run tests (optional)
echo 🧪 Running quick tests...
python test_app.py

if %errorlevel% neq 0 (
    echo ⚠️  Some tests failed, but continuing...
)

REM Start the application
echo.
echo 🚀 Starting Stunting Medical Assistant...
echo 📱 The app will open in your browser at http://localhost:8501
echo ⏹️  Press Ctrl+C to stop the application
echo ================================

streamlit run app.py --server.port=8501 --server.address=localhost

pause
