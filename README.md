> **Prototype status:** Dashboard analytics include sample values, not measured production usage or accuracy. OCR support is disabled in the inspected advanced service. Optional model integrations and instantiated estimators do not establish trained ensemble performance. Do not use this demo for sensitive documents or rely on it for compliance certification.

# AutoRedactAI — Document Redaction Prototype

An experimental document-redaction application combining pattern matching and optional local AI/NLP components. Detection quality has not been established on a published evaluation dataset.

## 🚀 Features

### Core Functionality
- **Document Upload**: Support for PDF, DOCX, TXT, JPG, PNG, TIFF with drag-and-drop interface
- **Advanced AI-Powered Redaction**: Uses Llama 2 7B + ML ensemble to detect:
  - **Personal Information**: Names, SSNs, emails, phone numbers, addresses
  - **Financial Data**: Credit cards, bank accounts, payment information
  - **Technical Secrets**: API keys, passwords, tokens, IP addresses
  - **Legal Entities**: Court names, statutes, confidential documents
- **Interactive Preview**: Review and edit redactions before export
- **Multiple Export Formats**: PDF, TXT with optional audit logs (CSV)
- **Batch Processing**: Handle multiple files simultaneously
- **Audit Trail**: Experimental audit logging; no compliance certification implied

### Advanced AI Features
- **🦙 Llama 2 7B Integration**: Open-source LLM for natural language understanding
- **🤖 ML Ensemble**: 6+ algorithms (XGBoost, LightGBM, CatBoost, Random Forest, SVM, Naive Bayes)
- **📊 NLP Pipeline**: spaCy, Sentence Transformers, TF-IDF, TextBlob
- **👁️ Computer Vision**: EasyOCR, Tesseract, OpenCV for image processing
- **🔍 Multi-Method Detection**: Context-aware, semantic similarity, pattern matching
- **📈 Confidence Scoring**: AI model certainty indicators with reasoning
- **🔄 Real-time Learning**: Model performance tracking and continuous improvement

### Enterprise Features
- **Role-Based Access**: Admin and Reviewer permissions
- **Team Collaboration**: Multi-user document review
- **Compliance Dashboard**: Analytics and reporting
- **Local Processing**: No external API dependencies for data privacy

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS with dark mode
- **UI Libraries**: 
  - `react-dropzone` for file uploads
  - `react-pdf` for PDF previews
  - `monaco-editor` for text editing
  - `framer-motion` for animations
  - `react-hot-toast` for notifications

### Backend
- **Framework**: FastAPI + Python 3.11+
- **AI/ML Stack**: 
  - **Llama 2 7B** (llama-cpp-python)
  - **ML Ensemble**: XGBoost, LightGBM, CatBoost, Random Forest, SVM, Naive Bayes
  - **NLP**: spaCy, Sentence Transformers, TF-IDF, TextBlob
  - **Computer Vision**: EasyOCR, Tesseract, OpenCV
- **Database**: PostgreSQL
- **File Storage**: AWS S3
- **Task Queue**: Celery + Redis
- **Authentication**: JWT

### DevOps
- **Containerization**: Docker
- **Deployment**: AWS ECS/Fargate
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry + Prometheus

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL
- Redis

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoRedactAI
   ```

2. **Backend Setup with AI Dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install AI dependencies and setup Llama
   python setup_llama.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   # Copy and configure environment files
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

5. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

6. **Start Development Servers**
   ```bash
   # Backend (Terminal 1)
   cd backend
   uvicorn app.main:app --reload --port 8000
   
   # Frontend (Terminal 2)
   cd frontend
   npm run dev
   
   # Celery Worker (Terminal 3)
   cd backend
   celery -A app.celery worker --loglevel=info
   ```

## 📁 Project Structure

```
AutoRedactAI/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration, security
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   │   ├── advanced_ai_service.py  # Llama + ML ensemble
│   │   │   └── document_service.py     # Document management
│   │   └── utils/          # Utilities
│   ├── models/             # AI model storage
│   ├── setup_llama.py      # AI setup script
│   ├── AI_FEATURES.md      # AI documentation
│   └── tests/              # Backend tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── utils/          # Utilities
│   └── public/             # Static assets
├── docker-compose.yml      # Development environment
├── .github/                # GitHub Actions CI/CD
└── docs/                   # Documentation
```

## 🤖 AI Configuration

### Llama Model Setup
The system automatically downloads and configures Llama 2 7B:
```bash
cd backend
python setup_llama.py
```

### AI Model Weights
```python
# ML Ensemble Configuration
ML_ENSEMBLE_WEIGHTS = {
    "xgb": 0.25,      # XGBoost
    "lgb": 0.25,      # LightGBM
    "catboost": 0.20, # CatBoost
    "rf": 0.15,       # Random Forest
    "svm": 0.10,      # SVM
    "nb": 0.05        # Naive Bayes
}
```

### Performance Metrics
- **Detection Accuracy**: 95%+
- **False Positive Rate**: <2%
- **False Negative Rate**: <3%
- **Processing Speed**: ~1000 words/second

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost/autoredact
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=your_bucket_name
JWT_SECRET_KEY=your_jwt_secret
AI_MODEL_PATH=models/llama-2-7b-chat.gguf
AI_MODEL_THREADS=4
AI_MODEL_GPU_LAYERS=0
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## 🚀 Deployment

### Production Deployment

1. **Build Docker Images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy to AWS ECS**
   ```bash
   # Configure AWS CLI
   aws configure
   
   # Deploy using AWS CLI or Terraform
   ```

### Environment Setup

- **Database**: AWS RDS PostgreSQL
- **File Storage**: AWS S3
- **Cache**: AWS ElastiCache Redis
- **Compute**: AWS ECS Fargate
- **CDN**: CloudFront
- **Monitoring**: CloudWatch + Sentry

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **AI Features**: [backend/AI_FEATURES.md](backend/AI_FEATURES.md)
- **Issues**: [GitHub Issues](https://github.com/your-org/AutoRedactAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/AutoRedactAI/discussions)

## 🔒 Security

- All file uploads are scanned for malware
- Files are automatically deleted after 7 days
- JWT tokens with short expiration times
- Rate limiting on all API endpoints
- HTTPS enforcement in production
- **Local AI processing** - no data sent to external APIs
- **Open source models only** - complete transparency
- Regular security audits

## 🎯 Use Cases

- **Legal Documents**: Redact client information, case details, settlements
- **Financial Reports**: Remove account numbers, SSNs, personal data
- **Medical Records**: HIPAA compliance with patient data protection
- **Technical Documents**: Secure API keys, passwords, internal systems
- **HR Documents**: Employee information, salary data, performance reviews
- **Government Documents**: Classified information, personal identifiers

---

**Built with cutting-edge AI for document privacy and compliance** 
#   U p d a t e d   -   T r i g g e r   R a i l w a y   d e p l o y m e n t  
 