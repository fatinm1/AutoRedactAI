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
            # Debug: Read and log the content of the built index.html
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    logger.info(f"Built index.html content (first 500 chars): {html_content[:500]}")
                    # Check if it contains the correct script references
                    if "/src/main.tsx" in html_content:
                        logger.warning("Built index.html still contains development script reference!")
                    if "/assets/" in html_content:
                        logger.info("Built index.html contains asset references - good!")
            except Exception as e:
                logger.error(f"Error reading index.html: {e}")
            
            # Try to serve the React frontend
            try:
                return FileResponse(index_path)
            except Exception as e:
                logger.error(f"Error serving React frontend: {e}")
                # Fallback to simple page if React fails
                return HTMLResponse(content="""
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
                        
                        <div style="margin-top: 30px;">
                            <a href="/test" class="btn">Test Page</a>
                            <a href="/api" class="btn">API Status</a>
                            <a href="/health" class="btn">Health Check</a>
                        </div>
                        
                        <div style="margin-top: 20px; font-size: 0.9rem; color: #94a3b8;">
                            <p><strong>Note:</strong> React frontend is being loaded...</p>
                        </div>
                    </div>
                </body>
                </html>
                """)
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
    # Return a simple SVG favicon if file doesn't exist
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
        <rect width="32" height="32" fill="#0ea5e9"/>
        <text x="16" y="22" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="18" font-weight="bold">A</text>
    </svg>"""
    return HTMLResponse(content=svg_content, media_type="image/svg+xml")

@app.get("/vite.svg")
async def serve_vite_svg():
    if frontend_available and frontend_dist_path:
        vite_svg_path = os.path.join(frontend_dist_path, "vite.svg")
        if os.path.exists(vite_svg_path):
            return FileResponse(vite_svg_path)
    # Return Vite logo if file doesn't exist
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="31.88" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 257"><defs><linearGradient id="IconifyId1813088fe1fbc01fb466" x1="-.828%" x2="57.636%" y1="7.652%" y2="78.411%"><stop offset="0%" stop-color="#41D1FF"></stop><stop offset="100%" stop-color="#BD34FE"></stop></linearGradient><linearGradient id="IconifyId1813088fe1fbc01fb467" x1="43.376%" x2="50.316%" y1="2.242%" y2="89.03%"><stop offset="0%" stop-color="#FFEA83"></stop><stop offset="8.333%" stop-color="#FFDD35"></stop><stop offset="100%" stop-color="#FFA800"></stop></linearGradient></defs><path fill="url(#IconifyId1813088fe1fbc01fb466)" d="M255.153 37.938L134.897 252.976c-2.483 4.44-8.862 4.466-11.382.048L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62Z"></path><path fill="url(#IconifyId1813088fe1fbc01fb467)" d="M185.432.063L96.44 17.501a3.268 3.268 0 0 0-2.634 3.014l-5.474 92.456a3.268 3.268 0 0 0 3.997 3.378l24.777-5.718c2.318-.535 4.413 1.507 3.936 3.838l-7.361 36.047c-.495 2.426 1.782 4.5 4.151 3.78l15.304-4.649c2.372-.72 4.652 1.36 4.15 3.788l-11.698 56.621c-.732 3.542 3.979 5.473 5.943 2.437l1.313-2.028l72.516-144.72c1.215-2.423-.88-5.186-3.54-4.672l-25.505 4.922c-2.396.462-4.435-1.77-3.759-4.114l16.646-57.705c.677-2.35-1.37-4.583-3.769-4.113Z"></path></svg>"""
    return HTMLResponse(content=svg_content, media_type="image/svg+xml")

@app.get("/site.webmanifest")
async def serve_manifest():
    if frontend_available and frontend_dist_path:
        manifest_path = os.path.join(frontend_dist_path, "site.webmanifest")
        if os.path.exists(manifest_path):
            return FileResponse(manifest_path)
    # Return a simple manifest if file doesn't exist
    manifest_content = """{
        "name": "AutoRedactAI",
        "short_name": "AutoRedactAI",
        "description": "AI-powered document redaction platform",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0ea5e9"
    }"""
    return HTMLResponse(content=manifest_content, media_type="application/manifest+json")

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