"""
Enhanced Document Processing Engine

Main processing engine with multi-format support, OCR capabilities, 
and advanced preprocessing features using open source technologies.
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import chardet

from processors.pdf_processor import PDFProcessor
from processors.docx_processor import DOCXProcessor
from processors.html_processor import HTMLProcessor
from processors.txt_processor import TXTProcessor
from core.ocr_processor import OCRProcessor
from core.table_extractor import TableExtractor
from core.image_processor import ImageProcessor
from core.quality_assessor import QualityAssessor

class DocumentType(Enum):
    PDF = "pdf"
    DOCX = "docx" 
    DOC = "doc"
    HTML = "html"
    TXT = "txt"
    RTF = "rtf"
    UNKNOWN = "unknown"

@dataclass
class ProcessingOptions:
    """Configuration options for document processing"""
    enable_ocr: bool = True
    extract_tables: bool = True
    extract_images: bool = True
    enhance_images: bool = True
    perform_quality_check: bool = True
    ocr_languages: List[str] = None
    confidence_threshold: float = 0.7
    
    def __post_init__(self):
        if self.ocr_languages is None:
            self.ocr_languages = ['en']

@dataclass 
class ProcessingResult:
    """Container for document processing results"""
    text_content: str
    document_type: DocumentType
    metadata: Dict
    tables: List[Dict] = None
    images: List[Dict] = None
    quality_score: float = 0.0
    ocr_confidence: float = 0.0
    processing_time: float = 0.0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.tables is None:
            self.tables = []
        if self.images is None:
            self.images = []
        if self.errors is None:
            self.errors = []

class EnhancedDocumentProcessor:
    """
    Enhanced document processing engine with multi-format support,
    OCR capabilities, and advanced preprocessing features.
    """
    
    def __init__(self, processing_options: ProcessingOptions = None):
        self.options = processing_options or ProcessingOptions()
        self.logger = logging.getLogger(__name__)
        
        # Initialize specialized processors
        self.pdf_processor = PDFProcessor()
        self.docx_processor = DOCXProcessor()
        self.html_processor = HTMLProcessor()
        self.txt_processor = TXTProcessor()
        
        # Initialize enhancement processors
        self.ocr_processor = OCRProcessor(languages=self.options.ocr_languages)
        self.table_extractor = TableExtractor()
        self.image_processor = ImageProcessor()
        self.quality_assessor = QualityAssessor()
        
        # File type mapping
        self.processors = {
            DocumentType.PDF: self.pdf_processor,
            DocumentType.DOCX: self.docx_processor,
            DocumentType.DOC: self.docx_processor,  # DOC uses same processor
            DocumentType.HTML: self.html_processor,
            DocumentType.TXT: self.txt_processor,
        }
    
    async def process_document(self, file_path: Union[str, Path]) -> ProcessingResult:
        """
        Process a document through the complete enhancement pipeline
        """
        start_time = time.time()
        
        try:
            file_path = Path(file_path)
            
            # Step 1: Detect document type and validate
            doc_type = self._detect_document_type(file_path)
            if doc_type == DocumentType.UNKNOWN:
                raise ValueError(f"Unsupported document type: {file_path.suffix}")
            
            # Step 2: Basic document processing
            processor = self.processors[doc_type]
            basic_result = await processor.process(file_path)
            
            # Step 3: Quality assessment
            quality_score = 0.0
            if self.options.perform_quality_check:
                quality_score = await self.quality_assessor.assess_quality(
                    basic_result, file_path
                )
            
            # Step 4: OCR processing for scanned documents or poor quality
            ocr_confidence = 0.0
            enhanced_text = basic_result.get('text_content', '')
            
            if self.options.enable_ocr and (quality_score < 0.5 or len(enhanced_text.strip()) < 100):
                self.logger.info("Applying OCR processing")
                ocr_result = await self.ocr_processor.process_document(file_path)
                if ocr_result.get('confidence', 0) > self.options.confidence_threshold:
                    enhanced_text = ocr_result.get('text', enhanced_text)
                    ocr_confidence = ocr_result.get('confidence', 0)
            
            # Step 5: Table extraction
            tables = []
            if self.options.extract_tables and doc_type == DocumentType.PDF:
                tables = await self.table_extractor.extract_tables(file_path)
            
            # Step 6: Image extraction and processing
            images = []
            if self.options.extract_images:
                images = await self.image_processor.extract_and_process_images(
                    file_path, enhance=self.options.enhance_images
                )
            
            # Step 7: Compile final result
            processing_time = time.time() - start_time
            
            result = ProcessingResult(
                text_content=enhanced_text,
                document_type=doc_type,
                metadata=basic_result.get('metadata', {}),
                tables=tables,
                images=images,
                quality_score=quality_score,
                ocr_confidence=ocr_confidence,
                processing_time=processing_time
            )
            
            self.logger.info(
                f"Document processed successfully in {processing_time:.2f}s "
                f"(Quality: {quality_score:.2f}, OCR: {ocr_confidence:.2f})"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Document processing failed: {str(e)}")
            raise
    
    def _detect_document_type(self, file_path: Path) -> DocumentType:
        """Detect document type using file extension"""
        
        # Primary detection by extension
        extension = file_path.suffix.lower()
        extension_mapping = {
            '.pdf': DocumentType.PDF,
            '.docx': DocumentType.DOCX,
            '.doc': DocumentType.DOC,
            '.html': DocumentType.HTML,
            '.htm': DocumentType.HTML,
            '.txt': DocumentType.TXT,
            '.rtf': DocumentType.RTF
        }
        
        return extension_mapping.get(extension, DocumentType.UNKNOWN)
    
    async def process_batch(self, file_paths: List[Union[str, Path]]) -> List[ProcessingResult]:
        """Process multiple documents concurrently"""
        
        tasks = [self.process_document(file_path) for file_path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Failed to process {file_paths[i]}: {result}")
                # Create error result
                error_result = ProcessingResult(
                    text_content="",
                    document_type=DocumentType.UNKNOWN,
                    metadata={},
                    errors=[str(result)]
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results