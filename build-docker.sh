#!/bin/bash

# Build script for Lab-Endoc Transcription Service
# Handles webrtcvad compilation issues

set -e

echo "🔧 Building Lab-Endoc Transcription Service..."

# Clean up any previous builds
docker-compose down --remove-orphans 2>/dev/null || true
docker system prune -f

# Build with specific platform if needed
if [[ "$(uname -m)" == "aarch64" || "$(uname -m)" == "arm64" ]]; then
    echo "🖥️  Detected ARM64 architecture - using platform-specific build"
    docker-compose build --no-cache transcription-service
else
    echo "🖥️  Building for current architecture"
    docker-compose build --no-cache transcription-service
fi

echo "✅ Build completed successfully!"
echo "🚀 To start the service, run: docker-compose up -d" 