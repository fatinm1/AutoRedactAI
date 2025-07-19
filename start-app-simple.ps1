Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    AutoRedactAI - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting AutoRedactAI application..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Create environment files if they don't exist
if (-not (Test-Path "backend\.env")) {
    Write-Host "Creating backend environment file..." -ForegroundColor Yellow
    $backendEnv = @"
APP_NAME=AutoRedactAI
VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./autoredact.db
MAX_FILE_SIZE=52428800
ALLOWED_FILE_TYPES=.pdf,.docx,.txt
FILE_RETENTION_DAYS=7
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000
ALLOWED_HOSTS=localhost,127.0.0.1,*
"@
    $backendEnv | Out-File -FilePath "backend\.env" -Encoding UTF8
}

if (-not (Test-Path "frontend\.env")) {
    Write-Host "Creating frontend environment file..." -ForegroundColor Yellow
    $frontendEnv = @"
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
"@
    $frontendEnv | Out-File -FilePath "frontend\.env" -Encoding UTF8
}

Write-Host "✓ Environment files created" -ForegroundColor Green
Write-Host ""

# Set up backend
Write-Host "Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment and install dependencies
Write-Host "Activating virtual environment and installing dependencies..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv pydantic sqlalchemy alembic structlog boto3 Pillow pypdf2 python-docx

# Start backend server in background
Write-Host "Starting backend server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

Set-Location ..

# Set up frontend
Write-Host "Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies if node_modules doesn't exist
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install
}

# Start frontend server in background
Write-Host "Starting frontend server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run dev" -WindowStyle Normal

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    AutoRedactAI is starting up!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "The application will open in your browser shortly..." -ForegroundColor Green
Write-Host ""
Write-Host "Press Enter to exit this script (servers will continue running)" -ForegroundColor Yellow
Read-Host 