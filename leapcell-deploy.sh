#!/bin/bash

# Leapcell Deployment Script for Lab-Endoc Transcription Service
# This script handles the webrtcvad compilation issue

set -e

echo "🚀 Starting Leapcell deployment for transcription service..."

# Update package lists
echo "📦 Updating package lists..."
apt-get update

# Install build tools and dependencies
echo "🔧 Installing build tools and dependencies..."
apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    ffmpeg \
    libsndfile1 \
    libasound2-dev \
    portaudio19-dev

# Upgrade pip and install build tools
echo "🐍 Upgrading pip and installing Python build tools..."
pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p /app/uploads /app/logs

# Set permissions
echo "🔐 Setting permissions..."
chmod -R 755 /app/uploads /app/logs

echo "✅ Deployment completed successfully!"
echo "🎯 Starting the application..."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000 