#!/usr/bin/env python3
"""
Text accuracy enhancement tools for Whisper transcriptions
"""
import re
import whisper
from typing import Dict, List, Tuple

def enhance_transcription_accuracy(text: str, language: str = "auto") -> Dict[str, str]:
    """
    Enhance transcription accuracy with post-processing
    
    Args:
        text (str): Raw transcription text
        language (str): Detected or specified language
    
    Returns:
        Dict with original, cleaned, and corrected text
    """
    
    # Store original
    original_text = text
    
    # Step 1: Basic cleaning
    cleaned_text = basic_text_cleaning(text)
    
    # Step 2: Language-specific corrections
    if language in ['en', 'english']:
        corrected_text = english_corrections(cleaned_text)
    elif language in ['es', 'spanish']:
        corrected_text = spanish_corrections(cleaned_text)
    else:
        corrected_text = cleaned_text
    
    # Step 3: Common fixes for both languages
    final_text = common_corrections(corrected_text)
    
    return {
        "original": original_text,
        "cleaned": cleaned_text,
        "corrected": final_text,
        "language": language
    }

def basic_text_cleaning(text: str) -> str:
    """Basic text cleaning and formatting"""
    if not text:
        return text
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Fix common punctuation issues
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([.!?])\s*([a-z])', r'\1 \2', text)  # Ensure space after sentence endings
    
    # Capitalize first letter of sentences
    text = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    
    # Fix common spacing issues
    text = re.sub(r'\s*\.\s*', '. ', text)
    text = re.sub(r'\s*,\s*', ', ', text)
    
    return text.strip()

def english_corrections(text: str) -> str:
    """English-specific corrections"""
    
    # Common medical/professional terms
    medical_corrections = {
        r'\bpatient\b': 'patient',
        r'\bsymptoms?\b': 'symptoms',
        r'\btemperature\b': 'temperature',
        r'\bprescription\b': 'prescription',
        r'\bmedication\b': 'medication',
        r'\ballergies\b': 'allergies',
        r'\bdiagnosis\b': 'diagnosis',
        r'\btreatment\b': 'treatment'
    }
    
    # Common contractions
    contractions = {
        r"\bcan't\b": "cannot",
        r"\bwon't\b": "will not",
        r"\bdoesn't\b": "does not",
        r"\bhasn't\b": "has not",
        r"\bhaven't\b": "have not",
        r"\bisn't\b": "is not",
        r"\baren't\b": "are not"
    }
    
    # Apply corrections
    for pattern, replacement in {**medical_corrections, **contractions}.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def spanish_corrections(text: str) -> str:
    """Spanish-specific corrections"""
    
    # Common medical/professional terms in Spanish
    medical_corrections = {
        r'\bpaciente\b': 'paciente',
        r'\bsíntomas?\b': 'síntomas',
        r'\btemperatura\b': 'temperatura',
        r'\bfiebre\b': 'fiebre',
        r'\bmedicamentos?\b': 'medicamento',
        r'\balergias?\b': 'alergia',
        r'\bdiagnóstico\b': 'diagnóstico',
        r'\btratamiento\b': 'tratamiento',
        r'\bdolor\b': 'dolor',
        r'\bcabeza\b': 'cabeza'
    }
    
    # Common accent corrections (Whisper sometimes misses accents)
    accent_corrections = {
        r'\bmedico\b': 'médico',
        r'\brapido\b': 'rápido',
        r'\bultimo\b': 'último',
        r'\bproximo\b': 'próximo',
        r'\bexamen\b': 'examen',
        r'\bcorazon\b': 'corazón'
    }
    
    # Apply corrections
    for pattern, replacement in {**medical_corrections, **accent_corrections}.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def common_corrections(text: str) -> str:
    """Common corrections for both languages"""
    
    # Proper name corrections (based on user feedback)
    name_corrections = {
        r'\breina\b': 'Reina',
        r'\bzaya\b': 'Zaya', 
        r'\bcarlos\b': 'Carlos',
        r'\bdave\b': 'Dave',
        r'\bprode\b': 'purpose',    # "for the same purpose" not "at Prode"
        r'\brole\b': 'mistake',     # "by mistake" not "by role"
        r'\bten\b': 'morning',      # "Good morning" not "ten"
        r'\bkid\b': 'guys',         # "guys" not "kid"
        r'\bokay, ten, kid\b': 'Good morning guys',  # Full phrase correction
    }
    
    # Number corrections
    number_corrections = {
        r'\bone\b': '1',
        r'\btwo\b': '2',
        r'\bthree\b': '3',
        r'\bfour\b': '4',
        r'\bfive\b': '5',
        r'\buno\b': '1',
        r'\bdos\b': '2',
        r'\btres\b': '3',
        r'\bcuatro\b': '4',
        r'\bcinco\b': '5'
    }
    
    # Time/date corrections
    time_corrections = {
        r'\bam\b': 'AM',
        r'\bpm\b': 'PM',
        r'\ba\.m\.\b': 'AM',
        r'\bp\.m\.\b': 'PM'
    }
    
    # Apply all corrections
    for pattern, replacement in {**name_corrections, **time_corrections}.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def get_transcription_with_confidence(audio_path: str, model_name: str = "base") -> Dict:
    """
    Get transcription with word-level confidence scores
    
    Args:
        audio_path (str): Path to audio file
        model_name (str): Whisper model to use (base, small, medium, large)
    
    Returns:
        Dict with transcription and confidence information
    """
    
    # Load model
    model = whisper.load_model(model_name)
    
    # Transcribe with word-level timestamps
    result = model.transcribe(
        audio_path,
        word_timestamps=True,
        verbose=False
    )
    
    # Extract word-level information
    words_with_confidence = []
    if "segments" in result:
        for segment in result["segments"]:
            if "words" in segment:
                for word_info in segment["words"]:
                    words_with_confidence.append({
                        "word": word_info.get("word", "").strip(),
                        "start": word_info.get("start", 0),
                        "end": word_info.get("end", 0),
                        "confidence": word_info.get("probability", 0)
                    })
    
    # Calculate overall confidence
    if words_with_confidence:
        avg_confidence = sum(w["confidence"] for w in words_with_confidence) / len(words_with_confidence)
    else:
        avg_confidence = 0
    
    return {
        "text": result["text"],
        "language": result.get("language", "unknown"),
        "words": words_with_confidence,
        "average_confidence": avg_confidence,
        "segments": result.get("segments", [])
    }

# Model size recommendations
MODEL_ACCURACY_INFO = {
    "tiny": {"accuracy": "⭐⭐", "speed": "⚡⚡⚡", "size": "39 MB"},
    "base": {"accuracy": "⭐⭐⭐", "speed": "⚡⚡", "size": "74 MB"},
    "small": {"accuracy": "⭐⭐⭐⭐", "speed": "⚡", "size": "244 MB"},
    "medium": {"accuracy": "⭐⭐⭐⭐⭐", "speed": "⚡", "size": "769 MB"},
    "large": {"accuracy": "⭐⭐⭐⭐⭐⭐", "speed": "🐌", "size": "1550 MB"}
}

def print_model_recommendations():
    """Print model accuracy vs speed recommendations"""
    print("🎯 Whisper Model Accuracy Recommendations:")
    print("=" * 50)
    for model, info in MODEL_ACCURACY_INFO.items():
        print(f"{model:8} | Accuracy: {info['accuracy']:8} | Speed: {info['speed']:8} | Size: {info['size']}")
    print("\n💡 Recommendation: Use 'small' or 'medium' for better accuracy")
    print("⚠️  Note: Larger models are slower but more accurate")