"""
HTML Document Processor using BeautifulSoup
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import chardet

class HTMLProcessor:
    """Process HTML documents and extract clean text"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process(self, file_path: Path) -> Dict:
        """Process HTML document with text extraction and metadata"""
        
        try:
            # Read and detect encoding
            content = await self._read_file_with_encoding(file_path)
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract text content
            text_content = await self._extract_text(soup)
            
            # Extract metadata
            metadata = await self._extract_metadata(soup, file_path)
            
            return {
                'text_content': text_content,
                'metadata': metadata,
                'extraction_method': 'html_processor'
            }
            
        except Exception as e:
            self.logger.error(f"HTML processing failed: {str(e)}")
            raise
    
    async def _read_file_with_encoding(self, file_path: Path) -> str:
        """Read file with proper encoding detection"""
        
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding']
            
            # Read with detected encoding
            with open(file_path, 'r', encoding=encoding or 'utf-8', errors='ignore') as f:
                return f.read()
    
    async def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text from HTML"""
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    async def _extract_metadata(self, soup: BeautifulSoup, file_path: Path) -> Dict:
        """Extract HTML metadata"""
        
        metadata = {
            'file_size': file_path.stat().st_size,
            'file_type': 'html'
        }
        
        try:
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text().strip()
            
            # Extract meta tags
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                name = meta.get('name', '').lower()
                content = meta.get('content', '')
                
                if name == 'description':
                    metadata['description'] = content
                elif name == 'keywords':
                    metadata['keywords'] = content
                elif name == 'author':
                    metadata['author'] = content
                elif name.startswith('og:'):
                    metadata[name] = content
            
            # Count elements
            metadata.update({
                'heading_count': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
                'paragraph_count': len(soup.find_all('p')),
                'link_count': len(soup.find_all('a')),
                'image_count': len(soup.find_all('img')),
                'table_count': len(soup.find_all('table'))
            })
            
        except Exception as e:
            self.logger.warning(f"HTML metadata extraction failed: {e}")
        
        return metadata