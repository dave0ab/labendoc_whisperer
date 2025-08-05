#!/usr/bin/env python3
"""
Startup script for Lab-Endoc Transcription Service
Handles environment setup and starts the FastAPI application
"""

import os
import sys
import tempfile
import uvicorn

def setup_environment():
    """Set up the environment for the transcription service"""
    print("🔧 Setting up environment...")
    
    # Create writable directories
    temp_dir = tempfile.gettempdir()
    cache_dir = os.path.join(temp_dir, "whisper_cache")
    uploads_dir = os.path.join(temp_dir, "uploads")
    logs_dir = os.path.join(temp_dir, "logs")
    
    # Create directories
    for directory in [cache_dir, uploads_dir, logs_dir]:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Set environment variables
    os.environ["XDG_CACHE_HOME"] = cache_dir
    os.environ["HF_HOME"] = cache_dir
    os.environ["UPLOAD_DIR"] = uploads_dir
    os.environ["LOG_DIR"] = logs_dir
    
    print(f"✅ Environment setup complete")
    print(f"   Cache directory: {cache_dir}")
    print(f"   Uploads directory: {uploads_dir}")
    print(f"   Logs directory: {logs_dir}")

def main():
    """Main startup function"""
    print("🚀 Starting Lab-Endoc Transcription Service...")
    
    # Setup environment
    setup_environment()
    
    # Import and start the FastAPI app
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Start the server
        print("🌐 Starting server on 0.0.0.0:8080...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8080,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 