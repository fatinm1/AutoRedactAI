#!/usr/bin/env python3
"""
AutoRedactAI - PostgreSQL Setup Script

This script helps set up PostgreSQL database for the AutoRedactAI application.
It provides options for both local PostgreSQL and cloud databases.

Usage:
    python setup_postgresql.py

Requirements:
    - PostgreSQL server running locally or cloud database URL
    - psycopg2-binary package installed
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🐘 PostgreSQL Setup for AutoRedactAI")
    print("=" * 50)

def check_postgresql_installation():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ PostgreSQL found: {result.stdout.strip()}")
            return True
        else:
            print("✗ PostgreSQL not found")
            return False
    except FileNotFoundError:
        print("✗ PostgreSQL not found in PATH")
        return False

def create_local_database():
    """Create local PostgreSQL database"""
    print("\n📝 Creating local PostgreSQL database...")
    
    # Database configuration
    db_name = "autoredact"
    db_user = "autoredact_user"
    db_password = "autoredact_password"
    
    try:
        # Create database user
        print("Creating database user...")
        subprocess.run([
            'psql', '-U', 'postgres', '-c', 
            f"CREATE USER {db_user} WITH PASSWORD '{db_password}';"
        ], check=True)
        
        # Create database
        print("Creating database...")
        subprocess.run([
            'psql', '-U', 'postgres', '-c', 
            f"CREATE DATABASE {db_name} OWNER {db_user};"
        ], check=True)
        
        # Grant privileges
        print("Granting privileges...")
        subprocess.run([
            'psql', '-U', 'postgres', '-c', 
            f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
        ], check=True)
        
        print("✓ Local database created successfully")
        
        # Update .env file
        update_env_file(db_name, db_user, db_password, "localhost", "5432")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create database: {e}")
        return False

def update_env_file(db_name, db_user, db_password, host, port):
    """Update .env file with database configuration"""
    env_file = Path(".env")
    
    if env_file.exists():
        # Read existing .env file
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update database URL
        new_db_url = f"postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}"
        
        # Replace or add DATABASE_URL
        if "DATABASE_URL=" in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("DATABASE_URL="):
                    lines[i] = f"DATABASE_URL={new_db_url}"
                    break
            content = '\n'.join(lines)
        else:
            content += f"\nDATABASE_URL={new_db_url}"
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✓ .env file updated with database configuration")
    else:
        print("⚠️  .env file not found, please create it manually")

def setup_cloud_database():
    """Setup cloud database (AWS RDS, etc.)"""
    print("\n☁️  Cloud Database Setup")
    print("Please provide your cloud database details:")
    
    host = input("Database Host: ").strip()
    port = input("Database Port (default: 5432): ").strip() or "5432"
    db_name = input("Database Name: ").strip()
    db_user = input("Database User: ").strip()
    db_password = input("Database Password: ").strip()
    
    if all([host, db_name, db_user, db_password]):
        update_env_file(db_name, db_user, db_password, host, port)
        print("✓ Cloud database configuration saved")
        return True
    else:
        print("✗ Incomplete database configuration")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        from app.core.config import settings
        from sqlalchemy import create_engine
        
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful")
            return True
            
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print_header()
    
    print("\nChoose your PostgreSQL setup option:")
    print("1. Local PostgreSQL (requires PostgreSQL installed)")
    print("2. Cloud Database (AWS RDS, etc.)")
    print("3. Skip database setup (use SQLite)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        if check_postgresql_installation():
            if create_local_database():
                test_database_connection()
        else:
            print("\n📦 PostgreSQL Installation Options:")
            print("- Windows: Download from https://www.postgresql.org/download/windows/")
            print("- macOS: brew install postgresql")
            print("- Ubuntu: sudo apt-get install postgresql postgresql-contrib")
            print("\nAfter installation, run this script again.")
    
    elif choice == "2":
        if setup_cloud_database():
            test_database_connection()
    
    elif choice == "3":
        print("✓ Skipping PostgreSQL setup, will use SQLite")
        print("Note: SQLite is suitable for development only")
    
    else:
        print("Invalid choice")
        return
    
    print("\n🎉 PostgreSQL setup completed!")
    print("\nNext steps:")
    print("1. Start the backend server: uvicorn app.main:app --reload")
    print("2. The database tables will be created automatically")
    print("3. Demo user will be created for testing")

if __name__ == "__main__":
    main() 