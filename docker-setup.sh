#!/bin/bash

# Lab-Endoc Whisper Docker Setup Script
# This script sets up and runs the transcription service using Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Setting up Lab-Endoc Whisper Transcription Service with Docker..."

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=2000

# Authentication
API_TOKEN=lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE

# Service Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info

# FFmpeg Configuration
FFMPEG_BINARY=/usr/bin/ffmpeg
FFPROBE_BINARY=/usr/bin/ffprobe
EOF
    print_success ".env file created"
    print_warning "Please edit .env with your actual API keys"
else
    print_success ".env file exists"
fi

# Stop and remove existing containers
print_status "Stopping existing containers..."
docker compose down 2>/dev/null || true

# Build the Docker image
print_status "Building Docker image..."
docker compose build --no-cache

# Start the service
print_status "Starting the service..."
docker compose up -d

# Wait for service to start
print_status "Waiting for service to start..."
sleep 10

# Check if service is running
if docker compose ps | grep -q "Up"; then
    print_success "Service is running!"
else
    print_error "Service failed to start"
    print_status "Checking container logs..."
    docker compose logs
    exit 1
fi

# Test the service
print_status "Testing the service..."
sleep 5

# Test health endpoint
if curl -s -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8000/health > /dev/null; then
    print_success "Health check passed!"
else
    print_error "Health check failed"
    print_status "Checking container logs..."
    docker compose logs
    exit 1
fi

# Test web interface
if curl -s http://localhost:8000/ | grep -q "Whisper Audio Transcription"; then
    print_success "Web interface is accessible!"
else
    print_warning "Web interface test failed"
fi

print_success "Docker setup complete!"
echo ""
echo "🎯 Docker Commands:"
echo "  Start:   docker-compose up -d"
echo "  Stop:    docker-compose down"
echo "  Restart: docker-compose restart"
echo "  Logs:    docker-compose logs -f"
echo "  Status:  docker-compose ps"
echo "  Shell:   docker-compose exec transcription-service bash"
echo ""
echo "🌐 Service URLs:"
echo "  Web Interface: http://localhost:8000"
echo "  Health Check:  http://localhost:8000/health"
echo "  API Docs:      http://localhost:8000/docs"
echo ""
echo "🔑 Default API Token: lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE"
echo ""
print_status "Service is now running in Docker and ready for use!" 