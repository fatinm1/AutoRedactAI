from fastapi import APIRouter, Depends, HTTPException
from app.models.database import User
from app.models.user import UserResponse
from app.services.user_service import UserService
from app.core.auth import get_current_user
from app.core.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()
user_service = UserService()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_user)):
    """Get all users (admin only)"""
    # In a real app, you'd check if current_user is admin
    users = user_service.get_all_users()
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active
        )
        for user in users
    ]

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active
    ) 