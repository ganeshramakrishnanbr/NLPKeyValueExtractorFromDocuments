import re
from typing import Dict, Optional, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleDynamicExtractor:
    """
    Simplified dynamic extractor using regex patterns only (no spaCy dependency)
    """
    
    def __init__(self):
        self._compile_patterns()
        self._define_extraction_strategies()
    
    def _compile_patterns(self):
        """Compile regex patterns for common data types"""
        self.patterns = {
            'ssn': re.compile(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b'),
            'phone': re.compile(r'\b(?:\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'date': [
                re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b'),
                re.compile(r'\b\d{1,2}-\d{1,2}-\d{4}\b'),
                re.compile(r'\b\d{4}-\d{1,2}-\d{1,2}\b'),
                re.compile(r'\b\d{1,2}\s+\w+\s+\d{4}\b'),
            ],
            'currency': re.compile(r'\$[\d,]+(?:\.\d{2})?'),
            'policy_number': [
                re.compile(r'\b[A-Z]{2,3}\d{6,10}\b'),
                re.compile(r'\bPOL[-_]?\d{6,8}\b', re.I),
                re.compile(r'\b\d{8,12}\b'),
                re.compile(r'\b[A-Z]\d{7,9}\b'),
            ],
            'zip_code': re.compile(r'\b\d{5}(?:-\d{4})?\b'),
            'name': re.compile(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'),
        }
    
    def _define_extraction_strategies(self):
        """Define extraction strategies for different field types"""
        self.extraction_strategies = {
            'name': self._extract_name,
            'person_name': self._extract_name,
            'full_name': self._extract_name,
            'customer_name': self._extract_name,
            'ssn': self._extract_ssn,
            'social_security': self._extract_ssn,
            'social_security_number': self._extract_ssn,
            'phone': self._extract_phone,
            'phone_number': self._extract_phone,
            'telephone': self._extract_phone,
            'email': self._extract_email,
            'email_address': self._extract_email,
            'date_of_birth': self._extract_date_of_birth,
            'dob': self._extract_date_of_birth,
            'birth_date': self._extract_date_of_birth,
            'address': self._extract_address,
            'street_address': self._extract_address,
            'mailing_address': self._extract_address,
            'policy_number': self._extract_policy_number,
            'policy_id': self._extract_policy_number,
            'account_number': self._extract_account_number,
            'coverage_amount': self._extract_currency_amount,
            'benefit_amount': self._extract_currency_amount,
            'premium': self._extract_currency_amount,
            'amount': self._extract_currency_amount,
            'date': self._extract_date,
            'effective_date': self._extract_date,
            'expiration_date': self._extract_date,
            'company': self._extract_company,
            'organization': self._extract_company,
            'employer': self._extract_company,
            'department': self._extract_company,
            'business': self._extract_company,
            'firm': self._extract_company,
            'salary': self._extract_currency_amount,
            'wage': self._extract_currency_amount,
            'employee_id': self._extract_account_number,
            'customer_id': self._extract_account_number,
            'id_number': self._extract_account_number,
            'start_date': self._extract_date,
            'end_date': self._extract_date,
            'hire_date': self._extract_date,
            'position': self._extract_contextual_field,
            'title': self._extract_contextual_field,
            'job_title': self._extract_contextual_field,
            'manager': self._extract_name,
            'supervisor': self._extract_name,
        }
    
    def extract_custom_fields(self, text: str, field_list: List[str]) -> Dict[str, Any]:
        """Extract custom fields from text - returns exactly the requested fields"""
        results = {}
        
        # Initialize all requested fields with None
        for field in field_list:
            results[field.strip()] = None
        
        # Extract values for each requested field
        for field in field_list:
            field_clean = field.strip()
            field_lower = field_clean.lower().replace(' ', '_')
            
            if field_lower in self.extraction_strategies:
                value = self.extraction_strategies[field_lower](text)
            else:
                value = self._extract_contextual_field(text, field_clean)
            
            # Only assign if we found a value
            if value:
                results[field_clean] = value
        
        extracted_fields = [k for k, v in results.items() if v]
        logger.info(f"Requested fields: {field_list}")
        logger.info(f"Successfully extracted: {extracted_fields}")
        
        return results
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract person names using regex patterns"""
        name_contexts = [
            r'(?:name|insured|policyholder|policy\s*owner|customer):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\s*,\s*(?:the\s*)?(?:insured|policyholder))',
        ]
        
        for pattern in name_contexts:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).strip()
        
        # Fallback to general name pattern
        match = self.patterns['name'].search(text)
        return match.group() if match else None
    
    def _extract_ssn(self, text: str) -> Optional[str]:
        """Extract Social Security Number"""
        match = self.patterns['ssn'].search(text)
        if match:
            ssn = re.sub(r'[^\d]', '', match.group())
            if len(ssn) == 9:
                return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        match = self.patterns['phone'].search(text)
        if match:
            return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        match = self.patterns['email'].search(text)
        return match.group() if match else None
    
    def _extract_date_of_birth(self, text: str) -> Optional[str]:
        """Extract date of birth"""
        birth_context = re.search(r'(?:date\s*of\s*birth|dob|born)[:\s]*([^\n]{0,30})', text, re.I)
        if birth_context:
            context_text = birth_context.group(1)
            for pattern in self.patterns['date']:
                match = pattern.search(context_text)
                if match:
                    return match.group()
        return None
    
    def _extract_address(self, text: str) -> Optional[str]:
        """Extract address using pattern matching"""
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Circle|Cir|Court|Ct)[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2}[,\s]*\d{5}'
        address_match = re.search(address_pattern, text, re.I)
        if address_match:
            return address_match.group().strip()
        return None
    
    def _extract_policy_number(self, text: str) -> Optional[str]:
        """Extract policy number"""
        policy_context = re.search(r'(?:policy\s*(?:number|#|no))[:\s]*([A-Z0-9\-_]{6,15})', text, re.I)
        if policy_context:
            return policy_context.group(1).strip()
        
        for pattern in self.patterns['policy_number']:
            match = pattern.search(text)
            if match:
                return match.group()
        return None
    
    def _extract_account_number(self, text: str) -> Optional[str]:
        """Extract account number"""
        account_context = re.search(r'(?:account\s*(?:number|#|no))[:\s]*([A-Z0-9\-_]{6,15})', text, re.I)
        if account_context:
            return account_context.group(1).strip()
        return None
    
    def _extract_currency_amount(self, text: str) -> Optional[str]:
        """Extract currency amounts"""
        amounts = self.patterns['currency'].findall(text)
        if amounts:
            return max(amounts, key=lambda x: float(re.sub(r'[$,]', '', x)))
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract general date"""
        for pattern in self.patterns['date']:
            match = pattern.search(text)
            if match:
                return match.group()
        return None
    
    def _extract_company(self, text: str) -> Optional[str]:
        """Extract company names"""
        company_patterns = [
            r'([A-Z][A-Za-z\s]+(?:Inc|LLC|Corp|Corporation|Company|Co\.|Insurance))',
            r'([A-Z][A-Za-z\s]+ Insurance)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_contextual_field(self, text: str, field_name: str) -> Optional[str]:
        """Generic contextual extraction for custom field names"""
        field_patterns = [
            rf'(?:{re.escape(field_name)})[:\s]+([^\n\r]+?)(?:\n|\r|$)',
            rf'(?:{re.escape(field_name)})[:\s]+([^,;]+)',
            rf'{re.escape(field_name)}:\s*([^\n]+)',
        ]
        
        field_name_spaces = field_name.replace('_', ' ')
        if field_name_spaces != field_name:
            field_patterns.extend([
                rf'(?:{re.escape(field_name_spaces)})[:\s]+([^\n\r]+?)(?:\n|\r|$)',
                rf'(?:{re.escape(field_name_spaces)})[:\s]+([^,;]+)',
                rf'{re.escape(field_name_spaces)}:\s*([^\n]+)',
            ])
        
        for pattern in field_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                value = match.group(1).strip()
                value = re.sub(r'[.,;]+$', '', value)
                if len(value) > 0 and len(value) < 200:
                    return value
        
        return None
    
    def calculate_confidence_score(self, extracted_data: Dict, requested_fields: List[str]) -> float:
        """Calculate confidence score"""
        if not requested_fields:
            return 0.0
        
        extracted_count = sum(1 for field in requested_fields 
                            if field in extracted_data and 
                            extracted_data[field] and 
                            str(extracted_data[field]).strip())
        
        confidence = extracted_count / len(requested_fields)
        return round(confidence, 2)