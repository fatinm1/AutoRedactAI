# AutoRedactAI - PostgreSQL Integration Guide

## 🐘 Overview

AutoRedactAI now supports **PostgreSQL** as the primary database, providing:
- **Persistent Data Storage**: All data survives server restarts
- **Production-Ready**: Scalable and reliable database solution
- **ACID Compliance**: Transactional integrity for data safety
- **Advanced Features**: Full-text search, JSON support, and more

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the PostgreSQL setup script
powershell -ExecutionPolicy Bypass -File start-postgresql.ps1
```

### Option 2: Manual Setup
```bash
# 1. Navigate to backend
cd backend

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run PostgreSQL setup
python setup_postgresql.py

# 4. Start the server
uvicorn app.main:app --reload
```

## 📊 Database Schema

### Core Tables

#### **Users Table**
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role VARCHAR DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_login TIMESTAMP WITH TIME ZONE
);
```

#### **Documents Table**
```sql
CREATE TABLE documents (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    original_filename VARCHAR NOT NULL,
    stored_filename VARCHAR NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR NOT NULL,
    s3_key VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'uploaded',
    processing_started TIMESTAMP WITH TIME ZONE,
    processing_completed TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    page_count INTEGER,
    word_count INTEGER,
    language VARCHAR DEFAULT 'en'
);
```

#### **Redactions Table**
```sql
CREATE TABLE redactions (
    id VARCHAR PRIMARY KEY,
    document_id VARCHAR REFERENCES documents(id),
    entity_type VARCHAR NOT NULL,
    entity_text TEXT NOT NULL,
    confidence_score FLOAT NOT NULL,
    start_char INTEGER NOT NULL,
    end_char INTEGER NOT NULL,
    page_number INTEGER,
    line_number INTEGER,
    is_redacted BOOLEAN DEFAULT TRUE,
    redaction_method VARCHAR DEFAULT 'black_box',
    custom_replacement VARCHAR,
    context_before TEXT,
    context_after TEXT,
    bounding_box JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### **Audit Logs Table**
```sql
CREATE TABLE audit_logs (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    document_id VARCHAR REFERENCES documents(id),
    action VARCHAR NOT NULL,
    details JSON,
    ip_address VARCHAR,
    user_agent VARCHAR,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔧 Configuration

### Environment Variables

#### **Backend (.env)**
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/autoredact
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Application Settings
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key

# File Processing
MAX_FILE_SIZE=52428800
ALLOWED_FILE_TYPES=.pdf,.docx,.txt
FILE_RETENTION_DAYS=7
```

### Database URL Format
```
postgresql://username:password@host:port/database_name
```

**Examples:**
- **Local**: `postgresql://autoredact_user:password@localhost:5432/autoredact`
- **Cloud**: `postgresql://user:pass@db.example.com:5432/autoredact`
- **Development**: `sqlite:///./autoredact.db` (fallback)

## 🛠️ Setup Options

### 1. Local PostgreSQL

#### **Installation**
- **Windows**: Download from [PostgreSQL.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql`
- **Ubuntu**: `sudo apt-get install postgresql postgresql-contrib`

#### **Setup Commands**
```bash
# Create database user
sudo -u postgres createuser --interactive autoredact_user

# Create database
sudo -u postgres createdb autoredact

# Set password
sudo -u postgres psql -c "ALTER USER autoredact_user PASSWORD 'your_password';"

# Grant privileges
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE autoredact TO autoredact_user;"
```

### 2. Cloud Database (AWS RDS)

#### **AWS RDS Setup**
1. Create RDS instance in AWS Console
2. Choose PostgreSQL engine
3. Configure security groups
4. Get connection details
5. Update `DATABASE_URL` in `.env`

#### **Connection String**
```
postgresql://username:password@your-rds-endpoint:5432/database_name
```

### 3. Docker PostgreSQL

#### **docker-compose.yml**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: autoredact
      POSTGRES_USER: autoredact_user
      POSTGRES_PASSWORD: autoredact_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔄 Migration from In-Memory Storage

### **What Changed**
- ✅ **User Data**: Now stored in PostgreSQL `users` table
- ✅ **Document Metadata**: Stored in PostgreSQL `documents` table
- ✅ **Redaction Data**: Stored in PostgreSQL `redactions` table
- ✅ **Audit Logs**: Stored in PostgreSQL `audit_logs` table
- ✅ **Session Management**: JWT tokens remain stateless

### **Data Persistence**
- **Before**: All data lost on server restart
- **After**: All data persists across restarts
- **Backup**: Database can be backed up and restored

## 📈 Performance Features

### **Connection Pooling**
```python
# Configured in database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,      # 10 connections
    max_overflow=settings.DATABASE_MAX_OVERFLOW, # 20 additional
    pool_pre_ping=True,                         # Connection health checks
    echo=settings.DEBUG                         # SQL logging in debug
)
```

### **Indexes for Performance**
```sql
-- User email lookup
CREATE INDEX idx_users_email ON users(email);

-- Document user lookup
CREATE INDEX idx_documents_user_id ON documents(user_id);

-- Redaction document lookup
CREATE INDEX idx_redactions_document_id ON redactions(document_id);

-- Audit log timestamps
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

## 🔒 Security Features

### **Password Security**
- **Bcrypt Hashing**: Industry-standard password hashing
- **Salt Generation**: Unique salt for each password
- **Secure Verification**: Constant-time comparison

### **Database Security**
- **Connection Encryption**: SSL/TLS for database connections
- **User Permissions**: Limited database user privileges
- **Audit Logging**: Complete action tracking

## 🧪 Testing

### **Database Connection Test**
```bash
# Test connection
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": 1753554243.3067338,
  "version": "1.0.0"
}
```

### **User Registration Test**
```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

## 🚨 Troubleshooting

### **Common Issues**

#### **1. Connection Refused**
```
Error: connection to server at "localhost" (127.0.0.1), port 5432 failed
```
**Solution**: Ensure PostgreSQL is running
```bash
# Windows
net start postgresql

# macOS
brew services start postgresql

# Ubuntu
sudo systemctl start postgresql
```

#### **2. Authentication Failed**
```
Error: password authentication failed for user "autoredact_user"
```
**Solution**: Check user credentials in `.env` file

#### **3. Database Does Not Exist**
```
Error: database "autoredact" does not exist
```
**Solution**: Create database
```bash
sudo -u postgres createdb autoredact
```

### **Debug Mode**
```env
# Enable SQL query logging
DEBUG=true
```

## 📊 Monitoring

### **Database Metrics**
- **Connection Pool**: Monitor active connections
- **Query Performance**: Track slow queries
- **Storage Usage**: Monitor database size
- **Backup Status**: Ensure regular backups

### **Health Checks**
```python
# Database health check endpoint
@app.get("/health/db")
async def database_health_check():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"database": "healthy"}
    except Exception as e:
        return {"database": "unhealthy", "error": str(e)}
```

## 🔄 Backup & Recovery

### **Automated Backups**
```bash
# Create backup script
#!/bin/bash
pg_dump -h localhost -U autoredact_user autoredact > backup_$(date +%Y%m%d_%H%M%S).sql
```

### **Restore Database**
```bash
# Restore from backup
psql -h localhost -U autoredact_user autoredact < backup_file.sql
```

## 🎯 Production Deployment

### **Recommended Setup**
1. **Database**: AWS RDS PostgreSQL or similar
2. **Connection Pooling**: Configure for expected load
3. **Backup Strategy**: Automated daily backups
4. **Monitoring**: Database performance monitoring
5. **Security**: SSL connections and proper user permissions

### **Environment Variables**
```env
# Production settings
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://prod_user:secure_password@prod-db.example.com:5432/autoredact
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
```

---

## 🎉 Success!

Your AutoRedactAI application now has **production-ready PostgreSQL integration** with:
- ✅ **Persistent Data Storage**
- ✅ **Scalable Architecture**
- ✅ **Security Best Practices**
- ✅ **Performance Optimization**
- ✅ **Comprehensive Monitoring**

The system is ready for production deployment! 🚀 