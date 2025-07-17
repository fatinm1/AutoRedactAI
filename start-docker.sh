#!/bin/bash

# AutoRedactAI Docker Development Startup Script

set -e

echo "🐳 Starting AutoRedactAI Docker Development Environment"
echo "======================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if environment files exist
if [ ! -f "backend/.env" ]; then
    print_warning "backend/.env not found. Please run ./setup.sh first."
    exit 1
fi

if [ ! -f "frontend/.env" ]; then
    print_warning "frontend/.env not found. Please run ./setup.sh first."
    exit 1
fi

# Start all services
print_status "Starting all services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 15

# Check if services are running
print_status "Checking service status..."

if docker-compose ps | grep -q "Up"; then
    print_success "All services are running!"
else
    print_warning "Some services may not be running properly. Check with 'docker-compose ps'"
fi

echo ""
print_success "🚀 AutoRedactAI is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - View service status: docker-compose ps"
echo ""
echo "⏳ Services are starting up. Please wait a moment before accessing the application." 