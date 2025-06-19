"""
Text File Processor with encoding detection
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
import chardet

class TXTProcessor:
    """Process plain text files with encoding detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process(self, file_path: Path) -> Dict:
        """Process text file with encoding detection and metadata"""
        
        try:
            # Read file with proper encoding
            text_content, encoding = await self._read_file_with_encoding(file_path)
            
            # Extract metadata
            metadata = await self._extract_metadata(text_content, file_path, encoding)
            
            return {
                'text_content': text_content,
                'metadata': metadata,
                'extraction_method': 'txt_processor'
            }
            
        except Exception as e:
            self.logger.error(f"Text processing failed: {str(e)}")
            raise
    
    async def _read_file_with_encoding(self, file_path: Path) -> tuple[str, str]:
        """Read file with encoding detection"""
        
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content, 'utf-8'
        except UnicodeDecodeError:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] or 'utf-8'
                confidence = detected['confidence'] or 0.0
            
            # Read with detected encoding
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                    return content, encoding
            except Exception as e:
                self.logger.warning(f"Encoding detection failed, using utf-8 with errors ignored: {e}")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    return content, 'utf-8'
    
    async def _extract_metadata(self, text_content: str, file_path: Path, encoding: str) -> Dict:
        """Extract text file metadata"""
        
        lines = text_content.splitlines()
        
        metadata = {
            'file_size': file_path.stat().st_size,
            'file_type': 'txt',
            'encoding': encoding,
            'line_count': len(lines),
            'character_count': len(text_content),
            'word_count': len(text_content.split()),
            'paragraph_count': len([line for line in lines if line.strip()]),
            'empty_line_count': len([line for line in lines if not line.strip()])
        }
        
        # Analyze content structure
        if lines:
            metadata['first_line'] = lines[0][:100] if lines[0] else ''
            metadata['has_headers'] = any(line.strip().isupper() for line in lines[:10])
            metadata['has_bullet_points'] = any(line.strip().startswith(('•', '-', '*', '1.', '2.')) for line in lines)
        
        return metadata