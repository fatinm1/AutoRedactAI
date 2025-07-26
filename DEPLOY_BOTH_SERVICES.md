# Deploy Both Frontend and Backend Together on Railway

## 🚀 Single Project, Multiple Services Approach

This guide will help you deploy both your frontend and backend in the same Railway project.

## 📋 Prerequisites

1. Railway account (free tier available)
2. GitHub repository with your code
3. Basic understanding of environment variables

## 🏗️ Step-by-Step Deployment

### Step 1: Create Railway Project

1. **Go to Railway**: Visit [railway.app](https://railway.app)
2. **Sign up/Login**: Use your GitHub account
3. **Create New Project**: Click "New Project"
4. **Choose "Deploy from GitHub repo"**
5. **Select your repository**: `fatinm1/AutoRedactAI`
6. **Choose branch**: `master`

### Step 2: Add Backend Service

1. **In your Railway project**, click **"New Service"**
2. **Choose "GitHub Repo"**
3. **Select the same repository**: `fatinm1/AutoRedactAI`
4. **IMPORTANT**: Set **"Root Directory"** to `backend/`
5. **Click "Deploy Now"**

### Step 3: Configure Backend Service

1. **Go to the backend service settings**
2. **Set environment variables**:
   ```bash
   SECRET_KEY=your-super-secret-production-key-here
   ENVIRONMENT=production
   DEBUG=false
   ALLOWED_HOSTS=*
   ```

### Step 4: Add PostgreSQL Database

1. **Click "New Service"** in your project
2. **Choose "Database" → "PostgreSQL"**
3. **Wait for it to provision**
4. **Copy the `DATABASE_URL`** from PostgreSQL service
5. **Add `DATABASE_URL`** to your backend service environment variables

### Step 5: Add Frontend Service

1. **Click "New Service"** again
2. **Choose "GitHub Repo"**
3. **Select the same repository**: `fatinm1/AutoRedactAI`
4. **IMPORTANT**: Set **"Root Directory"** to `frontend/`
5. **Click "Deploy Now"**

### Step 6: Configure Frontend Service

1. **Get your backend service URL** (e.g., `https://backend-service-name.up.railway.app`)
2. **Set environment variable** in frontend service:
   ```bash
   VITE_API_URL=https://your-backend-url.railway.app
   ```

### Step 7: Update CORS Settings

1. **In your backend service**, add your frontend URL to environment variables:
   ```bash
   ALLOWED_ORIGINS=https://your-frontend-url.railway.app,http://localhost:3000
   ```

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

## 📁 Project Structure in Railway

Your Railway project will have **3 services**:

1. **Backend Service**
   - Root Directory: `backend/`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Frontend Service**
   - Root Directory: `frontend/`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm run preview`

3. **PostgreSQL Database**
   - Managed by Railway
   - Provides `DATABASE_URL` for backend

## 🚨 Troubleshooting Common Issues

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

## 📊 Monitoring Your Deployment

### Railway Dashboard Features:
- **Real-time logs** for each service
- **Health checks** for backend and frontend
- **Environment variables** management
- **Service metrics** and performance
- **Automatic scaling** based on traffic

### Health Check URLs:
- **Backend**: `https://your-backend-url.railway.app/health`
- **Frontend**: `https://your-frontend-url.railway.app/`

## 🎯 Testing Your Deployment

1. **Test Backend Health**: Visit your backend health endpoint
2. **Test Frontend**: Visit your frontend URL
3. **Test User Registration**: Create a new account
4. **Test Login**: Log in with your credentials
5. **Test File Upload**: Upload a document and test redaction
6. **Test API Endpoints**: Verify all API calls work

## 🔐 Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **HTTPS**: Railway provides automatic HTTPS
3. **CORS**: Configure properly for production
4. **Rate Limiting**: Implement proper rate limiting
5. **Database**: Use Railway's managed PostgreSQL

## 📈 Scaling Your Application

### Railway Plans:
- **Free Tier**: Perfect for development and small projects
- **Pro Plan**: For production applications with higher traffic
- **Enterprise**: For large-scale deployments

### Auto-scaling Features:
- Railway automatically scales based on traffic
- Database connections are managed automatically
- CDN is available for static assets

## 🎉 Success Checklist

- [ ] Railway project created
- [ ] Backend service deployed with root directory `backend/`
- [ ] PostgreSQL database added and connected
- [ ] Frontend service deployed with root directory `frontend/`
- [ ] Environment variables configured correctly
- [ ] CORS settings updated
- [ ] Health checks passing
- [ ] User registration working
- [ ] File upload and redaction working
- [ ] All API endpoints responding correctly

## 📞 Need Help?

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Check the logs in Railway dashboard for specific error messages

---

**Happy Deploying! 🚀** 