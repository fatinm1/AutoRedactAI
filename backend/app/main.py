import os
import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jose import JWTError, jwt
import bcrypt
from pathlib import Path

# Try to import database components with fallback
try:
    from sqlalchemy.orm import Session
    from app.core.database import get_db, init_db
    from app.models.database import User as DBUser, Document as DBDocument
    from app.core.config import settings
    DATABASE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Database imports failed: {e}")
    DATABASE_AVAILABLE = False
    # Fallback to in-memory storage
    users_db = {}
    documents_db = {}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AutoRedactAI",
    description="AI-powered document redaction platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic models for API responses
class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class Document(BaseModel):
    id: str
    filename: str
    file_size: int
    status: str
    created_at: str
    redactions_count: int

class DocumentResponse(BaseModel):
    success: bool
    message: str
    document: Document

# JWT functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Authentication dependency
async def get_current_user(
    token: str = Depends(lambda x: x.headers.get("authorization", "").replace("Bearer ", "")),
    db: Session = Depends(get_db) if DATABASE_AVAILABLE else None
):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    
    if DATABASE_AVAILABLE and db:
        # Get user from database
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        return user
    else:
        # Fallback to in-memory storage
        user = None
        for email, user_data in users_db.items():
            if user_data["id"] == user_id:
                user = user_data
                break
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        return user

# Authentication endpoints
@app.post("/api/v1/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db) if DATABASE_AVAILABLE else None):
    try:
        if DATABASE_AVAILABLE and db:
            # Check if user already exists in database
            existing_user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            
            # Create new user in database
            user_id = str(uuid.uuid4())
            hashed_password = hash_password(user_data.password)
            
            db_user = DBUser(
                id=user_id,
                email=user_data.email,
                username=user_data.email.split('@')[0],  # Use email prefix as username
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                is_active=True,
                is_verified=True
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_id}, expires_delta=access_token_expires
            )
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse(
                    id=user_id,
                    email=user_data.email,
                    full_name=user_data.full_name,
                    is_active=True
                )
            )
        else:
            # Fallback to in-memory storage
            if user_data.email in users_db:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            
            # Create new user
            user_id = str(uuid.uuid4())
            hashed_password = hash_password(user_data.password)
            
            user = {
                "id": user_id,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "hashed_password": hashed_password,
                "is_active": True
            }
            
            users_db[user_data.email] = user
            
            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_id}, expires_delta=access_token_expires
            )
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse(
                    id=user_id,
                    email=user_data.email,
                    full_name=user_data.full_name,
                    is_active=True
                )
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        if DATABASE_AVAILABLE and db:
            db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db) if DATABASE_AVAILABLE else None):
    try:
        if DATABASE_AVAILABLE and db:
            # Check if user exists in database
            user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect email or password"
                )
            
            # Verify password
            if not verify_password(user_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect email or password"
                )
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.id}, expires_delta=access_token_expires
            )
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    is_active=user.is_active
                )
            )
        else:
            # Fallback to in-memory storage
            user = users_db.get(user_data.email)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect email or password"
                )
            
            # Verify password
            if not verify_password(user_data.password, user["hashed_password"]):
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect email or password"
                )
            
            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user["id"]}, expires_delta=access_token_expires
            )
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse(
                    id=user["id"],
                    email=user["email"],
                    full_name=user["full_name"],
                    is_active=user["is_active"]
                )
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Login failed"
        )

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    if DATABASE_AVAILABLE:
        return UserResponse(
            id=current_user.id,
            email=current_user.email,
            full_name=current_user.full_name,
            is_active=current_user.is_active
        )
    else:
        return UserResponse(
            id=current_user["id"],
            email=current_user["email"],
            full_name=current_user["full_name"],
            is_active=current_user["is_active"]
        )

# Document upload endpoint
@app.post("/api/v1/documents/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db) if DATABASE_AVAILABLE else None
):
    try:
        # Validate file type
        allowed_types = [".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png", ".tiff"]
        file_extension = file.filename.lower().split(".")[-1] if "." in file.filename else ""
        
        if f".{file_extension}" not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Validate file size (10MB limit)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 10MB"
            )
        
        if DATABASE_AVAILABLE and db:
            # Create document record in database
            document_id = str(uuid.uuid4())
            stored_filename = f"{document_id}_{file.filename}"
            
            db_document = DBDocument(
                id=document_id,
                user_id=current_user.id,
                original_filename=file.filename,
                stored_filename=stored_filename,
                file_size=file.size or 0,
                file_type=file_extension,
                s3_key=f"documents/{document_id}/{stored_filename}",
                status="uploaded"
            )
            
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            
            # Convert to response model
            document = Document(
                id=document_id,
                filename=file.filename,
                file_size=file.size or 0,
                status="uploaded",
                created_at=db_document.created_at.isoformat(),
                redactions_count=0
            )
        else:
            # Fallback to in-memory storage
            document_id = str(uuid.uuid4())
            document = Document(
                id=document_id,
                filename=file.filename,
                file_size=file.size or 0,
                status="uploaded",
                created_at=datetime.utcnow().isoformat(),
                redactions_count=0
            )
            
            # Store document (in memory for now)
            documents_db[document_id] = {
                "document": document,
                "user_id": current_user["id"]
            }
        
        return DocumentResponse(
            success=True,
            message="Document uploaded successfully",
            document=document
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Document upload failed", error=str(e))
        if DATABASE_AVAILABLE and db:
            db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to upload document"
        )

# Get documents endpoint
@app.get("/api/v1/documents/")
async def get_documents(
    current_user = Depends(get_current_user), 
    db: Session = Depends(get_db) if DATABASE_AVAILABLE else None
):
    try:
        if DATABASE_AVAILABLE and db:
            # Get user's documents from database
            db_documents = db.query(DBDocument).filter(DBDocument.user_id == current_user.id).all()
            
            # Convert to response models
            documents = []
            for db_doc in db_documents:
                # Count redactions for this document (placeholder for now)
                redactions_count = 0  # We'll implement proper redaction counting later
                
                document = Document(
                    id=db_doc.id,
                    filename=db_doc.original_filename,
                    file_size=db_doc.file_size,
                    status=db_doc.status,
                    created_at=db_doc.created_at.isoformat(),
                    redactions_count=redactions_count
                )
                documents.append(document)
        else:
            # Fallback to in-memory storage
            user_documents = []
            for doc_id, doc_data in documents_db.items():
                if doc_data["user_id"] == current_user["id"]:
                    user_documents.append(doc_data["document"])
            documents = user_documents
        
        return {
            "success": True,
            "message": "Documents retrieved successfully",
            "documents": documents
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Get documents failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to get documents"
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
    
    # Initialize database if available
    if DATABASE_AVAILABLE:
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # Continue without database
    else:
        logger.info("Running with in-memory storage (database not available)")
    
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
            
            # Check if assets directory exists
            assets_path = os.path.join(frontend_dist_path, "assets")
            if os.path.exists(assets_path):
                logger.info(f"Assets directory found at: {assets_path}")
                # List files in assets directory
                try:
                    for file in os.listdir(assets_path):
                        logger.info(f"  Asset file: {file}")
                except Exception as e:
                    logger.error(f"Error listing assets: {e}")
                
                # Note: We're handling static files explicitly with correct MIME types
                logger.info("Frontend assets will be served with explicit MIME types")
            else:
                logger.error(f"Assets directory not found at: {assets_path}")
        else:
            logger.warning("Frontend dist not found in any expected location")
            logger.info("Running in API-only mode")
        
        # Authentication endpoints are now directly in main.py - no need to load external routes
        logger.info("Authentication endpoints loaded directly in main.py")
        
    except Exception as e:
        logger.error("Failed to initialize application", error=str(e))
        # Don't raise the error to allow the app to start

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Debug endpoint to serve React script directly
@app.get("/debug-react-script")
async def debug_react_script():
    if not frontend_available or not frontend_dist_path:
        return {"error": "Frontend not available"}
    
    script_path = os.path.join(frontend_dist_path, "assets", "index-BbkOudU3.js")
    if os.path.exists(script_path):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"React script exists, size: {len(content)} bytes")
                logger.info(f"First 200 chars: {content[:200]}")
                return {
                    "status": "found",
                    "size": len(content),
                    "first_200_chars": content[:200],
                    "path": script_path
                }
        except Exception as e:
            logger.error(f"Error reading React script: {e}")
            return {"error": f"Error reading script: {e}"}
    else:
        logger.error(f"React script not found at: {script_path}")
        # List what files are actually in the assets directory
        assets_dir = os.path.join(frontend_dist_path, "assets")
        if os.path.exists(assets_dir):
            files = os.listdir(assets_dir)
            logger.info(f"Files in assets directory: {files}")
            return {
                "error": "Script not found",
                "available_files": files,
                "expected_path": script_path
            }
        else:
            return {"error": "Assets directory not found"}

# Explicit JavaScript file serving with correct MIME type (must be before catch-all)
@app.get("/assets/{filename:path}")
async def serve_js_files(filename: str, request: Request):
    logger.info(f"Assets endpoint called for: {filename}")
    logger.info(f"Request path: {request.url.path}")
    
    if not frontend_available or not frontend_dist_path:
        logger.error("Frontend not available for assets request")
        raise HTTPException(status_code=404, detail="Frontend not available")
    
    file_path = os.path.join(frontend_dist_path, "assets", filename)
    logger.info(f"Looking for file at: {file_path}")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Set correct MIME type based on file extension
            if filename.endswith('.js'):
                media_type = "application/javascript"
            elif filename.endswith('.js.map'):
                media_type = "application/json"
            elif filename.endswith('.css'):
                media_type = "text/css"
            elif filename.endswith('.svg'):
                media_type = "image/svg+xml"
            else:
                media_type = "application/octet-stream"
            
            logger.info(f"Serving {filename} with MIME type: {media_type}, size: {len(content)} bytes")
            return FileResponse(
                path=file_path,
                media_type=media_type,
                headers={"Cache-Control": "public, max-age=31536000"}
            )
        except Exception as e:
            logger.error(f"Error serving {filename}: {e}")
            raise HTTPException(status_code=500, detail="Error serving file")
    else:
        logger.error(f"File not found: {file_path}")
        # List what files are actually in the assets directory
        assets_dir = os.path.join(frontend_dist_path, "assets")
        if os.path.exists(assets_dir):
            files = os.listdir(assets_dir)
            logger.info(f"Available files in assets directory: {files}")
        raise HTTPException(status_code=404, detail="File not found")

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
                    
                    # Check for the actual script tags
                    if '<script type="module"' in html_content:
                        logger.info("Found script tags in built HTML")
                        # Find all script tags
                        import re
                        script_tags = re.findall(r'<script[^>]*src="([^"]*)"[^>]*>', html_content)
                        logger.info(f"Script tags found: {script_tags}")
                    else:
                        logger.warning("No script tags found in built HTML!")
                    
                    # Check for root element
                    if '<div id="root"></div>' in html_content:
                        logger.info("Root element found in built HTML")
                    else:
                        logger.warning("Root element not found in built HTML!")
                        
            except Exception as e:
                logger.error(f"Error reading index.html: {e}")
            
            # Serve the actual React app
            try:
                return FileResponse(index_path)
            except Exception as e:
                logger.error(f"Error serving React frontend: {e}")
                # Fallback to static page if React fails
                return HTMLResponse(content="""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>AutoRedactAI - Error</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
                        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                        h1 { color: #ef4444; }
                        .error { padding: 10px; background: #fef2f2; border-radius: 4px; margin: 10px 0; color: #991b1b; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🚨 AutoRedactAI Error</h1>
                        <div class="error">
                            <strong>Error:</strong> React frontend failed to load<br>
                            <small>Error: """ + str(e) + """</small>
                        </div>
                        <p>Please check the server logs for more details.</p>
                        <hr>
                        <p><a href="/test">Test Page</a></p>
                        <p><a href="/api">API Status</a></p>
                        <p><a href="/health">Health Check</a></p>
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
    
    # Don't serve frontend for assets routes (let the specific assets endpoint handle them)
    if full_path.startswith("assets/"):
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