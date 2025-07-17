from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

# Redis connection for rate limiting
redis_client = redis.from_url(settings.REDIS_URL)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = security) -> Dict[str, Any]:
    """Get current user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": user_id, "payload": payload}


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Create rate limit key
    minute_key = f"rate_limit:{client_ip}:{user_agent}:minute"
    hour_key = f"rate_limit:{client_ip}:{user_agent}:hour"
    
    try:
        # Check minute rate limit
        minute_count = redis_client.get(minute_key)
        if minute_count and int(minute_count) >= settings.RATE_LIMIT_PER_MINUTE:
            logger.warning(
                "Rate limit exceeded (minute)",
                client_ip=client_ip,
                user_agent=user_agent
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Check hour rate limit
        hour_count = redis_client.get(hour_key)
        if hour_count and int(hour_count) >= settings.RATE_LIMIT_PER_HOUR:
            logger.warning(
                "Rate limit exceeded (hour)",
                client_ip=client_ip,
                user_agent=user_agent
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Increment counters
        pipe = redis_client.pipeline()
        pipe.incr(minute_key)
        pipe.expire(minute_key, 60)
        pipe.incr(hour_key)
        pipe.expire(hour_key, 3600)
        pipe.execute()
        
        response = await call_next(request)
        return response
        
    except redis.RedisError as e:
        logger.error("Redis error in rate limiting", error=str(e))
        # Continue without rate limiting if Redis is down
        return await call_next(request)


def validate_file_type(filename: str) -> bool:
    """Validate if file type is allowed."""
    return any(filename.lower().endswith(ext) for ext in settings.ALLOWED_FILE_TYPES)


def validate_file_size(file_size: int) -> bool:
    """Validate if file size is within limits."""
    return file_size <= settings.MAX_FILE_SIZE


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    import re
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:255-len(ext)-1] + '.' + ext
    return filename


def generate_secure_filename(original_filename: str) -> str:
    """Generate a secure, unique filename."""
    import uuid
    import os
    
    # Get file extension
    _, ext = os.path.splitext(original_filename)
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    return f"{timestamp}_{unique_id}{ext}"


class SecurityUtils:
    """Utility class for security operations."""
    
    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data for logging."""
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    @staticmethod
    def mask_credit_card(card_number: str) -> str:
        """Mask credit card number for display."""
        if len(card_number) < 4:
            return card_number
        return "*" * (len(card_number) - 4) + card_number[-4:]
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address for display."""
        if "@" not in email:
            return email
        
        username, domain = email.split("@", 1)
        if len(username) <= 2:
            masked_username = username
        else:
            masked_username = username[0] + "*" * (len(username) - 2) + username[-1]
        
        return f"{masked_username}@{domain}"
    
    @staticmethod
    def mask_ssn(ssn: str) -> str:
        """Mask SSN for display."""
        if len(ssn) < 4:
            return ssn
        return "*" * (len(ssn) - 4) + ssn[-4:] 