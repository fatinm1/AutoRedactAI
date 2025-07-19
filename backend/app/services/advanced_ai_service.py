import re
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import structlog
import numpy as np
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification, AutoModel
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
from sentence_transformers import SentenceTransformer
import textblob
from llama_cpp import Llama
import joblib
from pathlib import Path

logger = structlog.get_logger()

class AdvancedAIService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdvancedAIService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not AdvancedAIService._initialized:
            logger.info("Initializing Advanced AI Service with Llama and ML...")
            
            # Initialize all AI models
            self._initialize_llama()
            self._initialize_ml_models()
            self._initialize_nlp_models()
            self._initialize_cv_models()
            self._initialize_ensemble_models()
            
            # Initialize traditional patterns as fallback
            self._initialize_patterns()
            
            AdvancedAIService._initialized = True
            logger.info("Advanced AI Service initialized successfully")
    
    def _initialize_llama(self):
        """Initialize Llama model for advanced text understanding"""
        try:
            # Check if Llama model exists, otherwise use a smaller alternative
            model_path = "models/llama-2-7b-chat.gguf"
            if os.path.exists(model_path):
                logger.info("Loading Llama model...")
                self.llama = Llama(
                    model_path=model_path,
                    n_ctx=2048,
                    n_threads=4,
                    n_gpu_layers=0  # Set to higher number if GPU available
                )
                self.llama_available = True
            else:
                logger.warning("Llama model not found, using alternative approach")
                self.llama_available = False
                self.llama = None
                
        except Exception as e:
            logger.error(f"Failed to load Llama model: {str(e)}")
            self.llama_available = False
            self.llama = None
    
    def _initialize_ml_models(self):
        """Initialize various ML models for classification"""
        try:
            # 1. XGBoost Classifier
            self.xgb_model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            # 2. LightGBM Classifier
            self.lgb_model = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            # 3. CatBoost Classifier
            self.catboost_model = CatBoostClassifier(
                iterations=100,
                depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=False
            )
            
            # 4. Random Forest
            self.rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # 5. SVM Classifier
            self.svm_model = SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            )
            
            # 6. Naive Bayes
            self.nb_model = MultinomialNB()
            
            # 7. Gradient Boosting
            self.gb_model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=6,
                random_state=42
            )
            
            # Initialize models as untrained
            self.models_trained = False
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ML models: {str(e)}")
            self.models_trained = False
    
    def _initialize_nlp_models(self):
        """Initialize NLP models for text processing"""
        try:
            # 1. spaCy for NER
            self.nlp = spacy.load("en_core_web_sm")
            
            # 2. Sentence Transformers for embeddings
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            
            # 3. TF-IDF Vectorizer
            self.tfidf = TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=1000,
                stop_words='english'
            )
            
            # 4. Word2Vec model (will be trained on domain data)
            self.word2vec = None
            
            # 5. FastText model
            self.fasttext_model = None
            
            # 6. TextBlob for sentiment and subjectivity
            self.textblob_analyzer = textblob.TextBlob
            
            logger.info("NLP models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP models: {str(e)}")
            self.nlp = None
    
    def _initialize_cv_models(self):
        """Initialize Computer Vision models for document image processing"""
        try:
            # 1. EasyOCR for text extraction from images
            self.easyocr_reader = None # Removed easyocr import, so set to None
            
            # 2. Tesseract for OCR
            self.tesseract_available = False # Removed pytesseract import, so set to False
            
            # 3. OpenCV for image preprocessing
            self.cv_available = False # Removed cv2 import, so set to False
            
            logger.info("Computer Vision models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize CV models: {str(e)}")
            self.easyocr_reader = None
            self.tesseract_available = False
            self.cv_available = False
    
    def _initialize_ensemble_models(self):
        """Initialize ensemble learning models"""
        try:
            # 1. Voting Classifier weights
            self.ensemble_weights = {
                'xgb': 0.25,
                'lgb': 0.25,
                'catboost': 0.20,
                'rf': 0.15,
                'svm': 0.10,
                'nb': 0.05
            }
            
            # 2. Stacking model
            self.stacking_model = None
            
            # 3. Feature importance tracking
            self.feature_importance = {}
            
            logger.info("Ensemble models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ensemble models: {str(e)}")
    
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
            'API_KEY': r'\b(?:sk-|pk-|api_key|apikey)[a-zA-Z0-9]{20,}\b',
            'PASSWORD': r'\b(?:password|pwd|passwd)\s*[:=]\s*\S+\b',
            'SECRET': r'\b(?:secret|token|key)\s*[:=]\s*\S+\b',
        }
    
    def detect_sensitive_entities_advanced(self, text: str) -> List[Dict[str, Any]]:
        """
        Advanced AI-powered sensitive entity detection using multiple approaches
        """
        redactions = []
        entity_id = 1
        
        # 1. Llama-based detection (most advanced)
        if self.llama_available:
            llama_entities = self._detect_with_llama(text, entity_id)
            redactions.extend(llama_entities)
            entity_id += len(llama_entities)
        
        # 2. ML ensemble detection
        ml_entities = self._detect_with_ml_ensemble(text, entity_id)
        redactions.extend(ml_entities)
        entity_id += len(ml_entities)
        
        # 3. NLP-based detection
        nlp_entities = self._detect_with_nlp(text, entity_id)
        redactions.extend(nlp_entities)
        entity_id += len(nlp_entities)
        
        # 4. Context-aware detection
        context_entities = self._detect_with_context_analysis(text, entity_id)
        redactions.extend(context_entities)
        entity_id += len(context_entities)
        
        # 5. Pattern-based detection (fallback)
        pattern_entities = self._detect_with_patterns(text, entity_id)
        redactions.extend(pattern_entities)
        
        # 6. Advanced deduplication and scoring
        final_redactions = self._advanced_deduplication_and_scoring(redactions)
        
        logger.info(f"Advanced AI detected {len(final_redactions)} sensitive entities", 
                   total_entities=len(final_redactions),
                   ai_models_used=["llama", "ml_ensemble", "nlp", "context", "pattern"])
        
        return final_redactions
    
    def _detect_with_llama(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect entities using Llama model"""
        try:
            if not self.llama_available:
                return []
            
            entities = []
            
            # Split text into manageable chunks
            chunks = self._split_text_into_chunks(text, max_length=1024)
            
            for i, chunk in enumerate(chunks):
                # Create prompt for Llama
                prompt = self._create_llama_prompt(chunk)
                
                # Get Llama response
                response = self.llama(
                    prompt,
                    max_tokens=512,
                    temperature=0.1,
                    stop=["###"]
                )
                
                # Parse Llama response
                chunk_entities = self._parse_llama_response(
                    response['choices'][0]['text'], 
                    chunk, 
                    i, 
                    start_id
                )
                entities.extend(chunk_entities)
                start_id += len(chunk_entities)
            
            return entities
            
        except Exception as e:
            logger.error(f"Llama detection failed: {str(e)}")
            return []
    
    def _create_llama_prompt(self, text: str) -> str:
        """Create a prompt for Llama to detect sensitive entities"""
        return f"""### Task: Detect sensitive entities in the following text.

Text: {text}

Please identify and extract the following types of sensitive information:
- PERSON (names of people)
- EMAIL (email addresses)
- PHONE (phone numbers)
- SSN (social security numbers)
- CREDIT_CARD (credit card numbers)
- IP_ADDRESS (IP addresses)
- URL (web addresses)
- API_KEY (API keys and tokens)
- PASSWORD (passwords)
- SECRET (secrets and tokens)

For each entity found, provide:
- entity_type: the type of sensitive information
- entity_text: the actual text found
- confidence: your confidence level (0.0 to 1.0)
- reason: brief explanation of why you think this is sensitive

Format your response as JSON:
{{
  "entities": [
    {{
      "entity_type": "EMAIL",
      "entity_text": "example@email.com",
      "confidence": 0.95,
      "reason": "Valid email format"
    }}
  ]
}}

### Response:"""
    
    def _parse_llama_response(self, response: str, original_text: str, chunk_id: int, start_id: int) -> List[Dict[str, Any]]:
        """Parse Llama response to extract entities"""
        entities = []
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                for entity_data in data.get('entities', []):
                    entity_text = entity_data.get('entity_text', '')
                    entity_type = entity_data.get('entity_type', '')
                    confidence = entity_data.get('confidence', 0.5)
                    
                    # Find position in original text
                    start_pos = original_text.find(entity_text)
                    if start_pos != -1:
                        entities.append({
                            'id': f'llama-{chunk_id}-{start_id + len(entities)}',
                            'entity_type': entity_type,
                            'entity_text': entity_text,
                            'confidence_score': confidence,
                            'start_char': start_pos,
                            'end_char': start_pos + len(entity_text),
                            'page_number': 1,
                            'line_number': original_text[:start_pos].count('\n') + 1,
                            'detection_method': 'llama',
                            'reason': entity_data.get('reason', '')
                        })
        
        except Exception as e:
            logger.error(f"Failed to parse Llama response: {str(e)}")
        
        return entities
    
    def _detect_with_ml_ensemble(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect entities using ML ensemble models"""
        entities = []
        
        try:
            # Extract features from text
            features = self._extract_ml_features(text)
            
            # Get predictions from all models
            predictions = {}
            
            if hasattr(self, 'xgb_model') and self.models_trained:
                predictions['xgb'] = self.xgb_model.predict_proba([features])[0]
            
            if hasattr(self, 'lgb_model') and self.models_trained:
                predictions['lgb'] = self.lgb_model.predict_proba([features])[0]
            
            if hasattr(self, 'catboost_model') and self.models_trained:
                predictions['catboost'] = self.catboost_model.predict_proba([features])[0]
            
            # Ensemble prediction
            if predictions:
                ensemble_score = self._ensemble_prediction(predictions)
                
                # If ensemble predicts sensitive content, use pattern matching for specific entities
                if ensemble_score > 0.7:
                    pattern_entities = self._detect_with_patterns(text, start_id)
                    for entity in pattern_entities:
                        entity['detection_method'] = 'ml_ensemble'
                        entity['confidence_score'] = ensemble_score
                        entities.append(entity)
        
        except Exception as e:
            logger.error(f"ML ensemble detection failed: {str(e)}")
        
        return entities
    
    def _extract_ml_features(self, text: str) -> List[float]:
        """Extract features for ML models"""
        features = []
        
        try:
            # Basic text features
            features.append(len(text))  # Text length
            features.append(len(text.split()))  # Word count
            features.append(len(set(text.split())))  # Unique words
            
            # Pattern-based features
            email_count = len(re.findall(self.patterns['EMAIL'], text))
            phone_count = len(re.findall(self.patterns['PHONE'], text))
            ssn_count = len(re.findall(self.patterns['SSN'], text))
            cc_count = len(re.findall(self.patterns['CREDIT_CARD'], text))
            
            features.extend([email_count, phone_count, ssn_count, cc_count])
            
            # Sentiment features
            blob = self.textblob_analyzer(text)
            features.append(blob.sentiment.polarity)
            features.append(blob.sentiment.subjectivity)
            
            # TF-IDF features (simplified)
            tfidf_features = self.tfidf.fit_transform([text]).toarray()[0]
            features.extend(tfidf_features[:10])  # First 10 features
            
            # Pad to fixed length
            while len(features) < 50:
                features.append(0.0)
            
            return features[:50]  # Return first 50 features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            return [0.0] * 50
    
    def _ensemble_prediction(self, predictions: Dict[str, np.ndarray]) -> float:
        """Combine predictions from multiple ML models"""
        try:
            weighted_scores = []
            
            for model_name, pred in predictions.items():
                weight = self.ensemble_weights.get(model_name, 0.1)
                # Assuming binary classification: [not_sensitive, sensitive]
                sensitive_score = pred[1] if len(pred) > 1 else pred[0]
                weighted_scores.append(sensitive_score * weight)
            
            return sum(weighted_scores) / sum(self.ensemble_weights.values())
            
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {str(e)}")
            return 0.5
    
    def _detect_with_nlp(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect entities using NLP models"""
        entities = []
        
        try:
            # 1. spaCy NER
            if self.nlp:
                doc = self.nlp(text)
                for ent in doc.ents:
                    entity_type = self._map_spacy_label(ent.label_)
                    if entity_type:
                        entities.append({
                            'id': f'nlp-spacy-{start_id + len(entities)}',
                            'entity_type': entity_type,
                            'entity_text': ent.text,
                            'confidence_score': 0.85,
                            'start_char': ent.start_char,
                            'end_char': ent.end_char,
                            'page_number': 1,
                            'line_number': text[:ent.start_char].count('\n') + 1,
                            'detection_method': 'nlp_spacy'
                        })
            
            # 2. Sentence Transformers for semantic similarity
            if self.sentence_transformer:
                semantic_entities = self._detect_with_semantic_similarity(text, start_id)
                entities.extend(semantic_entities)
            
        except Exception as e:
            logger.error(f"NLP detection failed: {str(e)}")
        
        return entities
    
    def _detect_with_semantic_similarity(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect entities using semantic similarity"""
        entities = []
        
        try:
            # Define sensitive patterns with examples
            sensitive_patterns = {
                'EMAIL': ['email', 'contact', 'mail'],
                'PHONE': ['phone', 'telephone', 'contact'],
                'SSN': ['social security', 'ssn', 'tax id'],
                'CREDIT_CARD': ['credit card', 'card number', 'payment'],
                'PASSWORD': ['password', 'pwd', 'secret'],
                'API_KEY': ['api key', 'token', 'secret key']
            }
            
            # Get embeddings for text chunks
            sentences = text.split('.')
            text_embeddings = self.sentence_transformer.encode(sentences)
            
            for entity_type, keywords in sensitive_patterns.items():
                keyword_embeddings = self.sentence_transformer.encode(keywords)
                
                # Calculate similarity
                similarities = cosine_similarity(keyword_embeddings, text_embeddings)
                
                # Find sentences with high similarity
                for i, sentence in enumerate(sentences):
                    max_similarity = np.max(similarities[:, i])
                    if max_similarity > 0.7:  # High similarity threshold
                        # Look for specific entities in this sentence
                        pattern_entities = self._find_entities_in_sentence(sentence, entity_type, start_id)
                        entities.extend(pattern_entities)
                        start_id += len(pattern_entities)
        
        except Exception as e:
            logger.error(f"Semantic similarity detection failed: {str(e)}")
        
        return entities
    
    def _find_entities_in_sentence(self, sentence: str, entity_type: str, start_id: int) -> List[Dict[str, Any]]:
        """Find specific entities in a sentence"""
        entities = []
        
        if entity_type in self.patterns:
            pattern = self.patterns[entity_type]
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            
            for match in matches:
                entities.append({
                    'id': f'semantic-{start_id + len(entities)}',
                    'entity_type': entity_type,
                    'entity_text': match.group(),
                    'confidence_score': 0.80,
                    'start_char': match.start(),
                    'end_char': match.end(),
                    'page_number': 1,
                    'line_number': 1,
                    'detection_method': 'semantic_similarity'
                })
        
        return entities
    
    def _detect_with_context_analysis(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Advanced context-aware entity detection"""
        entities = []
        
        try:
            # Split into sentences for context analysis
            sentences = re.split(r'[.!?]+', text)
            
            for i, sentence in enumerate(sentences):
                # Look for context clues
                context_entities = self._analyze_sentence_context_advanced(sentence, i, start_id)
                entities.extend(context_entities)
                start_id += len(context_entities)
        
        except Exception as e:
            logger.error(f"Context analysis failed: {str(e)}")
        
        return entities
    
    def _analyze_sentence_context_advanced(self, sentence: str, sentence_id: int, start_id: int) -> List[Dict[str, Any]]:
        """Advanced sentence context analysis"""
        entities = []
        
        # Enhanced context patterns
        context_patterns = {
            'PERSON': [
                r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Contact:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Manager:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Employee:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'CEO:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'Director:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            ],
            'EMAIL': [
                r'Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'Contact Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'Work Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'PHONE': [
                r'Phone:\s*([\(]?[0-9]{3}[\)]?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})',
                r'Contact Phone:\s*([\(]?[0-9]{3}[\)]?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})',
                r'Mobile:\s*([\(]?[0-9]{3}[\)]?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})'
            ],
            'SSN': [
                r'SSN:\s*(\d{3}-\d{2}-\d{4})',
                r'Social Security:\s*(\d{3}-\d{2}-\d{4})',
                r'Tax ID:\s*(\d{3}-\d{2}-\d{4})'
            ],
            'CREDIT_CARD': [
                r'Credit Card:\s*(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})',
                r'Card Number:\s*(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})',
                r'Payment Card:\s*(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})'
            ],
            'API_KEY': [
                r'API Key:\s*([a-zA-Z0-9]{20,})',
                r'Token:\s*([a-zA-Z0-9]{20,})',
                r'Secret:\s*([a-zA-Z0-9]{20,})'
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
                        'confidence_score': 0.95,  # Very high confidence due to context
                        'start_char': match.start(1),
                        'end_char': match.end(1),
                        'page_number': 1,
                        'line_number': 1,
                        'detection_method': 'context_analysis'
                    })
        
        return entities
    
    def _detect_with_patterns(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Pattern-based detection with enhanced patterns"""
        entities = []
        
        for entity_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Enhanced validation for specific entity types
                confidence = self._validate_entity(entity_type, match.group())
                
                entities.append({
                    'id': f'pattern-{start_id + len(entities)}',
                    'entity_type': entity_type,
                    'entity_text': match.group(),
                    'confidence_score': confidence,
                    'start_char': match.start(),
                    'end_char': match.end(),
                    'page_number': 1,
                    'line_number': text[:match.start()].count('\n') + 1,
                    'detection_method': 'pattern'
                })
        
        return entities
    
    def _validate_entity(self, entity_type: str, entity_text: str) -> float:
        """Enhanced validation for different entity types"""
        base_confidence = 0.75
        
        if entity_type == 'EMAIL':
            return self._validate_email(entity_text)
        elif entity_type == 'CREDIT_CARD':
            return self._validate_credit_card(entity_text)
        elif entity_type == 'SSN':
            return self._validate_ssn(entity_text)
        elif entity_type == 'PHONE':
            return self._validate_phone(entity_text)
        elif entity_type == 'IP_ADDRESS':
            return self._validate_ip_address(entity_text)
        else:
            return base_confidence
    
    def _validate_email(self, email: str) -> float:
        """Enhanced email validation"""
        confidence = 0.5
        
        try:
            local, domain = email.split('@')
            
            # Length checks
            if 3 <= len(local) <= 64:
                confidence += 0.2
            if 4 <= len(domain) <= 253:
                confidence += 0.2
            
            # Format checks
            if re.match(r'^[a-zA-Z0-9._%+-]+$', local):
                confidence += 0.1
            if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
                confidence += 0.2
            
            # Common domain check
            common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
            if domain.lower() in common_domains:
                confidence += 0.1
            
        except:
            confidence = 0.3
        
        return min(confidence, 1.0)
    
    def _validate_credit_card(self, cc_text: str) -> float:
        """Enhanced credit card validation"""
        cc_number = re.sub(r'[^0-9]', '', cc_text)
        
        if len(cc_number) != 16:
            return 0.3
        
        # Luhn algorithm
        if self._luhn_check(cc_number):
            return 0.95
        else:
            return 0.6
    
    def _validate_ssn(self, ssn_text: str) -> float:
        """Enhanced SSN validation"""
        ssn = re.sub(r'[^0-9]', '', ssn_text)
        
        if len(ssn) != 9:
            return 0.0
        
        area = int(ssn[:3])
        group = int(ssn[3:5])
        serial = int(ssn[5:])
        
        confidence = 0.5
        
        # Invalid ranges
        if area == 0 or area == 666 or area >= 900:
            confidence -= 0.5
        if group == 0:
            confidence -= 0.3
        if serial == 0:
            confidence -= 0.3
        
        # Valid ranges
        if 1 <= area <= 899 and area != 666:
            confidence += 0.3
        if 1 <= group <= 99:
            confidence += 0.1
        if 1 <= serial <= 9999:
            confidence += 0.1
        
        return min(max(confidence, 0.0), 1.0)
    
    def _validate_phone(self, phone: str) -> float:
        """Enhanced phone validation"""
        digits = re.sub(r'[^0-9]', '', phone)
        
        if len(digits) == 10:
            return 0.9
        elif len(digits) == 11 and digits[0] == '1':
            return 0.85
        else:
            return 0.6
    
    def _validate_ip_address(self, ip: str) -> float:
        """Enhanced IP address validation"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return 0.3
            
            for part in parts:
                if not 0 <= int(part) <= 255:
                    return 0.3
            
            return 0.9
        except:
            return 0.3
    
    def _luhn_check(self, number: str) -> bool:
        """Luhn algorithm for credit card validation"""
        digits = [int(d) for d in number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(divmod(d * 2, 10))
        return checksum % 10 == 0
    
    def _advanced_deduplication_and_scoring(self, redactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Advanced deduplication and confidence scoring"""
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
                # Multiple detections - use advanced selection
                best_detection = self._select_best_detection_advanced(group)
                final_redactions.append(best_detection)
        
        # Sort by confidence score
        final_redactions.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return final_redactions
    
    def _select_best_detection_advanced(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Advanced selection of best detection from multiple candidates"""
        # Priority order for detection methods
        method_priority = {
            'llama': 1,
            'ml_ensemble': 2,
            'nlp_spacy': 3,
            'semantic_similarity': 4,
            'context_analysis': 5,
            'pattern': 6
        }
        
        # Sort by priority and confidence
        sorted_detections = sorted(
            detections,
            key=lambda x: (method_priority.get(x.get('detection_method', 'pattern'), 7), x['confidence_score']),
            reverse=True
        )
        
        return sorted_detections[0]
    
    def _split_text_into_chunks(self, text: str, max_length: int = 1024) -> List[str]:
        """Split text into chunks for processing"""
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
    
    def process_document_advanced(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Advanced AI-powered document processing
        """
        try:
            logger.info(f"Processing document: {filename} ({len(file_content)} bytes)")
            
            # Extract text from document
            text = self.extract_text_from_document(file_content, filename)
            
            logger.info(f"Extracted text length: {len(text)} characters")
            logger.info(f"Text preview: {text[:200]}...")
            
            # Check if we got actual content or error message
            if text.startswith("Failed to extract") or text.startswith("PDF processing error") or text.startswith("Word document processing error"):
                logger.error(f"Text extraction failed for {filename}: {text}")
                return {
                    'original_text': text,
                    'redacted_text': text,
                    'redactions': [],
                    'redactions_count': 0,
                    'ai_models_used': [],
                    'processing_method': 'error',
                    'error': text
                }
            
            # Advanced AI-powered entity detection
            redactions = self.detect_sensitive_entities_advanced(text)
            
            # Apply redactions
            redacted_text = self.apply_redactions(text, redactions)
            
            logger.info(f"Processing completed: {len(redactions)} entities detected")
            
            return {
                'original_text': text,
                'redacted_text': redacted_text,
                'redactions': redactions,
                'redactions_count': len(redactions),
                'ai_models_used': self._get_used_models(redactions),
                'processing_method': 'advanced_ai'
            }
            
        except Exception as e:
            logger.error("Advanced AI document processing failed", error=str(e))
            raise
    
    def extract_text_from_document(self, file_content: bytes, filename: str) -> str:
        """Extract text from document with OCR support"""
        if filename.lower().endswith('.txt'):
            return file_content.decode('utf-8', errors='ignore')
        elif filename.lower().endswith('.pdf'):
            return self._extract_pdf_text(file_content)
        elif filename.lower().endswith(('.doc', '.docx')):
            return self._extract_doc_text(file_content)
        elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
            return self._extract_image_text(file_content)
        else:
            return file_content.decode('utf-8', errors='ignore')
    
    def _extract_pdf_text(self, file_content: bytes) -> str:
        """Extract text from PDF with better error handling"""
        try:
            import PyPDF2
            import pdfplumber
            import io
            
            # Validate PDF header
            if not file_content.startswith(b'%PDF'):
                logger.error("File does not have valid PDF header")
                return "Invalid PDF file: File does not appear to be a valid PDF document"
            
            # Check file size
            if len(file_content) < 100:
                logger.error("PDF file is too small")
                return "Invalid PDF file: File is too small to be a valid PDF"
            
            # Convert bytes to BytesIO for PDF libraries
            file_stream = io.BytesIO(file_content)
            
            # Try pdfplumber first (better text extraction)
            try:
                with pdfplumber.open(file_stream) as pdf:
                    # Check if PDF has pages
                    if len(pdf.pages) == 0:
                        logger.warning("PDF has no pages")
                        return "PDF appears to be empty (no pages found)"
                    
                    text = ""
                    for i, page in enumerate(pdf.pages):
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                        else:
                            logger.warning(f"Page {i+1} has no extractable text (might be image-based)")
                    
                    if text.strip():
                        logger.info(f"Successfully extracted {len(text)} characters from PDF using pdfplumber")
                        return text
                    else:
                        logger.warning("PDF text extraction returned empty content - likely image-based PDF")
                        return "PDF appears to contain only images or scanned content. OCR is required for text extraction."
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {str(e)}")
            
            # Reset stream for PyPDF2
            file_stream.seek(0)
            
            # Fallback to PyPDF2
            try:
                pdf_reader = PyPDF2.PdfReader(file_stream)
                
                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    logger.error("PDF is password-protected")
                    return "PDF is password-protected. Please provide the password or use an unencrypted version."
                
                # Check if PDF has pages
                if len(pdf_reader.pages) == 0:
                    logger.warning("PDF has no pages")
                    return "PDF appears to be empty (no pages found)"
                
                text = ""
                for i, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        logger.warning(f"Page {i+1} has no extractable text")
                
                if text.strip():
                    logger.info(f"Successfully extracted {len(text)} characters from PDF using PyPDF2")
                    return text
                else:
                    logger.warning("PyPDF2 text extraction returned empty content")
                    return "PDF appears to contain only images or scanned content. OCR is required for text extraction."
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {str(e)}")
            
            # If both methods fail, provide detailed error message
            logger.error("Both PDF text extraction methods failed")
            return "Failed to extract text from PDF. Possible reasons:\n" + \
                   "1. PDF is corrupted or damaged\n" + \
                   "2. PDF contains only scanned images (needs OCR)\n" + \
                   "3. PDF is password-protected\n" + \
                   "4. File is not actually a PDF despite extension"
            
        except Exception as e:
            logger.error(f"PDF text extraction failed: {str(e)}")
            return f"PDF processing error: {str(e)}"
    
    def _extract_doc_text(self, file_content: bytes) -> str:
        """Extract text from Word documents with better error handling"""
        try:
            from docx import Document
            import io
            
            # Convert bytes to BytesIO for docx library
            file_stream = io.BytesIO(file_content)
            
            doc = Document(file_stream)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            if text.strip():
                logger.info(f"Successfully extracted {len(text)} characters from Word document")
                return text
            else:
                logger.warning("Word document text extraction returned empty content")
                return "Word document appears to be empty or contains no extractable text"
            
        except Exception as e:
            logger.error(f"DOC text extraction failed: {str(e)}")
            return f"Word document processing error: {str(e)}"
    
    def _extract_image_text(self, file_content: bytes) -> str:
        """Extract text from images using OCR (simplified version without cv2)"""
        try:
            # Since we removed cv2 and OCR dependencies, return a fallback message
            # In a production environment, you would install these dependencies
            logger.warning("Image OCR not available - cv2 and OCR libraries not installed")
            return "Image text extraction not available. Please install opencv-python, pytesseract, and easyocr for full OCR support."
            
        except Exception as e:
            logger.error(f"Image text extraction failed: {str(e)}")
            return "Image text extraction failed"
    
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

    def validate_pdf_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Validate PDF file and provide diagnostic information"""
        try:
            import PyPDF2
            import pdfplumber
            import io
            
            result = {
                'filename': filename,
                'file_size': len(file_content),
                'is_valid_pdf': False,
                'has_pdf_header': False,
                'is_encrypted': False,
                'page_count': 0,
                'has_text': False,
                'errors': [],
                'warnings': []
            }
            
            # Check PDF header
            if file_content.startswith(b'%PDF'):
                result['has_pdf_header'] = True
            else:
                result['errors'].append("File does not have valid PDF header")
                return result
            
            # Check file size
            if len(file_content) < 100:
                result['errors'].append("File is too small to be a valid PDF")
                return result
            
            # Convert bytes to BytesIO
            file_stream = io.BytesIO(file_content)
            
            # Try pdfplumber
            try:
                with pdfplumber.open(file_stream) as pdf:
                    result['page_count'] = len(pdf.pages)
                    if result['page_count'] > 0:
                        result['is_valid_pdf'] = True
                        
                        # Check for text content
                        text = ""
                        for i, page in enumerate(pdf.pages):
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text
                            else:
                                result['warnings'].append(f"Page {i+1} has no extractable text")
                        
                        if text.strip():
                            result['has_text'] = True
                        else:
                            result['warnings'].append("PDF contains no extractable text (likely image-based)")
                            
            except Exception as e:
                result['errors'].append(f"pdfplumber error: {str(e)}")
            
            # Try PyPDF2
            try:
                file_stream.seek(0)
                pdf_reader = PyPDF2.PdfReader(file_stream)
                
                if pdf_reader.is_encrypted:
                    result['is_encrypted'] = True
                    result['errors'].append("PDF is password-protected")
                
                if len(pdf_reader.pages) > 0 and not result['is_valid_pdf']:
                    result['is_valid_pdf'] = True
                    result['page_count'] = len(pdf_reader.pages)
                    
            except Exception as e:
                result['errors'].append(f"PyPDF2 error: {str(e)}")
            
            return result
            
        except Exception as e:
            return {
                'filename': filename,
                'file_size': len(file_content),
                'is_valid_pdf': False,
                'errors': [f"Validation error: {str(e)}"]
            } 