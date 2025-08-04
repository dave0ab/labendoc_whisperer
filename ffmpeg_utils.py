#!/usr/bin/env python3
"""
Centralized FFmpeg utilities for dynamic path detection
"""
import os
import shutil
import subprocess
from typing import Tuple, Optional

def find_ffmpeg_binaries() -> Tuple[Optional[str], Optional[str]]:
    """
    Find FFmpeg and FFprobe binaries in common locations
    
    Returns:
        Tuple of (ffmpeg_path, ffprobe_path) or (None, None) if not found
    """
    possible_paths = [
        # Standard system paths
        "/usr/bin/ffmpeg",
        "/usr/local/bin/ffmpeg", 
        "/opt/homebrew/bin/ffmpeg",
        "/usr/bin/ffprobe",
        "/usr/local/bin/ffprobe",
        "/opt/homebrew/bin/ffprobe",
        # Common alternative paths
        "/usr/bin/avconv",
        "/usr/local/bin/avconv",
        # Windows paths (if running on Windows)
        "C:\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\ffmpeg\\bin\\ffprobe.exe",
    ]
    
    ffmpeg_path = None
    ffprobe_path = None
    
    # First try to find ffmpeg and ffprobe in PATH
    try:
        ffmpeg_path = shutil.which("ffmpeg")
        ffprobe_path = shutil.which("ffprobe")
        if ffmpeg_path and ffprobe_path:
            print(f"✅ Found FFmpeg binaries in PATH:")
            print(f"   ffmpeg: {ffmpeg_path}")
            print(f"   ffprobe: {ffprobe_path}")
            return ffmpeg_path, ffprobe_path
    except Exception as e:
        print(f"⚠️ Error checking PATH for FFmpeg: {e}")
    
    # If not in PATH, check common locations
    for path in possible_paths:
        if os.path.exists(path):
            if "ffmpeg" in path and not ffmpeg_path:
                ffmpeg_path = path
            elif "ffprobe" in path and not ffprobe_path:
                ffprobe_path = path
    
    # If we found both, return them
    if ffmpeg_path and ffprobe_path:
        print(f"✅ Found FFmpeg binaries in system paths:")
        print(f"   ffmpeg: {ffmpeg_path}")
        print(f"   ffprobe: {ffprobe_path}")
        return ffmpeg_path, ffprobe_path
    
    # If we only found one, try to find the other in the same directory
    if ffmpeg_path and not ffprobe_path:
        ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe")
        if os.path.exists(ffprobe_path):
            print(f"✅ Found FFprobe in same directory: {ffprobe_path}")
            return ffmpeg_path, ffprobe_path
    
    if ffprobe_path and not ffmpeg_path:
        ffmpeg_path = ffprobe_path.replace("ffprobe", "ffmpeg")
        if os.path.exists(ffmpeg_path):
            print(f"✅ Found FFmpeg in same directory: {ffmpeg_path}")
            return ffmpeg_path, ffprobe_path
    
    # If we still don't have both, try to install or provide instructions
    print("❌ FFmpeg binaries not found!")
    print("📋 Please install FFmpeg using one of these methods:")
    print("   Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
    print("   CentOS/RHEL: sudo yum install ffmpeg")
    print("   macOS: brew install ffmpeg")
    print("   Windows: Download from https://ffmpeg.org/download.html")
    print("   Or ensure ffmpeg and ffprobe are in your system PATH")
    
    return None, None

def setup_ffmpeg_environment() -> bool:
    """
    Set up FFmpeg environment variables for pydub
    
    Returns:
        True if FFmpeg was found and configured, False otherwise
    """
    ffmpeg_path, ffprobe_path = find_ffmpeg_binaries()
    
    if ffmpeg_path and ffprobe_path:
        # Set environment variables for pydub
        os.environ["FFMPEG_BINARY"] = ffmpeg_path
        os.environ["FFPROBE_BINARY"] = ffprobe_path
        print(f"🔧 Set FFmpeg environment variables:")
        print(f"   FFMPEG_BINARY: {ffmpeg_path}")
        print(f"   FFPROBE_BINARY: {ffprobe_path}")
        return True
    else:
        print("⚠️ FFmpeg not found - audio processing may fail!")
        # Set fallback paths (these will likely fail, but we'll handle the error gracefully)
        os.environ["FFMPEG_BINARY"] = "ffmpeg"  # Use PATH fallback
        os.environ["FFPROBE_BINARY"] = "ffprobe"  # Use PATH fallback
        return False

def configure_pydub_ffmpeg() -> bool:
    """
    Configure pydub to use the correct FFmpeg paths
    
    Returns:
        True if FFmpeg was found and configured, False otherwise
    """
    try:
        from pydub import AudioSegment
        import pydub
        
        ffmpeg_path, ffprobe_path = find_ffmpeg_binaries()
        
        if ffmpeg_path and ffprobe_path:
            pydub.AudioSegment.converter = ffmpeg_path
            pydub.AudioSegment.ffmpeg = ffmpeg_path
            pydub.AudioSegment.ffprobe = ffprobe_path
            print(f"✅ Configured pydub with FFmpeg paths")
            return True
        else:
            print("⚠️ Using default pydub FFmpeg configuration (may fail)")
            return False
    except ImportError:
        print("⚠️ pydub not available - FFmpeg configuration skipped")
        return False

def test_ffmpeg_installation() -> bool:
    """
    Test if FFmpeg is working correctly
    
    Returns:
        True if FFmpeg is working, False otherwise
    """
    try:
        # Test ffmpeg
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode != 0:
            print("❌ FFmpeg test failed")
            return False
            
        # Test ffprobe
        result = subprocess.run(
            ["ffprobe", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode != 0:
            print("❌ FFprobe test failed")
            return False
            
        print("✅ FFmpeg installation verified")
        return True
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"❌ FFmpeg test failed: {e}")
        return False

def get_ffmpeg_info() -> dict:
    """
    Get information about the FFmpeg installation
    
    Returns:
        Dictionary with FFmpeg information
    """
    ffmpeg_path, ffprobe_path = find_ffmpeg_binaries()
    
    info = {
        "ffmpeg_path": ffmpeg_path,
        "ffprobe_path": ffprobe_path,
        "installed": ffmpeg_path is not None and ffprobe_path is not None,
        "working": False
    }
    
    if info["installed"]:
        info["working"] = test_ffmpeg_installation()
    
    return info

# Auto-setup when module is imported
if __name__ != "__main__":
    setup_ffmpeg_environment() 