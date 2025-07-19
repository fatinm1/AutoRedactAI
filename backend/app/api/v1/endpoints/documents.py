from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional, Dict, Any
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document, DocumentResponse, DocumentListResponse
from app.services.document_service import DocumentService
from app.services.advanced_ai_service import AdvancedAIService
import uuid
from datetime import datetime
import structlog

logger = structlog.get_logger()
router = APIRouter()

# Use singleton instances
document_service = DocumentService()
advanced_ai_service = AdvancedAIService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document for processing
    """
    # Validate file type
    allowed_types = [".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png", ".tiff"]
    file_extension = file.filename.lower().split(".")[-1] if "." in file.filename else ""
    
    if f".{file_extension}" not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Validate file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum size is 10MB"
        )
    
    try:
        # Create document record
        document = Document(
            id=str(uuid.uuid4()),
            filename=file.filename,
            file_size=file.size,
            user_id=current_user.id,
            status="uploaded",
            created_at=datetime.utcnow().isoformat(),
            redactions_count=0
        )
        
        # Store document (in a real app, you'd save the file to storage)
        document_service.store_document(document)
        
        return DocumentResponse(
            success=True,
            message="Document uploaded successfully",
            document=document
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload document: {str(e)}"
        )

@router.post("/{document_id}/process", response_model=DocumentResponse)
async def process_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Process a document for redaction using Advanced AI (Llama + ML)
    """
    try:
        # Get the document
        document = document_service.get_document(document_id, current_user.id)
        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        if document.status != "uploaded":
            raise HTTPException(
                status_code=400,
                detail=f"Document is already {document.status}"
            )
        
        # Update status to processing
        document_service.update_document_status(document_id, current_user.id, "processing")
        
        # In a real app, you would read the actual file from storage
        # For now, we'll simulate file content based on filename
        file_content = b"Simulated file content"  # In real app: read from storage
        
        # Process document using Advanced AI service
        processing_result = advanced_ai_service.process_document_advanced(file_content, document.filename)
        
        # Store redactions in document service (in a real app, you'd store in database)
        document_service.store_document_redactions(document_id, processing_result['redactions'])
        
        # Update document status to completed with real redactions count
        updated_document = document_service.update_document_status(
            document_id, 
            current_user.id, 
            "completed", 
            processing_result['redactions_count']
        )
        
        logger.info("Advanced AI document processing completed successfully", 
                   document_id=document_id, 
                   user_id=current_user.id,
                   redactions_count=processing_result['redactions_count'],
                   ai_models_used=processing_result.get('ai_models_used', []),
                   processing_method=processing_result.get('processing_method', 'advanced_ai'),
                   detected_entities=[r['entity_type'] for r in processing_result['redactions']])
        
        return DocumentResponse(
            success=True,
            message="Document processed successfully with Advanced AI (Llama + ML)",
            document=updated_document
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Advanced AI document processing failed", 
                    document_id=document_id, 
                    user_id=current_user.id,
                    error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )

@router.get("/{document_id}/redactions")
async def get_document_redactions(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get redactions for a specific document
    """
    try:
        # Get the document
        document = document_service.get_document(document_id, current_user.id)
        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        if document.status != "completed":
            raise HTTPException(
                status_code=400,
                detail="Document has not been processed yet"
            )
        
        # Get redactions from document service
        redactions = document_service.get_document_redactions(document_id)
        
        return {
            "success": True,
            "message": "Redactions retrieved successfully",
            "redactions": redactions,
            "total_count": len(redactions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve redactions", 
                    document_id=document_id, 
                    user_id=current_user.id,
                    error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve redactions: {str(e)}"
        )

@router.get("/", response_model=DocumentListResponse)
async def get_documents(
    current_user: User = Depends(get_current_user)
):
    """
    Get all documents for the current user
    """
    try:
        documents = document_service.get_user_documents(current_user.id)
        return DocumentListResponse(
            success=True,
            message="Documents retrieved successfully",
            documents=documents
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve documents: {str(e)}"
        )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific document by ID
    """
    try:
        document = document_service.get_document(document_id, current_user.id)
        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        return DocumentResponse(
            success=True,
            message="Document retrieved successfully",
            document=document
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve document: {str(e)}"
        ) 