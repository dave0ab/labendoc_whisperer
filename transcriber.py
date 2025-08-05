import whisper
import os
import uuid
import subprocess
import shutil

# Import centralized FFmpeg utilities
from ffmpeg_utils import setup_ffmpeg_environment, configure_pydub_ffmpeg

# Set up FFmpeg environment
setup_ffmpeg_environment()

from pydub import AudioSegment

# Configure pydub to use the correct FFmpeg paths
configure_pydub_ffmpeg()

try:
    from accuracy_enhancer import enhance_transcription_accuracy
    from advanced_accuracy import enhance_transcription_with_datasets
except ImportError:
    print("⚠️ Accuracy enhancers not found - using basic transcription")
    
from openai_enhancer import enhance_with_openai, OpenAIEnhancer

try:
    from audio_enhancer import enhance_audio_for_transcription
    AUDIO_ENHANCEMENT_AVAILABLE = True
except ImportError:
    print("⚠️ Audio enhancer not available - skipping audio enhancement")
    AUDIO_ENHANCEMENT_AVAILABLE = False
    
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up writable cache directory for Whisper models
import os
import tempfile

# Create a writable cache directory
cache_dir = os.path.join(tempfile.gettempdir(), "whisper_cache")
os.makedirs(cache_dir, exist_ok=True)

# Set environment variable for Whisper cache
os.environ["XDG_CACHE_HOME"] = cache_dir
os.environ["HF_HOME"] = cache_dir

# Load the Whisper model once with custom cache directory
try:
    model = whisper.load_model("small", download_root=cache_dir)  # Use "small", "medium", or "large" for better accuracy
    print(f"✅ Whisper model loaded successfully from {cache_dir}")
except Exception as e:
    print(f"⚠️ Warning: Could not load Whisper model: {e}")
    print("📝 Will attempt to load model on first use...")
    model = None

def transcribe_audio(file_path: str, lang_hint: str = "es", enhance_accuracy: bool = True, 
                    use_openai: bool = False, enhancement_type: str = "professional",
                    enhance_audio: bool = True, audio_enhancement_level: str = "medium",
                    auto_translate_to_english: bool = False) -> dict:
    """
    Enhanced transcription with audio preprocessing and automatic English translation
    
    Args:
        file_path: Path to audio file
        lang_hint: Language hint for Whisper ("auto" for auto-detection)
        enhance_accuracy: Whether to enhance transcription accuracy 
        use_openai: Whether to use OpenAI for text enhancement
        enhancement_type: Type of OpenAI enhancement (professional, medical, business, legal)
        enhance_audio: Whether to enhance audio quality before transcription
        audio_enhancement_level: Audio enhancement level (light, medium, aggressive)
        auto_translate_to_english: Whether to automatically translate to English
        
    Returns:
        Dict with transcription results and metadata
    """
    
    print(f"🚀 Starting enhanced transcription...")
    print(f"📁 File: {file_path}")
    print(f"🌍 Language hint: {lang_hint}")
    print(f"🎵 Audio enhancement: {enhance_audio} ({audio_enhancement_level})")
    print(f"🤖 Text enhancement: {use_openai} ({enhancement_type})")
    print(f"🌐 Auto-translate to English: {auto_translate_to_english}")
    
    # STEP 1: Enhance audio quality for better transcription
    if enhance_audio and AUDIO_ENHANCEMENT_AVAILABLE:
        print(f"🎵 Enhancing audio quality (level: {audio_enhancement_level})...")
        try:
            enhanced_file_path, audio_metrics = enhance_audio_for_transcription(file_path, audio_enhancement_level)
            
            # Convert enhanced audio to WAV format
            try:
                audio = AudioSegment.from_file(enhanced_file_path)
                wav_path = f"enhanced_{uuid.uuid4()}.wav"
                audio.export(wav_path, format="wav")
                
                # Clean up enhanced file if it's different from original
                if enhanced_file_path != file_path and os.path.exists(enhanced_file_path):
                    os.remove(enhanced_file_path)
            except Exception as e:
                print(f"⚠️ Audio enhancement failed: {e}")
                print("📝 Proceeding with original audio...")
                # Fallback to original audio
                try:
                    audio = AudioSegment.from_file(file_path)
                    wav_path = f"{uuid.uuid4()}.wav"
                    audio.export(wav_path, format="wav")
                    audio_metrics = {"enhancement": "failed", "error": str(e)}
                except Exception as audio_error:
                    print(f"❌ Critical error: Cannot process audio file: {audio_error}")
                    return {
                        "error": f"Audio processing failed: {audio_error}",
                        "success": False,
                        "transcription": "",
                        "language": "unknown",
                        "enhancement_info": "Audio processing failed",
                        "audio_metrics": {"enhancement": "failed", "error": str(audio_error)}
                    }
        except Exception as e:
            print(f"⚠️ Audio enhancement failed: {e}")
            print("📝 Using original audio...")
            # Fallback to original audio
            try:
                audio = AudioSegment.from_file(file_path)
                wav_path = f"{uuid.uuid4()}.wav"
                audio.export(wav_path, format="wav")
                audio_metrics = {"enhancement": "failed", "error": str(e)}
            except Exception as audio_error:
                print(f"❌ Critical error: Cannot process audio file: {audio_error}")
                return {
                    "error": f"Audio processing failed: {audio_error}",
                    "success": False,
                    "transcription": "",
                    "language": "unknown",
                    "enhancement_info": "Audio processing failed",
                    "audio_metrics": {"enhancement": "failed", "error": str(audio_error)}
                }
    else:
        # Convert original audio to WAV format
        try:
            audio = AudioSegment.from_file(file_path)
            wav_path = f"{uuid.uuid4()}.wav"
            audio.export(wav_path, format="wav")
            audio_metrics = {"enhancement": "disabled" if not enhance_audio else "not_available"}
        except Exception as e:
            print(f"❌ Critical error: Cannot process audio file: {e}")
            return {
                "error": f"Audio processing failed: {e}",
                "success": False,
                "transcription": "",
                "language": "unknown",
                "enhancement_info": "Audio processing failed",
                "audio_metrics": {"enhancement": "failed", "error": str(e)}
            }

    # STEP 2: Transcribe with Whisper
    print("🎤 Transcribing with Whisper...")
    
    # Load model if not already loaded
    global model
    if model is None:
        try:
            model = whisper.load_model("small", download_root=cache_dir)
            print(f"✅ Whisper model loaded successfully from {cache_dir}")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            return {
                "error": f"Failed to load Whisper model: {e}",
                "success": False,
                "transcription": "",
                "language": "unknown"
            }
    
    # Auto-detect language if lang_hint is "auto" or None
    if lang_hint == "auto" or lang_hint is None:
        result = model.transcribe(
            wav_path,
            temperature=0,        # More consistent results
            word_timestamps=True, # Better accuracy
            verbose=False
        )
    else:
        result = model.transcribe(
            wav_path, 
            language=lang_hint,
            temperature=0,
            word_timestamps=True,
            verbose=False
        )

    # Clean up temporary audio file
    if os.path.exists(wav_path):
        os.remove(wav_path)
    
    # Get basic transcription
    original_text = result["text"]
    detected_language = result.get("language", "unknown")
    
    print(f"✅ Transcription completed!")
    print(f"🌍 Detected language: {detected_language}")
    print(f"📝 Original text: {original_text[:100]}{'...' if len(original_text) > 100 else ''}")
    
    # STEP 3: Enhance accuracy if requested
    if enhance_accuracy and original_text.strip():
        if use_openai:
            print("🤖 ✅ OpenAI GPT-4 Enhancement ACTIVATED!")
            print(f"🔧 Using model: gpt-4-turbo")
            print(f"🎯 Enhancement type: {enhancement_type}")
            # Use OpenAI GPT-4 for maximum accuracy enhancement
            openai_result = enhance_with_openai(original_text, detected_language, enhancement_type)
            final_text = openai_result.get("enhanced", original_text)
            enhancement_info = openai_result.get("improvements", "OpenAI enhancement applied")
            print(f"✅ OpenAI enhancement completed!")
            print(f"📈 Improvements: {enhancement_info}")
        else:
            print("📚 Using dataset-based enhancement (OpenAI disabled)")
            # Use advanced dataset-based enhancement
            enhanced = enhance_transcription_with_datasets(original_text, detected_language)
            final_text = enhanced["corrected"]
            enhancement_info = "Dataset-based enhancement applied"
    else:
        final_text = original_text
        enhancement_info = "No enhancement applied"

    # STEP 4: Automatic English translation if requested
    english_translation = None
    translation_info = "No translation performed"
    
    if auto_translate_to_english:
        print(f"🌍 ✅ AUTO-TRANSLATION TO ENGLISH ACTIVATED!")
        if detected_language == "en":
            english_translation = final_text
            translation_info = "Already in English - no translation needed"
            print("✅ Text is already in English - no translation needed!")
        else:
            print(f"🔄 TRANSLATING from {detected_language} to English...")
            print(f"📝 Original text: {final_text[:100]}{'...' if len(final_text) > 100 else ''}")
            try:
                openai_enhancer = OpenAIEnhancer()
                if openai_enhancer.enabled:
                    print(f"🤖 Using OpenAI {openai_enhancer.model} for translation...")
                    translation_result = openai_enhancer.translate_transcription(final_text, "English")
                    english_translation = translation_result.get("translation", final_text)
                    model_used = translation_result.get("model_used", "OpenAI")
                    translation_info = f"Translated from {detected_language} to English using {model_used}"
                    print(f"🎉 ✅ TRANSLATION COMPLETED with {model_used}!")
                    print(f"🌐 English result: {english_translation[:100]}{'...' if len(english_translation) > 100 else ''}")
                else:
                    translation_info = "Translation requested but OpenAI not available"
                    english_translation = final_text
                    print("❌ OpenAI not available - translation skipped")
            except Exception as e:
                print(f"❌ Translation failed: {e}")
                translation_info = f"Translation failed: {str(e)}"
                english_translation = final_text
    else:
        print("🌍 Auto-translation to English: DISABLED")
    
    # STEP 5: Prepare comprehensive results
    result = {
        "text": final_text,
        "original_text": original_text,
        "detected_language": detected_language,
        "enhancement_type": enhancement_type if use_openai else "dataset",
        "enhancement_info": enhancement_info,
        "audio_enhancement": audio_metrics,
        "translation_info": translation_info
    }
    
    # Add English translation and make it primary output if auto-translate is enabled
    if auto_translate_to_english:
        result["english_translation"] = english_translation
        result["original_language_text"] = final_text
        # Make English the primary output text
        result["text"] = english_translation
        print(f"🎯 Primary output set to English translation")
    elif english_translation and english_translation != final_text:
        result["english_translation"] = english_translation
    
    print("🎉 Enhanced transcription completed!")
    return result