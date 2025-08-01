from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from transcriber import transcribe_audio
import uuid
import shutil
import os

app = FastAPI(title="Whisper Audio Transcription API", description="AI-powered audio transcription using OpenAI Whisper")

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    file: UploadFile = File(...), 
    lang: str = "auto", 
    enhance_accuracy: bool = True,
    use_openai: bool = False,
    enhancement_type: str = "professional",
    enhance_audio: bool = True,
    audio_enhancement_level: str = "medium",
    auto_translate_to_english: bool = False
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
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

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
        # Prepare response with comprehensive information
        response = {
            "transcript": result["text"],
            "original_transcript": result.get("original_text", result["text"]),
            "detected_language": result["detected_language"],
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
            
        return response
    finally:
        os.remove(temp_filename)