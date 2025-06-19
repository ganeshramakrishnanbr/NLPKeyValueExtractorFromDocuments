from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

class CustomerInfo(BaseModel):
    """Primary information extracted from documents"""
    name: Optional[str] = Field(None, description="Person's full name")
    ssn: Optional[str] = Field(None, description="SSN/ID Number (XXX-XX-XXXX format)")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    address: Optional[str] = Field(None, description="Address information")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")

class PolicyInfo(BaseModel):
    """Secondary information extracted from documents"""
    policy_number: Optional[str] = Field(None, description="Account/Reference number")
    policy_type: Optional[str] = Field(None, description="Document type classification")
    coverage_amount: Optional[str] = Field(None, description="Amount or value found")
    premium: Optional[str] = Field(None, description="Additional information")

class DynamicExtractionRequest(BaseModel):
    """Request model for dynamic field extraction"""
    fields: List[str] = Field(..., description="List of fields to extract from the document")
    
    class Config:
        json_schema_extra = {
            "example": {
                "fields": ["name", "email", "phone", "address", "policy_number", "coverage_amount"]
            }
        }

class DynamicExtractionResult(BaseModel):
    """Result of dynamic field extraction"""
    document_type: str = Field(..., description="Classified document type")
    extracted_fields: Dict[str, Any] = Field(..., description="Dynamically extracted field values")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
    raw_text_preview: str = Field(..., description="Preview of extracted text (first 200 chars)")
    requested_fields: List[str] = Field(..., description="List of fields that were requested")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "employment_document",
                "extracted_fields": {
                    "name": "John Smith",
                    "email": "john.smith@email.com",
                    "phone": "(555) 123-4567",
                    "address": "123 Main St, Anytown, CA",
                    "employee_id": "EMP1234567",
                    "salary": "$75,000"
                },
                "confidence_score": 0.85,
                "processing_time": 2.3,
                "raw_text_preview": "EMPLOYMENT CONTRACT\nEmployee: John Smith\nEmail: john.smith@email.com...",
                "requested_fields": ["name", "email", "phone", "address", "employee_id", "salary"]
            }
        }

class ExtractionResult(BaseModel):
    """Complete result of document processing and information extraction"""
    document_type: str = Field(..., description="Classified document type")
    customer_info: CustomerInfo = Field(..., description="Extracted customer information")
    policy_info: PolicyInfo = Field(..., description="Extracted policy information")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
    raw_text_preview: str = Field(..., description="Preview of extracted text (first 200 chars)")

    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "employment_document",
                "customer_info": {
                    "name": "John Smith",
                    "ssn": "123-45-6789",
                    "date_of_birth": "01/15/1980",
                    "address": "123 Main St, Anytown, CA",
                    "phone": "555-123-4567",
                    "email": "john.smith@email.com"
                },
                "policy_info": {
                    "policy_number": "EMP1234567",
                    "policy_type": "Employment Document",
                    "coverage_amount": "$75,000",
                    "premium": "Additional Benefits"
                },
                "confidence_score": 0.85,
                "processing_time": 2.3,
                "raw_text_preview": "EMPLOYMENT CONTRACT\nEmployee: John Smith\nSSN: 123-45-6789\nDate of Birth: 01/15/1980\nAddress: 123 Main St, Anytown, CA 90210\nPhone: (555) 123-4567..."
            }
        }
