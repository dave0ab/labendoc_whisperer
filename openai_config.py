#!/usr/bin/env python3
"""
OpenAI configuration and setup
"""
import os
from pathlib import Path

def setup_openai_key():
    """Interactive setup for OpenAI API key"""
    
    print("🔑 OpenAI API Key Setup")
    print("=" * 30)
    
    print("To enable advanced OpenAI features, you need an API key from:")
    print("🌐 https://platform.openai.com/api-keys")
    print()
    
    # Check if key already exists
    env_file = Path(".env")
    current_key = os.getenv('OPENAI_API_KEY')
    
    if current_key:
        print(f"✅ Found existing API key: {current_key[:10]}...{current_key[-4:]}")
        replace = input("Replace existing key? (y/N): ").lower().strip()
        if replace != 'y':
            print("Keeping existing key.")
            return current_key
    
    # Get new key
    print("\n📝 Enter your OpenAI API key:")
    print("(starts with 'sk-')")
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return None
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: API key should start with 'sk-'")
        confirm = input("Continue anyway? (y/N): ").lower().strip()
        if confirm != 'y':
            return None
    
    # Save to .env file
    try:
        # Read existing .env content
        env_content = ""
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        # Remove any existing OPENAI_API_KEY line
        lines = [line for line in env_content.split('\n') 
                if not line.startswith('OPENAI_API_KEY=')]
        
        # Add new key
        lines.append(f"OPENAI_API_KEY={api_key}")
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ API key saved to .env file")
        
        # Set environment variable for current session
        os.environ['OPENAI_API_KEY'] = api_key
        
        return api_key
        
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return None

def test_openai_connection(api_key: str = None):
    """Test OpenAI API connection"""
    
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()
        
        # Use modern OpenAI client
        client = openai.OpenAI(api_key=api_key)
        model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')
        
        print(f"🧪 Testing OpenAI connection with {model}...")
        
        # Simple test call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        if "test successful" in result.lower():
            print(f"✅ OpenAI API connection successful with {model}!")
            return True
        else:
            print(f"⚠️  Unexpected response: {result}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def show_openai_features():
    """Show what OpenAI integration enables"""
    
    print("🚀 OpenAI Integration Features")
    print("=" * 35)
    
    features = [
        "🎯 Advanced Text Enhancement",
        "   • GPT-4 powered grammar and spelling correction",
        "   • Context-aware improvements", 
        "   • Professional language polishing",
        "",
        "🏥 Domain-Specific Enhancement", 
        "   • Medical transcription optimization",
        "   • Business meeting formatting",
        "   • Legal document processing",
        "",
        "📋 Smart Summarization",
        "   • Bullet point summaries",
        "   • Executive summaries", 
        "   • Action item extraction",
        "",
        "🌍 Professional Translation",
        "   • High-quality language translation",
        "   • Context-aware translations",
        "   • Professional tone preservation",
        "",
        "📄 Document Formatting", 
        "   • Meeting notes formatting",
        "   • Report structure creation",
        "   • Professional document templates",
        "",
        "🔍 Quality Analysis",
        "   • Transcription confidence scoring",
        "   • Improvement suggestions",
        "   • Quality metrics"
    ]
    
    for feature in features:
        print(feature)
    
    print(f"\n💰 Cost: ~$0.01-0.03 per transcription (very affordable)")
    print(f"🎯 Result: Professional-grade transcription quality")

def get_cost_estimate():
    """Show cost estimates for OpenAI usage"""
    
    print("💰 OpenAI Cost Estimates")
    print("=" * 25)
    
    print("GPT-4 Pricing (as of 2024):")
    print("• Input: $0.03 per 1K tokens")
    print("• Output: $0.06 per 1K tokens")
    print()
    
    print("Typical transcription enhancement:")
    print("• Input tokens: ~200-500 (your transcription)")
    print("• Output tokens: ~200-600 (enhanced version)")
    print("• Cost per enhancement: $0.01 - $0.04")
    print()
    
    print("Monthly estimates:")
    print("• 100 transcriptions: $1 - $4")
    print("• 500 transcriptions: $5 - $20") 
    print("• 1000 transcriptions: $10 - $40")
    print()
    
    print("💡 Very affordable for professional-grade quality!")

if __name__ == "__main__":
    show_openai_features()
    print()
    get_cost_estimate()
    print()
    
    setup_key = input("Setup OpenAI API key now? (y/N): ").lower().strip()
    if setup_key == 'y':
        api_key = setup_openai_key()
        if api_key:
            test_openai_connection(api_key)