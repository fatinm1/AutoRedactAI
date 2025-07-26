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

echo "✅ Build completed!" 