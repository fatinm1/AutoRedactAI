# Railway Deployment Helper Script
# This script helps set up the correct configuration for Railway deployment

Write-Host "🚀 AutoRedactAI Railway Deployment Helper" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

Write-Host "`n📋 Deployment Steps:" -ForegroundColor Yellow
Write-Host "1. Create a new Railway project" -ForegroundColor White
Write-Host "2. Add PostgreSQL database service" -ForegroundColor White
Write-Host "3. Add backend service with root directory: backend/" -ForegroundColor White
Write-Host "4. Add frontend service with root directory: frontend/" -ForegroundColor White
Write-Host "5. Configure environment variables" -ForegroundColor White

Write-Host "`n🔧 Backend Service Configuration:" -ForegroundColor Yellow
Write-Host "Repository: Your AutoRedactAI repo" -ForegroundColor White
Write-Host "Branch: main or master" -ForegroundColor White
Write-Host "Root Directory: backend/" -ForegroundColor Cyan
Write-Host "Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port `$PORT" -ForegroundColor White

Write-Host "`n🔧 Frontend Service Configuration:" -ForegroundColor Yellow
Write-Host "Repository: Your AutoRedactAI repo" -ForegroundColor White
Write-Host "Branch: main or master" -ForegroundColor White
Write-Host "Root Directory: frontend/" -ForegroundColor Cyan
Write-Host "Build Command: npm install && npm run build" -ForegroundColor White
Write-Host "Start Command: npm run preview" -ForegroundColor White

Write-Host "`n🔑 Required Environment Variables:" -ForegroundColor Yellow

Write-Host "`nBackend Variables:" -ForegroundColor Cyan
Write-Host "SECRET_KEY=your-super-secret-production-key-here" -ForegroundColor White
Write-Host "DATABASE_URL=postgresql://username:password@host:port/database" -ForegroundColor White
Write-Host "ENVIRONMENT=production" -ForegroundColor White
Write-Host "DEBUG=false" -ForegroundColor White
Write-Host "ALLOWED_ORIGINS=https://your-frontend-domain.railway.app,http://localhost:3000" -ForegroundColor White

Write-Host "`nFrontend Variables:" -ForegroundColor Cyan
Write-Host "VITE_API_URL=https://your-backend-domain.railway.app" -ForegroundColor White

Write-Host "`n⚠️  Important Notes:" -ForegroundColor Red
Write-Host "- Set the correct root directory for each service!" -ForegroundColor White
Write-Host "- Backend: backend/" -ForegroundColor White
Write-Host "- Frontend: frontend/" -ForegroundColor White
Write-Host "- This is the most common cause of deployment failures" -ForegroundColor White

Write-Host "`n✅ Success Checklist:" -ForegroundColor Green
Write-Host "□ Backend service deployed with root directory 'backend/'" -ForegroundColor White
Write-Host "□ Frontend service deployed with root directory 'frontend/'" -ForegroundColor White
Write-Host "□ PostgreSQL database added and connected" -ForegroundColor White
Write-Host "□ Environment variables configured correctly" -ForegroundColor White
Write-Host "□ Health checks passing" -ForegroundColor White
Write-Host "□ Frontend can communicate with backend" -ForegroundColor White

Write-Host "`n📚 For detailed instructions, see: RAILWAY_DEPLOYMENT_FIX.md" -ForegroundColor Blue
Write-Host "🐛 For troubleshooting, check Railway logs and this guide" -ForegroundColor Blue

Write-Host "`n🎯 Key Fix: Set Root Directory correctly for each service!" -ForegroundColor Green 