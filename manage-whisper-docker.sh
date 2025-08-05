#!/bin/bash

# Lab-Endoc Whisper Docker Management Script
# This script manages the Docker containers for the transcription service

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

# Configuration
SERVICE_NAME="whisper"
PROJECT_DIR="/home/dev/labendoc/transcribe"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if Docker Compose is available
check_docker_compose() {
    if ! docker compose version > /dev/null 2>&1; then
        print_error "Docker Compose is not available. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Check container status
check_status() {
    print_status "Checking container status..."
    if docker compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        print_success "Containers are running"
        docker compose -f "$COMPOSE_FILE" ps
        return 0
    else
        print_warning "Containers are not running"
        return 1
    fi
}

# Start containers
start_containers() {
    print_status "Starting Docker containers..."
    
    # Create necessary directories
    mkdir -p "$PROJECT_DIR/uploads" "$PROJECT_DIR/logs"
    
    # Build and start containers
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" build --no-cache
    docker compose -f "$COMPOSE_FILE" up -d
    
    # Wait for service to start
    sleep 10
    
    # Test the service
    if curl -s -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8000/health > /dev/null; then
        print_success "Service is running and healthy!"
    else
        print_warning "Service started but health check failed"
    fi
}

# Stop containers
stop_containers() {
    print_status "Stopping Docker containers..."
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" down
    print_success "Containers stopped"
}

# Restart containers
restart_containers() {
    print_status "Restarting Docker containers..."
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" restart
    print_success "Containers restarted"
}

# Show logs
show_logs() {
    print_status "Showing container logs..."
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" logs -f
}

# Show status
show_status() {
    print_status "Container status:"
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" ps
}

# Clean up
cleanup() {
    print_status "Cleaning up containers and images..."
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" down --rmi all --volumes
    print_success "Cleanup completed"
}

# Main function
main() {
    case "${1:-}" in
        "start")
            check_docker
            check_docker_compose
            start_containers
            ;;
        "stop")
            check_docker
            stop_containers
            ;;
        "restart")
            check_docker
            check_docker_compose
            restart_containers
            ;;
        "status")
            check_docker
            show_status
            ;;
        "logs")
            check_docker
            show_logs
            ;;
        "cleanup")
            check_docker
            cleanup
            ;;
        "health")
            check_docker
            if check_status; then
                print_success "Service is healthy"
            else
                print_error "Service is not healthy"
                exit 1
            fi
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|logs|cleanup|health}"
            echo ""
            echo "Commands:"
            echo "  start   - Start the Docker containers"
            echo "  stop    - Stop the Docker containers"
            echo "  restart - Restart the Docker containers"
            echo "  status  - Show container status"
            echo "  logs    - Show container logs"
            echo "  cleanup - Remove containers and images"
            echo "  health  - Check service health"
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 