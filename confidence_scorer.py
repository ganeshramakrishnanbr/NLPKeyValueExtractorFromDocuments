import re
from typing import Dict, List, Optional
import logging
import statistics

logger = logging.getLogger(__name__)

class EnhancedConfidenceScorer:
    """
    Enhanced confidence scoring system using multiple algorithms
    and validation techniques for document extraction
    """
    
    def __init__(self):
        # Field importance weights for confidence calculation
        self.field_weights = {
            # High importance fields
            "name": 0.15,
            "ssn": 0.20,
            "social_security_number": 0.20,
            "date_of_birth": 0.15,
            "dob": 0.15,
            "employee_id": 0.18,
            "policy_number": 0.18,
            "account_number": 0.18,
            
            # Medium importance fields
            "address": 0.10,
            "phone": 0.08,
            "phone_number": 0.08,
            "email": 0.08,
            "email_address": 0.08,
            "salary": 0.12,
            "amount": 0.10,
            "coverage_amount": 0.12,
            
            # Lower importance fields
            "department": 0.06,
            "company": 0.05,
            "organization": 0.05,
            "date": 0.05,
            "title": 0.04,
            "position": 0.04
        }
        
        # Pattern validation rules
        self.validation_patterns = {
            "ssn": r'^\d{3}-\d{2}-\d{4}$',
            "social_security_number": r'^\d{3}-\d{2}-\d{4}$',
            "phone": r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$',
            "phone_number": r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$',
            "email": r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$',
            "email_address": r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$',
            "employee_id": r'^[A-Z]{2,4}\d{3,8}$|^\d{6,10}$|^EMP\d{3,8}$',
            "policy_number": r'^[A-Z]{2,3}\d{6,10}$|^POL\d{6,8}$',
            "account_number": r'^\d{8,15}$|^ACC\d{6,10}$',
            "date_of_birth": r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$|^\d{4}[/-]\d{1,2}[/-]\d{1,2}$',
            "dob": r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$|^\d{4}[/-]\d{1,2}[/-]\d{1,2}$',
            "salary": r'^\$?[\d,]+(?:\.\d{2})?$',
            "amount": r'^\$?[\d,]+(?:\.\d{2})?$',
            "coverage_amount": r'^\$?[\d,]+(?:\.\d{2})?$'
        }
    
    def calculate_ensemble_confidence(self, 
                                    extracted_data: Dict, 
                                    template_classification: Dict = None,
                                    processing_metadata: Dict = None) -> Dict:
        """
        Calculate confidence using ensemble of multiple algorithms
        """
        try:
            # Algorithm 1: Field completion confidence
            completion_confidence = self._calculate_completion_confidence(extracted_data)
            
            # Algorithm 2: Pattern validation confidence
            validation_confidence = self._calculate_validation_confidence(extracted_data)
            
            # Algorithm 3: Template matching confidence
            template_confidence = self._calculate_template_confidence(template_classification)
            
            # Algorithm 4: Data quality confidence
            quality_confidence = self._calculate_data_quality_confidence(extracted_data)
            
            # Algorithm 5: Context consistency confidence
            consistency_confidence = self._calculate_consistency_confidence(extracted_data)
            
            # Weighted ensemble calculation
            overall_confidence = (
                0.25 * completion_confidence +
                0.25 * validation_confidence +
                0.20 * template_confidence +
                0.15 * quality_confidence +
                0.15 * consistency_confidence
            )
            
            # Risk assessment
            risk_factors = self._assess_risk_factors(extracted_data, overall_confidence)
            
            result = {
                "overall_confidence": round(overall_confidence, 3),
                "algorithm_scores": {
                    "completion_confidence": round(completion_confidence, 3),
                    "validation_confidence": round(validation_confidence, 3),
                    "template_confidence": round(template_confidence, 3),
                    "quality_confidence": round(quality_confidence, 3),
                    "consistency_confidence": round(consistency_confidence, 3)
                },
                "risk_assessment": risk_factors,
                "manual_review_required": overall_confidence < 0.75 or risk_factors["high_risk"],
                "quality_grade": self._assign_quality_grade(overall_confidence),
                "recommendations": self._generate_recommendations(overall_confidence, risk_factors)
            }
            
            logger.info(f"Ensemble confidence calculated: {overall_confidence:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating ensemble confidence: {str(e)}")
            return self._get_fallback_confidence()
    
    def _calculate_completion_confidence(self, extracted_data: Dict) -> float:
        """Calculate confidence based on field completion rates"""
        
        if not extracted_data:
            return 0.0
        
        # Handle both flat and nested data structures
        fields_to_check = {}
        
        if "extracted_fields" in extracted_data:
            fields_to_check = extracted_data["extracted_fields"]
        elif "customer_info" in extracted_data or "policy_info" in extracted_data:
            # Merge customer_info and policy_info
            customer_info = extracted_data.get("customer_info", {})
            policy_info = extracted_data.get("policy_info", {})
            fields_to_check = {**customer_info, **policy_info}
        else:
            fields_to_check = extracted_data
        
        total_weight = 0
        achieved_weight = 0
        
        for field_name, field_value in fields_to_check.items():
            field_weight = self.field_weights.get(field_name, 0.03)  # Default weight for unknown fields
            total_weight += field_weight
            
            if field_value and str(field_value).strip() and str(field_value).lower() != 'null':
                achieved_weight += field_weight
        
        return achieved_weight / total_weight if total_weight > 0 else 0.0
    
    def _calculate_validation_confidence(self, extracted_data: Dict) -> float:
        """Validate extracted data against known patterns"""
        
        # Get fields from data structure
        fields_to_validate = {}
        if "extracted_fields" in extracted_data:
            fields_to_validate = extracted_data["extracted_fields"]
        elif "customer_info" in extracted_data or "policy_info" in extracted_data:
            customer_info = extracted_data.get("customer_info", {})
            policy_info = extracted_data.get("policy_info", {})
            fields_to_validate = {**customer_info, **policy_info}
        else:
            fields_to_validate = extracted_data
        
        validation_scores = []
        
        for field_name, field_value in fields_to_validate.items():
            if field_value and str(field_value).strip():
                if field_name in self.validation_patterns:
                    pattern = self.validation_patterns[field_name]
                    is_valid = bool(re.match(pattern, str(field_value).strip()))
                    validation_scores.append(1.0 if is_valid else 0.0)
                else:
                    # For fields without specific patterns, check basic validity
                    basic_validity = self._check_basic_validity(field_name, str(field_value))
                    validation_scores.append(basic_validity)
        
        return statistics.mean(validation_scores) if validation_scores else 0.5
    
    def _check_basic_validity(self, field_name: str, field_value: str) -> float:
        """Check basic validity for fields without specific patterns"""
        
        value = field_value.strip()
        
        # Name fields should contain letters and reasonable length
        if 'name' in field_name.lower():
            if re.match(r'^[A-Za-z\s]{2,50}$', value):
                return 1.0
            elif re.match(r'^[A-Za-z\s.,]{2,}$', value):
                return 0.7
            else:
                return 0.3
        
        # Address fields should contain alphanumeric and reasonable length
        if 'address' in field_name.lower():
            if len(value) > 10 and re.search(r'\d', value):
                return 1.0
            elif len(value) > 5:
                return 0.7
            else:
                return 0.3
        
        # Department/company fields
        if any(term in field_name.lower() for term in ['department', 'company', 'organization']):
            if re.match(r'^[A-Za-z\s&.,]{2,}$', value):
                return 1.0
            else:
                return 0.5
        
        # Default validity check
        if len(value) > 1 and not value.isdigit():
            return 0.8
        
        return 0.5
    
    def _calculate_template_confidence(self, template_classification: Dict) -> float:
        """Calculate confidence based on template matching"""
        
        if not template_classification:
            return 0.5
        
        # Extract confidence indicators from template classification
        template_score = template_classification.get("template_match_score", 0.5)
        classification_confidence = template_classification.get("classification_confidence", 0.5)
        
        # Consider state compliance
        state_info = template_classification.get("state_regulations", {})
        state_confidence = 1.0 if state_info.get("compliance_needed", False) else 0.8
        
        # Weighted average
        template_confidence = (
            template_score * 0.5 +
            classification_confidence * 0.3 +
            state_confidence * 0.2
        )
        
        return template_confidence
    
    def _calculate_data_quality_confidence(self, extracted_data: Dict) -> float:
        """Assess overall data quality"""
        
        # Get fields from data structure
        fields_to_check = {}
        if "extracted_fields" in extracted_data:
            fields_to_check = extracted_data["extracted_fields"]
        elif "customer_info" in extracted_data or "policy_info" in extracted_data:
            customer_info = extracted_data.get("customer_info", {})
            policy_info = extracted_data.get("policy_info", {})
            fields_to_check = {**customer_info, **policy_info}
        else:
            fields_to_check = extracted_data
        
        quality_factors = []
        
        for field_name, field_value in fields_to_check.items():
            if field_value and str(field_value).strip():
                value = str(field_value).strip()
                
                # Length appropriateness
                if 'name' in field_name.lower():
                    length_score = 1.0 if 5 <= len(value) <= 50 else 0.5
                elif 'address' in field_name.lower():
                    length_score = 1.0 if 10 <= len(value) <= 100 else 0.7
                else:
                    length_score = 1.0 if 2 <= len(value) <= 100 else 0.6
                
                # Character variety (not just repeated characters)
                char_variety = len(set(value.lower())) / max(1, len(value))
                variety_score = min(1.0, char_variety * 2)
                
                # No suspicious patterns (like "N/A", "NULL", etc.)
                suspicious_patterns = ['n/a', 'null', 'none', 'unknown', '---', '***']
                suspicious_score = 0.0 if any(pattern in value.lower() for pattern in suspicious_patterns) else 1.0
                
                field_quality = (length_score + variety_score + suspicious_score) / 3
                quality_factors.append(field_quality)
        
        return statistics.mean(quality_factors) if quality_factors else 0.5
    
    def _calculate_consistency_confidence(self, extracted_data: Dict) -> float:
        """Check for consistency between related fields"""
        
        # Get fields from data structure
        fields_to_check = {}
        if "extracted_fields" in extracted_data:
            fields_to_check = extracted_data["extracted_fields"]
        elif "customer_info" in extracted_data or "policy_info" in extracted_data:
            customer_info = extracted_data.get("customer_info", {})
            policy_info = extracted_data.get("policy_info", {})
            fields_to_check = {**customer_info, **policy_info}
        else:
            fields_to_check = extracted_data
        
        consistency_scores = []
        
        # Check name consistency
        name_fields = [k for k in fields_to_check.keys() if 'name' in k.lower()]
        if len(name_fields) > 1:
            names = [str(fields_to_check[field]).strip() for field in name_fields 
                    if fields_to_check[field]]
            if len(names) > 1:
                # Simple consistency check - similar length and first word
                first_words = [name.split()[0] for name in names if name.split()]
                consistency = 1.0 if len(set(first_words)) == 1 else 0.5
                consistency_scores.append(consistency)
        
        # Check date consistency
        date_fields = [k for k in fields_to_check.keys() if 'date' in k.lower()]
        if date_fields:
            # Check if dates are in reasonable ranges
            current_year = 2024
            for field in date_fields:
                date_value = str(fields_to_check[field]) if fields_to_check[field] else ""
                years = re.findall(r'\b(19|20)\d{2}\b', date_value)
                if years:
                    year = int(years[0])
                    if 1900 <= year <= current_year:
                        consistency_scores.append(1.0)
                    else:
                        consistency_scores.append(0.0)
        
        # Check amount consistency
        amount_fields = [k for k in fields_to_check.keys() 
                        if any(term in k.lower() for term in ['amount', 'salary', 'premium'])]
        if amount_fields:
            for field in amount_fields:
                amount_value = str(fields_to_check[field]) if fields_to_check[field] else ""
                # Check if amount is reasonable (not too high/low)
                numbers = re.findall(r'[\d,]+', amount_value.replace('$', ''))
                if numbers:
                    try:
                        amount = float(numbers[0].replace(',', ''))
                        if 0 < amount < 10000000:  # Reasonable range
                            consistency_scores.append(1.0)
                        else:
                            consistency_scores.append(0.3)
                    except:
                        consistency_scores.append(0.5)
        
        return np.mean(consistency_scores) if consistency_scores else 0.8
    
    def _assess_risk_factors(self, extracted_data: Dict, overall_confidence: float) -> Dict:
        """Assess risk factors that might require manual review"""
        
        risk_factors = {
            "high_risk": False,
            "risk_reasons": [],
            "warning_signs": []
        }
        
        # Get fields from data structure
        fields_to_check = {}
        if "extracted_fields" in extracted_data:
            fields_to_check = extracted_data["extracted_fields"]
        elif "customer_info" in extracted_data or "policy_info" in extracted_data:
            customer_info = extracted_data.get("customer_info", {})
            policy_info = extracted_data.get("policy_info", {})
            fields_to_check = {**customer_info, **policy_info}
        else:
            fields_to_check = extracted_data
        
        # Risk Factor 1: Missing critical fields
        critical_fields = ['name', 'ssn', 'social_security_number', 'employee_id', 'policy_number']
        missing_critical = [field for field in critical_fields 
                           if field in fields_to_check and not fields_to_check[field]]
        
        if missing_critical:
            risk_factors["risk_reasons"].append(f"Missing critical fields: {missing_critical}")
            if len(missing_critical) > 1:
                risk_factors["high_risk"] = True
        
        # Risk Factor 2: Low validation scores
        if overall_confidence < 0.6:
            risk_factors["risk_reasons"].append("Overall confidence below threshold")
            risk_factors["high_risk"] = True
        
        # Risk Factor 3: Suspicious data patterns
        for field_name, field_value in fields_to_check.items():
            if field_value:
                value = str(field_value).lower()
                if any(pattern in value for pattern in ['test', 'sample', 'example', 'placeholder']):
                    risk_factors["warning_signs"].append(f"Suspicious value in {field_name}")
        
        # Risk Factor 4: Inconsistent formatting
        formatted_fields = ['ssn', 'phone', 'email']
        for field in formatted_fields:
            if field in fields_to_check and fields_to_check[field]:
                if field in self.validation_patterns:
                    pattern = self.validation_patterns[field]
                    if not re.match(pattern, str(fields_to_check[field]).strip()):
                        risk_factors["warning_signs"].append(f"Format issue in {field}")
        
        return risk_factors
    
    def _assign_quality_grade(self, confidence: float) -> str:
        """Assign quality grade based on confidence score"""
        
        if confidence >= 0.9:
            return "A"
        elif confidence >= 0.8:
            return "B"
        elif confidence >= 0.7:
            return "C"
        elif confidence >= 0.6:
            return "D"
        else:
            return "F"
    
    def _generate_recommendations(self, confidence: float, risk_factors: Dict) -> List[str]:
        """Generate recommendations based on confidence and risk assessment"""
        
        recommendations = []
        
        if confidence < 0.75:
            recommendations.append("Manual review recommended due to low confidence")
        
        if risk_factors["high_risk"]:
            recommendations.append("High risk factors detected - immediate review required")
        
        if risk_factors["warning_signs"]:
            recommendations.append("Data quality issues detected - verify suspicious fields")
        
        if confidence > 0.9:
            recommendations.append("High confidence extraction - safe for automated processing")
        elif confidence > 0.8:
            recommendations.append("Good confidence - spot check recommended")
        
        if not recommendations:
            recommendations.append("Standard processing acceptable")
        
        return recommendations
    
    def _get_fallback_confidence(self) -> Dict:
        """Return fallback confidence when errors occur"""
        return {
            "overall_confidence": 0.5,
            "algorithm_scores": {
                "completion_confidence": 0.5,
                "validation_confidence": 0.5,
                "template_confidence": 0.5,
                "quality_confidence": 0.5,
                "consistency_confidence": 0.5
            },
            "risk_assessment": {
                "high_risk": True,
                "risk_reasons": ["Error in confidence calculation"],
                "warning_signs": []
            },
            "manual_review_required": True,
            "quality_grade": "F",
            "recommendations": ["Manual review required due to processing error"]
        }