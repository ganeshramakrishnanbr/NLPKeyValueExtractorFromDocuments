"""
Enhanced Pydantic Models for Document Processing
"""

from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from enum import Enum

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    HTML = "html"
    TXT = "txt"
    RTF = "rtf"
    UNKNOWN = "unknown"

class ProcessingOptionsModel(BaseModel):
    """Configuration options for document processing"""
    enable_ocr: bool = True
    extract_tables: bool = True
    extract_images: bool = True
    enhance_images: bool = True
    perform_quality_check: bool = True
    ocr_languages: List[str] = ["en"]
    confidence_threshold: float = 0.7

class TableData(BaseModel):
    """Table extraction result"""
    page_number: int
    table_number: int
    data: List[List[str]]
    rows: int
    columns: int
    header: List[str]
    csv_string: str
    json_records: List[Dict[str, Any]]

class ImageData(BaseModel):
    """Image extraction and analysis result"""
    page_number: int
    image_number: int
    format: Optional[str]
    mode: Optional[str]
    size: List[int]
    width: int
    height: int
    aspect_ratio: float
    file_size: int
    sharpness: Optional[float]
    brightness: Optional[float]
    contrast: Optional[float]
    quality_score: Optional[float]
    enhanced: bool = False

class DocumentMetadata(BaseModel):
    """Document metadata information"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    page_count: Optional[int] = None
    file_size: int
    file_type: str
    encoding: Optional[str] = None
    
class EnhancedExtractionResult(BaseModel):
    """Complete enhanced document processing result"""
    document_type: str
    text_content: str
    metadata: Dict[str, Any]
    tables: List[Dict[str, Any]] = []
    images: List[Dict[str, Any]] = []
    quality_score: float = 0.0
    ocr_confidence: float = 0.0
    processing_time: float = 0.0
    errors: List[str] = []
    processing_options: Dict[str, Any] = {}

class BatchProcessingResult(BaseModel):
    """Batch processing result summary"""
    batch_id: str
    total_files: int
    processed_files: int
    processing_time: float
    results: List[Dict[str, Any]]

class HealthStatus(BaseModel):
    """System health status"""
    status: str
    version: str
    components: Dict[str, str]
    supported_formats: List[str]
    features: List[str]