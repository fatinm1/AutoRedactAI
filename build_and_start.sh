#!/bin/bash

# Build and Start Script for AutoRedactAI
# This script builds the frontend and then starts the backend

echo "🚀 Starting AutoRedactAI build and deployment..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Start backend (which will serve the frontend)
echo "🔧 Starting backend server..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT 