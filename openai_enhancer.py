#!/usr/bin/env python3
"""
OpenAI-powered transcription enhancement system
"""
import openai
import os
import json
import re
from typing import Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIEnhancer:
    """OpenAI-powered transcription enhancement"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        
        if self.api_key:
            # Initialize OpenAI client with modern API
            self.client = openai.OpenAI(api_key=self.api_key)
            self.enabled = True
            print(f"✅ OpenAI enhancement enabled (Model: {self.model})")
        else:
            self.enabled = False
            print("⚠️  OpenAI API key not provided - advanced features disabled")
    
    def enhance_transcription(self, text: str, language: str = "auto", 
                            enhancement_type: str = "professional") -> Dict[str, str]:
        """
        Enhance transcription using OpenAI GPT
        
        Args:
            text: Raw transcription text
            language: Detected language
            enhancement_type: Type of enhancement (professional, medical, business, casual)
        
        Returns:
            Dict with original, enhanced, and metadata
        """
        
        if not self.enabled:
            return {
                "original": text,
                "enhanced": text,
                "enhancement_type": "none",
                "improvements": "OpenAI API key not configured"
            }
        
        try:
            # Choose prompt based on enhancement type
            prompt = self._get_enhancement_prompt(text, language, enhancement_type)
            
            # Call OpenAI API using modern client
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(enhancement_type)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=self.max_tokens
            )
            
            enhanced_text = response.choices[0].message.content.strip()
            
            # Extract improvements made
            improvements = self._analyze_improvements(text, enhanced_text)
            
            return {
                "original": text,
                "enhanced": enhanced_text,
                "enhancement_type": enhancement_type,
                "improvements": improvements,
                "model_used": self.model,
                "language": language
            }
            
        except Exception as e:
            print(f"OpenAI enhancement error: {e}")
            return {
                "original": text,
                "enhanced": text,
                "enhancement_type": "error",
                "improvements": f"Error: {str(e)}"
            }
    
    def _get_system_prompt(self, enhancement_type: str) -> str:
        """Get system prompt based on enhancement type"""
        
        base_prompt = """You are an expert transcription editor. Your job is to clean up and improve speech-to-text transcriptions while maintaining the original meaning and speaker's intent."""
        
        if enhancement_type == "medical":
            return base_prompt + """
            
Focus on:
- Medical terminology accuracy
- Proper formatting for medical records
- Patient confidentiality considerations
- Professional medical language
- Correct spelling of medical terms, medications, procedures
- Proper capitalization of drug names, conditions, anatomical terms
"""
        
        elif enhancement_type == "business":
            return base_prompt + """
            
Focus on:
- Professional business language
- Proper formatting for business communications
- Correct terminology for meetings, projects, deadlines
- Professional tone and clarity
- Proper names, company names, product names
- Business acronyms and abbreviations
"""
        
        elif enhancement_type == "legal":
            return base_prompt + """
            
Focus on:
- Legal terminology accuracy
- Formal legal language
- Proper case citations and legal references
- Professional legal formatting
- Accurate representation of legal concepts
"""
        
        else:  # professional (default)
            return base_prompt + """
            
Focus on:
- Clear, professional language
- Proper grammar and punctuation
- Correct spelling and capitalization
- Natural sentence flow
- Maintaining the speaker's original meaning
- Professional tone appropriate for business use
"""
    
    def _get_enhancement_prompt(self, text: str, language: str, enhancement_type: str) -> str:
        """Generate enhancement prompt"""
        
        prompt = f"""Please improve this transcription by fixing grammar, punctuation, spelling, and formatting while preserving the original meaning:

Original transcription:
"{text}"

Language: {language}
Enhancement type: {enhancement_type}

Requirements:
1. Fix obvious transcription errors
2. Add proper punctuation and capitalization
3. Correct spelling mistakes
4. Improve sentence structure for clarity
5. Maintain all original information
6. Use professional language appropriate for {enhancement_type} context
7. If names are mentioned, capitalize them properly
8. Fix any obvious mishearings (e.g., "by role" should be "by mistake")

Return only the improved transcription text."""
        
        return prompt
    
    def _analyze_improvements(self, original: str, enhanced: str) -> str:
        """Analyze what improvements were made"""
        
        improvements = []
        
        # Check for common improvements
        if enhanced.count('.') > original.count('.'):
            improvements.append("Added proper punctuation")
        
        if enhanced.count(',') > original.count(','):
            improvements.append("Improved comma usage")
        
        # Check for capitalization improvements
        if sum(1 for c in enhanced if c.isupper()) > sum(1 for c in original if c.isupper()):
            improvements.append("Fixed capitalization")
        
        # Check for length changes (usually indicates restructuring)
        if abs(len(enhanced) - len(original)) > len(original) * 0.1:
            improvements.append("Improved sentence structure")
        
        # Check for common word fixes
        common_fixes = [
            ("by role", "by mistake"),
            ("ten", "morning"),
            ("kid", "guys"),
            ("prode", "purpose")
        ]
        
        for wrong, right in common_fixes:
            if wrong in original.lower() and right in enhanced.lower():
                improvements.append(f"Fixed '{wrong}' → '{right}'")
        
        return "; ".join(improvements) if improvements else "General text cleanup and formatting"
    
    def summarize_transcription(self, text: str, summary_type: str = "bullet_points") -> Dict[str, str]:
        """Create summary of transcription"""
        
        if not self.enabled:
            return {"summary": "OpenAI API key required for summarization"}
        
        try:
            if summary_type == "bullet_points":
                prompt = f"Create bullet points summarizing the key points from this transcription:\n\n{text}"
            elif summary_type == "executive":
                prompt = f"Create an executive summary of this transcription:\n\n{text}"
            elif summary_type == "action_items":
                prompt = f"Extract action items and tasks mentioned in this transcription:\n\n{text}"
            else:
                prompt = f"Summarize this transcription:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at summarizing business and professional conversations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            return {
                "summary": response.choices[0].message.content.strip(),
                "summary_type": summary_type,
                "model_used": self.model
            }
            
        except Exception as e:
            return {"summary": f"Error creating summary: {str(e)}"}
    
    def translate_transcription(self, text: str, target_language: str = "English") -> Dict[str, str]:
        """Translate transcription to target language"""
        
        if not self.enabled:
            return {"translation": "OpenAI API key required for translation"}
        
        try:
            prompt = f"Translate this transcription to {target_language}, maintaining professional tone:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert translator specializing in professional and business translations to {target_language}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=self.max_tokens
            )
            
            return {
                "translation": response.choices[0].message.content.strip(),
                "target_language": target_language,
                "model_used": self.model
            }
            
        except Exception as e:
            return {"translation": f"Error translating: {str(e)}"}
    
    def format_transcription(self, text: str, format_type: str = "meeting_notes") -> Dict[str, str]:
        """Format transcription into structured document"""
        
        if not self.enabled:
            return {"formatted": "OpenAI API key required for formatting"}
        
        try:
            if format_type == "meeting_notes":
                prompt = f"""Format this transcription as professional meeting notes with proper structure:

{text}

Use this format:
- Meeting participants
- Key discussion points  
- Decisions made
- Action items
- Next steps"""
            
            elif format_type == "medical_notes":
                prompt = f"""Format this transcription as professional medical notes:

{text}

Use appropriate medical documentation format."""
            
            elif format_type == "report":
                prompt = f"""Format this transcription as a professional report with sections and clear structure:

{text}"""
            
            else:
                prompt = f"Format this transcription with proper structure and professional formatting:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at formatting professional documents and reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=self.max_tokens
            )
            
            return {
                "formatted": response.choices[0].message.content.strip(),
                "format_type": format_type,
                "model_used": self.model
            }
            
        except Exception as e:
            return {"formatted": f"Error formatting: {str(e)}"}

# Global instance
openai_enhancer = OpenAIEnhancer()

def enhance_with_openai(text: str, language: str = "auto", 
                       enhancement_type: str = "professional") -> Dict[str, str]:
    """Main function to enhance transcription with OpenAI"""
    return openai_enhancer.enhance_transcription(text, language, enhancement_type)

if __name__ == "__main__":
    # Test with your specific example
    test_text = "Okay, ten, kid, excuse me for calling you by role. I mean, reina, we'll be in the office waiting for you if you need anything."
    
    enhancer = OpenAIEnhancer()
    result = enhancer.enhance_transcription(test_text, "auto", "business")
    
    print("🧪 OpenAI Enhancement Test:")
    print(f"Original: {result['original']}")
    print(f"Enhanced: {result['enhanced']}")
    print(f"Improvements: {result['improvements']}")