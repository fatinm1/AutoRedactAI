import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import re
from typing import List, Dict, Any, Tuple
import numpy as np
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()


@dataclass
class RedactionEntity:
    """Data class for redaction entities."""
    entity_type: str
    entity_text: str
    confidence_score: float
    start_char: int
    end_char: int
    page_number: int = None
    line_number: int = None
    context_before: str = ""
    context_after: str = ""


class RedactionEngine:
    """AI-powered redaction engine using spaCy and BERT."""
    
    def __init__(self):
        self.nlp = None
        self.bert_tokenizer = None
        self.bert_model = None
        self.ner_pipeline = None
        self._load_models()
        self._setup_regex_patterns()
    
    def _load_models(self):
        """Load spaCy and BERT models."""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
            
            # Load BERT model for NER
            model_name = "dslim/bert-base-NER"
            self.bert_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.bert_model = AutoModelForTokenClassification.from_pretrained(model_name)
            self.ner_pipeline = pipeline(
                "ner",
                model=self.bert_model,
                tokenizer=self.bert_tokenizer,
                aggregation_strategy="simple"
            )
            logger.info("BERT NER model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def _setup_regex_patterns(self):
        """Setup regex patterns for specific entity types."""
        self.regex_patterns = {
            "SSN": [
                r"\b\d{3}-\d{2}-\d{4}\b",  # 123-45-6789
                r"\b\d{9}\b",  # 123456789
            ],
            "EMAIL": [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            ],
            "PHONE": [
                r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # 123-456-7890
                r"\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b",  # (123) 456-7890
            ],
            "CREDIT_CARD": [
                r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # 4111 1111 1111 1111
                r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",
            ],
            "BANK_ACCOUNT": [
                r"\b\d{8,17}\b",  # 8-17 digit account numbers
            ],
            "IP_ADDRESS": [
                r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            ],
            "DATE": [
                r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",  # MM/DD/YYYY
                r"\b\d{4}-\d{2}-\d{2}\b",  # YYYY-MM-DD
            ],
        }
    
    def detect_entities(self, text: str) -> List[RedactionEntity]:
        """Detect sensitive entities in text using multiple methods."""
        entities = []
        
        # 1. spaCy NER detection
        spacy_entities = self._detect_spacy_entities(text)
        entities.extend(spacy_entities)
        
        # 2. BERT NER detection
        bert_entities = self._detect_bert_entities(text)
        entities.extend(bert_entities)
        
        # 3. Regex pattern detection
        regex_entities = self._detect_regex_entities(text)
        entities.extend(regex_entities)
        
        # 4. Remove duplicates and merge overlapping entities
        entities = self._merge_overlapping_entities(entities)
        
        # 5. Add context and filter by confidence
        entities = self._add_context_and_filter(text, entities)
        
        return entities
    
    def _detect_spacy_entities(self, text: str) -> List[RedactionEntity]:
        """Detect entities using spaCy."""
        entities = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            # Map spaCy entity types to our types
            entity_type = self._map_spacy_entity_type(ent.label_)
            if entity_type:
                entities.append(RedactionEntity(
                    entity_type=entity_type,
                    entity_text=ent.text,
                    confidence_score=0.8,  # spaCy doesn't provide confidence scores
                    start_char=ent.start_char,
                    end_char=ent.end_char
                ))
        
        return entities
    
    def _detect_bert_entities(self, text: str) -> List[RedactionEntity]:
        """Detect entities using BERT."""
        entities = []
        
        try:
            results = self.ner_pipeline(text)
            
            for result in results:
                entity_type = self._map_bert_entity_type(result["entity_group"])
                if entity_type:
                    entities.append(RedactionEntity(
                        entity_type=entity_type,
                        entity_text=result["word"],
                        confidence_score=result["score"],
                        start_char=result["start"],
                        end_char=result["end"]
                    ))
        except Exception as e:
            logger.error(f"Error in BERT entity detection: {e}")
        
        return entities
    
    def _detect_regex_entities(self, text: str) -> List[RedactionEntity]:
        """Detect entities using regex patterns."""
        entities = []
        
        for entity_type, patterns in self.regex_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entities.append(RedactionEntity(
                        entity_type=entity_type,
                        entity_text=match.group(),
                        confidence_score=0.95,  # High confidence for regex matches
                        start_char=match.start(),
                        end_char=match.end()
                    ))
        
        return entities
    
    def _map_spacy_entity_type(self, spacy_type: str) -> str:
        """Map spaCy entity types to our entity types."""
        mapping = {
            "PERSON": "PERSON",
            "ORG": "ORGANIZATION",
            "GPE": "LOCATION",
            "LOC": "LOCATION",
            "DATE": "DATE",
            "TIME": "TIME",
            "MONEY": "MONEY",
            "CARDINAL": "NUMBER",
            "ORDINAL": "NUMBER",
        }
        return mapping.get(spacy_type)
    
    def _map_bert_entity_type(self, bert_type: str) -> str:
        """Map BERT entity types to our entity types."""
        mapping = {
            "PER": "PERSON",
            "ORG": "ORGANIZATION",
            "LOC": "LOCATION",
            "MISC": "MISC",
        }
        return mapping.get(bert_type)
    
    def _merge_overlapping_entities(self, entities: List[RedactionEntity]) -> List[RedactionEntity]:
        """Merge overlapping entities and remove duplicates."""
        if not entities:
            return entities
        
        # Sort by start position
        entities.sort(key=lambda x: x.start_char)
        
        merged = []
        current = entities[0]
        
        for next_entity in entities[1:]:
            # Check for overlap
            if (current.end_char >= next_entity.start_char and 
                current.entity_type == next_entity.entity_type):
                # Merge overlapping entities
                current.end_char = max(current.end_char, next_entity.end_char)
                current.entity_text = current.entity_text + " " + next_entity.entity_text
                current.confidence_score = max(current.confidence_score, next_entity.confidence_score)
            else:
                merged.append(current)
                current = next_entity
        
        merged.append(current)
        return merged
    
    def _add_context_and_filter(self, text: str, entities: List[RedactionEntity]) -> List[RedactionEntity]:
        """Add context to entities and filter by confidence threshold."""
        filtered_entities = []
        
        for entity in entities:
            # Add context
            context_size = 50
            start_context = max(0, entity.start_char - context_size)
            end_context = min(len(text), entity.end_char + context_size)
            
            entity.context_before = text[start_context:entity.start_char].strip()
            entity.context_after = text[entity.end_char:end_context].strip()
            
            # Filter by confidence threshold
            if entity.confidence_score >= 0.7:
                filtered_entities.append(entity)
        
        return filtered_entities
    
    def redact_text(self, text: str, entities: List[RedactionEntity], 
                   method: str = "black_box") -> Tuple[str, List[Dict[str, Any]]]:
        """Redact sensitive entities from text."""
        redacted_text = text
        redaction_log = []
        
        # Sort entities by start position (reverse order to maintain indices)
        entities.sort(key=lambda x: x.start_char, reverse=True)
        
        for entity in entities:
            if entity.is_redacted:
                # Create redaction mask
                if method == "black_box":
                    mask = "█" * len(entity.entity_text)
                elif method == "white_out":
                    mask = " " * len(entity.entity_text)
                elif method == "custom_text":
                    mask = entity.custom_replacement or "[REDACTED]"
                else:
                    mask = "█" * len(entity.entity_text)
                
                # Apply redaction
                redacted_text = (
                    redacted_text[:entity.start_char] + 
                    mask + 
                    redacted_text[entity.end_char:]
                )
                
                # Log redaction
                redaction_log.append({
                    "entity_type": entity.entity_type,
                    "original_text": entity.entity_text,
                    "redacted_text": mask,
                    "start_char": entity.start_char,
                    "end_char": entity.end_char,
                    "confidence_score": entity.confidence_score,
                    "redaction_method": method
                })
        
        return redacted_text, redaction_log
    
    def get_entity_statistics(self, entities: List[RedactionEntity]) -> Dict[str, Any]:
        """Get statistics about detected entities."""
        stats = {
            "total_entities": len(entities),
            "entity_types": {},
            "confidence_distribution": {
                "high": 0,    # >= 0.9
                "medium": 0,  # 0.7-0.9
                "low": 0      # < 0.7
            }
        }
        
        for entity in entities:
            # Count by entity type
            entity_type = entity.entity_type
            if entity_type not in stats["entity_types"]:
                stats["entity_types"][entity_type] = 0
            stats["entity_types"][entity_type] += 1
            
            # Count by confidence level
            if entity.confidence_score >= 0.9:
                stats["confidence_distribution"]["high"] += 1
            elif entity.confidence_score >= 0.7:
                stats["confidence_distribution"]["medium"] += 1
            else:
                stats["confidence_distribution"]["low"] += 1
        
        return stats 