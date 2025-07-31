from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    filename: str
    file_size: Optional[int] = None
    user_id: str
    file_type: Optional[str] = None

class Document(BaseModel):
    id: str
    filename: str
    file_size: Optional[int] = None
    user_id: str
    status: str = "uploaded"  # uploaded, processing, completed, error
    created_at: str
    redactions_count: int = 0
    file_type: Optional[str] = None

class DocumentResponse(BaseModel):
    success: bool
    message: str
    document: Document

class DocumentListResponse(BaseModel):
    success: bool
    message: str
    documents: List[Document] 