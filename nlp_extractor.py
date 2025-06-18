import spacy
import re
from typing import Dict, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsuranceNLPExtractor:
    """
    NLP-based information extractor for insurance documents.
    Uses spaCy for named entity recognition and regex patterns for structured data.
    """
    
    def __init__(self):
        """Initialize the NLP extractor with spaCy model"""
        try:
            # Load spaCy model - requires: python -m spacy download en_core_web_lg
            self.nlp = spacy.load("en_core_web_lg")
            logger.info("Successfully loaded spaCy en_core_web_lg model")
        except OSError:
            try:
                # Fallback to smaller model if large model not available
                self.nlp = spacy.load("en_core_web_sm")
                logger.warning("Large model not found, using en_core_web_sm")
            except OSError:
                raise Exception("No spaCy English model found. Please install with: python -m spacy download en_core_web_lg")
        
        # Compile regex patterns for better performance
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for structured data extraction"""
        self.ssn_pattern = re.compile(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b')
        self.phone_pattern = re.compile(r'\b(?:\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Date patterns
        self.date_patterns = [
            re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b'),      # MM/DD/YYYY
            re.compile(r'\b\d{1,2}-\d{1,2}-\d{4}\b'),      # MM-DD-YYYY
            re.compile(r'\b\d{4}-\d{1,2}-\d{1,2}\b'),      # YYYY-MM-DD
            re.compile(r'\b\d{1,2}\s+\w+\s+\d{4}\b'),      # DD Month YYYY
        ]
        
        # Policy number patterns
        self.policy_patterns = [
            re.compile(r'\b[A-Z]{2,3}\d{6,10}\b'),         # ABC1234567
            re.compile(r'\bPOL[-_]?\d{6,8}\b', re.I),      # POL-123456
            re.compile(r'\b\d{8,12}\b'),                   # Pure numeric
            re.compile(r'\b[A-Z]\d{7,9}\b'),               # A1234567
        ]
        
        # Currency patterns
        self.currency_pattern = re.compile(r'\$[\d,]+(?:\.\d{2})?')
        self.premium_pattern = re.compile(r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|annually|monthly))?', re.I)
    
    def extract_customer_info(self, text: str) -> Dict:
        """
        Extract customer information using NLP and regex patterns
        
        Args:
            text: Document text to extract information from
            
        Returns:
            Dictionary with extracted customer information
        """
        doc = self.nlp(text)
        
        result = {
            "name": self._extract_name(doc, text),
            "ssn": self._extract_ssn(text),
            "date_of_birth": self._extract_dob(text),
            "address": self._extract_address(doc, text),
            "phone": self._extract_phone(text),
            "email": self._extract_email(text)
        }
        
        # Log extraction results
        extracted_fields = [k for k, v in result.items() if v]
        logger.info(f"Extracted customer fields: {extracted_fields}")
        
        return result
    
    def extract_policy_info(self, text: str) -> Dict:
        """
        Extract policy information from document text
        
        Args:
            text: Document text to extract information from
            
        Returns:
            Dictionary with extracted policy information
        """
        result = {
            "policy_number": self._extract_policy_number(text),
            "policy_type": self._extract_policy_type(text),
            "coverage_amount": self._extract_coverage_amount(text),
            "premium": self._extract_premium(text)
        }
        
        # Log extraction results
        extracted_fields = [k for k, v in result.items() if v]
        logger.info(f"Extracted policy fields: {extracted_fields}")
        
        return result
    
    def _extract_name(self, doc, text: str) -> Optional[str]:
        """Extract person names using spaCy NER and contextual clues"""
        # First try spaCy NER
        persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        
        # Filter out common false positives
        filtered_persons = []
        for person in persons:
            if len(person.split()) >= 2 and not any(word.lower() in ['company', 'insurance', 'corp', 'inc'] for word in person.split()):
                filtered_persons.append(person)
        
        if filtered_persons:
            return filtered_persons[0]
        
        # Try contextual extraction
        name_contexts = [
            r'(?:insured|policyholder|policy\s*owner|name):\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s*,\s*the\s*insured)',
        ]
        
        for pattern in name_contexts:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_ssn(self, text: str) -> Optional[str]:
        """Extract Social Security Number"""
        match = self.ssn_pattern.search(text)
        if match:
            # Normalize format to XXX-XX-XXXX
            ssn = re.sub(r'[^\d]', '', match.group())
            if len(ssn) == 9:
                return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
        return None
    
    def _extract_dob(self, text: str) -> Optional[str]:
        """Extract date of birth using multiple date patterns"""
        # Look for dates near birth-related keywords
        birth_context = re.search(r'(?:date\s*of\s*birth|dob|born)[:\s]*([^\n]{0,30})', text, re.I)
        if birth_context:
            context_text = birth_context.group(1)
            for pattern in self.date_patterns:
                match = pattern.search(context_text)
                if match:
                    return match.group()
        
        # General date extraction as fallback
        for pattern in self.date_patterns:
            match = pattern.search(text)
            if match:
                return match.group()
        
        return None
    
    def _extract_address(self, doc, text: str) -> Optional[str]:
        """Extract address using spaCy NER and pattern matching"""
        # Extract locations using spaCy
        locations = []
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"] and len(ent.text.strip()) > 2:
                locations.append(ent.text.strip())
        
        # Look for structured address patterns
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Circle|Cir|Court|Ct)[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2}[,\s]*\d{5}'
        address_match = re.search(address_pattern, text, re.I)
        if address_match:
            return address_match.group().strip()
        
        # Return locations if found
        if locations:
            return ", ".join(locations[:3])  # Limit to 3 locations
        
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        match = self.phone_pattern.search(text)
        if match:
            # Format as (XXX) XXX-XXXX
            return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        match = self.email_pattern.search(text)
        return match.group() if match else None
    
    def _extract_policy_number(self, text: str) -> Optional[str]:
        """Extract policy number using multiple patterns"""
        # Look for policy numbers near relevant keywords
        policy_context = re.search(r'(?:policy\s*(?:number|#|no))[:\s]*([A-Z0-9\-_]{6,15})', text, re.I)
        if policy_context:
            return policy_context.group(1).strip()
        
        # Try general patterns
        for pattern in self.policy_patterns:
            match = pattern.search(text)
            if match:
                return match.group()
        
        return None
    
    def _extract_policy_type(self, text: str) -> Optional[str]:
        """Extract policy type based on keywords"""
        policy_types = {
            "Term Life": ["term life", "term insurance"],
            "Whole Life": ["whole life", "permanent life"],
            "Universal Life": ["universal life", "ul insurance"],
            "Variable Life": ["variable life", "variable universal"],
            "Health Insurance": ["health insurance", "medical insurance"],
            "Auto Insurance": ["auto insurance", "car insurance", "vehicle insurance"],
            "Disability Insurance": ["disability insurance", "income protection"]
        }
        
        text_lower = text.lower()
        for policy_type, keywords in policy_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return policy_type
        
        return None
    
    def _extract_coverage_amount(self, text: str) -> Optional[str]:
        """Extract coverage/benefit amount"""
        # Look for coverage amounts near relevant keywords
        coverage_contexts = [
            r'(?:coverage|benefit|death\s*benefit|face\s*amount)[:\s]*(\$[\d,]+(?:\.\d{2})?)',
            r'(\$[\d,]+(?:\.\d{2})?)\s*(?:coverage|benefit|death\s*benefit)',
        ]
        
        for pattern in coverage_contexts:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1)
        
        # Look for large dollar amounts (likely coverage amounts)
        large_amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
        for amount in large_amounts:
            # Convert to number for comparison
            num_amount = float(re.sub(r'[$,]', '', amount))
            if num_amount >= 10000:  # Assume coverage amounts are >= $10,000
                return amount
        
        return None
    
    def _extract_premium(self, text: str) -> Optional[str]:
        """Extract premium amount and frequency"""
        # Look for premium with frequency indicators
        premium_match = self.premium_pattern.search(text)
        if premium_match:
            return premium_match.group()
        
        # Look for premium near relevant keywords
        premium_contexts = [
            r'(?:premium|monthly|annual)[:\s]*(\$[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|annually|monthly))?)',
            r'(\$[\d,]+(?:\.\d{2})?)\s*(?:premium|monthly|annual)',
        ]
        
        for pattern in premium_contexts:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1)
        
        return None
    
    def calculate_confidence_score(self, extracted_data: Dict) -> float:
        """
        Calculate confidence score based on extracted fields
        
        Args:
            extracted_data: Dictionary with all extracted information
            
        Returns:
            Confidence score between 0 and 1
        """
        # Define field weights (more important fields have higher weights)
        field_weights = {
            'name': 0.15,
            'ssn': 0.15,
            'date_of_birth': 0.10,
            'address': 0.10,
            'phone': 0.08,
            'email': 0.07,
            'policy_number': 0.15,
            'policy_type': 0.10,
            'coverage_amount': 0.10,
            'premium': 0.08
        }
        
        total_weight = sum(field_weights.values())
        achieved_weight = 0
        
        for field, weight in field_weights.items():
            if field in extracted_data and extracted_data[field] and extracted_data[field].strip():
                achieved_weight += weight
        
        confidence = achieved_weight / total_weight
        return round(confidence, 2)
