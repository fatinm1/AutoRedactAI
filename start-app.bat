@echo off
echo ========================================
echo    AutoRedactAI - Quick Start
echo ========================================
echo.

echo Starting AutoRedactAI application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

echo ✓ Python and Node.js found
echo.

REM Create environment files if they don't exist
if not exist "backend\.env" (
    echo Creating backend environment file...
    echo APP_NAME=AutoRedactAI > backend\.env
    echo VERSION=1.0.0 >> backend\.env
    echo ENVIRONMENT=development >> backend\.env
    echo DEBUG=true >> backend\.env
    echo SECRET_KEY=dev-secret-key-change-in-production >> backend\.env
    echo ALGORITHM=HS256 >> backend\.env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> backend\.env
    echo REFRESH_TOKEN_EXPIRE_DAYS=7 >> backend\.env
    echo DATABASE_URL=sqlite:///./autoredact.db >> backend\.env
    echo MAX_FILE_SIZE=52428800 >> backend\.env
    echo ALLOWED_FILE_TYPES=.pdf,.docx,.txt >> backend\.env
    echo FILE_RETENTION_DAYS=7 >> backend\.env
    echo ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173 >> backend\.env
    echo RATE_LIMIT_PER_MINUTE=100 >> backend\.env
    echo RATE_LIMIT_PER_HOUR=1000 >> backend\.env
    echo ALLOWED_HOSTS=localhost,127.0.0.1,* >> backend\.env
)

if not exist "frontend\.env" (
    echo Creating frontend environment file...
    echo VITE_API_URL=http://localhost:8000 > frontend\.env
    echo VITE_WS_URL=ws://localhost:8000/ws >> frontend\.env
)

echo ✓ Environment files created
echo.

REM Set up backend
echo Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv pydantic sqlalchemy alembic structlog boto3 Pillow pypdf2 python-docx

REM Start backend server in background
echo Starting backend server...
start "AutoRedactAI Backend" cmd /k "call venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

cd ..

REM Set up frontend
echo Setting up frontend...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

REM Start frontend server in background
echo Starting frontend server...
start "AutoRedactAI Frontend" cmd /k "npm run dev"

cd ..

echo.
echo ========================================
echo    AutoRedactAI is starting up!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo The application will open in your browser shortly...
echo.
echo Press any key to exit this script (servers will continue running)
pause >nul 