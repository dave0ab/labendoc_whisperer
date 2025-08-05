from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from transcriber import transcribe_audio
import uuid
import shutil
import os
import secrets
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Whisper Audio Transcription API", description="AI-powered audio transcription using OpenAI Whisper")

# Authentication configuration
API_TOKEN = os.getenv("API_TOKEN", "lSaWtIgjLeWUWBA%FinQI0RgVFiZJtLE")
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "api.testing.labendoc.com",
    "transcribe.testing.labendoc.com"
]

# Security middleware
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the API token"""
    print(f"🔐 Authentication attempt with token: {credentials.credentials[:10]}...")
    print(f"🔐 Expected token: {API_TOKEN[:10]}...")
    print(f"🔐 Token match: {credentials.credentials == API_TOKEN}")
    
    if credentials.credentials != API_TOKEN:
        print(f"❌ Authentication failed: Invalid token")
        print(f"❌ Received: {credentials.credentials}")
        print(f"❌ Expected: {API_TOKEN}")
        raise HTTPException(
            status_code=401,
            detail="Invalid API token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f"✅ Authentication successful")
    return credentials.credentials

def verify_host(request: Request):
    """Verify the request is from allowed hosts"""
    client_host = request.client.host
    print(f"🌐 Host verification: {client_host}")
    
    # For development, allow all localhost connections
    if client_host.startswith('127.') or client_host == 'localhost' or client_host in ALLOWED_HOSTS:
        print(f"✅ Host allowed: {client_host}")
        return client_host
    else:
        print(f"❌ Host not allowed: {client_host}")
        raise HTTPException(
            status_code=403,
            detail="Access denied: Host not allowed"
        )

# Enable CORS for web interface with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "https://transcribe.testing.labendoc.com",
        "https://api.testing.labendoc.com",
        "https://app.testing.labendoc.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check(
    request: Request, 
    token: str = Depends(verify_token)
):
    """Health check endpoint for Docker"""
    return {"status": "healthy", "service": "transcribe"}

@app.get("/", response_class=HTMLResponse)
async def get_web_interface():
    """Serve the web interface for testing the API"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Web interface not found. Please ensure index.html exists.</h1>", status_code=404)

@app.post("/transcribe")
async def transcribe(
    request: Request,
    file: UploadFile = File(...), 
    lang: str = "auto", 
    enhance_accuracy: bool = True,
    use_openai: bool = False,
    enhancement_type: str = "professional",
    enhance_audio: bool = True,
    audio_enhancement_level: str = "medium",
    auto_translate_to_english: bool = False,
    token: str = Depends(verify_token)
):
    """
    Transcribe an audio file using Whisper AI with audio enhancement and OpenAI features
    
    - **file**: Audio file to transcribe (supports mp3, wav, m4a, flac, etc.)
    - **lang**: Language hint for better transcription accuracy (default: auto)
    - **enhance_accuracy**: Apply post-processing improvements (default: true)
    - **use_openai**: Use OpenAI GPT-4 for maximum quality enhancement (requires API key)
    - **enhancement_type**: Type of OpenAI enhancement (professional, medical, business, legal)
    - **enhance_audio**: Apply audio preprocessing for better quality (default: true)
    - **audio_enhancement_level**: Audio enhancement level (light, medium, aggressive)
    - **auto_translate_to_english**: Automatically translate any language to English (requires OpenAI)
    """
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    print(f"🎵 Processing audio file: {temp_filename}")
    print(f"   📁 Original filename: {file.filename}")
    print(f"   📏 File size: {file.size} bytes")
    print(f"   🎯 Content type: {file.content_type}")
    
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print(f"   💾 Temporary file created: {temp_filename}")

    try:
        # OPTIMAL SETTINGS HARDCODED - No user configuration needed
        lang = "auto"
        enhance_accuracy = True
        use_openai = True
        enhancement_type = "professional"
        enhance_audio = True
        audio_enhancement_level = "aggressive"
        auto_translate_to_english = True
            
        print(f"🚀 Using optimal hardcoded settings:")
        print(f"   🔍 Language detection: Auto")
        print(f"   ✨ Accuracy enhancement: Enabled")
        print(f"   🤖 OpenAI GPT-4: Enabled")
        print(f"   🎯 Enhancement type: Professional")
        print(f"   🎵 Audio enhancement: Aggressive")
        print(f"   🌍 Auto-translate to English: Enabled")
            
        result = transcribe_audio(
            temp_filename, 
            lang_hint=lang, 
            enhance_accuracy=enhance_accuracy,
            use_openai=use_openai,
            enhancement_type=enhancement_type,
            enhance_audio=enhance_audio,
            audio_enhancement_level=audio_enhancement_level,
            auto_translate_to_english=auto_translate_to_english
        )
        
        # Check if transcription failed
        if "error" in result or "success" in result and not result.get("success", True):
            error_msg = result.get("error", "Transcription failed")
            print(f"   ❌ Transcription failed: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {error_msg}"
            )
        
        # Prepare response with comprehensive information
        response = {
            "transcript": result.get("text", ""),
            "original_transcript": result.get("original_text", result.get("text", "")),
            "detected_language": result.get("detected_language", "unknown"),
            "enhanced": enhance_accuracy,
            "openai_enhanced": use_openai,
            "enhancement_type": result.get("enhancement_type", "dataset"),
            "enhancement_info": result.get("enhancement_info", ""),
            "audio_enhancement": result.get("audio_enhancement", {}),
            "translation_info": result.get("translation_info", "No translation performed")
        }
        
        # Add English translation if available
        if "english_translation" in result:
            response["english_translation"] = result["english_translation"]
            
        # Add original language text if translation was performed
        if "original_language_text" in result:
            response["original_language_text"] = result["original_language_text"]
            
        print(f"   ✅ Transcription completed successfully")
        return response
    finally:
        print(f"   🗑️ Cleaning up temporary file: {temp_filename}")
        os.remove(temp_filename)