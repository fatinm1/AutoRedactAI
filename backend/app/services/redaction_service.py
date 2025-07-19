import re
import uuid
from typing import List, Dict, Any
from datetime import datetime
import structlog

logger = structlog.get_logger()

class RedactionService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedactionService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not RedactionService._initialized:
            # Initialize regex patterns for different entity types
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
            
            # Common names for person detection
            self.common_names = [
                'john', 'jane', 'mike', 'sarah', 'david', 'emma', 'james', 'lisa',
                'robert', 'anna', 'michael', 'jennifer', 'william', 'jessica',
                'richard', 'ashley', 'thomas', 'amanda', 'christopher', 'stephanie',
                'daniel', 'nicole', 'matthew', 'emily', 'anthony', 'elizabeth',
                'mark', 'madison', 'donald', 'brenda', 'steven', 'lauren',
                'paul', 'samantha', 'andrew', 'anna', 'joshua', 'emma',
                'kenneth', 'olivia', 'kevin', 'grace', 'brian', 'chloe',
                'george', 'sophia', 'timothy', 'ava', 'ronald', 'isabella',
                'jason', 'mia', 'edward', 'lily', 'jeffrey', 'zoey',
                'ryan', 'lillian', 'jacob', 'hannah', 'gary', 'layla',
                'nicholas', 'ellie', 'eric', 'riley', 'jonathan', 'nora',
                'stephen', 'lily', 'larry', 'eleanor', 'justin', 'hazel',
                'scott', 'violet', 'brandon', 'aurora', 'benjamin', 'luna',
                'samuel', 'scarlett', 'frank', 'chloe', 'gregory', 'lucy',
                'raymond', 'paisley', 'alexander', 'everly', 'patrick', 'skylar',
                'jack', 'isla', 'dennis', 'maya', 'jerry', 'ellie',
                'tyler', 'madelyn', 'aaron', 'kinsley', 'jose', 'brooklyn',
                'adam', 'mackenzie', 'nathan', 'ivy', 'henry', 'lilly',
                'douglas', 'bella', 'zachary', 'charlotte', 'peter', 'addison',
                'kyle', 'stella', 'walter', 'nora', 'ethan', 'zoey',
                'noah', 'leah', 'jeremy', 'hannah', 'christian', 'lillian',
                'keith', 'aubrey', 'roger', 'savannah', 'terry', 'audrey',
                'gerald', 'brooklyn', 'harold', 'bella', 'sean', 'claire',
                'austin', 'skylar', 'carl', 'lucy', 'arthur', 'paisley',
                'ryan', 'everly', 'lawrence', 'madelyn', 'dylan', 'peyton',
                'jesse', 'mackenzie', 'bryan', 'skylar', 'joe', 'caroline',
                'jordan', 'serenity', 'billy', 'autumn', 'bruce', 'lucy',
                'albert', 'brooklyn', 'willie', 'madelyn', 'gabriel', 'savannah',
                'logan', 'claire', 'alan', 'isabella', 'juan', 'skylar',
                'wayne', 'madelyn', 'roy', 'serenity', 'ralph', 'autumn',
                'randy', 'brooklyn', 'eugene', 'madelyn', 'vincent', 'savannah',
                'russell', 'claire', 'elijah', 'isabella', 'louis', 'skylar',
                'bobby', 'madelyn', 'philip', 'serenity', 'johnny', 'autumn'
            ]
            
            RedactionService._initialized = True
    
    def extract_text_from_document(self, file_content: bytes, filename: str) -> str:
        """
        Extract text from document based on file type
        In a real implementation, you'd use libraries like:
        - PyPDF2 for PDFs
        - python-docx for Word documents
        - For now, we'll simulate text extraction
        """
        # Simulate text extraction based on file type
        if filename.lower().endswith('.txt'):
            return file_content.decode('utf-8', errors='ignore')
        elif filename.lower().endswith('.pdf'):
            # In real implementation: return PyPDF2.PdfReader(file_content).extract_text()
            return self._simulate_pdf_text()
        elif filename.lower().endswith(('.doc', '.docx')):
            # In real implementation: return python-docx.Document(file_content).text
            return self._simulate_doc_text()
        else:
            return file_content.decode('utf-8', errors='ignore')
    
    def _simulate_pdf_text(self) -> str:
        """Simulate PDF text content with sensitive information"""
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
        """Simulate Word document text content with sensitive information"""
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
    
    def detect_sensitive_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect sensitive entities in text using regex patterns and NLP
        """
        redactions = []
        entity_id = 1
        
        # Detect entities using regex patterns
        for entity_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity_text = match.group()
                confidence = self._calculate_confidence(entity_type, entity_text)
                
                redactions.append({
                    'id': f'red-{entity_id}',
                    'entity_type': entity_type,
                    'entity_text': entity_text,
                    'confidence_score': confidence,
                    'start_char': match.start(),
                    'end_char': match.end(),
                    'page_number': 1,  # In real implementation, track page numbers
                    'line_number': text[:match.start()].count('\n') + 1
                })
                entity_id += 1
        
        # Detect person names (simplified approach)
        person_redactions = self._detect_person_names(text, entity_id)
        redactions.extend(person_redactions)
        
        # Sort by confidence score (highest first)
        redactions.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        # Remove duplicates (same text, same type)
        seen = set()
        unique_redactions = []
        for redaction in redactions:
            key = (redaction['entity_text'].lower(), redaction['entity_type'])
            if key not in seen:
                seen.add(key)
                unique_redactions.append(redaction)
        
        logger.info(f"Detected {len(unique_redactions)} sensitive entities", 
                   total_entities=len(unique_redactions))
        
        return unique_redactions
    
    def _detect_person_names(self, text: str, start_id: int) -> List[Dict[str, Any]]:
        """Detect person names using common name patterns"""
        redactions = []
        entity_id = start_id
        
        # Look for title + name patterns
        title_patterns = [
            r'\b(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)\b',
            r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+(Jr\.|Sr\.|III|IV)\b',
            r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        ]
        
        for pattern in title_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                full_name = match.group()
                # Check if it contains common names
                name_parts = full_name.lower().split()
                if any(part in self.common_names for part in name_parts):
                    redactions.append({
                        'id': f'red-{entity_id}',
                        'entity_type': 'PERSON',
                        'entity_text': full_name,
                        'confidence_score': 0.85,
                        'start_char': match.start(),
                        'end_char': match.end(),
                        'page_number': 1,
                        'line_number': text[:match.start()].count('\n') + 1
                    })
                    entity_id += 1
        
        return redactions
    
    def _calculate_confidence(self, entity_type: str, entity_text: str) -> float:
        """Calculate confidence score for detected entity"""
        base_confidence = {
            'EMAIL': 0.98,
            'PHONE': 0.95,
            'SSN': 0.99,
            'CREDIT_CARD': 0.97,
            'IP_ADDRESS': 0.90,
            'URL': 0.85,
            'DATE': 0.80,
            'ZIP_CODE': 0.88,
            'CURRENCY': 0.92,
        }
        
        confidence = base_confidence.get(entity_type, 0.75)
        
        # Adjust confidence based on text quality
        if entity_type == 'EMAIL':
            if '@' in entity_text and '.' in entity_text.split('@')[1]:
                confidence = 0.98
            else:
                confidence = 0.70
        elif entity_type == 'PHONE':
            if len(re.sub(r'[^\d]', '', entity_text)) == 10:
                confidence = 0.95
            else:
                confidence = 0.80
        elif entity_type == 'SSN':
            if len(re.sub(r'[^\d]', '', entity_text)) == 9:
                confidence = 0.99
            else:
                confidence = 0.60
        
        return confidence
    
    def apply_redactions(self, text: str, redactions: List[Dict[str, Any]]) -> str:
        """
        Apply redactions to text by replacing sensitive information with [REDACTED]
        """
        # Sort redactions by start position (reverse order to avoid index shifting)
        sorted_redactions = sorted(redactions, key=lambda x: x['start_char'], reverse=True)
        
        redacted_text = text
        for redaction in sorted_redactions:
            start = redaction['start_char']
            end = redaction['end_char']
            entity_type = redaction['entity_type']
            
            # Replace with redaction marker
            replacement = f'[REDACTED {entity_type}]'
            redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
        
        return redacted_text
    
    def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Main method to process a document and return redactions
        """
        try:
            # Extract text from document
            text = self.extract_text_from_document(file_content, filename)
            
            # Detect sensitive entities
            redactions = self.detect_sensitive_entities(text)
            
            # Apply redactions to create redacted text
            redacted_text = self.apply_redactions(text, redactions)
            
            return {
                'original_text': text,
                'redacted_text': redacted_text,
                'redactions': redactions,
                'redactions_count': len(redactions)
            }
            
        except Exception as e:
            logger.error("Document processing failed", error=str(e))
            raise 