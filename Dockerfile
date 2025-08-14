# Multi-stage build for both frontend and backend
FROM node:18-alpine AS frontend-builder

# Set work directory for frontend
WORKDIR /app/frontend

# Set environment variables for frontend build
ENV VITE_API_URL=https://autoredactai-production.up.railway.app
ENV NODE_ENV=development
ENV CI=true

# Copy frontend package files
COPY frontend/package*.json ./

# Install ALL dependencies (including dev dependencies needed for build)
RUN npm ci && npm cache clean --force

# Copy frontend source code
COPY frontend/ .

# Build frontend with better error handling
RUN npm run build

# Backend stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/app/backend:/app

# Set work directory
WORKDIR /app

# Install system dependencies for backend with better error handling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy startup script
COPY start.sh ./
RUN chmod +x start.sh

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (will be overridden by Railway)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run the application with the startup script
CMD ["./start.sh"] 