# 🚀 Quick Railway Deployment Guide

## The Key to Success: Root Directory Settings

The main issue you're facing is that Railway needs to know which part of your code to build. You need to set the **Root Directory** for each service.

## 📋 What You Need to Do:

### 1. Create Your Railway Project
- Go to [railway.app](https://railway.app)
- Create new project from GitHub repo: `fatinm1/AutoRedactAI`

### 2. Add Backend Service
- Click "New Service" → "GitHub Repo"
- Select your repo: `fatinm1/AutoRedactAI`
- **CRITICAL**: Set "Root Directory" to `backend/`
- Deploy

### 3. Add PostgreSQL Database
- Click "New Service" → "Database" → "PostgreSQL"
- Copy the `DATABASE_URL`

### 4. Configure Backend
- Set environment variables in backend service:
  ```
  SECRET_KEY=your-secret-key-here
  DATABASE_URL=postgresql://... (from step 3)
  ENVIRONMENT=production
  DEBUG=false
  ALLOWED_HOSTS=*
  ```

### 5. Add Frontend Service
- Click "New Service" → "GitHub Repo"
- Select your repo: `fatinm1/AutoRedactAI`
- **CRITICAL**: Set "Root Directory" to `frontend/`
- Deploy

### 6. Configure Frontend
- Get your backend URL (e.g., `https://backend-name.up.railway.app`)
- Set environment variable in frontend:
  ```
  VITE_API_URL=https://your-backend-url.railway.app
  ```

### 7. Update CORS
- Add frontend URL to backend's `ALLOWED_ORIGINS`

## 🎯 Your Final Project Structure:
```
Railway Project
├── Backend Service (root: backend/)
├── Frontend Service (root: frontend/)
└── PostgreSQL Database
```

## 🚨 The Root Directory is the Key!
- **Backend**: Root Directory = `backend/`
- **Frontend**: Root Directory = `frontend/`

This tells Railway where to find the build files for each service.

## 📞 Need Help?
- Check the detailed guide: `DEPLOY_BOTH_SERVICES.md`
- Railway docs: [docs.railway.app](https://docs.railway.app) 