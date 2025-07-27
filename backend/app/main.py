from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import structlog

logger = structlog.get_logger()

app = FastAPI(
    title="AutoRedactAI",
    version="1.0.0",
    description="AI-Powered Document Redaction System"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # Simplified for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AutoRedactAI"}

# API info endpoint
@app.get("/api")
async def api_info():
    return {"message": "AutoRedactAI API", "status": "running"}

# Global variable to track if frontend is available
frontend_available = False
frontend_dist_path = None

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    global frontend_available, frontend_dist_path
    logger.info("Starting AutoRedactAI application")
    
    try:
        # Check for frontend files - try multiple possible paths
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist"),
            os.path.join(os.getcwd(), "frontend", "dist"),
            "/app/frontend/dist"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                frontend_dist_path = path
                frontend_available = True
                logger.info(f"Found frontend at: {path}")
                break
        
        if frontend_available:
            # Mount static files directory
            app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_path, "assets")), name="assets")
            logger.info("Frontend static files mounted successfully")
        else:
            logger.warning("Frontend dist not found in any expected location")
            logger.info("Running in API-only mode")
        
        # Try to import and add API routes (but don't fail if they don't work)
        try:
            from app.api.v1.api import api_router
            app.include_router(api_router, prefix="/api/v1")
            logger.info("API routes loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load API routes: {e}")
            logger.info("Running in basic mode without API routes")
        
    except Exception as e:
        logger.error("Failed to initialize application", error=str(e))
        # Don't raise the error to allow the app to start

# Root endpoint - serve frontend or API info
@app.get("/")
async def root():
    if frontend_available and frontend_dist_path:
        index_path = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            logger.error(f"index.html not found at {index_path}")
    
    # Fallback to API info
    return {"message": "AutoRedactAI API", "status": "running", "note": "Frontend not available"}

# Serve static files that might be requested
@app.get("/favicon.svg")
async def serve_favicon_svg():
    if frontend_available and frontend_dist_path:
        favicon_path = os.path.join(frontend_dist_path, "favicon.svg")
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path)
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/vite.svg")
async def serve_vite_svg():
    if frontend_available and frontend_dist_path:
        vite_svg_path = os.path.join(frontend_dist_path, "vite.svg")
        if os.path.exists(vite_svg_path):
            return FileResponse(vite_svg_path)
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/site.webmanifest")
async def serve_manifest():
    if frontend_available and frontend_dist_path:
        manifest_path = os.path.join(frontend_dist_path, "site.webmanifest")
        if os.path.exists(manifest_path):
            return FileResponse(manifest_path)
    raise HTTPException(status_code=404, detail="Not found")

# Catch-all route for frontend routing (must be last)
@app.get("/{full_path:path}")
async def serve_frontend_routes(full_path: str):
    # Don't serve frontend for API routes
    if full_path.startswith("api") or full_path.startswith("health"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Serve frontend if available
    if frontend_available and frontend_dist_path:
        index_path = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    
    # Fallback
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 