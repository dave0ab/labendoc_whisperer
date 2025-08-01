#!/usr/bin/env python3
"""
Script to upgrade Whisper model for better accuracy
"""
import os
import sys

def upgrade_model(new_model="small"):
    """
    Upgrade the Whisper model in transcriber.py
    
    Args:
        new_model (str): Model to upgrade to (small, medium, large)
    """
    
    valid_models = ["tiny", "base", "small", "medium", "large"]
    
    if new_model not in valid_models:
        print(f"❌ Invalid model: {new_model}")
        print(f"Valid options: {', '.join(valid_models)}")
        return False
    
    transcriber_file = "transcriber.py"
    
    if not os.path.exists(transcriber_file):
        print(f"❌ File not found: {transcriber_file}")
        return False
    
    # Read current file
    with open(transcriber_file, 'r') as f:
        content = f.read()
    
    # Find and replace model line
    lines = content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if 'model = whisper.load_model(' in line and '# Load the Whisper model once' in lines[i-1]:
            old_line = line
            # Extract current model
            import re
            match = re.search(r'load_model\("([^"]+)"\)', line)
            current_model = match.group(1) if match else "unknown"
            
            # Update line
            lines[i] = f'model = whisper.load_model("{new_model}")  # Use "small", "medium", or "large" for better accuracy'
            updated = True
            
            print(f"✅ Updated model: {current_model} → {new_model}")
            print(f"   Old: {old_line.strip()}")
            print(f"   New: {lines[i].strip()}")
            break
    
    if not updated:
        print("❌ Could not find model definition to update")
        return False
    
    # Write updated file
    with open(transcriber_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"\n🎯 Model upgraded to '{new_model}'!")
    print("📊 Expected improvements:")
    
    improvements = {
        "tiny": "Faster but less accurate",
        "base": "Good balance of speed and accuracy",
        "small": "Better accuracy, slightly slower",
        "medium": "Much better accuracy, slower",
        "large": "Best accuracy, slowest"
    }
    
    print(f"   {improvements.get(new_model, 'Model information not available')}")
    
    print("\n⚠️  Important:")
    print("• Restart your server to load the new model")
    print("• First transcription will be slower (model download)")
    print("• Larger models require more memory")
    
    return True

def main():
    """Main function"""
    
    print("🔧 Whisper Model Upgrade Tool")
    print("=" * 30)
    
    if len(sys.argv) < 2:
        print("📖 Usage:")
        print(f"python {sys.argv[0]} <model_name>")
        print("\nAvailable models:")
        print("• tiny   - Fastest, least accurate")
        print("• base   - Current default")
        print("• small  - Better accuracy (recommended)")
        print("• medium - Much better accuracy")
        print("• large  - Best accuracy")
        print("\nExample:")
        print(f"python {sys.argv[0]} small")
        return
    
    new_model = sys.argv[1].lower()
    
    print(f"🎯 Upgrading to model: {new_model}")
    print("=" * 30)
    
    if upgrade_model(new_model):
        print("\n🚀 Next steps:")
        print("1. Restart your FastAPI server")
        print("2. Test with an audio file")
        print("3. Compare the improved accuracy!")
    else:
        print("\n💥 Upgrade failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()