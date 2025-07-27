# 🗄️ Railway Database Setup Guide

## Step 1: Add PostgreSQL Database to Railway

1. **Go to Railway Dashboard**
   - Visit https://railway.app/dashboard
   - Select your AutoRedactAI project

2. **Add PostgreSQL Service**
   - Click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provision the database

3. **Get Connection Details**
   - Click on the PostgreSQL service
   - Go to "Connect" tab
   - Copy the `DATABASE_URL` (it looks like: `postgresql://postgres:password@host:port/database`)

## Step 2: Configure Environment Variables

1. **Go to your main service** (the one running your app)
2. **Click "Variables" tab**
3. **Add these environment variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:password@host:port/database

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS (replace with your actual domain)
ALLOWED_ORIGINS=https://your-app-name.up.railway.app

# File Processing
MAX_FILE_SIZE=52428800
ALLOWED_FILE_TYPES=.pdf,.docx,.txt
FILE_RETENTION_DAYS=7

# AI/ML Models
SPACY_MODEL=en_core_web_sm
BERT_MODEL=bert-base-cased
CONFIDENCE_THRESHOLD=0.7
```

## Step 3: Run Database Setup

1. **SSH into your Railway service:**
   ```bash
   railway shell
   ```

2. **Run the database setup script:**
   ```bash
   python setup_database.py
   ```

3. **Verify the setup:**
   - Check that all tables are created
   - Verify admin and demo users are created

## Step 4: Test Database Connection

1. **Check the logs** in Railway dashboard
2. **Test API endpoints:**
   - Health check: `https://your-app.up.railway.app/health`
   - API info: `https://your-app.up.railway.app/api`

## Step 5: Verify Database Tables

The setup script will create these tables:

- ✅ **users** - User accounts and authentication
- ✅ **documents** - Uploaded files and metadata
- ✅ **redactions** - AI-detected sensitive information
- ✅ **audit_logs** - Compliance and tracking logs
- ✅ **processing_jobs** - Background task tracking
- ✅ **export_jobs** - Document export tracking
- ✅ **team_collaborations** - Multi-user document review
- ✅ **compliance_reports** - Analytics and reporting

## Default Users Created

### Admin User
- **Email:** admin@autoredact.ai
- **Password:** admin123
- **Role:** admin

### Demo User
- **Email:** demo@autoredact.ai
- **Password:** demo123
- **Role:** user

## Troubleshooting

### Common Issues:

1. **Connection Failed**
   - Check `DATABASE_URL` format
   - Verify Railway PostgreSQL service is running
   - Check network connectivity

2. **Permission Denied**
   - Ensure database user has proper permissions
   - Check if database exists

3. **Tables Not Created**
   - Check Python dependencies are installed
   - Verify SQLAlchemy models are imported correctly
   - Check for syntax errors in models

### Useful Commands:

```bash
# Check database connection
railway shell
python -c "from backend.app.core.database import engine; print(engine.execute('SELECT version()').fetchone())"

# View database logs
railway logs

# Restart service
railway up
```

## Next Steps

After database setup is complete:

1. **Test Authentication** - Try logging in with demo users
2. **Test File Upload** - Upload a test document
3. **Set up File Storage** - Configure AWS S3
4. **Configure AI Models** - Set up document processing
5. **Add Monitoring** - Set up logging and metrics

---

**Need Help?** Check the Railway documentation or create an issue in the project repository. 