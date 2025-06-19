"""
NLP Document Extraction API Backend

This is the main FastAPI backend application that provides intelligent document
processing capabilities through RESTful APIs. It handles document upload,
text extraction, field identification, and advanced NLP processing features.

Key Features:
- Multi-format document processing (PDF, DOCX, DOC, MD)
- Standard and custom field extraction
- Multi-technique comparative analysis
- Template learning and classification
- State compliance checking
- Advanced confidence scoring

Author: NLP Document Extraction Platform
Version: 2.0.0
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import tempfile
import os
import time
import logging
from pathlib import Path

# Configure logging for API operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.models.basic_models import ExtractionResult, CustomerInfo, PolicyInfo, DynamicExtractionResult
from backend.models.advanced_models import (
    AdvancedExtractionResult, TemplateListResponse, StateRequirementsResponse,
    TemplateLearnRequest, TemplateLearnResponse, HealthCheckAdvanced, APIInfoAdvanced,
    TechniqueInfo, TechniqueResult, MultiTechniqueAnalysisResult, MultiTechniqueRequest,
    TechniqueListResponse
)
from backend.processors.document_processor import DocumentProcessor
from backend.extractors.simple_extractor import SimpleDynamicExtractor
from backend.classifiers.template_classifier import AdvancedTemplateClassifier
from backend.classifiers.confidence_scorer import EnhancedConfidenceScorer
from backend.extractors.multi_technique_extractor import MultiTechniqueExtractor

app = FastAPI(
    title="NLP Document Extraction API Backend", 
    version="2.0.0",
    description="Intelligent document processing with advanced NLP capabilities"
)

# Initialize templates
templates = Jinja2Templates(directory="backend/templates")

# Initialize processors
document_processor = DocumentProcessor()
dynamic_extractor = SimpleDynamicExtractor()

# Initialize Phase 2 advanced components
template_classifier = AdvancedTemplateClassifier()
confidence_scorer = EnhancedConfidenceScorer()

# Initialize multi-technique extractor
multi_technique_extractor = MultiTechniqueExtractor()

@app.get("/")
async def root():
    """API backend - web interface moved to Django frontend"""
    return {
        "message": "NLP Document Extraction API Backend",
        "status": "active",
        "web_interface": "http://localhost:5000",
        "api_documentation": "/docs",
        "note": "Please use the Django frontend at http://localhost:5000 for the web interface"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API status"""
    return {
        "status": "healthy",
        "message": "NLP Document Extraction API is running",
        "timestamp": time.time()
    }

@app.post("/upload/", response_model=ExtractionResult)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process documents (PDF, DOCX, DOC, MD).
    
    This endpoint handles standard field extraction for common document types.
    It extracts predefined fields like names, addresses, phone numbers, etc.
    
    Args:
        file: The uploaded document file
        
    Returns:
        ExtractionResult: Contains extracted customer info, policy info, and metadata
    """
    start_time = time.time()
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    if file_extension not in document_processor.supported_formats:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format. Supported: {', '.join(document_processor.supported_formats)}"
        )
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract text
        extracted_text = document_processor.extract_text(temp_file_path, file_extension)
        
        # Classify document
        document_type = document_processor.classify_document_type(extracted_text)
        
        # Extract customer and policy information
        customer_info = dynamic_extractor.extract_customer_info(extracted_text)
        policy_info = dynamic_extractor.extract_policy_info(extracted_text)
        
        # Calculate confidence score
        confidence_score = dynamic_extractor.calculate_confidence_score(customer_info, policy_info)
        
        processing_time = round(time.time() - start_time, 2)
        
        return ExtractionResult(
            document_type=document_type,
            customer_info=customer_info,
            policy_info=policy_info,
            confidence_score=confidence_score,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass

@app.post("/extract-custom/", response_model=DynamicExtractionResult)
async def extract_custom_fields(file: UploadFile = File(...), fields: str = Form("")):
    """
    Extract custom user-defined fields from documents.
    
    This endpoint allows users to specify their own fields for extraction
    using comma-separated field names.
    
    Args:
        file: The uploaded document file
        fields: Comma-separated list of field names to extract
        
    Returns:
        DynamicExtractionResult: Contains extracted custom fields and metadata
    """
    start_time = time.time()
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not fields.strip():
        raise HTTPException(status_code=400, detail="No fields specified")
    
    # Parse requested fields
    requested_fields = [field.strip() for field in fields.split(',') if field.strip()]
    
    # Validate file type
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    if file_extension not in document_processor.supported_formats:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format. Supported: {', '.join(document_processor.supported_formats)}"
        )
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract text
        extracted_text = document_processor.extract_text(temp_file_path, file_extension)
        
        # Classify document
        document_type = document_processor.classify_document_type(extracted_text)
        
        # Extract custom fields
        extracted_fields = dynamic_extractor.extract_dynamic_fields(extracted_text, requested_fields)
        
        # Calculate confidence score
        confidence_score = dynamic_extractor.calculate_dynamic_confidence(extracted_fields, requested_fields)
        
        processing_time = round(time.time() - start_time, 2)
        
        return DynamicExtractionResult(
            document_type=document_type,
            extracted_fields=extracted_fields,
            requested_fields=requested_fields,
            confidence_score=confidence_score,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing custom extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)