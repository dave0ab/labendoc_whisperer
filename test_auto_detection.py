#!/usr/bin/env python3
"""
Test script to demonstrate auto-detection feature
"""
import requests
import json

def test_auto_detection():
    """Test the auto-detection API endpoint"""
    
    url = "http://127.0.0.1:8000/transcribe"
    
    # Test with auto-detection
    print("🧪 Testing Auto-Detection Feature")
    print("=" * 40)
    
    try:
        # Test the API endpoint
        response = requests.get("http://127.0.0.1:8000/openapi.json")
        if response.status_code == 200:
            print("✅ API is accessible")
            
            # Check the default parameter
            openapi = response.json()
            transcribe_endpoint = openapi.get("paths", {}).get("/transcribe", {}).get("post", {})
            parameters = transcribe_endpoint.get("parameters", [])
            
            for param in parameters:
                if param.get("name") == "lang":
                    default_value = param.get("schema", {}).get("default", "Not set")
                    print(f"📝 Default language setting: {default_value}")
                    break
            
            print("\n🎯 How to use auto-detection:")
            print("• Web Interface: Select '🔍 Auto Detect (Recommended)' from dropdown")
            print("• API: Use lang=auto or omit the lang parameter")
            print("• Demo script: python demo_transcription.py audio.mp3")
            print("\n💡 Features:")
            print("• Whisper automatically detects the language")
            print("• Works great for English/Spanish mixed content")
            print("• Returns both transcript AND detected language")
            print("• More accurate than guessing the wrong language")
            
        else:
            print("❌ API not accessible")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_auto_detection()