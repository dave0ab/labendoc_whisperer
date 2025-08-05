# Lab-Endoc Transcription Service

AI-powered audio transcription service using OpenAI Whisper with audio enhancement and automatic English translation.

## 🚀 Deployment

This service is deployed on **Leapcell** at:
- **URL**: https://labendocwhisperer-dave0ab9103-dcy37ba4.leapcell.dev
- **Health Check**: https://labendocwhisperer-dave0ab9103-dcy37ba4.leapcell.dev/health
- **API Docs**: https://labendocwhisperer-dave0ab9103-dcy37ba4.leapcell.dev/docs

## 🎯 Features

- **🎵 Audio Enhancement**: Pre-processes audio for better transcription quality
- **🤖 OpenAI GPT-4 Integration**: Professional text enhancement and translation
- **🌍 Multi-language Support**: Auto-detection and translation to English
- **📊 Real-time Processing**: Background job processing with status tracking
- **🔐 Secure Authentication**: Bearer token authentication

## 📋 API Endpoints

### Health Check
```bash
GET /health
Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE
```

### Transcribe Audio
```bash
POST /transcribe
Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE
Content-Type: multipart/form-data

Parameters:
- file: Audio file (MP3, WAV, M4A, FLAC, OGG, WEBM, MP4)
- lang: Language hint (default: auto)
- enhance_accuracy: Apply post-processing (default: true)
- use_openai: Use GPT-4 enhancement (default: true)
- enhancement_type: Enhancement type (professional, medical, business, legal)
- enhance_audio: Audio preprocessing (default: true)
- audio_enhancement_level: Enhancement level (light, medium, aggressive)
- auto_translate_to_english: Auto-translate to English (default: true)
```

### Web Interface
```bash
GET /
```
Provides a user-friendly web interface for testing the transcription service.

## 🔧 Technology Stack

- **FastAPI**: Modern Python web framework
- **OpenAI Whisper**: AI-powered speech recognition
- **FFmpeg**: Audio processing and enhancement
- **OpenAI GPT-4**: Text enhancement and translation
- **Leapcell**: Cloud deployment platform

## 📁 Project Structure

```
transcribe/
├── main.py              # FastAPI application
├── start.py             # Startup script for Leapcell
├── transcriber.py       # Core transcription logic
├── audio_enhancer.py    # Audio enhancement utilities
├── openai_enhancer.py   # OpenAI integration
├── ffmpeg_utils.py      # FFmpeg utilities
├── requirements.txt     # Python dependencies
├── index.html          # Web interface
└── accuracy_data/      # Accuracy enhancement data
```

## 🛠️ Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export API_TOKEN=lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE
   ```

3. **Run the service**:
   ```bash
   python start.py
   ```

4. **Test the API**:
   ```bash
   curl -H "Authorization: Bearer lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE" http://localhost:8080/health
   ```

## 🔗 Integration

This service is integrated with the Lab-Endoc backend system:

- **Backend URL**: Uses Leapcell deployment URL
- **Authentication**: Bearer token system
- **Job Tracking**: Database-stored job status
- **File Processing**: Background async processing

## 📊 Performance

- **Response Time**: 30-60 seconds for typical audio files
- **File Size Limit**: 10MB per file
- **Supported Formats**: MP3, WAV, M4A, FLAC, OGG, WEBM, MP4
- **Languages**: Auto-detection with 99+ language support

## 🔐 Security

- **Authentication**: Bearer token required for all endpoints
- **File Validation**: Strict file type and size validation
- **Error Handling**: Comprehensive error logging and handling
- **Rate Limiting**: Built-in request throttling

## 📝 License

This project is part of the Lab-Endoc medical assessment platform. 