# Railway Deployment - Step by Step Guide

## 🚨 IMPORTANT: Fix for Build Failure

The build failed because Railway doesn't know which service to deploy. Here's how to fix it:

## Method 1: Multi-Service Project (Recommended)

### Step 1: Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository: `fatinm1/AutoRedactAI`
5. Choose branch: `master`

### Step 2: Add Backend Service
1. In your Railway project, click "New Service"
2. Choose "GitHub Repo"
3. Select the same repository: `fatinm1/AutoRedactAI`
4. **IMPORTANT**: Set "Root Directory" to `backend/`
5. Click "Deploy Now"

### Step 3: Configure Backend Service
1. Go to the backend service settings
2. Set environment variables:
   ```
   SECRET_KEY=your-super-secret-production-key-here
   ENVIRONMENT=production
   DEBUG=false
   ALLOWED_HOSTS=*
   ```

### Step 4: Add PostgreSQL Database
1. Click "New Service" in your project
2. Choose "Database" → "PostgreSQL"
3. Wait for it to provision
4. Copy the `DATABASE_URL` from PostgreSQL service
5. Add `DATABASE_URL` to your backend service environment variables

### Step 5: Add Frontend Service
1. Click "New Service" again
2. Choose "GitHub Repo"
3. Select the same repository: `fatinm1/AutoRedactAI`
4. **IMPORTANT**: Set "Root Directory" to `frontend/`
5. Click "Deploy Now"

### Step 6: Configure Frontend Service
1. Get your backend service URL (e.g., `https://backend-service-name.up.railway.app`)
2. Set environment variable in frontend service:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

### Step 7: Update CORS Settings
1. In your backend service, add your frontend URL to environment variables:
   ```
   ALLOWED_ORIGINS=https://your-frontend-url.railway.app,http://localhost:3000
   ```

## Method 2: Separate Projects (Alternative)

### Backend Project:
1. Create new Railway project
2. Connect to GitHub repo
3. Set root directory to `backend/`
4. Add PostgreSQL service
5. Configure environment variables

### Frontend Project:
1. Create another Railway project
2. Connect to same GitHub repo
3. Set root directory to `frontend/`
4. Set `VITE_API_URL` to backend URL

## 🔧 Environment Variables Reference

### Backend Service Variables:
```bash
# Required
SECRET_KEY=your-very-long-random-secret-key
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=*

# Optional
REDIS_URL=redis://username:password@host:port
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
FRONTEND_URL=https://your-frontend-url.railway.app
```

### Frontend Service Variables:
```bash
VITE_API_URL=https://your-backend-url.railway.app
```

## 🚨 Common Issues & Solutions

### Issue 1: "Nixpacks was unable to generate a build plan"
**Solution**: Make sure you set the correct root directory (`backend/` or `frontend/`)

### Issue 2: Build fails in backend
**Solution**: Check that `requirements.txt` exists in the backend directory

### Issue 3: Build fails in frontend
**Solution**: Check that `package.json` exists in the frontend directory

### Issue 4: Database connection fails
**Solution**: Verify `DATABASE_URL` is correctly set in backend service

### Issue 5: CORS errors
**Solution**: Update `ALLOWED_ORIGINS` with your frontend domain

## 📋 Deployment Checklist

- [ ] Railway project created
- [ ] Backend service added with root directory `backend/`
- [ ] PostgreSQL database added
- [ ] Backend environment variables set
- [ ] Frontend service added with root directory `frontend/`
- [ ] Frontend environment variables set
- [ ] CORS configured
- [ ] Both services deployed successfully
- [ ] Health checks passing
- [ ] Application tested

## 🎯 Next Steps After Deployment

1. **Test Backend**: Visit `https://your-backend-url.railway.app/health`
2. **Test Frontend**: Visit your frontend URL
3. **Test Login**: Try creating an account and logging in
4. **Test File Upload**: Upload a document and test redaction
5. **Monitor Logs**: Check Railway logs for any issues

## 📞 Need Help?

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Check the logs in Railway dashboard for specific error messages 