# Single Service Deployment Guide

## 🚀 Deploy Frontend and Backend Together

This guide shows you how to deploy both the frontend and backend as a **single service** in Railway.

## 📋 How It Works

1. **Single Service**: One Railway service handles both frontend and backend
2. **Backend Serves Frontend**: The FastAPI backend serves the React frontend static files
3. **Unified Build**: Frontend is built and served by the backend
4. **Single URL**: Everything runs on one domain

## 🏗️ Architecture

```
Railway Service
├── Backend (FastAPI)
│   ├── API endpoints (/api/v1/*)
│   ├── Static file serving (/static/*)
│   └── Frontend routes (/*)
├── Frontend (React)
│   ├── Built to static files
│   └── Served by backend
└── PostgreSQL Database
```

## 🚀 Deployment Steps

### Step 1: Create Railway Project

1. **Go to Railway**: Visit [railway.app](https://railway.app)
2. **Create New Project**: Click "New Project"
3. **Choose "Deploy from GitHub repo"**
4. **Select your repository**: `fatinm1/AutoRedactAI`
5. **Choose branch**: `master`

### Step 2: Configure the Service

1. **Set Root Directory**: Leave empty (uses project root)
2. **Build Command**: Railway will auto-detect (no custom build needed)
3. **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add PostgreSQL Database

1. **Click "New Service"** in your project
2. **Choose "Database" → "PostgreSQL"**
3. **Wait for it to provision**
4. **Copy the `DATABASE_URL`** from PostgreSQL service

### Step 4: Set Environment Variables

In your main service, set these environment variables:

```bash
# Required
SECRET_KEY=your-super-secret-production-key-here
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=*

# Optional
REDIS_URL=redis://username:password@host:port
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

## 🔧 How the Single Service Works

### Frontend Building
- Frontend is built during backend startup if `dist` folder doesn't exist
- Uses `npm install` and `npm run build` in the frontend directory
- Built files are served by FastAPI static file handler

### Backend Serving
- API endpoints: `/api/v1/*`
- Static files: `/static/*` (served from `frontend/dist`)
- Frontend routes: `/*` (serves `index.html` for client-side routing)

### File Structure
```
/
├── backend/
│   ├── app/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── dist/ (built files)
└── railway.json
```

## 🎯 Benefits

1. **Simplified Deployment**: Only one service to manage
2. **Single Domain**: Everything runs on one URL
3. **No CORS Issues**: Frontend and backend are on same origin
4. **Easier Configuration**: Fewer environment variables to manage
5. **Cost Effective**: Only one service to pay for

## 🚨 Important Notes

1. **Build Time**: Initial deployment takes longer as it builds frontend
2. **Memory Usage**: Single service uses more memory
3. **Scaling**: Scales both frontend and backend together
4. **Updates**: Any code change redeploys both frontend and backend

## 📊 Monitoring

- **Health Check**: `/health` endpoint
- **API Docs**: `/docs` (if not in production)
- **Frontend**: Root path `/`
- **Logs**: Combined logs for both frontend and backend

## 🔍 Troubleshooting

### Frontend Not Loading
- Check if `frontend/dist` exists
- Verify build logs in Railway
- Check static file serving configuration

### API Endpoints Not Working
- Verify environment variables are set
- Check database connection
- Review backend logs

### Build Failures
- Ensure Node.js is available
- Check frontend dependencies
- Verify build scripts

## 🎉 Success Indicators

- ✅ Service deploys successfully
- ✅ Health check passes (`/health`)
- ✅ Frontend loads at root URL (`/`)
- ✅ API endpoints work (`/api/v1/health`)
- ✅ Database connection established
- ✅ User registration/login works

---

**Happy Deploying! 🚀** 