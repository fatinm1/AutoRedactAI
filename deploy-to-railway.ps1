# AutoRedactAI Railway Deployment Script (PowerShell)
# This script helps you deploy your application to Railway

Write-Host "🚀 AutoRedactAI Railway Deployment Script" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if Railway CLI is installed
try {
    $railwayVersion = railway --version
    Write-Host "✅ Railway CLI is installed: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI is not installed." -ForegroundColor Red
    Write-Host "Please install it first: npm install -g @railway/cli" -ForegroundColor Yellow
    Write-Host "Then run: railway login" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in
try {
    $whoami = railway whoami
    Write-Host "✅ Logged in to Railway as: $whoami" -ForegroundColor Green
} catch {
    Write-Host "❌ You are not logged in to Railway." -ForegroundColor Red
    Write-Host "Please run: railway login" -ForegroundColor Yellow
    exit 1
}

# Create new project
Write-Host "📦 Creating Railway project..." -ForegroundColor Blue
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$projectName = "autoredact-ai-$timestamp"

try {
    railway init --name $projectName
    Write-Host "✅ Project created: $projectName" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create project. You may need to create it manually in the Railway dashboard." -ForegroundColor Red
}

# Add PostgreSQL database
Write-Host "🗄️ Adding PostgreSQL database..." -ForegroundColor Blue
Write-Host "Please add a PostgreSQL service manually in the Railway dashboard." -ForegroundColor Yellow

# Set environment variables
Write-Host "🔧 Setting up environment variables..." -ForegroundColor Blue

# Generate a secure secret key
$secretKey = -join ((48..57) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})

try {
    railway variables set SECRET_KEY=$secretKey
    railway variables set ENVIRONMENT=production
    railway variables set DEBUG=false
    railway variables set ALLOWED_HOSTS="*"
    Write-Host "✅ Environment variables set" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not set environment variables automatically." -ForegroundColor Yellow
    Write-Host "Please set them manually in the Railway dashboard:" -ForegroundColor Yellow
    Write-Host "SECRET_KEY=$secretKey" -ForegroundColor Cyan
    Write-Host "ENVIRONMENT=production" -ForegroundColor Cyan
    Write-Host "DEBUG=false" -ForegroundColor Cyan
    Write-Host "ALLOWED_HOSTS=*" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 Railway project setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to Railway dashboard: https://railway.app" -ForegroundColor White
Write-Host "2. Select your project: $projectName" -ForegroundColor White
Write-Host "3. Add your GitHub repository" -ForegroundColor White
Write-Host "4. Set the root directory to 'backend/' for the backend service" -ForegroundColor White
Write-Host "5. Create another service for frontend with root directory 'frontend/'" -ForegroundColor White
Write-Host "6. Copy the DATABASE_URL from PostgreSQL service to backend service" -ForegroundColor White
Write-Host "7. Set VITE_API_URL in frontend service to your backend URL" -ForegroundColor White
Write-Host ""
Write-Host "📖 For detailed instructions, see: RAILWAY_DEPLOYMENT.md" -ForegroundColor Cyan 