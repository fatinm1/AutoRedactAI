# Single Service Railway Deployment Guide

## 🚀 Deploy Frontend + Backend in One Service

This guide shows you how to deploy both the frontend and backend of AutoRedactAI in a single Railway service.

## 📋 Prerequisites

- Railway account
- GitHub repository with your AutoRedactAI code
- Basic understanding of Docker and environment variables

## 🔧 Configuration

### 1. Railway Configuration (`railway.json`)

The root `railway.json` is configured to use Docker for building both frontend and backend:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Multi-Stage Dockerfile

The `Dockerfile` uses a multi-stage build to:
1. Build the frontend in a Node.js container
2. Copy the built frontend to the Python backend container
3. Serve both from the same service

```dockerfile
# Multi-stage build for both frontend and backend
FROM node:18-alpine AS frontend-builder

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Backend stage
FROM python:3.11-slim

# Install dependencies and copy code
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy backend and built frontend
COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Run the application
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🚀 Deployment Steps

### Step 1: Create Railway Project

1. Go to [Railway.app](https://railway.app)
2. Create a new project
3. Select "Deploy from GitHub repo"
4. Choose your AutoRedactAI repository

### Step 2: Configure Service

1. **Root Directory**: Leave as `/` (root of project)
2. **Build Command**: Leave empty (Dockerfile handles this)
3. **Start Command**: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add PostgreSQL Database

1. Add a new service → Select "PostgreSQL"
2. Copy the `DATABASE_URL` from the PostgreSQL service
3. Add it to your main service's environment variables

### Step 4: Set Environment Variables

Add these environment variables to your service:

```bash
# Required
SECRET_KEY=your-super-secret-production-key-here
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
DEBUG=false

# Optional
ALLOWED_ORIGINS=https://your-domain.railway.app,http://localhost:3000
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
```

### Step 5: Deploy

1. Click "Deploy" in Railway
2. Wait for the build to complete
3. Check the logs for any errors

## 🌐 Accessing Your Application

### API Endpoints
- **API Base**: `https://your-domain.railway.app/api/v1`
- **Health Check**: `https://your-domain.railway.app/health`
- **API Docs**: `https://your-domain.railway.app/docs`

### Frontend Application
- **Main App**: `https://your-domain.railway.app/app`
- **Login**: `https://your-domain.railway.app/app/login`
- **Dashboard**: `https://your-domain.railway.app/app/dashboard`

## 🔍 How It Works

### Backend Startup Process

1. **Database Initialization**: Connects to PostgreSQL
2. **Frontend Check**: Looks for built frontend files
3. **Static File Serving**: Mounts frontend files at `/app` route
4. **API Routes**: Serves API at `/api/v1` routes
5. **Health Check**: Responds at `/health` endpoint

### Frontend Integration

The frontend is built during the Docker build process and served by the FastAPI backend:

```python
# Serve frontend static files
if os.path.exists(frontend_dist_path):
    app.mount("/static", StaticFiles(directory=frontend_dist_path), name="static")
    
    @app.get("/app")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_dist_path, "index.html"))
```

## 🔧 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check if all dependencies are in `requirements.txt` and `package.json`
   - Verify Node.js and Python versions are compatible
   - Check Railway logs for specific error messages

2. **Frontend Not Loading**
   - Verify the frontend was built successfully
   - Check if `/app` route is accessible
   - Ensure static files are being served correctly

3. **Database Connection Issues**
   - Verify `DATABASE_URL` is correct
   - Check if PostgreSQL service is running
   - Ensure database migrations are applied

4. **API Errors**
   - Check if backend is starting correctly
   - Verify environment variables are set
   - Check `/health` endpoint for service status

### Debug Commands

```bash
# Check Railway logs
railway logs

# View service status
railway status

# Connect to database
railway connect

# Check build logs
railway logs --build
```

## 📊 Monitoring

### Health Check
The service provides a health check endpoint at `/health` that Railway uses to monitor the service.

### Logs
- **Application Logs**: Check Railway dashboard for real-time logs
- **Build Logs**: View Docker build process logs
- **Error Logs**: Monitor for any startup or runtime errors

## 🔒 Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **HTTPS**: Railway provides automatic HTTPS
3. **CORS**: Configure properly for production
4. **Database**: Use Railway's managed PostgreSQL
5. **File Uploads**: Implement proper validation and limits

## 🚀 Performance Optimization

1. **Caching**: Consider adding Redis for caching
2. **CDN**: Use Railway's CDN for static assets
3. **Database**: Optimize database queries and connections
4. **Monitoring**: Set up proper monitoring and alerting

## ✅ Success Checklist

- [ ] Service deployed successfully
- [ ] Health check passing (`/health` endpoint)
- [ ] Frontend accessible at `/app`
- [ ] API endpoints working at `/api/v1`
- [ ] Database connected and working
- [ ] Environment variables configured
- [ ] HTTPS working correctly
- [ ] File uploads functioning
- [ ] Authentication working

## 📞 Support

If you encounter issues:

1. **Check Railway Logs**: Look for specific error messages
2. **Verify Configuration**: Ensure all files are in the correct locations
3. **Test Locally**: Try running with `docker-compose up` first
4. **Review Documentation**: Check the main README and other guides

---

**🎉 Your AutoRedactAI application is now deployed as a single service on Railway!** 