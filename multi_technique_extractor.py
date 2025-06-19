import re
import logging
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter
import statistics

logger = logging.getLogger(__name__)

class MultiTechniqueExtractor:
    """
    Multi-technique NLP extraction system that compares different approaches
    and provides confidence scores for each method
    """
    
    def __init__(self):
        self.techniques = {
            "regex_pattern_matching": self._regex_pattern_matching,
            "fuzzy_string_matching": self._fuzzy_string_matching,
            "keyword_proximity_analysis": self._keyword_proximity_analysis,
            "levenshtein_distance_matching": self._levenshtein_distance_matching,
            "statistical_frequency_analysis": self._statistical_frequency_analysis,
            "context_aware_extraction": self._context_aware_extraction,
            "template_based_extraction": self._template_based_extraction,
            "position_based_extraction": self._position_based_extraction,
            "pattern_ensemble_method": self._pattern_ensemble_method,
            "confidence_weighted_extraction": self._confidence_weighted_extraction
        }
        
        # Initialize pattern libraries for each technique
        self._initialize_patterns()
        
    def _initialize_patterns(self):
        """Initialize pattern libraries and configurations for each technique"""
        
        # Regex patterns for different field types
        self.regex_patterns = {
            "name": [
                r'(?i)(?:name|full\s*name|customer\s*name|employee\s*name|insured\s*name)[:\s]*([A-Za-z\s]{2,50})',
                r'(?i)(?:first\s*name|last\s*name)[:\s]*([A-Za-z\s]{2,30})',
                r'(?i)name[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
            ],
            "email": [
                r'(?i)(?:email|e-mail|email\s*address)[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            "phone": [
                r'(?i)(?:phone|telephone|mobile|cell)[:\s]*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
                r'\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
            ],
            "ssn": [
                r'(?i)(?:ssn|social\s*security)[:\s]*(\d{3}-\d{2}-\d{4})',
                r'\b\d{3}-\d{2}-\d{4}\b'
            ],
            "address": [
                r'(?i)(?:address|street|residence)[:\s]*([0-9]+\s+[A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[A-Za-z\s,0-9]*)',
                r'\d+\s+[A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)'
            ],
            "date": [
                r'(?i)(?:date|born|birth)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b'
            ],
            "amount": [
                r'(?i)(?:amount|salary|premium|coverage)[:\s]*(\$?[\d,]+(?:\.\d{2})?)',
                r'\$[\d,]+(?:\.\d{2})?'
            ],
            "employee_id": [
                r'(?i)(?:employee\s*id|emp\s*id|id)[:\s]*([A-Z]{2,4}\d{3,8})',
                r'\b[A-Z]{2,4}\d{3,8}\b'
            ],
            "policy_number": [
                r'(?i)(?:policy\s*number|policy\s*no)[:\s]*([A-Z]{2,3}\d{6,10})',
                r'\b[A-Z]{2,3}\d{6,10}\b'
            ]
        }
        
        # Fuzzy matching keywords
        self.fuzzy_keywords = {
            "name": ["name", "full name", "customer name", "employee name", "insured name"],
            "email": ["email", "e-mail", "email address", "electronic mail"],
            "phone": ["phone", "telephone", "mobile", "cell phone", "contact number"],
            "ssn": ["ssn", "social security", "social security number", "tax id"],
            "address": ["address", "street address", "mailing address", "residence"],
            "date": ["date", "date of birth", "birth date", "dob"],
            "amount": ["amount", "salary", "premium", "coverage amount", "benefit amount"],
            "employee_id": ["employee id", "emp id", "employee number", "staff id"],
            "policy_number": ["policy number", "policy no", "contract number"]
        }
        
        # Context words for proximity analysis
        self.context_words = {
            "name": ["named", "called", "known as", "individual", "person"],
            "email": ["contact", "reach", "correspondence", "electronic"],
            "phone": ["call", "contact", "reach", "dial", "number"],
            "ssn": ["identification", "tax", "social", "security"],
            "address": ["located", "residing", "mailing", "street", "city"],
            "date": ["born", "age", "year", "month", "day"],
            "amount": ["dollars", "payment", "cost", "value", "worth"],
            "employee_id": ["identification", "badge", "staff", "employee"],
            "policy_number": ["contract", "agreement", "coverage", "insurance"]
        }
    
    def extract_with_multiple_techniques(self, text: str, requested_fields: List[str], 
                                       selected_techniques: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Extract fields using multiple techniques and return comparative results
        """
        if selected_techniques is None:
            selected_techniques = list(self.techniques.keys())
        
        results = {
            "technique_results": {},
            "consolidated_results": {},
            "technique_confidence_scores": {},
            "best_technique_per_field": {},
            "overall_technique_ranking": {}
        }
        
        # Run each selected technique
        for technique_name in selected_techniques:
            if technique_name in self.techniques:
                try:
                    technique_func = self.techniques[technique_name]
                    technique_result = technique_func(text, requested_fields)
                    
                    results["technique_results"][technique_name] = technique_result["extracted_fields"]
                    results["technique_confidence_scores"][technique_name] = technique_result["confidence_score"]
                    
                    logger.info(f"Technique '{technique_name}' completed with confidence: {technique_result['confidence_score']:.3f}")
                    
                except Exception as e:
                    logger.error(f"Error in technique '{technique_name}': {str(e)}")
                    results["technique_results"][technique_name] = {}
                    results["technique_confidence_scores"][technique_name] = 0.0
        
        # Consolidate results and find best techniques
        results["consolidated_results"] = self._consolidate_results(
            results["technique_results"], requested_fields
        )
        
        results["best_technique_per_field"] = self._find_best_technique_per_field(
            results["technique_results"], results["technique_confidence_scores"], requested_fields
        )
        
        results["overall_technique_ranking"] = self._rank_techniques_overall(
            results["technique_confidence_scores"]
        )
        
        return results
    
    def _regex_pattern_matching(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 1: Regex Pattern Matching"""
        extracted = {}
        successful_extractions = 0
        
        for field in fields:
            if field in self.regex_patterns:
                for pattern in self.regex_patterns[field]:
                    matches = re.findall(pattern, text)
                    if matches:
                        extracted[field] = matches[0] if isinstance(matches[0], str) else matches[0][0]
                        successful_extractions += 1
                        break
                
                if field not in extracted:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Regular expression pattern matching with predefined patterns"
        }
    
    def _fuzzy_string_matching(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 2: Fuzzy String Matching"""
        extracted = {}
        successful_extractions = 0
        
        # Split text into lines for better matching
        lines = text.split('\n')
        
        for field in fields:
            if field in self.fuzzy_keywords:
                best_match = None
                best_score = 0
                
                for line in lines:
                    for keyword in self.fuzzy_keywords[field]:
                        # Find best fuzzy match for the keyword in this line
                        match = process.extractOne(keyword, [line])
                        if match and match[1] > 70:  # Threshold for fuzzy matching
                            # Extract value after the matched keyword
                            value = self._extract_value_after_keyword(line, keyword)
                            if value and match[1] > best_score:
                                best_match = value
                                best_score = match[1]
                
                if best_match:
                    extracted[field] = best_match
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Fuzzy string matching with keyword variations"
        }
    
    def _keyword_proximity_analysis(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 3: Keyword Proximity Analysis"""
        extracted = {}
        successful_extractions = 0
        
        words = text.split()
        
        for field in fields:
            if field in self.fuzzy_keywords:
                best_value = None
                best_proximity = float('inf')
                
                for keyword in self.fuzzy_keywords[field]:
                    keyword_words = keyword.lower().split()
                    
                    # Find keyword position in text
                    for i in range(len(words) - len(keyword_words) + 1):
                        window = [w.lower() for w in words[i:i+len(keyword_words)]]
                        
                        # Check if this window matches the keyword
                        if self._fuzzy_match_window(window, keyword_words):
                            # Look for value in proximity (next 5 words)
                            for j in range(i + len(keyword_words), min(i + len(keyword_words) + 5, len(words))):
                                value = self._extract_structured_value(words[j], field)
                                if value:
                                    proximity = j - (i + len(keyword_words))
                                    if proximity < best_proximity:
                                        best_value = value
                                        best_proximity = proximity
                
                if best_value:
                    extracted[field] = best_value
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Keyword proximity analysis with distance weighting"
        }
    
    def _levenshtein_distance_matching(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 4: Levenshtein Distance Matching"""
        extracted = {}
        successful_extractions = 0
        
        lines = text.split('\n')
        
        for field in fields:
            if field in self.fuzzy_keywords:
                best_match = None
                best_distance = float('inf')
                
                for line in lines:
                    line_lower = line.lower()
                    
                    for keyword in self.fuzzy_keywords[field]:
                        keyword_lower = keyword.lower()
                        
                        # Find substring with minimum Levenshtein distance
                        for i in range(len(line_lower) - len(keyword_lower) + 1):
                            substring = line_lower[i:i+len(keyword_lower)]
                            distance = levenshtein_distance(substring, keyword_lower)
                            
                            # If distance is acceptable, extract value
                            if distance <= 2 and distance < best_distance:
                                value = self._extract_value_after_position(line, i + len(keyword_lower))
                                if value:
                                    best_match = value
                                    best_distance = distance
                
                if best_match:
                    extracted[field] = best_match
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Levenshtein distance matching with edit distance optimization"
        }
    
    def _statistical_frequency_analysis(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 5: Statistical Frequency Analysis"""
        extracted = {}
        successful_extractions = 0
        
        # Analyze text patterns and frequencies
        patterns = self._analyze_text_patterns(text)
        
        for field in fields:
            candidates = []
            
            if field == "name":
                candidates = patterns["capitalized_words"]
            elif field == "email":
                candidates = patterns["email_patterns"]
            elif field == "phone":
                candidates = patterns["phone_patterns"]
            elif field == "ssn":
                candidates = patterns["ssn_patterns"]
            elif field == "date":
                candidates = patterns["date_patterns"]
            elif field == "amount":
                candidates = patterns["amount_patterns"]
            elif field in ["employee_id", "policy_number"]:
                candidates = patterns["id_patterns"]
            
            # Select most frequent or highest confidence candidate
            if candidates:
                best_candidate = self._select_best_candidate(candidates, field)
                if best_candidate:
                    extracted[field] = best_candidate
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Statistical frequency analysis with pattern recognition"
        }
    
    def _context_aware_extraction(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 6: Context-Aware Extraction"""
        extracted = {}
        successful_extractions = 0
        
        sentences = re.split(r'[.!?]+', text)
        
        for field in fields:
            best_value = None
            best_context_score = 0
            
            if field in self.context_words:
                for sentence in sentences:
                    # Calculate context score for this sentence
                    context_score = 0
                    sentence_lower = sentence.lower()
                    
                    for context_word in self.context_words[field]:
                        if context_word in sentence_lower:
                            context_score += 1
                    
                    # If sentence has good context, try to extract value
                    if context_score > 0:
                        value = self._extract_from_sentence(sentence, field)
                        if value and context_score > best_context_score:
                            best_value = value
                            best_context_score = context_score
                
                if best_value:
                    extracted[field] = best_value
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Context-aware extraction using semantic context analysis"
        }
    
    def _template_based_extraction(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 7: Template-Based Extraction"""
        extracted = {}
        successful_extractions = 0
        
        # Identify document structure patterns
        structure = self._analyze_document_structure(text)
        
        for field in fields:
            value = None
            
            # Try to extract based on document structure
            if structure["has_form_structure"]:
                value = self._extract_from_form_structure(text, field)
            elif structure["has_table_structure"]:
                value = self._extract_from_table_structure(text, field)
            elif structure["has_list_structure"]:
                value = self._extract_from_list_structure(text, field)
            else:
                value = self._extract_from_freeform_text(text, field)
            
            if value:
                extracted[field] = value
                successful_extractions += 1
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Template-based extraction with structure recognition"
        }
    
    def _position_based_extraction(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 8: Position-Based Extraction"""
        extracted = {}
        successful_extractions = 0
        
        lines = text.split('\n')
        
        for field in fields:
            value = None
            
            # Look for field in common positions
            if field in ["name", "employee_id"]:
                # Usually in first few lines
                value = self._search_in_lines(lines[:5], field)
            elif field in ["ssn", "date"]:
                # Often in middle sections
                mid_start = len(lines) // 4
                mid_end = 3 * len(lines) // 4
                value = self._search_in_lines(lines[mid_start:mid_end], field)
            elif field in ["amount", "salary"]:
                # Often towards the end
                value = self._search_in_lines(lines[-10:], field)
            else:
                # Search entire document
                value = self._search_in_lines(lines, field)
            
            if value:
                extracted[field] = value
                successful_extractions += 1
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Position-based extraction using document layout analysis"
        }
    
    def _pattern_ensemble_method(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 9: Pattern Ensemble Method"""
        extracted = {}
        successful_extractions = 0
        
        # Combine multiple pattern approaches
        for field in fields:
            candidates = []
            
            # Collect candidates from different pattern methods
            if field in self.regex_patterns:
                for pattern in self.regex_patterns[field]:
                    matches = re.findall(pattern, text)
                    candidates.extend(matches)
            
            # Add fuzzy matching candidates
            if field in self.fuzzy_keywords:
                fuzzy_candidates = self._get_fuzzy_candidates(text, field)
                candidates.extend(fuzzy_candidates)
            
            # Vote on best candidate
            if candidates:
                best_candidate = self._vote_on_candidates(candidates, field)
                if best_candidate:
                    extracted[field] = best_candidate
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Pattern ensemble method with voting mechanism"
        }
    
    def _confidence_weighted_extraction(self, text: str, fields: List[str]) -> Dict[str, Any]:
        """Technique 10: Confidence-Weighted Extraction"""
        extracted = {}
        successful_extractions = 0
        
        for field in fields:
            candidates_with_scores = []
            
            # Get candidates from multiple methods with confidence scores
            candidates_with_scores.extend(self._get_regex_candidates_with_confidence(text, field))
            candidates_with_scores.extend(self._get_fuzzy_candidates_with_confidence(text, field))
            candidates_with_scores.extend(self._get_context_candidates_with_confidence(text, field))
            
            # Select candidate with highest weighted confidence
            if candidates_with_scores:
                best_candidate = max(candidates_with_scores, key=lambda x: x[1])
                if best_candidate[1] > 0.5:  # Minimum confidence threshold
                    extracted[field] = best_candidate[0]
                    successful_extractions += 1
                else:
                    extracted[field] = ""
            else:
                extracted[field] = ""
        
        confidence = successful_extractions / len(fields) if fields else 0.0
        
        return {
            "extracted_fields": extracted,
            "confidence_score": confidence,
            "method_details": "Confidence-weighted extraction with multi-method scoring"
        }
    
    # Helper methods for extraction techniques
    
    def _extract_value_after_keyword(self, line: str, keyword: str) -> str:
        """Extract value that appears after a keyword in a line"""
        line_lower = line.lower()
        keyword_lower = keyword.lower()
        
        pos = line_lower.find(keyword_lower)
        if pos != -1:
            remaining = line[pos + len(keyword):].strip()
            # Remove common separators
            remaining = re.sub(r'^[:\-=\s]+', '', remaining)
            # Extract first meaningful value
            match = re.match(r'^([^,\n\r]+)', remaining)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_value_after_position(self, line: str, position: int) -> str:
        """Extract value after a specific position in a line"""
        if position < len(line):
            remaining = line[position:].strip()
            remaining = re.sub(r'^[:\-=\s]+', '', remaining)
            match = re.match(r'^([^,\n\r]+)', remaining)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_structured_value(self, word: str, field_type: str) -> str:
        """Extract structured value based on field type"""
        if field_type == "email" and "@" in word:
            return word
        elif field_type == "phone" and re.match(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', word):
            return word
        elif field_type == "ssn" and re.match(r'\d{3}-\d{2}-\d{4}', word):
            return word
        elif field_type == "date" and re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', word):
            return word
        elif field_type in ["amount", "salary"] and re.match(r'\$?[\d,]+(?:\.\d{2})?', word):
            return word
        elif field_type in ["employee_id", "policy_number"] and re.match(r'[A-Z]{2,4}\d{3,8}', word):
            return word
        elif field_type == "name" and re.match(r'^[A-Z][a-z]+$', word) and len(word) > 2:
            return word
        
        return ""
    
    def _fuzzy_match_window(self, window: List[str], keyword_words: List[str]) -> bool:
        """Check if window fuzzy matches keyword words"""
        if len(window) != len(keyword_words):
            return False
        
        total_distance = sum(levenshtein_distance(w1, w2) for w1, w2 in zip(window, keyword_words))
        avg_distance = total_distance / len(window)
        
        return avg_distance <= 1.0  # Allow average of 1 character difference per word
    
    def _analyze_text_patterns(self, text: str) -> Dict[str, List[str]]:
        """Analyze text for various patterns"""
        patterns = {
            "capitalized_words": re.findall(r'\b[A-Z][a-z]{2,}\b', text),
            "email_patterns": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            "phone_patterns": re.findall(r'\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text),
            "ssn_patterns": re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text),
            "date_patterns": re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b', text),
            "amount_patterns": re.findall(r'\$[\d,]+(?:\.\d{2})?\b', text),
            "id_patterns": re.findall(r'\b[A-Z]{2,4}\d{3,8}\b', text)
        }
        
        return patterns
    
    def _select_best_candidate(self, candidates: List[str], field_type: str) -> str:
        """Select best candidate based on frequency and field type validation"""
        if not candidates:
            return ""
        
        # Count frequency of each candidate
        candidate_counts = Counter(candidates)
        
        # Filter valid candidates based on field type
        valid_candidates = []
        for candidate, count in candidate_counts.items():
            if self._validate_field_format(candidate, field_type):
                valid_candidates.append((candidate, count))
        
        if valid_candidates:
            # Return most frequent valid candidate
            return max(valid_candidates, key=lambda x: x[1])[0]
        
        # If no valid candidates, return most frequent
        return max(candidate_counts, key=candidate_counts.get)
    
    def _validate_field_format(self, value: str, field_type: str) -> bool:
        """Validate if value matches expected format for field type"""
        if field_type == "email":
            return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', value))
        elif field_type == "phone":
            return bool(re.match(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$', value))
        elif field_type == "ssn":
            return bool(re.match(r'^\d{3}-\d{2}-\d{4}$', value))
        elif field_type == "date":
            return bool(re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$', value))
        elif field_type in ["amount", "salary"]:
            return bool(re.match(r'^\$?[\d,]+(?:\.\d{2})?$', value))
        elif field_type in ["employee_id", "policy_number"]:
            return bool(re.match(r'^[A-Z]{2,4}\d{3,8}$', value))
        elif field_type == "name":
            return bool(re.match(r'^[A-Za-z\s]{2,50}$', value)) and len(value.split()) >= 2
        
        return True  # Default to valid for other field types
    
    def _analyze_document_structure(self, text: str) -> Dict[str, bool]:
        """Analyze document structure patterns"""
        lines = text.split('\n')
        
        # Check for form structure (field: value pairs)
        form_lines = sum(1 for line in lines if ':' in line and len(line.split(':')) == 2)
        has_form_structure = form_lines > len(lines) * 0.3
        
        # Check for table structure
        table_lines = sum(1 for line in lines if line.count('|') > 2 or line.count('\t') > 2)
        has_table_structure = table_lines > 3
        
        # Check for list structure
        list_lines = sum(1 for line in lines if re.match(r'^\s*[-*•]\s+', line) or re.match(r'^\s*\d+\.\s+', line))
        has_list_structure = list_lines > 3
        
        return {
            "has_form_structure": has_form_structure,
            "has_table_structure": has_table_structure,
            "has_list_structure": has_list_structure
        }
    
    def _extract_from_form_structure(self, text: str, field: str) -> str:
        """Extract from form-like structure"""
        lines = text.split('\n')
        
        if field in self.fuzzy_keywords:
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        label = parts[0].strip().lower()
                        value = parts[1].strip()
                        
                        for keyword in self.fuzzy_keywords[field]:
                            if fuzz.ratio(label, keyword.lower()) > 80:
                                return value
        
        return ""
    
    def _extract_from_table_structure(self, text: str, field: str) -> str:
        """Extract from table-like structure"""
        # Simple table extraction - can be enhanced
        return self._extract_from_form_structure(text, field)
    
    def _extract_from_list_structure(self, text: str, field: str) -> str:
        """Extract from list-like structure"""
        lines = text.split('\n')
        
        for line in lines:
            if re.match(r'^\s*[-*•]\s+', line) or re.match(r'^\s*\d+\.\s+', line):
                for keyword in self.fuzzy_keywords.get(field, []):
                    if keyword.lower() in line.lower():
                        # Extract value after keyword
                        return self._extract_value_after_keyword(line, keyword)
        
        return ""
    
    def _extract_from_freeform_text(self, text: str, field: str) -> str:
        """Extract from freeform text"""
        # Fall back to regex patterns
        if field in self.regex_patterns:
            for pattern in self.regex_patterns[field]:
                matches = re.findall(pattern, text)
                if matches:
                    return matches[0] if isinstance(matches[0], str) else matches[0][0]
        
        return ""
    
    def _search_in_lines(self, lines: List[str], field: str) -> str:
        """Search for field in specific lines"""
        for line in lines:
            if field in self.regex_patterns:
                for pattern in self.regex_patterns[field]:
                    matches = re.findall(pattern, line)
                    if matches:
                        return matches[0] if isinstance(matches[0], str) else matches[0][0]
        
        return ""
    
    def _get_fuzzy_candidates(self, text: str, field: str) -> List[str]:
        """Get candidates using fuzzy matching"""
        candidates = []
        lines = text.split('\n')
        
        if field in self.fuzzy_keywords:
            for line in lines:
                for keyword in self.fuzzy_keywords[field]:
                    if fuzz.partial_ratio(keyword.lower(), line.lower()) > 70:
                        value = self._extract_value_after_keyword(line, keyword)
                        if value:
                            candidates.append(value)
        
        return candidates
    
    def _vote_on_candidates(self, candidates: List[str], field_type: str) -> str:
        """Vote on best candidate from multiple sources"""
        if not candidates:
            return ""
        
        # Score candidates based on frequency and validity
        candidate_scores = {}
        
        for candidate in candidates:
            if candidate not in candidate_scores:
                candidate_scores[candidate] = 0
            
            # Add frequency score
            candidate_scores[candidate] += candidates.count(candidate)
            
            # Add validity bonus
            if self._validate_field_format(candidate, field_type):
                candidate_scores[candidate] += 5
        
        # Return highest scoring candidate
        return max(candidate_scores, key=candidate_scores.get) if candidate_scores else ""
    
    def _get_regex_candidates_with_confidence(self, text: str, field: str) -> List[Tuple[str, float]]:
        """Get regex candidates with confidence scores"""
        candidates = []
        
        if field in self.regex_patterns:
            for i, pattern in enumerate(self.regex_patterns[field]):
                matches = re.findall(pattern, text)
                if matches:
                    # Higher confidence for more specific patterns (later in list)
                    confidence = 0.8 + (i * 0.1)
                    for match in matches:
                        value = match if isinstance(match, str) else match[0]
                        candidates.append((value, confidence))
        
        return candidates
    
    def _get_fuzzy_candidates_with_confidence(self, text: str, field: str) -> List[Tuple[str, float]]:
        """Get fuzzy candidates with confidence scores"""
        candidates = []
        lines = text.split('\n')
        
        if field in self.fuzzy_keywords:
            for line in lines:
                for keyword in self.fuzzy_keywords[field]:
                    ratio = fuzz.partial_ratio(keyword.lower(), line.lower())
                    if ratio > 70:
                        value = self._extract_value_after_keyword(line, keyword)
                        if value:
                            confidence = ratio / 100.0
                            candidates.append((value, confidence))
        
        return candidates
    
    def _get_context_candidates_with_confidence(self, text: str, field: str) -> List[Tuple[str, float]]:
        """Get context candidates with confidence scores"""
        candidates = []
        sentences = re.split(r'[.!?]+', text)
        
        if field in self.context_words:
            for sentence in sentences:
                context_score = 0
                sentence_lower = sentence.lower()
                
                for context_word in self.context_words[field]:
                    if context_word in sentence_lower:
                        context_score += 1
                
                if context_score > 0:
                    value = self._extract_from_sentence(sentence, field)
                    if value:
                        confidence = min(context_score / len(self.context_words[field]), 1.0)
                        candidates.append((value, confidence))
        
        return candidates
    
    def _extract_from_sentence(self, sentence: str, field: str) -> str:
        """Extract value from a sentence"""
        if field in self.regex_patterns:
            for pattern in self.regex_patterns[field]:
                matches = re.findall(pattern, sentence)
                if matches:
                    return matches[0] if isinstance(matches[0], str) else matches[0][0]
        
        return ""
    
    def _consolidate_results(self, technique_results: Dict[str, Dict[str, str]], 
                           requested_fields: List[str]) -> Dict[str, str]:
        """Consolidate results from multiple techniques"""
        consolidated = {}
        
        for field in requested_fields:
            candidates = []
            
            # Collect all non-empty results for this field
            for technique_name, results in technique_results.items():
                if field in results and results[field].strip():
                    candidates.append(results[field])
            
            # Select best candidate (most frequent or first valid)
            if candidates:
                candidate_counts = Counter(candidates)
                consolidated[field] = max(candidate_counts, key=candidate_counts.get)
            else:
                consolidated[field] = ""
        
        return consolidated
    
    def _find_best_technique_per_field(self, technique_results: Dict[str, Dict[str, str]], 
                                     confidence_scores: Dict[str, float], 
                                     requested_fields: List[str]) -> Dict[str, str]:
        """Find best technique for each field"""
        best_techniques = {}
        
        for field in requested_fields:
            best_technique = None
            best_score = -1
            
            for technique_name, results in technique_results.items():
                if field in results and results[field].strip():
                    # Technique found a value for this field
                    score = confidence_scores.get(technique_name, 0.0)
                    if score > best_score:
                        best_score = score
                        best_technique = technique_name
            
            best_techniques[field] = best_technique or "none"
        
        return best_techniques
    
    def _rank_techniques_overall(self, confidence_scores: Dict[str, float]) -> Dict[str, int]:
        """Rank techniques by overall performance"""
        sorted_techniques = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)
        
        rankings = {}
        for i, (technique_name, score) in enumerate(sorted_techniques):
            rankings[technique_name] = i + 1
        
        return rankings
    
    def get_available_techniques(self) -> List[Dict[str, str]]:
        """Return list of available techniques with descriptions"""
        return [
            {
                "name": "regex_pattern_matching",
                "display_name": "Regex Pattern Matching",
                "description": "Uses regular expressions to find structured patterns in text"
            },
            {
                "name": "fuzzy_string_matching",
                "display_name": "Fuzzy String Matching",
                "description": "Matches keywords with tolerance for spelling variations"
            },
            {
                "name": "keyword_proximity_analysis",
                "display_name": "Keyword Proximity Analysis",
                "description": "Finds values near relevant keywords based on distance"
            },
            {
                "name": "levenshtein_distance_matching",
                "display_name": "Levenshtein Distance Matching",
                "description": "Uses edit distance to find similar text patterns"
            },
            {
                "name": "statistical_frequency_analysis",
                "display_name": "Statistical Frequency Analysis",
                "description": "Analyzes text patterns and selects most frequent matches"
            },
            {
                "name": "context_aware_extraction",
                "display_name": "Context-Aware Extraction",
                "description": "Uses semantic context to improve extraction accuracy"
            },
            {
                "name": "template_based_extraction",
                "display_name": "Template-Based Extraction",
                "description": "Recognizes document structure and extracts accordingly"
            },
            {
                "name": "position_based_extraction",
                "display_name": "Position-Based Extraction",
                "description": "Uses document layout and position patterns for extraction"
            },
            {
                "name": "pattern_ensemble_method",
                "display_name": "Pattern Ensemble Method",
                "description": "Combines multiple pattern approaches with voting"
            },
            {
                "name": "confidence_weighted_extraction",
                "display_name": "Confidence-Weighted Extraction",
                "description": "Weights results by confidence scores from multiple methods"
            }
        ]