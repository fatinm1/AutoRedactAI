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

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting AutoRedactAI application")
    try:
        # Check for frontend files
        frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")
        if os.path.exists(frontend_dist_path):
            app.mount("/static", StaticFiles(directory=frontend_dist_path), name="static")
            
            # Serve frontend at root path
            @app.get("/")
            async def serve_frontend():
                return FileResponse(os.path.join(frontend_dist_path, "index.html"))
            
            # Serve frontend for all other routes (for client-side routing)
            @app.get("/{full_path:path}")
            async def serve_frontend_routes(full_path: str):
                # Don't serve frontend for API routes
                if full_path.startswith("api") or full_path.startswith("health"):
                    raise HTTPException(status_code=404, detail="Not found")
                # Serve index.html for all other routes to support client-side routing
                return FileResponse(os.path.join(frontend_dist_path, "index.html"))
            
            logger.info("Frontend static files mounted successfully")
        else:
            logger.info("Frontend dist not found, running in API-only mode")
            # If no frontend, serve API info at root
            @app.get("/")
            async def root():
                return {"message": "AutoRedactAI API", "status": "running", "note": "Frontend not found"}
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 