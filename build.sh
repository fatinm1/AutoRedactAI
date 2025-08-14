#!/bin/bash

# Build script for AutoRedactAI with better error handling

set -e  # Exit on any error

echo "🚀 Starting AutoRedactAI build process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if required files exist
print_status "Checking required files..."
if [ ! -f "Dockerfile" ]; then
    print_error "Dockerfile not found in current directory"
    exit 1
fi

if [ ! -f "frontend/package.json" ]; then
    print_error "Frontend package.json not found"
    exit 1
fi

if [ ! -f "backend/requirements.txt" ]; then
    print_error "Backend requirements.txt not found"
    exit 1
fi

print_status "All required files found"

# Clean up any existing containers and images
print_status "Cleaning up existing containers and images..."
docker system prune -f > /dev/null 2>&1 || true

# Build the image with detailed output
print_status "Building Docker image..."
if docker build --progress=plain --no-cache -t autoredactai:latest .; then
    print_status "✅ Build completed successfully!"
    
    # Show image info
    print_status "Image details:"
    docker images autoredactai:latest
    
    print_status "🎉 AutoRedactAI is ready to run!"
    echo ""
    echo "To run the application:"
    echo "  docker run -p 8000:8000 autoredactai:latest"
    echo ""
    echo "Or use docker-compose:"
    echo "  docker-compose up"
    
else
    print_error "❌ Build failed!"
    echo ""
    echo "Troubleshooting tips:"
    echo "1. Check the error messages above"
    echo "2. Ensure all dependencies are available"
    echo "3. Try building with --no-cache flag"
    echo "4. Check if all required files exist"
    exit 1
fi 