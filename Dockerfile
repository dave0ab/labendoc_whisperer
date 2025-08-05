# Dockerfile for Lab-Endoc Transcription Service
# Includes FFmpeg and all necessary dependencies

FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including FFmpeg and audio processing tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libasound2-dev \
    portaudio19-dev \
    python3-dev \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with specific handling for webrtcvad
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set FFmpeg environment variables
ENV FFMPEG_BINARY=/usr/bin/ffmpeg
ENV FFPROBE_BINARY=/usr/bin/ffprobe

# Create necessary directories
RUN mkdir -p /app/uploads /app/logs

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', headers={'Authorization': 'Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE'})" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 