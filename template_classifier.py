import re
from typing import Dict, List, Tuple, Optional
import json
import logging
from collections import Counter

logger = logging.getLogger(__name__)

class AdvancedTemplateClassifier:
    """
    Advanced template classification system for document varieties
    with state-specific regulation identification
    """
    
    def __init__(self):
        self.template_embeddings = {}
        self.template_keywords = {}
        self.state_regulations = {}
        self.load_template_database()
    
    def load_template_database(self):
        """Load or initialize template database for document varieties"""
        
        # Document type categories with comprehensive patterns
        self.product_categories = {
            "employment_document": [
                "employment", "employee", "job", "work", "position", "salary", "wage",
                "contract", "hire", "staff", "personnel", "benefits", "compensation"
            ],
            "financial_document": [
                "financial", "bank", "account", "transaction", "payment", "money",
                "credit", "debit", "balance", "statement", "invoice", "receipt"
            ],
            "insurance_document": [
                "insurance", "policy", "coverage", "premium", "claim", "benefit",
                "insured", "beneficiary", "carrier", "underwriter", "risk"
            ],
            "legal_document": [
                "legal", "contract", "agreement", "terms", "conditions", "clause",
                "party", "signatory", "witness", "notary", "jurisdiction"
            ],
            "medical_document": [
                "medical", "health", "patient", "doctor", "physician", "treatment",
                "diagnosis", "prescription", "medication", "hospital", "clinic"
            ],
            "educational_document": [
                "education", "student", "school", "university", "college", "degree",
                "certificate", "transcript", "course", "academic", "learning"
            ],
            "identification_document": [
                "identification", "identity", "passport", "license", "permit",
                "certificate", "registration", "credential", "authorization"
            ],
            "real_estate_document": [
                "real estate", "property", "mortgage", "deed", "title", "lease",
                "rental", "tenant", "landlord", "appraisal", "inspection"
            ],
            "tax_document": [
                "tax", "taxes", "irs", "filing", "return", "deduction", "income",
                "withholding", "refund", "assessment", "liability"
            ],
            "business_document": [
                "business", "company", "corporation", "llc", "partnership",
                "enterprise", "commercial", "trade", "industry", "market"
            ]
        }
        
        # State-specific patterns for all 50 US states
        self.state_patterns = {
            "alabama": ["AL", "Alabama", "Yellowhammer State"],
            "alaska": ["AK", "Alaska", "Last Frontier"],
            "arizona": ["AZ", "Arizona", "Grand Canyon State"],
            "arkansas": ["AR", "Arkansas", "Natural State"],
            "california": ["CA", "California", "Golden State", "Calif"],
            "colorado": ["CO", "Colorado", "Centennial State"],
            "connecticut": ["CT", "Connecticut", "Constitution State"],
            "delaware": ["DE", "Delaware", "First State"],
            "florida": ["FL", "Florida", "Sunshine State"],
            "georgia": ["GA", "Georgia", "Peach State"],
            "hawaii": ["HI", "Hawaii", "Aloha State"],
            "idaho": ["ID", "Idaho", "Gem State"],
            "illinois": ["IL", "Illinois", "Prairie State"],
            "indiana": ["IN", "Indiana", "Hoosier State"],
            "iowa": ["IA", "Iowa", "Hawkeye State"],
            "kansas": ["KS", "Kansas", "Sunflower State"],
            "kentucky": ["KY", "Kentucky", "Bluegrass State"],
            "louisiana": ["LA", "Louisiana", "Pelican State"],
            "maine": ["ME", "Maine", "Pine Tree State"],
            "maryland": ["MD", "Maryland", "Old Line State"],
            "massachusetts": ["MA", "Massachusetts", "Bay State"],
            "michigan": ["MI", "Michigan", "Great Lakes State"],
            "minnesota": ["MN", "Minnesota", "North Star State"],
            "mississippi": ["MS", "Mississippi", "Magnolia State"],
            "missouri": ["MO", "Missouri", "Show Me State"],
            "montana": ["MT", "Montana", "Big Sky Country"],
            "nebraska": ["NE", "Nebraska", "Cornhusker State"],
            "nevada": ["NV", "Nevada", "Silver State"],
            "new_hampshire": ["NH", "New Hampshire", "Live Free or Die"],
            "new_jersey": ["NJ", "New Jersey", "Garden State"],
            "new_mexico": ["NM", "New Mexico", "Land of Enchantment"],
            "new_york": ["NY", "New York", "Empire State"],
            "north_carolina": ["NC", "North Carolina", "Tar Heel State"],
            "north_dakota": ["ND", "North Dakota", "Peace Garden State"],
            "ohio": ["OH", "Ohio", "Buckeye State"],
            "oklahoma": ["OK", "Oklahoma", "Sooner State"],
            "oregon": ["OR", "Oregon", "Beaver State"],
            "pennsylvania": ["PA", "Pennsylvania", "Keystone State"],
            "rhode_island": ["RI", "Rhode Island", "Ocean State"],
            "south_carolina": ["SC", "South Carolina", "Palmetto State"],
            "south_dakota": ["SD", "South Dakota", "Mount Rushmore State"],
            "tennessee": ["TN", "Tennessee", "Volunteer State"],
            "texas": ["TX", "Texas", "Lone Star State"],
            "utah": ["UT", "Utah", "Beehive State"],
            "vermont": ["VT", "Vermont", "Green Mountain State"],
            "virginia": ["VA", "Virginia", "Old Dominion"],
            "washington": ["WA", "Washington", "Evergreen State"],
            "west_virginia": ["WV", "West Virginia", "Mountain State"],
            "wisconsin": ["WI", "Wisconsin", "Badger State"],
            "wyoming": ["WY", "Wyoming", "Equality State"]
        }
        
        # Major organizations/carriers
        self.major_organizations = [
            "Aetna", "Anthem", "Blue Cross", "Blue Shield", "Cigna", "Humana",
            "UnitedHealth", "Kaiser Permanente", "MetLife", "Prudential",
            "State Farm", "Allstate", "GEICO", "Progressive", "Nationwide",
            "Liberty Mutual", "Travelers", "AIG", "Chubb", "Hartford"
        ]
    
    def classify_document_advanced(self, text: str) -> Dict:
        """
        Advanced document classification with template recognition
        """
        try:
            # Step 1: Primary category classification
            primary_category = self._classify_primary_category(text)
            
            # Step 2: Sub-category classification
            sub_category = self._classify_sub_category(text, primary_category)
            
            # Step 3: State-specific identification
            state_info = self._identify_state_regulations(text)
            
            # Step 4: Organization/carrier identification
            organization_info = self._identify_organizations(text)
            
            # Step 5: Document complexity analysis
            complexity_score = self._analyze_document_complexity(text)
            
            # Step 6: Template similarity scoring
            template_score = self._calculate_template_similarity(text, primary_category)
            
            result = {
                "primary_category": primary_category,
                "sub_category": sub_category,
                "state_regulations": state_info,
                "organizations": organization_info,
                "complexity_score": complexity_score,
                "template_match_score": template_score,
                "classification_confidence": self._calculate_classification_confidence(text, primary_category)
            }
            
            logger.info(f"Advanced classification completed: {primary_category}")
            return result
            
        except Exception as e:
            logger.error(f"Error in advanced classification: {str(e)}")
            return self._get_fallback_classification()
    
    def _classify_primary_category(self, text: str) -> str:
        """Classify into main document categories using keyword scoring"""
        text_lower = text.lower()
        
        category_scores = {}
        for category, keywords in self.product_categories.items():
            score = 0
            for keyword in keywords:
                # Count occurrences with partial matching
                if keyword in text_lower:
                    score += text_lower.count(keyword) * len(keyword)
            
            # Normalize by category keyword count
            category_scores[category] = score / len(keywords) if keywords else 0
        
        # Return category with highest score
        if category_scores:
            best_category = max(category_scores.keys(), key=lambda k: category_scores[k])
            return best_category if category_scores[best_category] > 0 else "general_document"
        return "general_document"
    
    def _classify_sub_category(self, text: str, primary_category: str) -> str:
        """Detailed sub-category classification based on primary category"""
        
        # Define sub-categories for each primary category
        sub_categories = {
            "employment_document": {
                "employment_contract": ["contract", "agreement", "terms of employment"],
                "payroll_document": ["payroll", "paycheck", "salary statement"],
                "benefits_summary": ["benefits", "health plan", "retirement"],
                "performance_review": ["review", "evaluation", "performance"],
                "job_application": ["application", "resume", "cv", "cover letter"]
            },
            "financial_document": {
                "bank_statement": ["statement", "account summary", "balance"],
                "loan_document": ["loan", "mortgage", "credit agreement"],
                "investment_report": ["investment", "portfolio", "returns"],
                "tax_document": ["tax", "w-2", "1099", "tax return"],
                "invoice": ["invoice", "bill", "payment request"]
            },
            "insurance_document": {
                "life_insurance": ["life insurance", "death benefit", "life policy"],
                "health_insurance": ["health insurance", "medical coverage"],
                "auto_insurance": ["auto insurance", "vehicle coverage"],
                "property_insurance": ["property insurance", "homeowners"],
                "disability_insurance": ["disability", "income protection"]
            },
            "legal_document": {
                "contract": ["contract", "agreement", "binding"],
                "will_testament": ["will", "testament", "inheritance"],
                "power_attorney": ["power of attorney", "legal authority"],
                "court_document": ["court", "legal proceeding", "lawsuit"],
                "deed": ["deed", "property transfer", "title"]
            }
        }
        
        if primary_category in sub_categories:
            text_lower = text.lower()
            sub_scores = {}
            
            for sub_cat, keywords in sub_categories[primary_category].items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                sub_scores[sub_cat] = score
            
            if sub_scores and max(sub_scores.values()) > 0:
                return max(sub_scores.keys(), key=lambda k: sub_scores[k])
        
        return "standard"
    
    def _identify_state_regulations(self, text: str) -> Dict:
        """Identify state-specific regulations and requirements"""
        
        identified_states = []
        state_requirements = {}
        
        text_upper = text.upper()
        
        # Check for state mentions
        for state, patterns in self.state_patterns.items():
            for pattern in patterns:
                if pattern.upper() in text_upper:
                    identified_states.append(state)
                    break
        
        # Get state-specific requirements
        for state in identified_states:
            state_requirements[state] = self._get_state_requirements(state)
        
        return {
            "identified_states": identified_states,
            "requirements": state_requirements,
            "compliance_needed": len(state_requirements) > 0,
            "multi_state": len(identified_states) > 1
        }
    
    def _get_state_requirements(self, state: str) -> Dict:
        """Get specific requirements for each state"""
        
        # State-specific requirements database
        state_reqs = {
            "california": {
                "required_disclosures": ["California Privacy Notice", "Consumer Rights"],
                "mandatory_components": ["Unruh Civil Rights Act compliance"],
                "filing_requirements": ["California Department filing"],
                "regulatory_implications": ["CCPA compliance required"]
            },
            "new_york": {
                "required_disclosures": ["New York Insurance Law disclosure"],
                "mandatory_components": ["DFS approval requirements"],
                "filing_requirements": ["New York DFS filing"],
                "regulatory_implications": ["NY Insurance Law compliance"]
            },
            "texas": {
                "required_disclosures": ["Texas Insurance Code notice"],
                "mandatory_components": ["TDI requirements"],
                "filing_requirements": ["Texas Department filing"],
                "regulatory_implications": ["Texas Insurance Code compliance"]
            },
            "florida": {
                "required_disclosures": ["Florida statutes disclosure"],
                "mandatory_components": ["Florida OIR requirements"],
                "filing_requirements": ["Florida OIR filing"],
                "regulatory_implications": ["Florida Insurance Code compliance"]
            }
        }
        
        return state_reqs.get(state, {
            "required_disclosures": ["Standard state disclosures"],
            "mandatory_components": ["Basic compliance requirements"],
            "filing_requirements": ["State regulatory filing"],
            "regulatory_implications": ["State law compliance"]
        })
    
    def _identify_organizations(self, text: str) -> Dict:
        """Identify organizations/carriers mentioned in document"""
        
        identified_organizations = []
        text_lower = text.lower()
        
        for organization in self.major_organizations:
            if organization.lower() in text_lower:
                identified_organizations.append(organization)
        
        # Use regex to find additional company patterns
        company_patterns = [
            r'\b([A-Z][a-zA-Z\s]+(?:Inc|LLC|Corp|Corporation|Company|Co\.|Insurance|Group))\b',
            r'\b([A-Z][a-zA-Z\s]+ Insurance)\b',
            r'\b([A-Z][a-zA-Z\s]+ Financial)\b'
        ]
        
        additional_orgs = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            additional_orgs.extend(matches)
        
        return {
            "known_organizations": identified_organizations,
            "additional_organizations": list(set(additional_orgs)),
            "primary_organization": identified_organizations[0] if identified_organizations else None,
            "organization_count": len(identified_organizations) + len(additional_orgs)
        }
    
    def _analyze_document_complexity(self, text: str) -> float:
        """Analyze document complexity based on various metrics"""
        
        # Word count
        word_count = len(text.split())
        
        # Sentence count
        sentence_count = len(re.findall(r'[.!?]+', text))
        
        # Average words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Number of technical terms
        technical_terms = ['pursuant', 'heretofore', 'whereas', 'notwithstanding', 
                          'thereunder', 'herein', 'thereof', 'hereby']
        technical_count = sum(1 for term in technical_terms if term in text.lower())
        
        # Number patterns (dates, amounts, etc.)
        number_patterns = len(re.findall(r'\d+', text))
        
        # Complexity score (0-1)
        complexity = min(1.0, (
            (word_count / 2000) * 0.3 +
            (avg_words_per_sentence / 25) * 0.3 +
            (technical_count / 10) * 0.2 +
            (number_patterns / 50) * 0.2
        ))
        
        return round(complexity, 3)
    
    def _calculate_template_similarity(self, text: str, category: str) -> float:
        """Calculate similarity to known templates"""
        
        # Simple template matching based on category keywords
        if category in self.product_categories:
            keywords = self.product_categories[category]
            text_lower = text.lower()
            
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            similarity = matches / len(keywords) if keywords else 0
            
            return round(min(1.0, similarity), 3)
        
        return 0.5
    
    def _calculate_classification_confidence(self, text: str, category: str) -> float:
        """Calculate confidence in classification result"""
        
        # Factor 1: Length of text (more text = higher confidence)
        length_factor = min(1.0, len(text) / 1000)
        
        # Factor 2: Number of category-specific keywords found
        keywords = self.product_categories.get(category, [])
        text_lower = text.lower()
        keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
        keyword_factor = min(1.0, keyword_matches / max(1, len(keywords) * 0.3))
        
        # Factor 3: Presence of structured elements
        structure_patterns = [r'\d+\.', r'\([a-z]\)', r'\([0-9]+\)', r'[A-Z][a-z]+:']
        structure_count = sum(len(re.findall(pattern, text)) for pattern in structure_patterns)
        structure_factor = min(1.0, structure_count / 10)
        
        # Weighted confidence
        confidence = (
            length_factor * 0.3 +
            keyword_factor * 0.5 +
            structure_factor * 0.2
        )
        
        return round(confidence, 3)
    
    def _get_fallback_classification(self) -> Dict:
        """Return fallback classification when errors occur"""
        return {
            "primary_category": "general_document",
            "sub_category": "standard",
            "state_regulations": {
                "identified_states": [],
                "requirements": {},
                "compliance_needed": False,
                "multi_state": False
            },
            "organizations": {
                "known_organizations": [],
                "additional_organizations": [],
                "primary_organization": None,
                "organization_count": 0
            },
            "complexity_score": 0.5,
            "template_match_score": 0.5,
            "classification_confidence": 0.3
        }
    
    def learn_new_template(self, text: str, template_name: str, category: Optional[str] = None) -> bool:
        """Learn and store new template patterns"""
        try:
            # Extract keywords for the new template
            keywords = self._extract_template_keywords(text)
            
            # Store template information
            template_info = {
                "keywords": keywords,
                "category": category if category is not None else "custom",
                "length": len(text),
                "complexity": self._analyze_document_complexity(text)
            }
            
            self.template_keywords[template_name] = template_info
            
            logger.info(f"New template learned: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error learning template {template_name}: {str(e)}")
            return False
    
    def _extract_template_keywords(self, text: str) -> List[str]:
        """Extract key phrases that identify this template"""
        
        # Extract words that are likely to be significant
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        
        # Filter for document-specific terms
        document_terms = []
        significant_words = ['policy', 'contract', 'agreement', 'certificate', 
                           'statement', 'document', 'form', 'application', 'notice']
        
        for word in words:
            if (any(term in word for term in significant_words) or 
                word.istitle() or 
                len(word) > 8):
                document_terms.append(word)
        
        # Remove duplicates and limit to top terms
        return list(set(document_terms))[:20]
    
    def get_available_templates(self) -> Dict:
        """Return available template categories and information"""
        return {
            "primary_categories": list(self.product_categories.keys()),
            "state_coverage": list(self.state_patterns.keys()),
            "known_organizations": self.major_organizations,
            "custom_templates": list(self.template_keywords.keys())
        }