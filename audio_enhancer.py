#!/usr/bin/env python3
"""
Advanced Audio Enhancement System for Improved Transcription
"""
import numpy as np
import librosa
import noisereduce as nr
from scipy import signal
import os
import tempfile

# Import centralized FFmpeg utilities
from ffmpeg_utils import setup_ffmpeg_environment, configure_pydub_ffmpeg

# Set up FFmpeg environment
setup_ffmpeg_environment()

from pydub import AudioSegment

# Configure pydub to use the correct FFmpeg paths
configure_pydub_ffmpeg()

import webrtcvad
import io
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class AudioEnhancer:
    """Advanced audio enhancement for better transcription accuracy"""
    
    def __init__(self):
        """Initialize audio enhancer"""
        self.sample_rate = 16000  # Optimal for Whisper
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level (0-3)
        
    def enhance_audio(self, file_path: str, enhancement_level: str = "medium") -> str:
        """
        Enhance audio file for better transcription
        
        Args:
            file_path: Path to audio file
            enhancement_level: 'light', 'medium', 'aggressive'
            
        Returns:
            Path to enhanced audio file
        """
        
        print(f"🎵 Enhancing audio with {enhancement_level} level...")
        
        try:
            # Load audio file
            audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
            
            # Apply enhancement chain based on level
            if enhancement_level == "light":
                enhanced = self._light_enhancement(audio_data, sr)
            elif enhancement_level == "medium":
                enhanced = self._medium_enhancement(audio_data, sr)
            elif enhancement_level == "aggressive":
                enhanced = self._aggressive_enhancement(audio_data, sr)
            else:
                enhanced = self._medium_enhancement(audio_data, sr)  # Default
            
            # Save enhanced audio to writable temporary directory
            temp_dir = os.path.join(tempfile.gettempdir(), "transcribe_temp")
            os.makedirs(temp_dir, exist_ok=True)
            output_path = os.path.join(temp_dir, f"enhanced_{os.path.basename(file_path)}.wav")
            self._save_audio(enhanced, sr, output_path)
            
            print(f"✅ Audio enhanced successfully -> {output_path}")
            return output_path
            
        except Exception as e:
            print(f"⚠️ Audio enhancement failed: {e}")
            print("📝 Proceeding with original audio...")
            return file_path
    
    def _light_enhancement(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Light enhancement - basic cleaning"""
        # 1. Normalize volume
        audio = self._normalize_audio(audio)
        
        # 2. Light noise reduction
        audio = nr.reduce_noise(y=audio, sr=sr, prop_decrease=0.8)
        
        # 3. High-pass filter to remove low rumble
        audio = self._high_pass_filter(audio, sr, cutoff=80)
        
        return audio
    
    def _medium_enhancement(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Medium enhancement - balanced quality improvement"""
        # 1. Normalize volume
        audio = self._normalize_audio(audio)
        
        # 2. Remove silence/noise segments
        audio = self._remove_silence(audio, sr)
        
        # 3. Noise reduction
        audio = nr.reduce_noise(y=audio, sr=sr, prop_decrease=0.9)
        
        # 4. Frequency filtering
        audio = self._band_pass_filter(audio, sr, low=80, high=7000)
        
        # 5. Dynamic range compression
        audio = self._compress_dynamic_range(audio)
        
        # 6. Final normalization
        audio = self._normalize_audio(audio)
        
        return audio
    
    def _aggressive_enhancement(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Aggressive enhancement - maximum cleaning"""
        # 1. Normalize volume
        audio = self._normalize_audio(audio)
        
        # 2. Advanced silence removal
        audio = self._remove_silence(audio, sr, aggressive=True)
        
        # 3. Strong noise reduction
        audio = nr.reduce_noise(y=audio, sr=sr, prop_decrease=0.95)
        
        # 4. Spectral subtraction for additional noise removal
        audio = self._spectral_subtraction(audio, sr)
        
        # 5. Enhanced frequency filtering
        audio = self._band_pass_filter(audio, sr, low=100, high=6000)
        
        # 6. Voice enhancement
        audio = self._enhance_voice_frequencies(audio, sr)
        
        # 7. Dynamic range compression
        audio = self._compress_dynamic_range(audio, ratio=4.0)
        
        # 8. Final normalization
        audio = self._normalize_audio(audio)
        
        return audio
    
    def _normalize_audio(self, audio: np.ndarray, target_lufs: float = -23.0) -> np.ndarray:
        """Normalize audio volume"""
        # Simple RMS-based normalization
        rms = np.sqrt(np.mean(audio**2))
        if rms > 0:
            target_rms = 10**(target_lufs/20)
            audio = audio * (target_rms / rms)
        
        # Prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0.95:
            audio = audio * (0.95 / max_val)
            
        return audio
    
    def _remove_silence(self, audio: np.ndarray, sr: int, aggressive: bool = False) -> np.ndarray:
        """Remove silence using voice activity detection"""
        try:
            # Convert to 16-bit PCM for WebRTC VAD
            audio_16bit = (audio * 32767).astype(np.int16)
            
            # Frame parameters
            frame_duration = 30  # ms
            frame_length = int(sr * frame_duration / 1000)
            
            # Process in frames
            voiced_frames = []
            for i in range(0, len(audio_16bit) - frame_length + 1, frame_length):
                frame = audio_16bit[i:i + frame_length]
                
                # Check if frame contains voice
                if len(frame) == frame_length:
                    frame_bytes = frame.tobytes()
                    try:
                        is_speech = self.vad.is_speech(frame_bytes, sr)
                        if is_speech or not aggressive:
                            voiced_frames.append(audio[i:i + frame_length])
                    except:
                        # If VAD fails, keep the frame
                        voiced_frames.append(audio[i:i + frame_length])
            
            if voiced_frames:
                return np.concatenate(voiced_frames)
            else:
                return audio  # Return original if no voice detected
                
        except Exception as e:
            print(f"⚠️ Silence removal failed: {e}")
            return audio
    
    def _high_pass_filter(self, audio: np.ndarray, sr: int, cutoff: float = 80) -> np.ndarray:
        """Apply high-pass filter to remove low-frequency noise"""
        sos = signal.butter(5, cutoff, btype='high', fs=sr, output='sos')
        return signal.sosfilt(sos, audio)
    
    def _band_pass_filter(self, audio: np.ndarray, sr: int, low: float = 80, high: float = 7000) -> np.ndarray:
        """Apply band-pass filter for voice frequencies"""
        sos = signal.butter(5, [low, high], btype='band', fs=sr, output='sos')
        return signal.sosfilt(sos, audio)
    
    def _compress_dynamic_range(self, audio: np.ndarray, ratio: float = 3.0, threshold: float = -20.0) -> np.ndarray:
        """Apply dynamic range compression"""
        # Convert to dB
        audio_db = 20 * np.log10(np.abs(audio) + 1e-10)
        
        # Apply compression
        compressed_db = np.where(
            audio_db > threshold,
            threshold + (audio_db - threshold) / ratio,
            audio_db
        )
        
        # Convert back to linear
        compressed = np.sign(audio) * (10 ** (compressed_db / 20))
        return compressed
    
    def _spectral_subtraction(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Advanced spectral subtraction for noise reduction"""
        try:
            # STFT
            stft = librosa.stft(audio, n_fft=2048, hop_length=512)
            magnitude = np.abs(stft)
            phase = np.angle(stft)
            
            # Estimate noise from first 0.5 seconds
            noise_frames = int(0.5 * sr / 512)
            noise_spectrum = np.mean(magnitude[:, :noise_frames], axis=1, keepdims=True)
            
            # Spectral subtraction
            alpha = 2.0  # Over-subtraction factor
            enhanced_magnitude = magnitude - alpha * noise_spectrum
            
            # Ensure non-negative values
            enhanced_magnitude = np.maximum(enhanced_magnitude, 0.1 * magnitude)
            
            # Reconstruct
            enhanced_stft = enhanced_magnitude * np.exp(1j * phase)
            enhanced_audio = librosa.istft(enhanced_stft, hop_length=512)
            
            return enhanced_audio
            
        except Exception as e:
            print(f"⚠️ Spectral subtraction failed: {e}")
            return audio
    
    def _enhance_voice_frequencies(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Enhance human voice frequency range (85-255 Hz fundamental, harmonics up to 4kHz)"""
        try:
            # STFT
            stft = librosa.stft(audio, n_fft=2048, hop_length=512)
            magnitude = np.abs(stft)
            phase = np.angle(stft)
            
            # Frequency bins
            freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
            
            # Create voice enhancement filter
            enhancement = np.ones_like(freqs)
            
            # Boost voice fundamentals (85-255 Hz)
            voice_fundamental = (freqs >= 85) & (freqs <= 255)
            enhancement[voice_fundamental] *= 1.2
            
            # Boost voice harmonics (300-4000 Hz)
            voice_harmonics = (freqs >= 300) & (freqs <= 4000)
            enhancement[voice_harmonics] *= 1.1
            
            # Apply enhancement
            enhanced_magnitude = magnitude * enhancement.reshape(-1, 1)
            
            # Reconstruct
            enhanced_stft = enhanced_magnitude * np.exp(1j * phase)
            enhanced_audio = librosa.istft(enhanced_stft, hop_length=512)
            
            return enhanced_audio
            
        except Exception as e:
            print(f"⚠️ Voice enhancement failed: {e}")
            return audio
    
    def _save_audio(self, audio: np.ndarray, sr: int, output_path: str):
        """Save enhanced audio to file"""
        # Convert to AudioSegment
        audio_int16 = (audio * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            audio_int16.tobytes(),
            frame_rate=sr,
            sample_width=2,  # 16-bit
            channels=1
        )
        
        # Export as WAV
        audio_segment.export(output_path, format="wav")
    
    def get_audio_quality_metrics(self, original_path: str, enhanced_path: str) -> dict:
        """Compare audio quality metrics"""
        try:
            # Load both files
            orig_audio, sr1 = librosa.load(original_path, sr=self.sample_rate)
            enh_audio, sr2 = librosa.load(enhanced_path, sr=self.sample_rate)
            
            # Calculate metrics
            orig_rms = np.sqrt(np.mean(orig_audio**2))
            enh_rms = np.sqrt(np.mean(enh_audio**2))
            
            orig_snr = self._estimate_snr(orig_audio)
            enh_snr = self._estimate_snr(enh_audio)
            
            return {
                "original_rms": float(orig_rms),
                "enhanced_rms": float(enh_rms),
                "original_snr_db": float(orig_snr),
                "enhanced_snr_db": float(enh_snr),
                "snr_improvement_db": float(enh_snr - orig_snr),
                "volume_change_db": float(20 * np.log10(enh_rms / orig_rms)) if orig_rms > 0 else 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _estimate_snr(self, audio: np.ndarray) -> float:
        """Estimate signal-to-noise ratio"""
        try:
            # Simple SNR estimation using signal variance
            signal_power = np.var(audio)
            
            # Estimate noise from quieter segments
            audio_sorted = np.sort(np.abs(audio))
            noise_samples = audio_sorted[:len(audio_sorted)//4]  # Bottom 25%
            noise_power = np.var(noise_samples)
            
            if noise_power > 0:
                snr = 10 * np.log10(signal_power / noise_power)
            else:
                snr = 60  # Very clean signal
                
            return max(0, min(60, snr))  # Clamp between 0-60 dB
            
        except:
            return 20  # Default reasonable value

# Global instance
audio_enhancer = AudioEnhancer()

def enhance_audio_for_transcription(file_path: str, enhancement_level: str = "medium") -> Tuple[str, dict]:
    """
    Main function to enhance audio for better transcription
    
    Returns:
        Tuple of (enhanced_file_path, quality_metrics)
    """
    enhanced_path = audio_enhancer.enhance_audio(file_path, enhancement_level)
    
    # Get quality metrics if enhancement was applied
    if enhanced_path != file_path:
        metrics = audio_enhancer.get_audio_quality_metrics(file_path, enhanced_path)
    else:
        metrics = {"enhancement": "skipped"}
    
    return enhanced_path, metrics

if __name__ == "__main__":
    # Test the audio enhancer
    print("🎵 Audio Enhancement Test")
    print("=" * 30)
    
    # Test file (you can replace with actual test file)
    test_file = "test_audio.wav"
    
    if os.path.exists(test_file):
        enhanced_file, metrics = enhance_audio_for_transcription(test_file, "medium")
        print(f"📈 Quality Metrics: {metrics}")
    else:
        print("ℹ️  No test file found. Audio enhancer is ready to use!")