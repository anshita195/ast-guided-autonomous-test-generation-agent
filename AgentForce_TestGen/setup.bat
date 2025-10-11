@echo off
echo 🚀 AgentForce TestGen Setup (Windows)
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Install Python dependencies
echo 🔧 Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

REM Install Node.js dependencies
echo 🔧 Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 🔧 Creating environment configuration...
    copy env.example .env
    echo ✅ Created .env file
    echo.
    echo 🔑 Please edit .env file and add your GEMINI_API_KEY
    echo    Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    pause
)

REM Create necessary directories
mkdir tests 2>nul
mkdir js_tests 2>nul
mkdir coverage 2>nul

echo 🎉 Setup completed successfully!
echo.
echo 📖 Next steps:
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Start the server: python -m uvicorn app.main:app --reload
echo 3. Visit http://localhost:8000/docs for API documentation
echo.
pause
