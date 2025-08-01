# FastAPI Whisper Transcription Service 🎙️

A powerful HTTP API for transcribing audio files using OpenAI's Whisper model.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create and activate virtual environment
python3 -m venv whisper_env
source whisper_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Server
```bash
# From the whisper_api directory
source whisper_env/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The server will be available at: **http://127.0.0.1:8000**

## 📖 API Documentation

- **Interactive Docs**: http://127.0.0.1:8000/docs
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

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
curl -X POST "http://127.0.0.1:8000/transcribe?lang=auto" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.mp3"

# Or specify a language
curl -X POST "http://127.0.0.1:8000/transcribe?lang=es" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.mp3"
```

#### Using Python requests
```python
import requests

url = "http://127.0.0.1:8000/transcribe"
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

fetch('http://127.0.0.1:8000/transcribe?lang=auto', {
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

## 🧪 Testing Accuracy Features

### Demo Scripts
```bash
# Test accuracy enhancements
python test_accuracy_demo.py

# Upgrade to better model
python upgrade_model.py small
```

### Tips for Better Accuracy
- Use clear, high-quality audio
- Minimize background noise
- Keep enhancement mode enabled
- Consider upgrading to 'small' or 'medium' model for professional use

## 📝 Notes

- First transcription may take longer as the Whisper model downloads (~140MB)
- Audio files are temporarily stored and automatically cleaned up
- The service runs on CPU by default (GPU support available with PyTorch CUDA)
- Enhanced mode adds ~10-20% processing time but significantly improves quality