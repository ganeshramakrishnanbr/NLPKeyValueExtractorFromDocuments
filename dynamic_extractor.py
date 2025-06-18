import spacy
import re
from typing import Dict, Optional, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicNLPExtractor:
    """
    Dynamic NLP-based information extractor that can extract custom fields
    specified by the user from any type of document.
    """
    
    def __init__(self):
        """Initialize the dynamic NLP extractor with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_lg")
            logger.info("Successfully loaded spaCy en_core_web_lg model")
        except OSError:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.warning("Large model not found, using en_core_web_sm")
            except OSError:
                raise Exception("No spaCy English model found. Please install with: python -m spacy download en_core_web_sm")
        
        # Compile common regex patterns
        self._compile_patterns()
        
        # Define common field extraction strategies
        self._define_extraction_strategies()
    
    def _compile_patterns(self):
        """Compile regex patterns for common data types"""
        self.patterns = {
            'ssn': re.compile(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b'),
            'phone': re.compile(r'\b(?:\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'date': [
                re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b'),      # MM/DD/YYYY
                re.compile(r'\b\d{1,2}-\d{1,2}-\d{4}\b'),      # MM-DD-YYYY
                re.compile(r'\b\d{4}-\d{1,2}-\d{1,2}\b'),      # YYYY-MM-DD
                re.compile(r'\b\d{1,2}\s+\w+\s+\d{4}\b'),      # DD Month YYYY
            ],
            'currency': re.compile(r'\$[\d,]+(?:\.\d{2})?'),
            'percentage': re.compile(r'\d+(?:\.\d+)?%'),
            'policy_number': [
                re.compile(r'\b[A-Z]{2,3}\d{6,10}\b'),         # ABC1234567
                re.compile(r'\bPOL[-_]?\d{6,8}\b', re.I),      # POL-123456
                re.compile(r'\b\d{8,12}\b'),                   # Pure numeric
                re.compile(r'\b[A-Z]\d{7,9}\b'),               # A1234567
            ],
            'zip_code': re.compile(r'\b\d{5}(?:-\d{4})?\b'),
            'url': re.compile(r'https?://[^\s<>"\']+'),
        }
    
    def _define_extraction_strategies(self):
        """Define extraction strategies for different field types"""
        self.extraction_strategies = {
            'name': self._extract_person_name,
            'person_name': self._extract_person_name,
            'full_name': self._extract_person_name,
            'customer_name': self._extract_person_name,
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
            'company': self._extract_organization,
            'organization': self._extract_organization,
            'employer': self._extract_organization,
        }
    
    def extract_custom_fields(self, text: str, field_list: List[str]) -> Dict[str, Any]:
        """
        Extract custom fields specified by the user from document text
        
        Args:
            text: Document text to extract information from
            field_list: List of field names to extract
            
        Returns:
            Dictionary with extracted field values
        """
        doc = self.nlp(text)
        results = {}
        
        for field in field_list:
            field_lower = field.lower().replace(' ', '_')
            
            # Try specific extraction strategy first
            if field_lower in self.extraction_strategies:
                value = self.extraction_strategies[field_lower](doc, text)
            else:
                # Use generic contextual extraction
                value = self._extract_contextual_field(text, field)
            
            results[field] = value
        
        # Log extraction results
        extracted_fields = [k for k, v in results.items() if v]
        logger.info(f"Extracted fields: {extracted_fields}")
        
        return results
    
    def _extract_person_name(self, doc, text: str) -> Optional[str]:
        """Extract person names using spaCy NER and contextual clues"""
        # Try spaCy NER first
        persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        
        # Filter out common false positives
        filtered_persons = []
        for person in persons:
            if (len(person.split()) >= 2 and 
                not any(word.lower() in ['company', 'insurance', 'corp', 'inc', 'llc'] for word in person.split())):
                filtered_persons.append(person)
        
        if filtered_persons:
            return filtered_persons[0]
        
        # Try contextual extraction
        name_contexts = [
            r'(?:name|insured|policyholder|policy\s*owner|customer):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\s*,\s*(?:the\s*)?(?:insured|policyholder))',
        ]
        
        for pattern in name_contexts:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_ssn(self, doc, text: str) -> Optional[str]:
        """Extract Social Security Number"""
        match = self.patterns['ssn'].search(text)
        if match:
            # Normalize format to XXX-XX-XXXX
            ssn = re.sub(r'[^\d]', '', match.group())
            if len(ssn) == 9:
                return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
        return None
    
    def _extract_phone(self, doc, text: str) -> Optional[str]:
        """Extract phone number"""
        match = self.patterns['phone'].search(text)
        if match:
            return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
        return None
    
    def _extract_email(self, doc, text: str) -> Optional[str]:
        """Extract email address"""
        match = self.patterns['email'].search(text)
        return match.group() if match else None
    
    def _extract_date_of_birth(self, doc, text: str) -> Optional[str]:
        """Extract date of birth using contextual search"""
        # Look for dates near birth-related keywords
        birth_context = re.search(r'(?:date\s*of\s*birth|dob|born)[:\s]*([^\n]{0,30})', text, re.I)
        if birth_context:
            context_text = birth_context.group(1)
            for pattern in self.patterns['date']:
                match = pattern.search(context_text)
                if match:
                    return match.group()
        
        return None
    
    def _extract_address(self, doc, text: str) -> Optional[str]:
        """Extract address using spaCy NER and pattern matching"""
        # Look for structured address patterns
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Circle|Cir|Court|Ct)[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2}[,\s]*\d{5}'
        address_match = re.search(address_pattern, text, re.I)
        if address_match:
            return address_match.group().strip()
        
        # Extract locations using spaCy
        locations = []
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"] and len(ent.text.strip()) > 2:
                locations.append(ent.text.strip())
        
        if locations:
            return ", ".join(locations[:3])  # Limit to 3 locations
        
        return None
    
    def _extract_policy_number(self, doc, text: str) -> Optional[str]:
        """Extract policy number using multiple patterns"""
        # Look for policy numbers near relevant keywords
        policy_context = re.search(r'(?:policy\s*(?:number|#|no))[:\s]*([A-Z0-9\-_]{6,15})', text, re.I)
        if policy_context:
            return policy_context.group(1).strip()
        
        # Try general patterns
        for pattern in self.patterns['policy_number']:
            match = pattern.search(text)
            if match:
                return match.group()
        
        return None
    
    def _extract_account_number(self, doc, text: str) -> Optional[str]:
        """Extract account number"""
        account_context = re.search(r'(?:account\s*(?:number|#|no))[:\s]*([A-Z0-9\-_]{6,15})', text, re.I)
        if account_context:
            return account_context.group(1).strip()
        return None
    
    def _extract_currency_amount(self, doc, text: str) -> Optional[str]:
        """Extract currency amounts"""
        amounts = self.patterns['currency'].findall(text)
        if amounts:
            # Return the largest amount found (likely coverage/benefit amount)
            return max(amounts, key=lambda x: float(re.sub(r'[$,]', '', x)))
        return None
    
    def _extract_date(self, doc, text: str) -> Optional[str]:
        """Extract general date"""
        for pattern in self.patterns['date']:
            match = pattern.search(text)
            if match:
                return match.group()
        return None
    
    def _extract_organization(self, doc, text: str) -> Optional[str]:
        """Extract organization names using spaCy NER"""
        orgs = [ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"]
        return orgs[0] if orgs else None
    
    def _extract_contextual_field(self, text: str, field_name: str) -> Optional[str]:
        """
        Generic contextual extraction for custom field names
        
        Args:
            text: Document text
            field_name: Name of the field to extract
            
        Returns:
            Extracted value or None
        """
        # Create patterns based on field name
        field_patterns = [
            rf'(?:{re.escape(field_name)})[:\s]+([^\n\r]+?)(?:\n|\r|$)',
            rf'(?:{re.escape(field_name)})[:\s]+([^,;]+)',
            rf'{re.escape(field_name)}:\s*([^\n]+)',
        ]
        
        # Also try with underscores replaced by spaces
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
                # Clean up the extracted value
                value = re.sub(r'[.,;]+$', '', value)  # Remove trailing punctuation
                if len(value) > 0 and len(value) < 200:  # Reasonable length
                    return value
        
        return None
    
    def calculate_confidence_score(self, extracted_data: Dict, requested_fields: List[str]) -> float:
        """
        Calculate confidence score based on extracted fields vs requested fields
        
        Args:
            extracted_data: Dictionary with all extracted information
            requested_fields: List of fields that were requested
            
        Returns:
            Confidence score between 0 and 1
        """
        if not requested_fields:
            return 0.0
        
        # Count successfully extracted fields
        extracted_count = sum(1 for field in requested_fields 
                            if field in extracted_data and 
                            extracted_data[field] and 
                            str(extracted_data[field]).strip())
        
        confidence = extracted_count / len(requested_fields)
        return round(confidence, 2)