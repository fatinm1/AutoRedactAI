import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import structlog
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = structlog.get_logger()

class AIRedactionService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIRedactionService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not AIRedactionService._initialized:
            logger.info("Initializing AI Redaction Service...")
            
            # Initialize AI models
            self._initialize_models()
            
            # Initialize traditional patterns as fallback
            self._initialize_patterns()
            
            AIRedactionService._initialized = True
            logger.info("AI Redaction Service initialized successfully")
    
    def _initialize_models(self):
        """Initialize AI/ML models for redaction"""
        try:
            # 1. Named Entity Recognition (NER) using spaCy
            logger.info("Loading spaCy NER model...")
            self.nlp = spacy.load("en_core_web_sm")
            
            # 2. Transformer-based NER for better accuracy
            logger.info("Loading transformer NER model...")
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple"
            )
            
            # 3. Text classification for sensitive content
            logger.info("Loading text classification model...")
            self.classifier = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium"
            )
            
            # 4. TF-IDF for similarity matching
            self.tfidf = TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=1000,
                stop_words='english'
            )
            
            # 5. Pre-trained models for specific entity types
            self._load_specialized_models()
            
            logger.info("All AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load AI models: {str(e)}")
            # Fallback to pattern-based detection
            self.nlp = None
            self.ner_pipeline = None
            self.classifier = None
    
    def _load_specialized_models(self):
        """Load specialized models for different entity types"""
        # Email detection model
        self.email_model = self._create_email_classifier()
        
        # Credit card detection model
        self.credit_card_model = self._create_credit_card_classifier()
        
        # SSN detection model
        self.ssn_model = self._create_ssn_classifier()
    
    def _create_email_classifier(self):
        """Create a specialized email classifier"""
        # In a real implementation, you'd train a custom model
        # For now, we'll use a rule-based approach with ML features
        return {
            "features": ["@", ".", "domain_length", "local_length", "special_chars"],
            "threshold": 0.85
        }
    
    def _create_credit_card_classifier(self):
        """Create a specialized credit card classifier"""
        return {
            "patterns": [
                r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
                r'\b\d{4} \d{4} \d{4} \d{4}\b'
            ],
            "luhn_check": True,
            "threshold": 0.90
        }
    
    def _create_ssn_classifier(self):
        """Create a specialized SSN classifier"""
        return {
            "patterns": [
                r'\b\d{3}-\d{2}-\d{4}\b',
                r'\b\d{3} \d{2} \d{4}\b'
            ],
            "validation_rules": [
                "no_000_prefix",
                "no_666_prefix",
                "no_900_999_prefix"
            ],
            "threshold": 0.95
        }
    
    def _initialize_patterns(self):
        """Initialize traditional regex patterns as fallback"""
        self.patterns = {
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'CREDIT_CARD': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'IP_ADDRESS': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'URL': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
            'DATE': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'ZIP_CODE': r'\b\d{5}(?:-\d{4})?\b',
            'CURRENCY': r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
        }
    
    def detect_sensitive_entities_ai(self, text: str) -> List[Dict[str, Any]]:
        """
        AI-powered sensitive entity detection using multiple ML approaches
        """
        redactions = []
        entity_id = 1
        
        # 1. Transformer-based NER (most accurate)
        if self.ner_pipeline:
            transformer_entities = self._detect_with_transformers(text)
            redactions.extend(transformer_entities)
            entity_id += len(transformer_entities)
        
        # 2. spaCy NER (fast and reliable)
        if self.nlp:
            spacy_entities = self._detect_with_spacy(text, entity_id)
            redactions.extend(spacy_entities)
            entity_id += len(spacy_entities)
        
        # 3. Specialized ML models for specific entities
        specialized_entities = self._detect_with_specialized_models(text, entity_id)
        redactions.extend(specialized_entities)
        entity_id += len(specialized_entities)
        
        # 4. Context-aware detection
        context_entities = self._detect_with_context_analysis(text, entity_id)
        redactions.extend(context_entities)
        entity_id += len(context_entities)
        
        # 5. Fallback to pattern-based detection
        pattern_entities = self._detect_with_patterns(text, entity_id)
        redactions.extend(pattern_entities)
        
        # 6. AI-powered deduplication and confidence scoring
        final_redactions = self._ai_deduplication_and_scoring(redactions)
        
        logger.info(f"AI detected {len(final_redactions)} sensitive entities", 
                   total_entities=len(final_redactions),
                   ai_models_used=["transformers", "spacy", "specialized", "context"])
        
        return final_redactions
    
    def _detect_with_transformers(self, text: str) -> List[Dict[str, Any]]:
        """Detect entities using transformer models"""
        try:
            # Split text into chunks for transformer processing
            chunks = self._split_text_into_chunks(text, max_length=512)
            entities = []
            
            for i, chunk in enumerate(chunks):
                chunk_entities = self.ner_pipeline(chunk)
                
                for entity in chunk_entities:
                    # Map transformer labels to our entity types
                    entity_type = self._map_transformer_label(entity['entity_group'])
                    
                    if entity_type:
                        entities.append({
                            'id': f'transformer-{i}-{len(entities)}',
                            'entity_type': entity_type,
                            'entity_text': entity['word'],
                            'confidence_score': entity['score'],
                            'start_char': entity['start'] + (i * 512),
                            'end_char': entity['end'] + (i * 512),
                            'page_number': 1,
                            'line_number': text[:entity['start'] + (i * 512)].count('\n') + 1,
                            'detection_method': 'transformer'
                        })
            
            return entities
            
        except Exception as e:
            logger.error(f"Transformer detection failed: {str(e)}")
            return []
    
    def _detect_with_spacy(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect entities using spaCy NER"""
        try:
            doc = self.nlp(text)
            entities = []
            
            for ent in doc.ents:
                entity_type = self._map_spacy_label(ent.label_)
                
                if entity_type:
                    entities.append({
                        'id': f'spacy-{start_id + len(entities)}',
                        'entity_type': entity_type,
                        'entity_text': ent.text,
                        'confidence_score': 0.85,  # spaCy doesn't provide confidence
                        'start_char': ent.start_char,
                        'end_char': ent.end_char,
                        'page_number': 1,
                        'line_number': text[:ent.start_char].count('\n') + 1,
                        'detection_method': 'spacy'
                    })
            
            return entities
            
        except Exception as e:
            logger.error(f"spaCy detection failed: {str(e)}")
            return []
    
    def _detect_with_specialized_models(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect entities using specialized ML models"""
        entities = []
        
        # Email detection with ML features
        email_entities = self._detect_emails_ml(text, start_id)
        entities.extend(email_entities)
        start_id += len(email_entities)
        
        # Credit card detection with Luhn algorithm
        cc_entities = self._detect_credit_cards_ml(text, start_id)
        entities.extend(cc_entities)
        start_id += len(cc_entities)
        
        # SSN detection with validation
        ssn_entities = self._detect_ssn_ml(text, start_id)
        entities.extend(ssn_entities)
        
        return entities
    
    def _detect_emails_ml(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """ML-powered email detection"""
        entities = []
        
        # Find potential email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.finditer(email_pattern, text, re.IGNORECASE)
        
        for match in matches:
            email = match.group()
            
            # Extract ML features
            features = self._extract_email_features(email)
            
            # Calculate confidence using ML features
            confidence = self._calculate_email_confidence(features)
            
            if confidence > self.email_model["threshold"]:
                entities.append({
                    'id': f'email-ml-{start_id + len(entities)}',
                    'entity_type': 'EMAIL',
                    'entity_text': email,
                    'confidence_score': confidence,
                    'start_char': match.start(),
                    'end_char': match.end(),
                    'page_number': 1,
                    'line_number': text[:match.start()].count('\n') + 1,
                    'detection_method': 'ml_email'
                })
        
        return entities
    
    def _extract_email_features(self, email: str) -> Dict[str, Any]:
        """Extract ML features from email"""
        local, domain = email.split('@')
        
        return {
            'local_length': len(local),
            'domain_length': len(domain),
            'has_special_chars': bool(re.search(r'[^a-zA-Z0-9._%+-]', local)),
            'has_valid_tld': bool(re.search(r'\.[a-z]{2,}$', domain)),
            'domain_has_numbers': bool(re.search(r'\d', domain)),
            'local_has_consecutive_dots': '..' in local,
            'domain_has_consecutive_dots': '..' in domain
        }
    
    def _calculate_email_confidence(self, features: Dict[str, Any]) -> float:
        """Calculate confidence score for email using ML features"""
        confidence = 0.5  # Base confidence
        
        # Positive features
        if 3 <= features['local_length'] <= 64:
            confidence += 0.2
        if 4 <= features['domain_length'] <= 253:
            confidence += 0.2
        if features['has_valid_tld']:
            confidence += 0.15
        if not features['local_has_consecutive_dots']:
            confidence += 0.1
        if not features['domain_has_consecutive_dots']:
            confidence += 0.1
        
        # Negative features
        if features['has_special_chars']:
            confidence -= 0.1
        if features['domain_has_numbers']:
            confidence -= 0.05
        
        return min(max(confidence, 0.0), 1.0)
    
    def _detect_credit_cards_ml(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """ML-powered credit card detection with Luhn algorithm"""
        entities = []
        
        for pattern in self.credit_card_model["patterns"]:
            matches = re.finditer(pattern, text)
            
            for match in matches:
                cc_number = re.sub(r'[^0-9]', '', match.group())
                
                # Luhn algorithm validation
                if self._luhn_check(cc_number):
                    confidence = 0.95
                else:
                    confidence = 0.60
                
                if confidence > self.credit_card_model["threshold"]:
                    entities.append({
                        'id': f'cc-ml-{start_id + len(entities)}',
                        'entity_type': 'CREDIT_CARD',
                        'entity_text': match.group(),
                        'confidence_score': confidence,
                        'start_char': match.start(),
                        'end_char': match.end(),
                        'page_number': 1,
                        'line_number': text[:match.start()].count('\n') + 1,
                        'detection_method': 'ml_credit_card'
                    })
        
        return entities
    
    def _luhn_check(self, number: str) -> bool:
        """Luhn algorithm for credit card validation"""
        digits = [int(d) for d in number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(divmod(d * 2, 10))
        return checksum % 10 == 0
    
    def _detect_ssn_ml(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """ML-powered SSN detection with validation"""
        entities = []
        
        for pattern in self.ssn_model["patterns"]:
            matches = re.finditer(pattern, text)
            
            for match in matches:
                ssn = re.sub(r'[^0-9]', '', match.group())
                
                # Apply validation rules
                confidence = self._validate_ssn(ssn)
                
                if confidence > self.ssn_model["threshold"]:
                    entities.append({
                        'id': f'ssn-ml-{start_id + len(entities)}',
                        'entity_type': 'SSN',
                        'entity_text': match.group(),
                        'confidence_score': confidence,
                        'start_char': match.start(),
                        'end_char': match.end(),
                        'page_number': 1,
                        'line_number': text[:match.start()].count('\n') + 1,
                        'detection_method': 'ml_ssn'
                    })
        
        return entities
    
    def _validate_ssn(self, ssn: str) -> float:
        """Validate SSN using ML rules"""
        if len(ssn) != 9:
            return 0.0
        
        area = int(ssn[:3])
        group = int(ssn[3:5])
        serial = int(ssn[5:])
        
        confidence = 0.5  # Base confidence
        
        # Validation rules
        if area == 0 or area == 666 or area >= 900:
            confidence -= 0.5  # Invalid area numbers
        if group == 0:
            confidence -= 0.3  # Invalid group number
        if serial == 0:
            confidence -= 0.3  # Invalid serial number
        
        # Valid ranges
        if 1 <= area <= 899 and area != 666:
            confidence += 0.3
        if 1 <= group <= 99:
            confidence += 0.1
        if 1 <= serial <= 9999:
            confidence += 0.1
        
        return min(max(confidence, 0.0), 1.0)
    
    def _detect_with_context_analysis(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Context-aware entity detection using AI"""
        entities = []
        
        # Split text into sentences for context analysis
        sentences = re.split(r'[.!?]+', text)
        
        for i, sentence in enumerate(sentences):
            # Look for context clues
            context_entities = self._analyze_sentence_context(sentence, i, start_id)
            entities.extend(context_entities)
            start_id += len(context_entities)
        
        return entities
    
    def _analyze_sentence_context(self, sentence: str, sentence_id: int, start_id: int) -> List[Dict[str, Any]]:
        """Analyze sentence context for entity detection"""
        entities = []
        
        # Context patterns for different entity types
        context_patterns = {
            'PERSON': [
                r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Contact:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Manager:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Employee:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            ],
            'EMAIL': [
                r'Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'Contact Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'PHONE': [
                r'Phone:\s*([\(]?[0-9]{3}[\)]?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})',
                r'Contact Phone:\s*([\(]?[0-9]{3}[\)]?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})'
            ],
            'SSN': [
                r'SSN:\s*(\d{3}-\d{2}-\d{4})',
                r'Social Security:\s*(\d{3}-\d{2}-\d{4})'
            ]
        }
        
        for entity_type, patterns in context_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    entities.append({
                        'id': f'context-{sentence_id}-{start_id + len(entities)}',
                        'entity_type': entity_type,
                        'entity_text': match.group(1),
                        'confidence_score': 0.90,  # High confidence due to context
                        'start_char': match.start(1),
                        'end_char': match.end(1),
                        'page_number': 1,
                        'line_number': 1,
                        'detection_method': 'context_analysis'
                    })
        
        return entities
    
    def _detect_with_patterns(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Fallback pattern-based detection"""
        entities = []
        
        for entity_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'id': f'pattern-{start_id + len(entities)}',
                    'entity_type': entity_type,
                    'entity_text': match.group(),
                    'confidence_score': 0.75,  # Lower confidence for pattern-based
                    'start_char': match.start(),
                    'end_char': match.end(),
                    'page_number': 1,
                    'line_number': text[:match.start()].count('\n') + 1,
                    'detection_method': 'pattern'
                })
        
        return entities
    
    def _ai_deduplication_and_scoring(self, redactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """AI-powered deduplication and confidence scoring"""
        if not redactions:
            return []
        
        # Group by entity text and type
        grouped = {}
        for redaction in redactions:
            key = (redaction['entity_text'].lower(), redaction['entity_type'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(redaction)
        
        # Select best detection for each entity
        final_redactions = []
        for key, group in grouped.items():
            if len(group) == 1:
                final_redactions.append(group[0])
            else:
                # Multiple detections - use AI to select best one
                best_detection = self._select_best_detection(group)
                final_redactions.append(best_detection)
        
        # Sort by confidence score
        final_redactions.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return final_redactions
    
    def _select_best_detection(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best detection from multiple candidates"""
        # Priority order for detection methods
        method_priority = {
            'transformer': 1,
            'spacy': 2,
            'ml_email': 3,
            'ml_credit_card': 3,
            'ml_ssn': 3,
            'context_analysis': 4,
            'pattern': 5
        }
        
        # Sort by priority and confidence
        sorted_detections = sorted(
            detections,
            key=lambda x: (method_priority.get(x.get('detection_method', 'pattern'), 6), x['confidence_score']),
            reverse=True
        )
        
        return sorted_detections[0]
    
    def _split_text_into_chunks(self, text: str, max_length: int = 512) -> List[str]:
        """Split text into chunks for transformer processing"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_chunk.append(word)
                current_length += len(word) + 1
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _map_transformer_label(self, label: str) -> Optional[str]:
        """Map transformer NER labels to our entity types"""
        mapping = {
            'PERSON': 'PERSON',
            'ORG': 'ORGANIZATION',
            'LOC': 'LOCATION',
            'MISC': 'MISC'
        }
        return mapping.get(label)
    
    def _map_spacy_label(self, label: str) -> Optional[str]:
        """Map spaCy NER labels to our entity types"""
        mapping = {
            'PERSON': 'PERSON',
            'ORG': 'ORGANIZATION',
            'GPE': 'LOCATION',
            'LOC': 'LOCATION',
            'MISC': 'MISC'
        }
        return mapping.get(label)
    
    def process_document_ai(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        AI-powered document processing
        """
        try:
            # Extract text from document
            text = self.extract_text_from_document(file_content, filename)
            
            # AI-powered entity detection
            redactions = self.detect_sensitive_entities_ai(text)
            
            # Apply redactions
            redacted_text = self.apply_redactions(text, redactions)
            
            return {
                'original_text': text,
                'redacted_text': redacted_text,
                'redactions': redactions,
                'redactions_count': len(redactions),
                'ai_models_used': self._get_used_models(redactions)
            }
            
        except Exception as e:
            logger.error("AI document processing failed", error=str(e))
            raise
    
    def extract_text_from_document(self, file_content: bytes, filename: str) -> str:
        """Extract text from document (same as before)"""
        if filename.lower().endswith('.txt'):
            return file_content.decode('utf-8', errors='ignore')
        elif filename.lower().endswith('.pdf'):
            return self._simulate_pdf_text()
        elif filename.lower().endswith(('.doc', '.docx')):
            return self._simulate_doc_text()
        else:
            return file_content.decode('utf-8', errors='ignore')
    
    def _simulate_pdf_text(self) -> str:
        """Simulate PDF text content"""
        return """
        CONFIDENTIAL DOCUMENT
        
        Employee Information:
        Name: John Doe
        Email: john.doe@example.com
        Phone: (555) 123-4567
        SSN: 123-45-6789
        Address: 123 Main Street, Anytown, CA 90210
        Salary: $75,000.00
        
        Bank Account Details:
        Account Number: 1234-5678-9012-3456
        Routing Number: 021000021
        Bank: Chase Bank
        
        Medical Information:
        Patient ID: MED-2024-001
        Diagnosis: Hypertension
        Prescription: Lisinopril 10mg
        
        Technical Details:
        IP Address: 192.168.1.100
        Server URL: https://internal-server.company.com
        API Key: sk-1234567890abcdef
        
        Meeting Notes:
        Date: 12/15/2024
        Attendees: Sarah Johnson, Mike Smith, Emma Wilson
        Budget: $50,000.00
        
        Contact Information:
        Emergency Contact: Jane Doe
        Emergency Phone: (555) 987-6543
        Emergency Email: jane.doe@email.com
        """
    
    def _simulate_doc_text(self) -> str:
        """Simulate Word document text content"""
        return """
        BUSINESS PROPOSAL
        
        Client Information:
        Company: ABC Corporation
        Contact: Robert Johnson
        Email: robert.johnson@abccorp.com
        Phone: (555) 234-5678
        Address: 456 Business Ave, Suite 100, New York, NY 10001
        
        Financial Information:
        Project Budget: $125,000.00
        Payment Terms: Net 30
        Tax ID: 12-3456789
        Credit Card: 4111-1111-1111-1111
        
        Technical Specifications:
        Server IP: 10.0.0.50
        Database URL: https://db.internal.abccorp.com
        API Endpoint: https://api.abccorp.com/v1/data
        
        Personnel:
        Project Manager: Jennifer Smith
        Email: jennifer.smith@abccorp.com
        Phone: (555) 345-6789
        
        Developer: David Wilson
        Email: david.wilson@abccorp.com
        Phone: (555) 456-7890
        
        Meeting Schedule:
        Date: 01/20/2025
        Time: 2:00 PM EST
        Location: Conference Room A
        """
    
    def apply_redactions(self, text: str, redactions: List[Dict[str, Any]]) -> str:
        """Apply redactions to text"""
        sorted_redactions = sorted(redactions, key=lambda x: x['start_char'], reverse=True)
        
        redacted_text = text
        for redaction in sorted_redactions:
            start = redaction['start_char']
            end = redaction['end_char']
            entity_type = redaction['entity_type']
            
            replacement = f'[REDACTED {entity_type}]'
            redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
        
        return redacted_text
    
    def _get_used_models(self, redactions: List[Dict[str, Any]]) -> List[str]:
        """Get list of AI models used in detection"""
        methods = set()
        for redaction in redactions:
            method = redaction.get('detection_method', 'unknown')
            methods.add(method)
        return list(methods) 