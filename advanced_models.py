from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class AdvancedExtractionResult(BaseModel):
    """Result model for advanced extraction with template recognition"""
    document_type: str = Field(..., description="Primary document category")
    sub_category: str = Field(..., description="Detailed sub-category classification")
    extracted_fields: Dict[str, Any] = Field(..., description="Extracted field values")
    
    # Template Classification
    template_classification: Dict[str, Any] = Field(..., description="Template recognition results")
    
    # Enhanced Confidence Scoring
    confidence_analysis: Dict[str, Any] = Field(..., description="Multi-algorithm confidence analysis")
    
    # State Compliance
    state_regulations: Dict[str, Any] = Field(..., description="State-specific requirements")
    
    # Organization Information
    organizations: Dict[str, Any] = Field(..., description="Identified organizations/carriers")
    
    # Processing Metadata
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
    complexity_score: float = Field(..., ge=0.0, le=1.0, description="Document complexity score")
    raw_text_preview: str = Field(..., description="Preview of extracted text")
    requested_fields: List[str] = Field(..., description="Fields that were requested")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "employment_document",
                "sub_category": "employment_contract",
                "extracted_fields": {
                    "name": "John Smith",
                    "employee_id": "EMP001234",
                    "salary": "$85,000",
                    "department": "Engineering"
                },
                "template_classification": {
                    "primary_category": "employment_document",
                    "sub_category": "employment_contract",
                    "template_match_score": 0.92,
                    "classification_confidence": 0.88
                },
                "confidence_analysis": {
                    "overall_confidence": 0.91,
                    "quality_grade": "A",
                    "manual_review_required": False,
                    "algorithm_scores": {
                        "completion_confidence": 0.95,
                        "validation_confidence": 0.90,
                        "template_confidence": 0.88,
                        "quality_confidence": 0.92,
                        "consistency_confidence": 0.89
                    }
                },
                "state_regulations": {
                    "identified_states": ["california"],
                    "compliance_needed": True,
                    "multi_state": False
                },
                "organizations": {
                    "known_organizations": ["Acme Corporation"],
                    "primary_organization": "Acme Corporation"
                },
                "processing_time": 0.25,
                "complexity_score": 0.72,
                "raw_text_preview": "EMPLOYMENT CONTRACT\nEmployee: John Smith\nEmployee ID: EMP001234...",
                "requested_fields": ["name", "employee_id", "salary", "department"]
            }
        }

class TemplateInfo(BaseModel):
    """Information about document templates"""
    template_name: str = Field(..., description="Name of the template")
    category: str = Field(..., description="Template category")
    keywords: List[str] = Field(..., description="Key identifying terms")
    complexity: float = Field(..., ge=0.0, le=1.0, description="Template complexity score")
    learned_date: Optional[datetime] = Field(None, description="When template was learned")

class TemplateListResponse(BaseModel):
    """Response for template listing endpoint"""
    primary_categories: List[str] = Field(..., description="Available primary document categories")
    state_coverage: List[str] = Field(..., description="States with specific regulations")
    known_organizations: List[str] = Field(..., description="Recognized organizations")
    custom_templates: List[TemplateInfo] = Field(..., description="User-defined templates")
    total_templates: int = Field(..., description="Total number of available templates")

class StateRequirementsResponse(BaseModel):
    """Response for state-specific requirements"""
    state: str = Field(..., description="State name")
    requirements: Dict[str, List[str]] = Field(..., description="State-specific requirements")
    compliance_level: str = Field(..., description="Required compliance level")
    regulatory_authority: str = Field(..., description="Governing regulatory authority")
    
    class Config:
        json_schema_extra = {
            "example": {
                "state": "california",
                "requirements": {
                    "required_disclosures": ["California Privacy Notice", "Consumer Rights"],
                    "mandatory_components": ["Unruh Civil Rights Act compliance"],
                    "filing_requirements": ["California Department filing"]
                },
                "compliance_level": "Strict",
                "regulatory_authority": "California Department of Insurance"
            }
        }

class TemplateLearnRequest(BaseModel):
    """Request to learn new template"""
    template_name: str = Field(..., description="Name for the new template")
    sample_text: str = Field(..., description="Sample text to learn from")
    category: Optional[str] = Field(None, description="Optional category assignment")
    
class TemplateLearnResponse(BaseModel):
    """Response for template learning"""
    success: bool = Field(..., description="Whether learning was successful")
    template_name: str = Field(..., description="Name of the learned template")
    extracted_keywords: List[str] = Field(..., description="Keywords extracted from template")
    message: str = Field(..., description="Status message")

class AdvancedProcessingRequest(BaseModel):
    """Request for advanced processing with specific options"""
    enable_template_learning: bool = Field(False, description="Learn from this document")
    state_compliance_check: bool = Field(True, description="Check state compliance")
    organization_detection: bool = Field(True, description="Detect organizations")
    enhanced_validation: bool = Field(True, description="Use enhanced validation")
    
class BatchProcessingRequest(BaseModel):
    """Request for batch processing multiple documents"""
    processing_options: AdvancedProcessingRequest = Field(..., description="Processing options")
    fields: Optional[str] = Field("", description="Comma-separated fields to extract")

class BatchProcessingResponse(BaseModel):
    """Response for batch processing"""
    total_documents: int = Field(..., description="Total documents processed")
    successful_extractions: int = Field(..., description="Successful extractions")
    failed_extractions: int = Field(..., description="Failed extractions")
    results: List[AdvancedExtractionResult] = Field(..., description="Individual results")
    batch_processing_time: float = Field(..., description="Total batch processing time")
    average_confidence: float = Field(..., description="Average confidence across all documents")

class HealthCheckAdvanced(BaseModel):
    """Enhanced health check response"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    timestamp: float = Field(..., description="Current timestamp")
    advanced_features: Dict[str, bool] = Field(..., description="Advanced feature availability")
    template_count: int = Field(..., description="Number of available templates")
    supported_states: int = Field(..., description="Number of states with regulations")
    
class APIInfoAdvanced(BaseModel):
    """Enhanced API information"""
    message: str = Field(..., description="API description")
    version: str = Field(..., description="API version")
    supported_formats: List[str] = Field(..., description="Supported file formats")
    endpoints: Dict[str, str] = Field(..., description="Available endpoints")
    advanced_features: List[str] = Field(..., description="Advanced capabilities")
    template_categories: List[str] = Field(..., description="Available template categories")

class TechniqueInfo(BaseModel):
    """Information about an extraction technique"""
    name: str = Field(..., description="Technical name of the technique")
    display_name: str = Field(..., description="User-friendly display name")
    description: str = Field(..., description="Description of how the technique works")

class TechniqueResult(BaseModel):
    """Result from a single extraction technique"""
    technique_name: str = Field(..., description="Name of the technique used")
    extracted_fields: Dict[str, str] = Field(..., description="Fields extracted by this technique")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for this technique")
    method_details: str = Field(..., description="Details about the extraction method")

class MultiTechniqueAnalysisResult(BaseModel):
    """Result from multi-technique comparative analysis"""
    document_summary: Dict[str, str] = Field(..., description="Basic document information")
    technique_results: List[TechniqueResult] = Field(..., description="Results from each technique")
    consolidated_results: Dict[str, str] = Field(..., description="Best consolidated extraction results")
    technique_confidence_scores: Dict[str, float] = Field(..., description="Confidence scores for each technique")
    best_technique_per_field: Dict[str, str] = Field(..., description="Best technique for each field")
    overall_technique_ranking: Dict[str, int] = Field(..., description="Overall ranking of techniques")
    processing_time: float = Field(..., description="Total processing time")
    requested_fields: List[str] = Field(..., description="Fields that were requested")
    selected_techniques: List[str] = Field(..., description="Techniques that were selected for analysis")

class MultiTechniqueRequest(BaseModel):
    """Request for multi-technique analysis"""
    selected_techniques: List[str] = Field(..., description="List of techniques to use for analysis")
    fields: Optional[str] = Field("", description="Comma-separated fields to extract")

class TechniqueListResponse(BaseModel):
    """Response listing available extraction techniques"""
    available_techniques: List[TechniqueInfo] = Field(..., description="List of available extraction techniques")
    total_techniques: int = Field(..., description="Total number of available techniques")
    recommended_techniques: List[str] = Field(..., description="Recommended techniques for general use")