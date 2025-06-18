from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

class CustomerInfo(BaseModel):
    """Customer information extracted from insurance documents"""
    name: Optional[str] = Field(None, description="Customer's full name")
    ssn: Optional[str] = Field(None, description="Social Security Number (XXX-XX-XXXX format)")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    address: Optional[str] = Field(None, description="Customer's address")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")

class PolicyInfo(BaseModel):
    """Policy information extracted from insurance documents"""
    policy_number: Optional[str] = Field(None, description="Policy identification number")
    policy_type: Optional[str] = Field(None, description="Type of insurance policy")
    coverage_amount: Optional[str] = Field(None, description="Coverage amount or benefit")
    premium: Optional[str] = Field(None, description="Premium amount and frequency")

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
                "document_type": "life_insurance",
                "extracted_fields": {
                    "name": "John Smith",
                    "email": "john.smith@email.com",
                    "phone": "(555) 123-4567",
                    "address": "123 Main St, Anytown, CA",
                    "policy_number": "LIF1234567",
                    "coverage_amount": "$500,000"
                },
                "confidence_score": 0.85,
                "processing_time": 2.3,
                "raw_text_preview": "LIFE INSURANCE POLICY\nPolicyowner: John Smith\nEmail: john.smith@email.com...",
                "requested_fields": ["name", "email", "phone", "address", "policy_number", "coverage_amount"]
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
                "document_type": "life_insurance",
                "customer_info": {
                    "name": "John Smith",
                    "ssn": "123-45-6789",
                    "date_of_birth": "01/15/1980",
                    "address": "123 Main St, Anytown, CA",
                    "phone": "555-123-4567",
                    "email": "john.smith@email.com"
                },
                "policy_info": {
                    "policy_number": "LIF1234567",
                    "policy_type": "Term Life",
                    "coverage_amount": "$500,000",
                    "premium": "$85.50/month"
                },
                "confidence_score": 0.85,
                "processing_time": 2.3,
                "raw_text_preview": "LIFE INSURANCE POLICY\nPolicyowner: John Smith\nSSN: 123-45-6789\nDate of Birth: 01/15/1980\nAddress: 123 Main St, Anytown, CA 90210\nPhone: (555) 123-4567..."
            }
        }
