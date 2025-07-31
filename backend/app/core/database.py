from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings
import structlog
import os

logger = structlog.get_logger()

# Database URL configuration
if settings.ENVIRONMENT == "development":
    # Use SQLite for development if PostgreSQL is not available
    DATABASE_URL = settings.DATABASE_URL
else:
    # Use PostgreSQL for production/staging
    DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine with proper configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,
        echo=settings.DEBUG,  # Log SQL queries in debug mode
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Database session error", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    try:
        # Import the Base class from models.database
        from app.models.database import Base, User, Document, Redaction, AuditLog, ProcessingJob, ExportJob, TeamCollaboration, ComplianceReport
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
            
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise

 