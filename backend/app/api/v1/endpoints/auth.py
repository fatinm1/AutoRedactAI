from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService
from app.core.auth import create_access_token, verify_token, get_current_user
from app.core.database import get_db
from datetime import timedelta
import structlog

logger = structlog.get_logger()
router = APIRouter()

# Use singleton instance
user_service = UserService()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = user_service.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
        
        # Create new user
        user = user_service.create_user(db, user_data)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=30)
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    try:
        logger.info("Login attempt", email=user_data.email)
        
        # Debug: Check if user exists
        user = user_service.get_user_by_email(db, user_data.email)
        if not user:
            logger.warning("User not found", email=user_data.email)
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        
        logger.info("User found", user_id=user.id, email=user.email)
        
        # Authenticate user
        authenticated_user = user_service.authenticate_user(db, user_data.email, user_data.password)
        if not authenticated_user:
            logger.warning("Authentication failed", email=user_data.email)
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        
        logger.info("Authentication successful", user_id=authenticated_user.id)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": authenticated_user.id},
            expires_delta=timedelta(minutes=30)
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=authenticated_user.id,
                email=authenticated_user.email,
                full_name=authenticated_user.full_name,
                is_active=authenticated_user.is_active
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Login failed"
        )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (in a real app, you'd blacklist the token)"""
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token"""
    try:
        # Verify refresh token (in a real app, you'd have separate refresh tokens)
        payload = verify_token(refresh_data.refresh_token)
        if not payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        
        # Create new access token
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=30)
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Token refresh failed"
        ) 