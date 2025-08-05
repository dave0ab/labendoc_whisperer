#!/bin/bash

# Lab-Endoc Whisper Service Wrapper
# This script manages the Docker containers for the transcription service

set -e

# Configuration
PROJECT_DIR="/home/dev/labendoc/transcribe"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"
SERVICE_NAME="labendoc-transcription"

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

# Function to start containers
start_containers() {
    print_status "Starting Docker containers..."
    
    # Create necessary directories
    mkdir -p "$PROJECT_DIR/uploads" "$PROJECT_DIR/logs"
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Build and start containers
    docker compose -f "$COMPOSE_FILE" build --no-cache
    docker compose -f "$COMPOSE_FILE" up -d
    
    # Wait for service to start
    sleep 10
    
    # Test the service
    if curl -s -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8000/health > /dev/null; then
        print_success "Service is running and healthy!"
        return 0
    else
        print_warning "Service started but health check failed"
        return 1
    fi
}

# Function to stop containers
stop_containers() {
    print_status "Stopping Docker containers..."
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" down
    print_success "Containers stopped"
}

# Function to restart containers
restart_containers() {
    print_status "Restarting Docker containers..."
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" restart
    print_success "Containers restarted"
}

# Function to check if containers are running
check_containers() {
    cd "$PROJECT_DIR"
    if docker compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        return 0
    else
        return 1
    fi
}

# Main function
main() {
    case "${1:-}" in
        "start")
            if check_containers; then
                print_status "Containers are already running"
                return 0
            else
                start_containers
            fi
            ;;
        "stop")
            if check_containers; then
                stop_containers
            else
                print_status "Containers are not running"
            fi
            ;;
        "restart")
            if check_containers; then
                restart_containers
            else
                print_status "Containers are not running, starting them..."
                start_containers
            fi
            ;;
        "status")
            if check_containers; then
                print_success "Containers are running"
                docker compose -f "$COMPOSE_FILE" ps
            else
                print_warning "Containers are not running"
            fi
            ;;
        *)
            print_error "Usage: $0 {start|stop|restart|status}"
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 