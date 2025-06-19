"""
Document Quality Assessment Module
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Optional
import re

class QualityAssessor:
    """Assess document processing quality and determine if OCR is needed"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def assess_quality(self, processing_result: Dict, file_path: Path) -> float:
        """Assess overall document processing quality (0.0 to 1.0)"""
        
        try:
            text_content = processing_result.get('text_content', '')
            metadata = processing_result.get('metadata', {})
            
            # Calculate various quality metrics
            text_quality = await self._assess_text_quality(text_content)
            extraction_quality = await self._assess_extraction_quality(processing_result)
            metadata_quality = await self._assess_metadata_quality(metadata)
            
            # Weighted overall score
            overall_quality = (
                text_quality * 0.6 +
                extraction_quality * 0.3 +
                metadata_quality * 0.1
            )
            
            return min(1.0, max(0.0, overall_quality))
            
        except Exception as e:
            self.logger.error(f"Quality assessment failed: {str(e)}")
            return 0.5  # Default neutral score
    
    async def _assess_text_quality(self, text_content: str) -> float:
        """Assess text extraction quality"""
        
        if not text_content or len(text_content.strip()) < 10:
            return 0.0
        
        quality_score = 0.0
        
        # Length factor (longer text generally indicates better extraction)
        length_score = min(1.0, len(text_content) / 1000)
        quality_score += length_score * 0.3
        
        # Character diversity (more diverse = better extraction)
        unique_chars = len(set(text_content.lower()))
        char_diversity = min(1.0, unique_chars / 50)
        quality_score += char_diversity * 0.2
        
        # Word structure assessment
        words = text_content.split()
        if words:
            # Average word length (reasonable words indicate good extraction)
            avg_word_length = sum(len(word) for word in words) / len(words)
            word_length_score = 1.0 if 3 <= avg_word_length <= 8 else 0.5
            quality_score += word_length_score * 0.2
            
            # Ratio of dictionary-like words
            valid_word_ratio = await self._calculate_valid_word_ratio(words)
            quality_score += valid_word_ratio * 0.3
        
        return min(1.0, quality_score)
    
    async def _calculate_valid_word_ratio(self, words: list) -> float:
        """Calculate ratio of potentially valid words"""
        
        if not words:
            return 0.0
        
        valid_word_count = 0
        
        for word in words:
            # Clean word
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            if len(clean_word) >= 2:
                # Check if word has reasonable character patterns
                has_vowels = bool(re.search(r'[aeiou]', clean_word))
                has_consonants = bool(re.search(r'[bcdfghjklmnpqrstvwxyz]', clean_word))
                not_too_repetitive = len(set(clean_word)) > len(clean_word) * 0.3
                
                if has_vowels and has_consonants and not_too_repetitive:
                    valid_word_count += 1
        
        return valid_word_count / len(words)
    
    async def _assess_extraction_quality(self, processing_result: Dict) -> float:
        """Assess extraction method effectiveness"""
        
        extraction_method = processing_result.get('extraction_method', '')
        text_length = len(processing_result.get('text_content', ''))
        
        # Base score based on extraction success
        if text_length == 0:
            return 0.0
        elif text_length < 50:
            return 0.3
        elif text_length < 200:
            return 0.6
        else:
            return 0.9
    
    async def _assess_metadata_quality(self, metadata: Dict) -> float:
        """Assess metadata extraction completeness"""
        
        if not metadata:
            return 0.0
        
        # Key metadata fields to check
        important_fields = ['title', 'author', 'creation_date', 'page_count', 'file_size']
        present_fields = sum(1 for field in important_fields if metadata.get(field))
        
        return present_fields / len(important_fields)