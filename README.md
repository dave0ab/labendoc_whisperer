# Labendoc Whisperer 🎙️

A powerful HTTP API for transcribing audio files using OpenAI's Whisper model, specifically optimized for medical and professional transcription with enhanced accuracy features.

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

- 🎯 **High Accuracy Transcription**: Powered by OpenAI's Whisper model
- 🏥 **Medical Term Optimization**: Enhanced accuracy for medical terminology
- 🌍 **Multi-language Support**: 90+ languages with automatic detection
- 🔧 **Post-processing Enhancement**: Automatic punctuation, capitalization, and term correction
- 📊 **Web Interface**: User-friendly web UI for easy transcription
- ⚡ **Fast Processing**: Optimized for quick turnaround
- 🔒 **Secure**: Local processing, no data sent to external servers

## 🚀 Quick Start

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio processing)
- At least 2GB RAM (4GB+ recommended)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html)

### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd labendoc_whisperer

# Create and activate virtual environment
python3 -m venv whisper_env
source whisper_env/bin/activate  # On Windows: whisper_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Server
```bash
# Activate virtual environment and start server
source whisper_env/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at: **http://localhost:8000** or **http://0.0.0.0:8000**

## 📖 API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🎯 API Usage

### Transcribe Audio File

**Endpoint**: `POST /transcribe`

**Parameters**:
- `file` (required): Audio file (supports .mp3, .wav, .m4a, .flac, etc.)
- `lang` (optional): Language hint (default: "auto" for automatic detection)
  - "auto" for automatic language detection (recommended)
  - "en" for English
  - "es" for Spanish
  - "fr" for French
  - etc.
- `enhance_accuracy` (optional): Apply post-processing improvements (default: true)

### Examples

#### Using curl
```bash
# Auto-detect language (recommended)
curl -X POST "http://localhost:8000/transcribe?lang=auto" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.mp3"

# Or specify a language
curl -X POST "http://localhost:8000/transcribe?lang=es" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.mp3"
```

#### Using Python requests
```python
import requests

url = "http://localhost:8000/transcribe"
files = {"file": open("recording.mp3", "rb")}
params = {"lang": "auto"}  # Auto-detect language

response = requests.post(url, files=files, params=params)
result = response.json()

print(f"Detected language: {result['detected_language']}")
print(f"Transcript: {result['transcript']}")
```

#### Using JavaScript/fetch
```javascript
const formData = new FormData();
formData.append('file', audioFile);

fetch('http://localhost:8000/transcribe?lang=auto', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Detected language:', data.detected_language);
  console.log('Transcript:', data.transcript);
});
```

### Response Format
```json
{
  "transcript": "El paciente presenta síntomas de fiebre y dolor de cabeza...",
  "original_transcript": "el paciente presenta sintomas de fiebre y dolor de cabeza",
  "detected_language": "es",
  "enhanced": true
}
```

## 🔧 Configuration

### Supported Audio Formats
- MP3, WAV, M4A, FLAC, OGG, WEBM, MP4, and more
- Files are automatically converted to WAV format for processing

### 🎯 Accuracy Enhancement Features
- **Auto Language Detection**: Automatically detects English/Spanish and other languages
- **Text Post-Processing**: Fixes punctuation, capitalization, and medical terminology
- **Language-Specific Corrections**: Handles accents, contractions, and professional terms
- **Before/After Comparison**: See improvements in the web interface

### Whisper Model Options
| Model  | Accuracy | Speed | Size | Use Case |
|--------|----------|-------|------|----------|
| tiny   | ⭐⭐      | ⚡⚡⚡   | 39MB | Testing |
| base   | ⭐⭐⭐     | ⚡⚡    | 74MB | Default |
| small  | ⭐⭐⭐⭐    | ⚡     | 244MB | **Recommended** |
| medium | ⭐⭐⭐⭐⭐   | ⚡     | 769MB | Professional |
| large  | ⭐⭐⭐⭐⭐⭐  | 🐌     | 1550MB | Best Quality |

#### Upgrade Model for Better Accuracy:
```bash
python upgrade_model.py small  # or medium, large
```

### Language Support
The API supports all languages that Whisper supports, including:
- English ("en") - with medical term corrections
- Spanish ("es") - with accent and medical term corrections  
- French ("fr")
- German ("de")
- Portuguese ("pt")
- And 90+ more languages...

## 🛠️ Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **OpenAI Whisper**: Speech-to-text model
- **pydub**: Audio file processing
- **ffmpeg**: Audio format conversion (system dependency)

## 📁 Project Structure

```
labendoc_whisperer/
├── main.py                 # FastAPI application entry point
├── transcriber.py          # Core transcription functionality
├── enhanced_transcriber.py # Enhanced transcription with post-processing
├── audio_enhancer.py       # Audio quality enhancement
├── openai_enhancer.py      # OpenAI-based enhancements
├── accuracy_enhancer.py    # Accuracy improvement utilities
├── custom_vocabulary.py    # Custom medical vocabulary
├── requirements.txt        # Python dependencies
├── index.html             # Web interface
├── README.md              # This file
├── *.md                   # Various documentation guides
└── test_*.py              # Test and demo scripts
```

## 🧪 Testing

### Demo Scripts
```bash
# Test accuracy enhancements
python test_accuracy_demo.py

# Test custom system prompts
python test_custom_system.py

# Test auto-detection features
python test_auto_detection.py

# Test server functionality
python test_server.py

# Upgrade to better model
python upgrade_model.py small
```

### Tips for Better Accuracy
- Use clear, high-quality audio (16kHz+ sample rate recommended)
- Minimize background noise and echo
- Keep enhancement mode enabled for best results
- Consider upgrading to 'small' or 'medium' model for professional use
- Use appropriate language hints when known

## 🔧 Troubleshooting

### Common Issues

**FFmpeg not found:**
```bash
# Install FFmpeg (see Installation section above)
sudo apt install ffmpeg  # Ubuntu/Debian
```

**Out of memory errors:**
- Use smaller Whisper model: `python upgrade_model.py tiny`
- Close other applications to free RAM
- Process shorter audio files

**Slow transcription:**
- First run downloads the model (~140MB)
- Consider using GPU if available
- Use smaller model for faster processing

**Audio format not supported:**
- Ensure FFmpeg is properly installed
- Convert audio to common formats (MP3, WAV, M4A)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 Notes

- First transcription may take longer as the Whisper model downloads (~140MB)
- Audio files are temporarily stored and automatically cleaned up
- The service runs on CPU by default (GPU support available with PyTorch CUDA)
- Enhanced mode adds ~10-20% processing time but significantly improves quality
- All processing is done locally - no data is sent to external servers