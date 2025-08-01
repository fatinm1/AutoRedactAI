from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.database import DBDocument as Document, Redaction, AuditLog
import uuid
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()

class DocumentService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not DocumentService._initialized:
            DocumentService._initialized = True
            logger.info("DocumentService initialized with database")
    
    def store_document(self, db: Session, document: Document) -> Document:
        """Store a new document"""
        db.add(document)
        db.commit()
        db.refresh(document)
        logger.info("Document stored", document_id=document.id, filename=document.original_filename)
        return document
    
    def store_document_redactions(self, db: Session, document_id: str, redactions: List[Dict[str, Any]]) -> None:
        """Store redactions for a document"""
        # Delete existing redactions for this document
        db.query(Redaction).filter(Redaction.document_id == document_id).delete()
        
        # Add new redactions
        for redaction_data in redactions:
            redaction = Redaction(
                id=str(uuid.uuid4()),
                document_id=document_id,
                entity_type=redaction_data.get('entity_type', 'UNKNOWN'),
                entity_text=redaction_data.get('entity_text', ''),
                confidence_score=redaction_data.get('confidence_score', 0.0),
                start_char=redaction_data.get('start_char', 0),
                end_char=redaction_data.get('end_char', 0),
                page_number=redaction_data.get('page_number'),
                line_number=redaction_data.get('line_number'),
                is_redacted=redaction_data.get('is_redacted', True),
                redaction_method=redaction_data.get('redaction_method', 'black_box'),
                custom_replacement=redaction_data.get('custom_replacement'),
                context_before=redaction_data.get('context_before'),
                context_after=redaction_data.get('context_after'),
                bounding_box=redaction_data.get('bounding_box')
            )
            db.add(redaction)
        
        db.commit()
        logger.info("Redactions stored", document_id=document_id, count=len(redactions))
    
    def get_document_redactions(self, db: Session, document_id: str) -> List[Dict[str, Any]]:
        """Get redactions for a document"""
        redactions = db.query(Redaction).filter(Redaction.document_id == document_id).all()
        
        # Convert to dictionary format for API compatibility
        redaction_list = []
        for redaction in redactions:
            redaction_dict = {
                'id': redaction.id,
                'entity_type': redaction.entity_type,
                'entity_text': redaction.entity_text,
                'confidence_score': redaction.confidence_score,
                'start_char': redaction.start_char,
                'end_char': redaction.end_char,
                'page_number': redaction.page_number,
                'line_number': redaction.line_number,
                'is_redacted': redaction.is_redacted,
                'redaction_method': redaction.redaction_method,
                'custom_replacement': redaction.custom_replacement,
                'context_before': redaction.context_before,
                'context_after': redaction.context_after,
                'bounding_box': redaction.bounding_box,
                'created_at': redaction.created_at.isoformat() if redaction.created_at else None
            }
            redaction_list.append(redaction_dict)
        
        return redaction_list
    
    def get_user_documents(self, db: Session, user_id: str) -> List[Document]:
        """Get all documents for a specific user"""
        return db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()
    
    def get_document(self, db: Session, document_id: str, user_id: str) -> Optional[Document]:
        """Get a specific document by ID for a user"""
        return db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()
    
    def update_document_status(self, db: Session, document_id: str, user_id: str, status: str, redactions_count: int = 0) -> Optional[Document]:
        """Update document status and redactions count"""
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()
        
        if document:
            document.status = status
            if status == "processing":
                document.processing_started = datetime.utcnow()
            elif status == "completed":
                document.processing_completed = datetime.utcnow()
            
            db.commit()
            db.refresh(document)
            logger.info("Document status updated", document_id=document_id, status=status)
        
        return document
    
    def delete_document(self, db: Session, document_id: str, user_id: str) -> bool:
        """Delete a document"""
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user_id
        ).first()
        
        if document:
            # Delete associated redactions
            db.query(Redaction).filter(Redaction.document_id == document_id).delete()
            
            # Delete associated audit logs
            db.query(AuditLog).filter(AuditLog.document_id == document_id).delete()
            
            # Delete the document
            db.delete(document)
            db.commit()
            
            logger.info("Document deleted", document_id=document_id)
            return True
        
        return False
    
    def cleanup_expired_documents(self, db: Session) -> int:
        """Clean up documents that have expired"""
        from app.core.config import settings
        
        expiry_date = datetime.utcnow() - timedelta(days=settings.FILE_RETENTION_DAYS)
        expired_documents = db.query(Document).filter(
            Document.created_at < expiry_date,
            Document.status.in_(["completed", "failed"])
        ).all()
        
        deleted_count = 0
        for document in expired_documents:
            # Delete associated redactions and audit logs
            db.query(Redaction).filter(Redaction.document_id == document.id).delete()
            db.query(AuditLog).filter(AuditLog.document_id == document.id).delete()
            
            # Delete the document
            db.delete(document)
            deleted_count += 1
        
        db.commit()
        logger.info("Expired documents cleaned up", count=deleted_count)
        return deleted_count
    
    def create_audit_log(self, db: Session, user_id: str, action: str, document_id: str = None, details: Dict = None, ip_address: str = None, user_agent: str = None) -> AuditLog:
        """Create an audit log entry"""
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            document_id=document_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        logger.info("Audit log created", action=action, user_id=user_id, document_id=document_id)
        return audit_log 