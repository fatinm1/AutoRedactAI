# AutoRedactAI – Web-Based Document Privacy Assistant

A modern, AI-powered document redaction platform that automatically detects and redacts sensitive information from PDFs, DOCX, and TXT files.

## 🚀 Features

### Core Functionality
- **Document Upload**: Support for PDF, DOCX, and TXT files with drag-and-drop interface
- **AI-Powered Redaction**: Uses spaCy & fine-tuned BERT to detect:
  - PII (names, SSNs, emails, addresses)
  - Financial information (bank accounts, credit cards)
  - Legal entities (court names, statutes, dates)
- **Interactive Preview**: Review and edit redactions before export
- **Multiple Export Formats**: PDF, TXT with optional audit logs (CSV)
- **Batch Processing**: Handle multiple files simultaneously
- **Audit Trail**: Complete logging for compliance (GDPR, HIPAA)

### Advanced Features
- **Confidence Scoring**: AI model certainty indicators
- **Role-Based Access**: Admin and Reviewer permissions
- **Team Collaboration**: Multi-user document review
- **Compliance Dashboard**: Analytics and reporting

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
- **AI/ML**: spaCy + Transformers (BERT)
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

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
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
│   │   ├── ml/             # AI/ML models
│   │   └── utils/          # Utilities
│   ├── alembic/            # Database migrations
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
OPENAI_API_KEY=your_openai_key
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
- **Issues**: [GitHub Issues](https://github.com/your-org/AutoRedactAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/AutoRedactAI/discussions)

## 🔒 Security

- All file uploads are scanned for malware
- Files are automatically deleted after 7 days
- JWT tokens with short expiration times
- Rate limiting on all API endpoints
- HTTPS enforcement in production
- Regular security audits

---

Built with ❤️ for document privacy and compliance 