#!/bin/bash

echo "🚀 Building AutoRedactAI..."

# Install frontend dependencies and build
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
echo "🐍 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Make sure the backend can find its modules
echo "🔧 Setting up Python path..."
export PYTHONPATH="${PYTHONPATH}:/app/backend"

echo "✅ Build completed!" 