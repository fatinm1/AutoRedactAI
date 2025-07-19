#!/usr/bin/env python3
"""
AutoRedactAI - Advanced AI Setup Script

This script sets up the complete AI infrastructure for the document redaction system:
1. Creates necessary directories for models and data
2. Installs all AI/ML dependencies
3. Downloads and configures Llama 2.7B model
4. Sets up NLP models (spaCy, NLTK)
5. Configures ML ensemble models

Usage:
    python setup_llama.py

Requirements:
    - Python 3.8+
    - Internet connection for model downloads
    - 4GB+ disk space for Llama model
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path
import zipfile
import tarfile

def print_header():
    """Print setup header with system information"""
    print("🚀 Setting up Advanced AI Redaction System")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("=" * 50)

def create_directories():
    """
    Create necessary directories for AI models and data storage
    
    Directory structure:
    - models/          # AI model files (Llama, etc.)
    - data/           # Training and test data
    - logs/           # System logs and performance metrics
    """
    directories = ["models", "data", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")

def install_dependencies():
    """
    Install all Python dependencies from requirements.txt
    
    This installs:
    - Core AI/ML libraries (torch, transformers, spacy)
    - ML ensemble models (xgboost, lightgbm, catboost)
    - NLP tools (sentence-transformers, textblob)
    - Document processing (PyPDF2, python-docx, pdfplumber)
    - Llama integration (llama-cpp-python)
    """
    print("Installing Python dependencies...")
    
    try:
        # Install requirements using pip
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True, check=True)
        
        print("✓ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def download_llama_model():
    """
    Download Llama 2.7B model for advanced text understanding
    
    The Llama model provides:
    - Natural language understanding
    - Context-aware entity detection
    - Complex document analysis
    - Semantic understanding of sensitive information
    
    Model size: ~4GB
    Download time: 10-30 minutes (depending on internet speed)
    """
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.gguf"
    model_path = "models/llama-2-7b-chat.gguf"
    
    if os.path.exists(model_path):
        print("✓ Llama model already exists")
        return True
    
    print("Downloading Llama 2.7B model...")
    print("This may take 10-30 minutes depending on your internet speed.")
    print("Model size: ~4GB")
    
    try:
        # Download with progress tracking
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = (downloaded / total_size) * 100
            print(f"\rDownload progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end="")
        
        urllib.request.urlretrieve(model_url, model_path, progress_hook)
        print(f"\n✓ Llama model downloaded successfully: {model_path}")
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to download Llama model: {e}")
        print("You can still use the system without Llama - it will use ML ensemble instead.")
        return False

def setup_nlp_models():
    """
    Set up NLP models for text processing
    
    This includes:
    - spaCy English model for Named Entity Recognition (NER)
    - NLTK data for text processing
    - Sentence Transformers for semantic similarity
    """
    print("Setting up NLP models...")
    
    try:
        # Download spaCy English model
        print("Downloading spaCy English model...")
        subprocess.run([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ], check=True)
        print("✓ spaCy English model downloaded")
        
        # Download NLTK data
        print("Downloading NLTK data...")
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        print("✓ NLTK data downloaded")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to setup NLP models: {e}")
        return False

def verify_installation():
    """
    Verify that all AI components are properly installed and configured
    
    Checks:
    - Python packages are importable
    - Model files exist
    - Basic functionality works
    """
    print("Verifying installation...")
    
    try:
        # Test core imports
        import torch
        import transformers
        import spacy
        import xgboost
        import lightgbm
        import catboost
        import sentence_transformers
        import textblob
        
        print("✓ All core AI libraries imported successfully")
        
        # Test spaCy model
        nlp = spacy.load("en_core_web_sm")
        test_text = "John Doe lives in New York."
        doc = nlp(test_text)
        print(f"✓ spaCy NER working: Found {len(doc.ents)} entities")
        
        # Test Llama model if available
        if os.path.exists("models/llama-2-7b-chat.gguf"):
            print("✓ Llama model file exists")
        else:
            print("⚠ Llama model not found (system will use ML ensemble)")
        
        print("✓ Installation verification completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Installation verification failed: {e}")
        return False

def main():
    """
    Main setup function that orchestrates the complete AI system setup
    
    Setup steps:
    1. Create directories
    2. Install dependencies
    3. Download Llama model (optional)
    4. Setup NLP models
    5. Verify installation
    """
    print_header()
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("✗ Setup failed during dependency installation")
        return False
    
    # Step 3: Download Llama model (optional)
    download_llama_model()
    
    # Step 4: Setup NLP models
    if not setup_nlp_models():
        print("✗ Setup failed during NLP model setup")
        return False
    
    # Step 5: Verify installation
    if not verify_installation():
        print("✗ Setup verification failed")
        return False
    
    print("\n🎉 Advanced AI Redaction System setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend server: uvicorn app.main:app --reload")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Upload documents and test AI redaction")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 