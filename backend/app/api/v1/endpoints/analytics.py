from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter()

@router.get("/overview")
async def get_analytics_overview(
    current_user: User = Depends(get_current_user)
):
    """Get analytics overview"""
    # Mock analytics data
    return {
        "total_documents": 25,
        "total_redactions": 150,
        "avg_processing_time": "2.3s",
        "accuracy_rate": "98.5%",
        "monthly_trend": [
            {"month": "Jan", "documents": 5},
            {"month": "Feb", "documents": 8},
            {"month": "Mar", "documents": 12}
        ]
    }

@router.get("/documents")
async def get_document_analytics(
    current_user: User = Depends(get_current_user)
):
    """Get document processing analytics"""
    return {
        "documents_processed": 25,
        "documents_pending": 3,
        "documents_failed": 1,
        "processing_success_rate": "96.2%"
    }

@router.get("/redactions")
async def get_redaction_analytics(
    current_user: User = Depends(get_current_user)
):
    """Get redaction analytics"""
    return {
        "total_redactions": 150,
        "redactions_by_type": {
            "PERSON": 45,
            "EMAIL": 30,
            "PHONE": 25,
            "ADDRESS": 20,
            "SSN": 15,
            "CREDIT_CARD": 15
        },
        "avg_confidence_score": "94.2%"
    } 