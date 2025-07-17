#!/bin/bash

# AutoRedactAI Setup Script
# This script sets up the development environment for AutoRedactAI

set -e

echo "🚀 Setting up AutoRedactAI Development Environment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if Node.js is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. Installing via Docker instead."
        return 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_warning "Node.js version is less than 18. Using Docker instead."
        return 1
    fi
    
    print_success "Node.js is installed and version is compatible"
    return 0
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. Installing via Docker instead."
        return 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ "$PYTHON_VERSION" < "3.11" ]]; then
        print_warning "Python version is less than 3.11. Using Docker instead."
        return 1
    fi
    
    print_success "Python 3 is installed and version is compatible"
    return 0
}

# Setup environment files
setup_env_files() {
    print_status "Setting up environment files..."
    
    # Backend environment
    if [ ! -f "backend/.env" ]; then
        cp backend/env.example backend/.env
        print_success "Created backend/.env from template"
    else
        print_warning "backend/.env already exists, skipping..."
    fi
    
    # Frontend environment
    if [ ! -f "frontend/.env" ]; then
        cp frontend/env.example frontend/.env
        print_success "Created frontend/.env from template"
    else
        print_warning "frontend/.env already exists, skipping..."
    fi
}

# Setup local development (without Docker)
setup_local() {
    print_status "Setting up local development environment..."
    
    # Backend setup
    print_status "Setting up Python backend..."
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Created Python virtual environment"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Download spaCy model
    python -m spacy download en_core_web_sm
    
    cd ..
    
    # Frontend setup
    print_status "Setting up Node.js frontend..."
    cd frontend
    
    # Install dependencies
    npm install
    
    cd ..
    
    print_success "Local development environment setup complete"
}

# Setup Docker development
setup_docker() {
    print_status "Setting up Docker development environment..."
    
    # Build and start services
    docker-compose up -d postgres redis
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Run database migrations
    print_status "Running database migrations..."
    docker-compose exec backend alembic upgrade head
    
    print_success "Docker development environment setup complete"
}

# Main setup function
main() {
    print_status "Checking system requirements..."
    
    check_docker
    
    # Check if we can use local development
    NODE_AVAILABLE=false
    PYTHON_AVAILABLE=false
    
    if check_node; then
        NODE_AVAILABLE=true
    fi
    
    if check_python; then
        PYTHON_AVAILABLE=true
    fi
    
    # Setup environment files
    setup_env_files
    
    # Choose setup method
    if [ "$NODE_AVAILABLE" = true ] && [ "$PYTHON_AVAILABLE" = true ]; then
        echo ""
        echo "Both Node.js and Python are available locally."
        read -p "Do you want to use local development (y) or Docker (n)? [y/N]: " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            setup_local
        else
            setup_docker
        fi
    else
        print_status "Using Docker for development..."
        setup_docker
    fi
    
    echo ""
    print_success "Setup complete! 🎉"
    echo ""
    echo "Next steps:"
    echo "1. Configure your environment variables in backend/.env and frontend/.env"
    echo "2. Start the development servers:"
    echo "   - Local: ./start-local.sh"
    echo "   - Docker: ./start-docker.sh"
    echo "3. Visit http://localhost:3000 to access the application"
    echo ""
    echo "For more information, see the README.md file."
}

# Run main function
main "$@" 