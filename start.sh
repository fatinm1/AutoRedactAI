#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

# Set Python path to include the backend directory
export PYTHONPATH=/app/backend:$PYTHONPATH

# Set API URL for frontend
if [ -z "$VITE_API_URL" ]; then
    # In production, use the same host/port as the server
    export VITE_API_URL="http://0.0.0.0:$PORT"
fi

echo "Starting AutoRedactAI on port $PORT"
echo "Python path: $PYTHONPATH"
echo "Current directory: $(pwd)"
echo "API URL: $VITE_API_URL"

# Check if frontend dist exists
if [ ! -d "/app/frontend/dist" ]; then
    echo "Warning: Frontend dist not found, running in API-only mode"
else
    echo "Frontend dist found"
fi

# Check if backend directory exists
if [ ! -d "/app/backend" ]; then
    echo "Error: Backend directory not found"
    exit 1
fi

# Check if app directory exists
if [ ! -d "/app/backend/app" ]; then
    echo "Error: Backend app directory not found"
    exit 1
fi

# Test Python import
echo "Testing Python import..."
cd /app/backend
python -c "import app.main; print('Import successful')" || {
    echo "Import failed, trying alternative approach..."
    python -c "import sys; sys.path.insert(0, '/app/backend'); import app.main; print('Import successful with sys.path')"
}

# Start the application
echo "Starting uvicorn server..."
cd /app/backend
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT 