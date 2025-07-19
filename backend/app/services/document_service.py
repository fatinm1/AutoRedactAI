from typing import List, Optional, Dict, Any
from app.models.document import Document
import uuid
from datetime import datetime

class DocumentService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not DocumentService._initialized:
            # In-memory storage for documents (in a real app, this would be a database)
            self.documents: List[Document] = []
            # In-memory storage for redactions (in a real app, this would be a database)
            self.redactions: Dict[str, List[Dict[str, Any]]] = {}
            DocumentService._initialized = True
    
    def store_document(self, document: Document) -> Document:
        """Store a new document"""
        self.documents.append(document)
        return document
    
    def store_document_redactions(self, document_id: str, redactions: List[Dict[str, Any]]) -> None:
        """Store redactions for a document"""
        self.redactions[document_id] = redactions
    
    def get_document_redactions(self, document_id: str) -> List[Dict[str, Any]]:
        """Get redactions for a document"""
        return self.redactions.get(document_id, [])
    
    def get_user_documents(self, user_id: str) -> List[Document]:
        """Get all documents for a specific user"""
        return [doc for doc in self.documents if doc.user_id == user_id]
    
    def get_document(self, document_id: str, user_id: str) -> Optional[Document]:
        """Get a specific document by ID for a user"""
        for doc in self.documents:
            if doc.id == document_id and doc.user_id == user_id:
                return doc
        return None
    
    def update_document_status(self, document_id: str, user_id: str, status: str, redactions_count: int = 0) -> Optional[Document]:
        """Update document status and redactions count"""
        for doc in self.documents:
            if doc.id == document_id and doc.user_id == user_id:
                doc.status = status
                doc.redactions_count = redactions_count
                return doc
        return None
    
    def delete_document(self, document_id: str, user_id: str) -> bool:
        """Delete a document"""
        for i, doc in enumerate(self.documents):
            if doc.id == document_id and doc.user_id == user_id:
                del self.documents[i]
                # Also delete associated redactions
                if document_id in self.redactions:
                    del self.redactions[document_id]
                return True
        return False 