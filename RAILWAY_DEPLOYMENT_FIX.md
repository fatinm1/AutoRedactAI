# Railway Deployment Fix Guide

## 🚨 Current Issue
The deployment is failing because Railway is trying to deploy the entire project instead of just the backend or frontend. The error message "Please set root directory to backend/ or frontend/" indicates the configuration issue.

## 🔧 Solution: Deploy Backend and Frontend as Separate Services

### Step 1: Deploy Backend Service

1. **Create a new Railway project** (if you haven't already)
2. **Add a new service** and select "Deploy from GitHub repo"
3. **Configure the backend service**:
   - **Repository**: Your AutoRedactAI repository
   - **Branch**: `main` or `master`
   - **Root Directory**: `backend/` ⚠️ **This is crucial!**
   - **Build Command**: Leave empty (Railway will auto-detect)
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables** for backend:
   ```bash
   SECRET_KEY=your-super-secret-production-key-here
   DATABASE_URL=postgresql://username:password@host:port/database
   ENVIRONMENT=production
   DEBUG=false
   ALLOWED_ORIGINS=https://your-frontend-domain.railway.app,http://localhost:3000
   ```

5. **Deploy the backend service**

### Step 2: Add PostgreSQL Database

1. **Add a new service** in your Railway project
2. **Select "PostgreSQL"** from the template
3. **Copy the DATABASE_URL** from the PostgreSQL service
4. **Update the backend service** with the DATABASE_URL

### Step 3: Deploy Frontend Service

1. **Add another new service** and select "Deploy from GitHub repo"
2. **Configure the frontend service**:
   - **Repository**: Your AutoRedactAI repository
   - **Branch**: `main` or `master`
   - **Root Directory**: `frontend/` ⚠️ **This is crucial!**
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview`

3. **Set Environment Variables** for frontend:
   ```bash
   VITE_API_URL=https://your-backend-domain.railway.app
   ```

4. **Deploy the frontend service**

### Step 4: Configure Domains and CORS

1. **Get the domains** for both services from Railway
2. **Update the backend CORS settings** with the frontend domain
3. **Test the connection** between frontend and backend

## 📁 Updated Configuration Files

### Backend Railway Config (`backend/railway.json`)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Frontend Railway Config (`frontend/railway.json`)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm run preview",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 🔍 Troubleshooting

### Common Issues:

1. **Health Check Failing**
   - Backend: Check if `/health` endpoint is accessible
   - Frontend: Check if the app is serving on the correct port

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Check if PostgreSQL service is running

3. **CORS Errors**
   - Update ALLOWED_ORIGINS with your frontend domain
   - Ensure frontend URL is correct in VITE_API_URL

4. **Build Failures**
   - Check if all dependencies are in requirements.txt/package.json
   - Verify Node.js and Python versions are compatible

### Debug Commands:

```bash
# Check Railway logs
railway logs

# View service status
railway status

# Connect to database
railway connect
```

## 🚀 Alternative: Single Service Deployment

If you prefer to deploy as a single service, you can:

1. **Set Root Directory** to `/` (root of project)
2. **Update the start command** to:
   ```bash
   cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. **Build the frontend** in the backend startup process

However, **separate services are recommended** for better scalability and maintenance.

## ✅ Success Checklist

- [ ] Backend service deployed with root directory `backend/`
- [ ] Frontend service deployed with root directory `frontend/`
- [ ] PostgreSQL database added and connected
- [ ] Environment variables configured correctly
- [ ] Health checks passing
- [ ] Frontend can communicate with backend
- [ ] CORS configured properly

## 📞 Support

If you continue to have issues:
1. Check Railway logs for specific error messages
2. Verify all configuration files are in the correct locations
3. Ensure environment variables are set correctly
4. Test locally first with `docker-compose up`

---

**The key fix is setting the correct root directory for each service!** 🎯 