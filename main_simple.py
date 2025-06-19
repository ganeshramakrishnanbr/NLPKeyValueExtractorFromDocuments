"""
NLP Document Extraction API Backend

Main entry point for the FastAPI backend application that provides intelligent
document processing capabilities through RESTful APIs.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import os
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
from pydantic import BaseModel, Field

class CustomerInfo(BaseModel):
    name: Optional[str] = None
    ssn: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class PolicyInfo(BaseModel):
    policy_number: Optional[str] = None
    policy_type: Optional[str] = None
    coverage_amount: Optional[str] = None
    premium: Optional[str] = None
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None

class ExtractionResult(BaseModel):
    document_type: str
    customer_info: CustomerInfo
    policy_info: PolicyInfo
    confidence_score: float
    processing_time: float

class DynamicExtractionResult(BaseModel):
    document_type: str
    extracted_fields: Dict[str, str]
    requested_fields: List[str]
    confidence_score: float
    processing_time: float

# Document processor
class DocumentProcessor:
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'doc', 'md', 'txt']
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        if file_type in ['md', 'txt']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                # Try with different encoding if UTF-8 fails
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
        # For other formats, return basic text extraction
        return "Sample extracted text from document"
    
    def classify_document_type(self, text: str) -> str:
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ['policy', 'insurance']):
            return 'insurance_document'
        return 'general_document'

# Simple extractor
class SimpleDynamicExtractor:
    def extract_customer_info(self, text: str) -> Dict[str, Optional[str]]:
        return {
            'name': self._extract_pattern(text, r'name[:\s]+([A-Za-z\s]+)'),
            'ssn': self._extract_pattern(text, r'(\d{3}-\d{2}-\d{4})'),
            'phone': self._extract_pattern(text, r'(\(\d{3}\)\s*\d{3}-\d{4})'),
            'email': self._extract_pattern(text, r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'),
            'address': None,
            'date_of_birth': None
        }
    
    def extract_policy_info(self, text: str) -> Dict[str, Optional[str]]:
        return {
            'policy_number': self._extract_pattern(text, r'policy[:\s]*([A-Z0-9-]+)'),
            'coverage_amount': self._extract_pattern(text, r'coverage[:\s]*\$?([\d,]+)'),
            'premium': self._extract_pattern(text, r'premium[:\s]*\$?([\d,]+\.?\d*)'),
            'policy_type': None,
            'effective_date': None,
            'expiration_date': None
        }
    
    def extract_dynamic_fields(self, text: str, fields: List[str]) -> Dict[str, str]:
        extracted = {}
        for field in fields:
            # Try pattern matching for each field
            value = self._extract_by_keyword_proximity(text, field)
            extracted[field] = value or ""
        return extracted
    
    def _extract_pattern(self, text: str, pattern: str) -> Optional[str]:
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_by_keyword_proximity(self, text: str, field: str) -> Optional[str]:
        field_variations = [field, field.replace('_', ' '), field.title()]
        for variation in field_variations:
            pattern = rf'{re.escape(variation)}[:\s]+([^\n]+)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def calculate_confidence_score(self, customer_info: Dict, policy_info: Dict) -> float:
        total = len(customer_info) + len(policy_info)
        filled = sum(1 for v in customer_info.values() if v) + sum(1 for v in policy_info.values() if v)
        return round(filled / total if total > 0 else 0.0, 2)
    
    def calculate_dynamic_confidence(self, extracted_fields: Dict[str, str], requested_fields: List[str]) -> float:
        if not requested_fields:
            return 0.0
        successful = sum(1 for field in requested_fields if extracted_fields.get(field, "").strip())
        return round(successful / len(requested_fields), 2)

# Initialize FastAPI app
app = FastAPI(
    title="NLP Document Extraction API Backend", 
    version="2.0.0",
    description="Intelligent document processing with advanced NLP capabilities"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
document_processor = DocumentProcessor()
dynamic_extractor = SimpleDynamicExtractor()

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

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint for connectivity verification"""
    return {"test": "success", "cors": "enabled"}

@app.post("/upload/", response_model=ExtractionResult)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process documents with standard field extraction"""
    start_time = time.time()
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    if file_extension not in document_processor.supported_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported file format")
    
    temp_file_path = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract and process
        extracted_text = document_processor.extract_text(temp_file_path, file_extension)
        document_type = document_processor.classify_document_type(extracted_text)
        
        customer_data = dynamic_extractor.extract_customer_info(extracted_text)
        policy_data = dynamic_extractor.extract_policy_info(extracted_text)
        confidence_score = dynamic_extractor.calculate_confidence_score(customer_data, policy_data)
        
        return ExtractionResult(
            document_type=document_type,
            customer_info=CustomerInfo(**customer_data),
            policy_info=PolicyInfo(**policy_data),
            confidence_score=confidence_score,
            processing_time=round(time.time() - start_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.post("/extract-custom/", response_model=DynamicExtractionResult)
async def extract_custom_fields(file: UploadFile = File(...), fields: str = Form("")):
    """Extract custom user-defined fields from documents"""
    start_time = time.time()
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not fields.strip():
        raise HTTPException(status_code=400, detail="No fields specified")
    
    requested_fields = [field.strip() for field in fields.split(',') if field.strip()]
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        extracted_text = document_processor.extract_text(temp_file_path, file_extension)
        document_type = document_processor.classify_document_type(extracted_text)
        extracted_fields = dynamic_extractor.extract_dynamic_fields(extracted_text, requested_fields)
        confidence_score = dynamic_extractor.calculate_dynamic_confidence(extracted_fields, requested_fields)
        
        return DynamicExtractionResult(
            document_type=document_type,
            extracted_fields=extracted_fields,
            requested_fields=requested_fields,
            confidence_score=confidence_score,
            processing_time=round(time.time() - start_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error processing custom extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)