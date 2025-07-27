from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import subprocess
import sys
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import init_db
import structlog

logger = structlog.get_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-Powered Document Redaction System"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AutoRedactAI"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "AutoRedactAI API", "status": "running"}

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting AutoRedactAI application")
    try:
        # Initialize database connection
        init_db()
        logger.info("Database initialized successfully")
        
        # Build frontend if it doesn't exist
        frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")
        if not os.path.exists(frontend_dist_path):
            logger.info("Frontend dist not found, building frontend...")
            try:
                frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend")
                
                # Check if Node.js is available
                try:
                    subprocess.run(["node", "--version"], check=True, capture_output=True)
                    logger.info("Node.js is available, building frontend...")
                    
                    # Install frontend dependencies
                    logger.info("Installing frontend dependencies...")
                    subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
                    
                    # Build frontend
                    logger.info("Building frontend...")
                    subprocess.run(["npm", "run", "build"], cwd=frontend_path, check=True)
                    
                    logger.info("Frontend built successfully")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    logger.warning("Node.js not available, skipping frontend build")
                    logger.info("Frontend will not be served - API only mode")
                    
            except Exception as e:
                logger.warning(f"Failed to build frontend: {e}")
                logger.info("Frontend will not be served - API only mode")
        
        # Serve frontend static files if they exist
        if os.path.exists(frontend_dist_path):
            app.mount("/static", StaticFiles(directory=frontend_dist_path), name="static")
            
            @app.get("/app")
            async def serve_frontend():
                return FileResponse(os.path.join(frontend_dist_path, "index.html"))
            
            @app.get("/app/{full_path:path}")
            async def serve_frontend_routes(full_path: str):
                # Serve index.html for all routes to support client-side routing
                return FileResponse(os.path.join(frontend_dist_path, "index.html"))
            
            logger.info("Frontend static files mounted successfully")
        else:
            logger.info("Frontend dist not found, running in API-only mode")
        
    except Exception as e:
        logger.error("Failed to initialize application", error=str(e))
        # Don't raise the error in production to allow the app to start
        if settings.ENVIRONMENT == "development":
            raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 