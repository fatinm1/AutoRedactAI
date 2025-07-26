#!/bin/bash

# AutoRedactAI Railway Deployment Script
# This script helps you deploy your application to Railway

echo "🚀 AutoRedactAI Railway Deployment Script"
echo "=========================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed."
    echo "Please install it first: npm install -g @railway/cli"
    echo "Then run: railway login"
    exit 1
fi

echo "✅ Railway CLI is installed"

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "❌ You are not logged in to Railway."
    echo "Please run: railway login"
    exit 1
fi

echo "✅ Logged in to Railway"

# Create new project if it doesn't exist
echo "📦 Creating Railway project..."
PROJECT_NAME="autoredact-ai-$(date +%s)"
railway init --name "$PROJECT_NAME"

echo "✅ Project created: $PROJECT_NAME"

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
railway add

echo "✅ PostgreSQL database added"

# Set environment variables for backend
echo "🔧 Setting up environment variables..."

# Generate a secure secret key
SECRET_KEY=$(openssl rand -hex 32)

# Set backend environment variables
railway variables set SECRET_KEY="$SECRET_KEY"
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set ALLOWED_HOSTS="*"

echo "✅ Environment variables set"

echo ""
echo "🎉 Railway project setup complete!"
echo ""
echo "Next steps:"
echo "1. Go to Railway dashboard: https://railway.app"
echo "2. Select your project: $PROJECT_NAME"
echo "3. Add your GitHub repository"
echo "4. Set the root directory to 'backend/' for the backend service"
echo "5. Create another service for frontend with root directory 'frontend/'"
echo "6. Copy the DATABASE_URL from PostgreSQL service to backend service"
echo "7. Set VITE_API_URL in frontend service to your backend URL"
echo ""
echo "📖 For detailed instructions, see: RAILWAY_DEPLOYMENT.md" 