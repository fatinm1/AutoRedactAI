#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

echo "Starting AutoRedactAI on port $PORT"

# Check if frontend dist exists
if [ ! -d "/app/frontend/dist" ]; then
    echo "Warning: Frontend dist not found, running in API-only mode"
fi

# Check if backend directory exists
if [ ! -d "/app/backend" ]; then
    echo "Error: Backend directory not found"
    exit 1
fi

# Start the application
echo "Starting uvicorn server..."
exec python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT 