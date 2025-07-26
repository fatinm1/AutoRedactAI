# AutoRedactAI - Railway Deployment Guide

This guide will help you deploy the AutoRedactAI application to Railway, including the backend API, frontend, and PostgreSQL database.

## 🚀 Quick Start

### 1. Prerequisites
- Railway account (free tier available)
- GitHub repository with your code
- Basic understanding of environment variables

### 2. Railway Setup

#### Step 1: Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Create a new project

#### Step 2: Connect Your Repository
1. Click "Deploy from GitHub repo"
2. Select your AutoRedactAI repository
3. Choose the branch (usually `master` or `main`)

## 🏗️ Service Configuration

### Backend Service (FastAPI)

Railway will automatically detect this as a Python service based on the `requirements.txt` file.

**Configuration:**
- **Root Directory**: `backend/`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables to Set:**
```bash
# Required
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
DEBUG=false

# Optional
REDIS_URL=redis://username:password@host:port
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
FRONTEND_URL=https://your-frontend-domain.railway.app
```

### Frontend Service (React)

Create a separate service for the frontend.

**Configuration:**
- **Root Directory**: `frontend/`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run preview`

**Environment Variables:**
```bash
VITE_API_URL=https://your-backend-domain.railway.app
```

### Database Service (PostgreSQL)

Railway provides managed PostgreSQL databases.

1. Add a new service
2. Select "PostgreSQL" from the template
3. Railway will automatically provide the `DATABASE_URL`

## 🔧 Environment Variables Setup

### Backend Environment Variables

In your Railway backend service, set these variables:

#### Required Variables:
```bash
SECRET_KEY=your-very-long-random-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=*
```

#### Optional Variables:
```bash
# Redis (if using)
REDIS_URL=redis://username:password@host:port

# AWS S3 (if using)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket-name

# Frontend URL for CORS
FRONTEND_URL=https://your-frontend-domain.railway.app

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

### Frontend Environment Variables

In your Railway frontend service:

```bash
VITE_API_URL=https://your-backend-domain.railway.app
```

## 📁 Project Structure for Railway

```
AutoRedactAI/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── railway.json
│   └── env.production.template
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── railway.json
└── RAILWAY_DEPLOYMENT.md
```

## 🚀 Deployment Steps

### Step 1: Deploy Backend
1. Create a new service in Railway
2. Connect to your GitHub repository
3. Set root directory to `backend/`
4. Configure environment variables
5. Deploy

### Step 2: Deploy Database
1. Add PostgreSQL service
2. Copy the `DATABASE_URL` to your backend service
3. The database will be automatically provisioned

### Step 3: Deploy Frontend
1. Create another service for frontend
2. Set root directory to `frontend/`
3. Configure build and start commands
4. Set `VITE_API_URL` environment variable
5. Deploy

### Step 4: Configure Domains
1. Go to each service's settings
2. Generate custom domains or use Railway's provided domains
3. Update CORS settings in backend with frontend domain

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check `requirements.txt` for missing dependencies
   - Ensure all Python packages are compatible

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is correctly set
   - Check if database service is running

3. **CORS Errors**
   - Update `ALLOWED_ORIGINS` with your frontend domain
   - Ensure frontend URL is correct

4. **Environment Variables**
   - Double-check all required variables are set
   - Use Railway's environment variable editor

### Debugging Commands:

```bash
# Check Railway logs
railway logs

# View service status
railway status

# Connect to database
railway connect
```

## 📊 Monitoring and Scaling

### Railway Features:
- **Auto-scaling**: Railway automatically scales based on traffic
- **Health checks**: Configured in `railway.json`
- **Logs**: Real-time logs in Railway dashboard
- **Metrics**: Built-in monitoring and analytics

### Performance Optimization:
- Enable Redis for caching
- Use CDN for static assets
- Configure proper database connection pooling

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

### Scaling Strategies:
1. **Horizontal Scaling**: Railway handles this automatically
2. **Database Scaling**: Upgrade PostgreSQL plan as needed
3. **Caching**: Add Redis for better performance
4. **CDN**: Use Railway's CDN for static assets

## 🎯 Next Steps

After deployment:
1. Test all API endpoints
2. Verify frontend-backend communication
3. Set up monitoring and alerts
4. Configure custom domains
5. Set up CI/CD pipeline

## 📞 Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- AutoRedactAI Issues: Create an issue in the GitHub repository

---

**Happy Deploying! 🚀** 