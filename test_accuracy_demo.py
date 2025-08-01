#!/usr/bin/env python3
"""
Demo script to test accuracy enhancement features
"""
import requests
from accuracy_enhancer import print_model_recommendations, MODEL_ACCURACY_INFO

def test_accuracy_features():
    """Test the accuracy enhancement features"""
    
    print("🎯 Whisper Accuracy Enhancement Demo")
    print("=" * 50)
    
    # Show model recommendations
    print_model_recommendations()
    
    print("\n🔧 Current Setup:")
    print("• Model: base (⭐⭐⭐ accuracy, ⚡⚡ speed)")
    print("• Auto-detection: Enabled")
    print("• Post-processing: Enabled by default")
    
    print("\n✨ Accuracy Enhancement Features:")
    print("=" * 40)
    
    print("1. 🔍 Auto Language Detection")
    print("   • Automatically detects English/Spanish")
    print("   • No need to guess the language")
    print("   • Better accuracy than wrong language hint")
    
    print("\n2. 📝 Text Post-Processing")
    print("   • Fixes common punctuation errors")
    print("   • Corrects medical terminology")
    print("   • Improves capitalization")
    print("   • Handles contractions properly")
    
    print("\n3. 🌍 Language-Specific Improvements")
    print("   • English: Medical terms, contractions")
    print("   • Spanish: Accent corrections, medical terms")
    print("   • Universal: Number formatting, time/date")
    
    print("\n4. 🎚️ Model Size Options")
    print("   • Current: 'base' - Good balance")
    print("   • Better: 'small' - More accurate")
    print("   • Best: 'medium' or 'large' - Highest accuracy")
    
    print("\n🧪 How to Test:")
    print("=" * 20)
    print("1. Visit: http://127.0.0.1:8000")
    print("2. Upload an audio file")
    print("3. Keep 'Enhanced' mode selected")
    print("4. Compare before/after results!")
    
    print("\n💡 Tips for Better Accuracy:")
    print("=" * 30)
    print("• Use clear, high-quality audio")
    print("• Minimize background noise")
    print("• Speak clearly and at normal pace")
    print("• Use enhancement mode for medical/professional terms")
    
    # Test API availability
    try:
        response = requests.get("http://127.0.0.1:8000/openapi.json", timeout=5)
        if response.status_code == 200:
            print("\n✅ API is running and ready for testing!")
        else:
            print(f"\n⚠️  API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("\n❌ API not accessible. Start the server first:")
        print("uvicorn main:app --host 127.0.0.1 --port 8000 --reload")
    except Exception as e:
        print(f"\n❌ Error checking API: {e}")

def show_upgrade_guide():
    """Show how to upgrade to better models"""
    
    print("\n📈 Upgrade Guide for Better Accuracy")
    print("=" * 40)
    
    print("To use a more accurate model, edit transcriber.py:")
    print("Change: model = whisper.load_model('base')")
    print("To:     model = whisper.load_model('small')  # or 'medium' or 'large'")
    
    print("\n⚖️  Trade-offs:")
    for model, info in MODEL_ACCURACY_INFO.items():
        print(f"• {model:8}: {info['accuracy']} accuracy, {info['speed']} speed, {info['size']}")
    
    print("\n🏥 For Medical/Professional Use:")
    print("• Recommended: 'medium' model")
    print("• Best results: 'large' model")
    print("• Keep enhancement enabled")

if __name__ == "__main__":
    test_accuracy_features()
    show_upgrade_guide()