# 🐳 Docker Setup for Lab-Endoc Whisper Transcription Service

This guide explains how to run the transcription service using Docker.

## 🚀 Quick Start

### Prerequisites
- Docker installed
- Docker Compose installed

### Automated Setup
```bash
# Run the automated setup script
./docker-setup.sh
```

This script will:
- ✅ Install all dependencies
- ✅ Build the Docker image
- ✅ Start the service
- ✅ Test the endpoints
- ✅ Verify everything is working

## 🔧 Manual Setup

### 1. Create Environment File
```bash
# Create .env file
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
```

### 2. Build and Run
```bash
# Build the image
docker-compose build

# Start the service
docker-compose up -d

# Check status
docker-compose ps
```

## 🎯 Docker Commands

### Service Management
```bash
# Start service
docker-compose up -d

# Stop service
docker-compose down

# Restart service
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Container Access
```bash
# Access container shell
docker-compose exec transcription-service bash

# View container logs
docker-compose logs transcription-service

# Check container health
docker-compose exec transcription-service python -c "import requests; print(requests.get('http://localhost:8000/health', headers={'Authorization': 'Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE'}).json())"
```

## 🌐 Service URLs

- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **Transcription API**: http://localhost:8000/transcribe

## 🔑 Authentication

Default API Token: `lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE`

### Test API
```bash
# Health check
curl -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8000/health

# Test transcription (replace with your audio file)
curl -X POST \
  -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" \
  -F "file=@your-audio-file.wav" \
  http://localhost:8000/transcribe
```

## 📁 Volumes

The Docker setup includes these volumes:
- `./uploads:/app/uploads` - For uploaded audio files
- `./logs:/app/logs` - For application logs
- `./.env:/app/.env:ro` - Environment configuration

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key
- `API_TOKEN` - Authentication token
- `FFMPEG_BINARY` - FFmpeg binary path
- `FFPROBE_BINARY` - FFprobe binary path

### Port Configuration
- Container port: 8000
- Host port: 8000 (configurable in docker-compose.yml)

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs

# Check container status
docker-compose ps

# Restart service
docker-compose down && docker-compose up -d
```

### FFmpeg Issues
```bash
# Check FFmpeg in container
docker-compose exec transcription-service ffmpeg -version
docker-compose exec transcription-service ffprobe -version
```

### Permission Issues
```bash
# Fix volume permissions
sudo chown -R $USER:$USER uploads logs
```

### Health Check Fails
```bash
# Test health manually
curl -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8000/health
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes
docker-compose down -v

# Complete cleanup
docker system prune -a
```

## 📊 Monitoring

### Container Stats
```bash
# View resource usage
docker stats labendoc-transcription

# View container info
docker inspect labendoc-transcription
```

### Logs
```bash
# Follow logs
docker-compose logs -f transcription-service

# View recent logs
docker-compose logs --tail=100 transcription-service
```

## 🔒 Security

- Non-root user inside container
- Read-only environment file mount
- Isolated network
- Health checks enabled
- Resource limits (configurable)

## 🚀 Production Deployment

For production deployment:

1. **Update .env file** with production values
2. **Configure reverse proxy** (nginx/apache)
3. **Set up SSL certificates**
4. **Configure monitoring** (Prometheus/Grafana)
5. **Set up logging** (ELK stack)
6. **Configure backups** for uploads and logs

## 📝 Notes

- The container includes FFmpeg and all audio processing dependencies
- The service runs on port 8000 inside the container
- Health checks run every 30 seconds
- Logs are available via `docker-compose logs`
- The web interface is accessible at the root URL 