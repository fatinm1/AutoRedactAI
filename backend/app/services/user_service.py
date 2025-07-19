import bcrypt
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.user import User, UserCreate
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
            # In-memory storage for users (in a real app, this would be a database)
            self.users: Dict[str, User] = {}
            self._initialize_demo_user()
            UserService._initialized = True
    
    def _initialize_demo_user(self):
        """Initialize demo user"""
        demo_user = User(
            id="demo-user-id",
            email="demo@autoredact.ai",
            full_name="Demo User",
            hashed_password=self._hash_password("demo123"),
            is_active=True,
            created_at=datetime.utcnow().isoformat()
        )
        self.users[demo_user.id] = demo_user
        logger.info("Demo user initialized", email=demo_user.email, user_id=demo_user.id)
    
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
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        for user in self.users.values():
            if user.email == user_data.email:
                raise ValueError("User with this email already exists")
        
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=self._hash_password(user_data.password),
            is_active=True,
            created_at=datetime.utcnow().isoformat()
        )
        
        self.users[user.id] = user
        logger.info("User created", user_id=user.id, email=user.email)
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        logger.info("Authenticating user", email=email)
        
        # Find user by email
        user = self.get_user_by_email(email)
        if not user:
            logger.warning("User not found during authentication", email=email)
            return None
        
        logger.info("User found during authentication", user_id=user.id)
        
        # Verify password
        if not self._verify_password(password, user.hashed_password):
            logger.warning("Password verification failed", email=email)
            return None
        
        logger.info("Authentication successful", user_id=user.id)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        for user in self.users.values():
            if user.email == email:
                logger.info("User found by email", email=email, user_id=user.id)
                return user
        logger.warning("User not found by email", email=email)
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        user = self.users.get(user_id)
        if user:
            logger.info("User found by ID", user_id=user_id)
        else:
            logger.warning("User not found by ID", user_id=user_id)
        return user
    
    def get_all_users(self) -> list[User]:
        """Get all users"""
        return list(self.users.values())
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user information"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        # Update allowed fields
        for key, value in kwargs.items():
            if hasattr(user, key) and key not in ['id', 'hashed_password']:
                setattr(user, key, value)
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False 