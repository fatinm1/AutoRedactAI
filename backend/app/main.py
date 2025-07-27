from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
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
            # Debug: List files in dist directory
            logger.info(f"Files in frontend dist directory:")
            try:
                for root, dirs, files in os.walk(frontend_dist_path):
                    for file in files:
                        logger.info(f"  {os.path.join(root, file)}")
            except Exception as e:
                logger.error(f"Error listing files: {e}")
            
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
            # For now, let's serve a simple test page to see if the issue is with React
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>AutoRedactAI - Document Privacy Assistant</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                        margin: 0; 
                        padding: 0; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .container { 
                        background: white; 
                        padding: 40px; 
                        border-radius: 16px; 
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        text-align: center;
                        max-width: 500px;
                        margin: 20px;
                    }
                    h1 { 
                        color: #1e293b; 
                        margin-bottom: 20px;
                        font-size: 2.5rem;
                        font-weight: 700;
                    }
                    .status { 
                        padding: 16px; 
                        background: #f0f9ff; 
                        border: 2px solid #0ea5e9;
                        border-radius: 8px; 
                        margin: 20px 0;
                        color: #0c4a6e;
                    }
                    .features {
                        text-align: left;
                        margin: 20px 0;
                    }
                    .features h3 {
                        color: #1e293b;
                        margin-bottom: 10px;
                    }
                    .features ul {
                        color: #64748b;
                        line-height: 1.6;
                    }
                    .btn {
                        display: inline-block;
                        background: #0ea5e9;
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 8px;
                        margin: 10px;
                        transition: background 0.3s;
                    }
                    .btn:hover {
                        background: #0284c7;
                    }
                    .logo {
                        font-size: 3rem;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo">🤖</div>
                    <h1>AutoRedactAI</h1>
                    <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 30px;">
                        AI-Powered Document Privacy Assistant
                    </p>
                    
                    <div class="status">
                        <strong>✅ Backend Status:</strong> Running successfully!
                    </div>
                    
                    <div class="features">
                        <h3>🚀 Features:</h3>
                        <ul>
                            <li>AI-powered document redaction</li>
                            <li>Privacy and compliance tools</li>
                            <li>PDF and DOCX support</li>
                            <li>Advanced ML models</li>
                        </ul>
                    </div>
                    
                    <div style="margin-top: 30px;">
                        <a href="/test" class="btn">Test Page</a>
                        <a href="/api" class="btn">API Status</a>
                        <a href="/health" class="btn">Health Check</a>
                    </div>
                    
                    <div style="margin-top: 20px; font-size: 0.9rem; color: #94a3b8;">
                        <p><strong>Note:</strong> This is a test page. The React frontend is being debugged.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content)
        else:
            logger.error(f"index.html not found at {index_path}")
    
    # Fallback to API info
    return {"message": "AutoRedactAI API", "status": "running", "note": "Frontend not available"}

# Test endpoint to serve a simple HTML page
@app.get("/test")
async def test_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AutoRedactAI Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #0ea5e9; }
            .status { padding: 10px; background: #e0f2fe; border-radius: 4px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AutoRedactAI Test Page</h1>
            <div class="status">
                <strong>Status:</strong> Backend is working! ✅
            </div>
            <p>If you can see this page, the backend is serving HTML correctly.</p>
            <p>This means the issue is likely with the React frontend or its assets.</p>
            <hr>
            <p><a href="/">← Back to main page</a></p>
            <p><a href="/api">API Status</a></p>
            <p><a href="/health">Health Check</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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