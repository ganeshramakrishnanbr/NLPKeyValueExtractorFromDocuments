"""
PDF Document Processor using pdfplumber and PyMuPDF
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pdfplumber
import fitz  # PyMuPDF
import chardet

class PDFProcessor:
    """Advanced PDF processing with multiple extraction methods"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process(self, file_path: Path) -> Dict:
        """Process PDF document with text extraction and metadata"""
        
        try:
            # Primary extraction with pdfplumber
            text_content = await self._extract_with_pdfplumber(file_path)
            
            # Fallback to PyMuPDF if pdfplumber fails
            if not text_content.strip():
                text_content = await self._extract_with_pymupdf(file_path)
            
            # Extract metadata
            metadata = await self._extract_metadata(file_path)
            
            return {
                'text_content': text_content,
                'metadata': metadata,
                'page_count': metadata.get('page_count', 0),
                'extraction_method': 'pdf_processor'
            }
            
        except Exception as e:
            self.logger.error(f"PDF processing failed: {str(e)}")
            raise
    
    async def _extract_with_pdfplumber(self, file_path: Path) -> str:
        """Extract text using pdfplumber"""
        
        text_parts = []
        
        try:
            with pdfplumber.open(str(file_path)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            self.logger.warning(f"pdfplumber extraction failed: {e}")
            return ""
    
    async def _extract_with_pymupdf(self, file_path: Path) -> str:
        """Extract text using PyMuPDF as fallback"""
        
        text_parts = []
        
        try:
            doc = fitz.open(str(file_path))
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                if page_text.strip():
                    text_parts.append(page_text)
            
            doc.close()
            return "\n\n".join(text_parts)
            
        except Exception as e:
            self.logger.warning(f"PyMuPDF extraction failed: {e}")
            return ""
    
    async def _extract_metadata(self, file_path: Path) -> Dict:
        """Extract PDF metadata"""
        
        metadata = {}
        
        try:
            doc = fitz.open(str(file_path))
            pdf_metadata = doc.metadata
            
            metadata.update({
                'title': pdf_metadata.get('title', ''),
                'author': pdf_metadata.get('author', ''),
                'subject': pdf_metadata.get('subject', ''),
                'creator': pdf_metadata.get('creator', ''),
                'producer': pdf_metadata.get('producer', ''),
                'creation_date': pdf_metadata.get('creationDate', ''),
                'modification_date': pdf_metadata.get('modDate', ''),
                'page_count': len(doc),
                'file_size': file_path.stat().st_size
            })
            
            doc.close()
            
        except Exception as e:
            self.logger.warning(f"Metadata extraction failed: {e}")
            metadata = {'page_count': 0, 'file_size': file_path.stat().st_size}
        
        return metadata