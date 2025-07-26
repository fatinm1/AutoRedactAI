import bcrypt
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.database import User
from app.models.user import UserCreate
import structlog

logger = structlog.get_logger()

class UserService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not UserService._initialized:
            UserService._initialized = True
            logger.info("UserService initialized with database")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            result = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            logger.info("Password verification", result=result)
            return result
        except Exception as e:
            logger.error("Password verification failed", error=str(e))
            return False
    
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            username=user_data.email.split('@')[0],  # Use email prefix as username
            full_name=user_data.full_name,
            hashed_password=self._hash_password(user_data.password),
            is_active=True,
            is_verified=False,  # Email verification would be implemented later
            role="user"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info("User created", user_id=user.id, email=user.email)
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        logger.info("Authenticating user", email=email)
        
        # Find user by email
        user = self.get_user_by_email(db, email)
        if not user:
            logger.warning("User not found during authentication", email=email)
            return None
        
        logger.info("User found during authentication", user_id=user.id)
        
        # Verify password
        if not self._verify_password(password, user.hashed_password):
            logger.warning("Password verification failed", email=email)
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        logger.info("Authentication successful", user_id=user.id)
        return user
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        user = db.query(User).filter(User.email == email).first()
        if user:
            logger.info("User found by email", email=email, user_id=user.id)
        else:
            logger.warning("User not found by email", email=email)
        return user
    
    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            logger.info("User found by ID", user_id=user_id)
        else:
            logger.warning("User not found by ID", user_id=user_id)
        return user
    
    def get_all_users(self, db: Session) -> list[User]:
        """Get all users"""
        return db.query(User).all()
    
    def update_user(self, db: Session, user_id: str, **kwargs) -> Optional[User]:
        """Update user information"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Update allowed fields
        for key, value in kwargs.items():
            if hasattr(user, key) and key not in ['id', 'hashed_password']:
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def delete_user(self, db: Session, user_id: str) -> bool:
        """Delete user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    
    def verify_user_email(self, db: Session, user_id: str) -> bool:
        """Verify user email"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = True
            db.commit()
            return True
        return False 