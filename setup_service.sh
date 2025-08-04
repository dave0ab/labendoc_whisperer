#!/bin/bash

# Lab-Endoc Whisper Service Setup Script
# This script sets up the systemd service for the transcription service

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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Configuration
SERVICE_NAME="whisper"
SERVICE_FILE="whisper.service"
PROJECT_DIR="/home/dev/labendoc/transcribe"
VENV_DIR="$PROJECT_DIR/venv"

print_status "Setting up Whisper Transcription Service..."

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory not found: $PROJECT_DIR"
    print_status "Please make sure the project is in the correct location"
    exit 1
fi

print_success "Project directory found: $PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    print_warning "Virtual environment not found. Creating one..."
    cd "$PROJECT_DIR"
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment found"
fi

# Install dependencies
print_status "Installing Python dependencies..."
cd "$PROJECT_DIR"
source venv/bin/activate
pip install -r requirements.txt
print_success "Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f "$PROJECT_DIR/.env" ]; then
    print_status "Creating .env file..."
    cat > "$PROJECT_DIR/.env" << EOF
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
EOF
    print_success ".env file created"
    print_warning "Please edit .env with your actual API keys"
else
    print_success ".env file exists"
fi

# Copy service file to systemd
print_status "Installing systemd service..."
sudo cp "$PROJECT_DIR/$SERVICE_FILE" /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/$SERVICE_FILE

# Reload systemd
print_status "Reloading systemd..."
sudo systemctl daemon-reload

# Enable service
print_status "Enabling service..."
sudo systemctl enable $SERVICE_NAME

print_success "Service setup complete!"
echo ""
echo "🎯 Service Commands:"
echo "  Start:   sudo systemctl start $SERVICE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart: sudo systemctl restart $SERVICE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_NAME"
echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "🌐 Service URLs:"
echo "  Web Interface: http://your-server-ip:8000"
echo "  Health Check:  http://your-server-ip:8000/health"
echo "  API Docs:      http://your-server-ip:8000/docs"
echo ""
echo "🔑 Default API Token: lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE"
echo ""
print_status "To start the service, run: sudo systemctl start $SERVICE_NAME" 