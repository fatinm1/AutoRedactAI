#!/usr/bin/env python3
"""
Setup script for Llama model and AI dependencies
"""

import os
import sys
import subprocess
import requests
from pathlib import Path
import zipfile
import tarfile

def create_directories():
    """Create necessary directories"""
    directories = [
        "models",
        "data",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def download_llama_model():
    """Download Llama model (smaller version for testing)"""
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    model_path = "models/llama-2-7b-chat.gguf"
    
    if os.path.exists(model_path):
        print(f"✓ Llama model already exists: {model_path}")
        return
    
    print("Downloading Llama model (this may take a while)...")
    print(f"URL: {model_url}")
    
    try:
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rDownload progress: {progress:.1f}%", end='', flush=True)
        
        print(f"\n✓ Downloaded Llama model: {model_path}")
        
    except Exception as e:
        print(f"✗ Failed to download Llama model: {str(e)}")
        print("You can manually download it from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF")
        print("Or use a smaller model for testing")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {str(e)}")
        return False
    
    return True

def setup_spacy():
    """Setup spaCy English model"""
    print("Setting up spaCy English model...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ spaCy English model installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install spaCy model: {str(e)}")

def setup_nltk():
    """Setup NLTK data"""
    print("Setting up NLTK data...")
    
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        print("✓ NLTK data downloaded")
    except Exception as e:
        print(f"✗ Failed to setup NLTK: {str(e)}")

def create_config():
    """Create configuration file"""
    config_content = """# AI Configuration
AI_MODEL_PATH = "models/llama-2-7b-chat.gguf"
AI_MODEL_THREADS = 4
AI_MODEL_GPU_LAYERS = 0

# ML Configuration
ML_ENSEMBLE_WEIGHTS = {
    "xgb": 0.25,
    "lgb": 0.25,
    "catboost": 0.20,
    "rf": 0.15,
    "svm": 0.10,
    "nb": 0.05
}

# Processing Configuration
MAX_TEXT_LENGTH = 1024
CONFIDENCE_THRESHOLD = 0.7
"""
    
    with open("ai_config.py", "w") as f:
        f.write(config_content)
    
    print("✓ Created AI configuration file")

def main():
    """Main setup function"""
    print("🚀 Setting up Advanced AI Redaction System")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("✗ Setup failed during dependency installation")
        return
    
    # Setup NLP models
    setup_spacy()
    setup_nltk()
    
    # Download Llama model
    download_llama_model()
    
    # Create configuration
    create_config()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend server: uvicorn app.main:app --reload")
    print("2. Start the frontend: npm start (in frontend directory)")
    print("3. Upload a document and test the AI redaction")
    print("\nNote: If Llama model download failed, the system will use alternative AI methods")

if __name__ == "__main__":
    main() 