#!/usr/bin/env python3
"""
Database Setup Script for AutoRedactAI
This script initializes the PostgreSQL database with all required tables and initial data.
"""

import os
import sys
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import structlog

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.config import settings
from backend.app.models.database import Base, User
from backend.app.core.security import get_password_hash

logger = structlog.get_logger()

def setup_database():
    """Initialize the database with tables and initial data."""
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL', settings.DATABASE_URL)
    
    logger.info(f"Setting up database: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(
            database_url,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            echo=True  # Log SQL queries
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"Connected to PostgreSQL: {version}")
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@autoredact.ai").first()
        
        if not admin_user:
            # Create admin user
            logger.info("Creating admin user...")
            admin_user = User(
                email="admin@autoredact.ai",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("✅ Admin user created successfully!")
            logger.info("📧 Email: admin@autoredact.ai")
            logger.info("🔑 Password: admin123")
        else:
            logger.info("✅ Admin user already exists")
        
        # Create demo user
        demo_user = db.query(User).filter(User.email == "demo@autoredact.ai").first()
        
        if not demo_user:
            logger.info("Creating demo user...")
            demo_user = User(
                email="demo@autoredact.ai",
                username="demo",
                hashed_password=get_password_hash("demo123"),
                full_name="Demo User",
                role="user",
                is_active=True,
                is_verified=True
            )
            db.add(demo_user)
            db.commit()
            logger.info("✅ Demo user created successfully!")
            logger.info("📧 Email: demo@autoredact.ai")
            logger.info("🔑 Password: demo123")
        else:
            logger.info("✅ Demo user already exists")
        
        db.close()
        
        logger.info("🎉 Database setup completed successfully!")
        logger.info("📊 Tables created:")
        logger.info("   - users")
        logger.info("   - documents")
        logger.info("   - redactions")
        logger.info("   - audit_logs")
        logger.info("   - processing_jobs")
        logger.info("   - export_jobs")
        logger.info("   - team_collaborations")
        logger.info("   - compliance_reports")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

def main():
    """Main function to run database setup."""
    print("🚀 AutoRedactAI Database Setup")
    print("=" * 40)
    
    success = setup_database()
    
    if success:
        print("\n✅ Database setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Configure environment variables in Railway")
        print("2. Test the API endpoints")
        print("3. Set up file storage (AWS S3)")
        print("4. Configure AI models")
    else:
        print("\n❌ Database setup failed!")
        print("Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 