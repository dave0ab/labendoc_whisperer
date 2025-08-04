# Lab-Endoc Transcription Service

AI-powered audio transcription service using OpenAI Whisper with audio enhancement and text improvement.

## 🚀 Quick Setup

### 1. Install System Dependencies
```bash
# Install FFmpeg (required for audio processing)
sudo apt update
sudo apt install ffmpeg python3-pip python3-venv
```

### 2. Create Virtual Environment
```bash
# Navigate to project directory
cd /path/to/labendoc/transcribe

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
# Make sure venv is activated (you should see (venv) in prompt)
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Create .env file
cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=2000

# Authentication
API_TOKEN=your_secure_auth_token_here

# Service Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
EOF
```

### 5. Start the Service
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Start the service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Usage

### Service URLs
- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

### Default API Token
```
lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE
```

### Test the Service
```bash
# Health check
curl -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8000/health

# Transcribe audio file
curl -X POST http://localhost:8000/transcribe \
  -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" \
  -F "audio=@your_audio_file.wav"
```

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **FFmpeg**: For audio processing
- **OpenAI API Key**: For text enhancement (optional)
- **RAM**: 2GB+ recommended
- **Storage**: 1GB+ free space

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build
```bash
# Build image
docker build -t labendoc-transcription .

# Run container
docker run -d \
  --name labendoc-transcription \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e API_TOKEN=your_token \
  labendoc-transcription
```

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill existing processes
pkill -f uvicorn

# Or use different port
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### FFmpeg Not Found
```bash
# Install FFmpeg
sudo apt update && sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### Dependencies Not Found
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 🔒 Security

- Change the default API token in `.env` file
- Use HTTPS in production
- Configure firewall rules
- Limit access to trusted IPs

## 📊 Features

- **Multi-language transcription** with automatic language detection
- **Audio enhancement** for better transcription quality
- **OpenAI GPT-4 integration** for text improvement
- **Automatic translation** to English
- **Web interface** for easy testing
- **RESTful API** for integration
- **Docker support** for containerized deployment

## 📁 Project Structure

```
transcribe/
├── main.py              # FastAPI application
├── transcriber.py       # Core transcription logic
├── ffmpeg_utils.py      # FFmpeg utilities
├── audio_enhancer.py    # Audio enhancement
├── openai_enhancer.py   # OpenAI integration
├── requirements.txt     # Python dependencies
├── venv/               # Virtual environment
├── index.html          # Web interface
├── docker-compose.yml  # Docker configuration
└── Dockerfile          # Docker build file
```

## 🎯 Quick Commands

```bash
# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run (every time)
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Stop
Ctrl+C

# Deactivate venv
deactivate
``` 