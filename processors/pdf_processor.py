"""
PDF Document Processor using pdfplumber and PyMuPDF
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pdfplumber
import chardet

class PDFProcessor:
    """Advanced PDF processing with multiple extraction methods"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process(self, file_path: Path) -> Dict:
        """Process PDF document with text extraction and metadata"""
        
        try:
            # Extract with pdfplumber
            text_content = await self._extract_with_pdfplumber(file_path)
            
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
    
    async def _count_pages(self, file_path: Path) -> int:
        """Count PDF pages using pdfplumber"""
        try:
            with pdfplumber.open(str(file_path)) as pdf:
                return len(pdf.pages)
        except Exception:
            return 0
    
    async def _extract_metadata(self, file_path: Path) -> Dict:
        """Extract basic PDF metadata"""
        
        page_count = await self._count_pages(file_path)
        
        metadata = {
            'file_size': file_path.stat().st_size,
            'file_type': 'pdf',
            'page_count': page_count,
            'title': '',
            'author': '',
            'subject': '',
            'creator': 'PDF',
            'producer': '',
            'creation_date': '',
            'modification_date': ''
        }
        
        # Try to extract metadata from pdfplumber
        try:
            with pdfplumber.open(str(file_path)) as pdf:
                if hasattr(pdf, 'metadata') and pdf.metadata:
                    metadata.update({
                        'title': pdf.metadata.get('Title', ''),
                        'author': pdf.metadata.get('Author', ''),
                        'subject': pdf.metadata.get('Subject', ''),
                        'creator': pdf.metadata.get('Creator', 'PDF'),
                        'producer': pdf.metadata.get('Producer', ''),
                        'creation_date': str(pdf.metadata.get('CreationDate', '')),
                        'modification_date': str(pdf.metadata.get('ModDate', ''))
                    })
        except Exception as e:
            self.logger.warning(f"Metadata extraction failed: {e}")
        
        return metadata