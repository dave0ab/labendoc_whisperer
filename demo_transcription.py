#!/usr/bin/env python3
"""
Demo script for testing the Whisper API transcription service
"""
import requests
import json
import os
import sys

def test_transcription(audio_file_path, language="auto"):
    """
    Test the transcription API with an audio file
    
    Args:
        audio_file_path (str): Path to the audio file
        language (str): Language hint for transcription
    """
    
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        return False
    
    url = "http://127.0.0.1:8000/transcribe"
    
    try:
        print(f"🎙️  Transcribing: {audio_file_path}")
        print(f"📝 Language: {language}")
        print("⏳ Processing...")
        
        with open(audio_file_path, 'rb') as audio_file:
            files = {"file": audio_file}
            params = {"lang": language}
            
            response = requests.post(url, files=files, params=params)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transcription successful!")
            if result.get("detected_language"):
                print(f"🔍 Detected Language: {result['detected_language']}")
            print("📄 Result:")
            print("-" * 50)
            print(result["transcript"])
            print("-" * 50)
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_server():
    """Check if the server is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running on http://127.0.0.1:8000")
            return True
    except:
        pass
    
    print("❌ Server is not running. Start it with:")
    print("source whisper_env/bin/activate && uvicorn main:app --host 127.0.0.1 --port 8000 --reload")
    return False

def main():
    """Main demo function"""
    print("🎤 FastAPI Whisper Transcription Demo")
    print("=" * 40)
    
    # Check if server is running
    if not check_server():
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n📖 Usage:")
        print(f"python {sys.argv[0]} <audio_file> [language]")
        print("\nExamples:")
        print(f"python {sys.argv[0]} recording.mp3")
        print(f"python {sys.argv[0]} audio.wav auto")
        print(f"python {sys.argv[0]} speech.m4a en")
        print("\nSupported formats: mp3, wav, m4a, flac, ogg, webm, mp4")
        print("Supported languages: auto (recommended), en, es, fr, de, pt, it, and many more")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    # Run transcription
    success = test_transcription(audio_file, language)
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n💥 Demo failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()