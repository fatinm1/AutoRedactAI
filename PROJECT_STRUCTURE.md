# AutoRedactAI Project Structure

This document provides a comprehensive overview of the AutoRedactAI project structure and architecture.

## 📁 Root Directory Structure

```
AutoRedactAI/
├── 📁 backend/                    # FastAPI Backend Application
├── 📁 frontend/                   # React Frontend Application
├── 📁 docs/                       # Project Documentation
├── 📁 .github/                    # GitHub Actions CI/CD
├── 📄 docker-compose.yml          # Docker Development Environment
├── 📄 setup.sh                    # Development Environment Setup Script
├── 📄 start-docker.sh             # Docker Startup Script
├── 📄 README.md                   # Main Project Documentation
└── 📄 PROJECT_STRUCTURE.md        # This File
```

## 🔧 Backend Structure (`backend/`)

### Core Application (`backend/app/`)

```
backend/app/
├── 📁 api/                        # API Routes and Endpoints
│   └── 📁 v1/
│       ├── 📄 api.py              # Main API router
│       └── 📁 endpoints/          # API endpoint modules
│           ├── 📄 auth.py         # Authentication endpoints
│           ├── 📄 documents.py    # Document management
│           ├── 📄 redactions.py   # Redaction operations
│           ├── 📄 users.py        # User management
│           ├── 📄 exports.py      # Export functionality
│           └── 📄 analytics.py    # Analytics and reporting
├── 📁 core/                       # Core Configuration
│   ├── 📄 config.py               # Application settings
│   └── 📄 security.py             # Security utilities
├── 📁 models/                     # Database Models
│   └── 📄 database.py             # SQLAlchemy models
├── 📁 services/                   # Business Logic Services
│   ├── 📄 user_service.py         # User management logic
│   ├── 📄 document_service.py     # Document processing
│   ├── 📄 redaction_service.py    # Redaction operations
│   └── 📄 export_service.py       # Export operations
├── 📁 ml/                         # AI/ML Components
│   ├── 📄 redaction_engine.py     # Main redaction engine
│   ├── 📄 models/                 # AI model configurations
│   └── 📄 utils/                  # ML utilities
├── 📁 utils/                      # Utility Functions
│   ├── 📄 file_utils.py           # File handling utilities
│   ├── 📄 text_utils.py           # Text processing utilities
│   └── 📄 validators.py           # Data validation
└── 📄 main.py                     # FastAPI application entry point
```

### Database and Migrations

```
backend/
├── 📁 alembic/                    # Database migrations
│   ├── 📄 versions/               # Migration files
│   ├── 📄 env.py                  # Alembic environment
│   └── 📄 alembic.ini             # Alembic configuration
└── 📁 tests/                      # Backend tests
    ├── 📁 unit/                   # Unit tests
    ├── 📁 integration/            # Integration tests
    └── 📁 fixtures/               # Test data
```

### Configuration Files

```
backend/
├── 📄 requirements.txt            # Python dependencies
├── 📄 Dockerfile                  # Backend Docker image
├── 📄 env.example                 # Environment variables template
└── 📄 .env                        # Local environment variables
```

## 🎨 Frontend Structure (`frontend/`)

### Source Code (`frontend/src/`)

```
frontend/src/
├── 📁 components/                 # Reusable React Components
│   ├── 📁 Layout/                 # Layout components
│   │   ├── 📄 Layout.tsx          # Main layout wrapper
│   │   ├── 📄 Sidebar.tsx         # Navigation sidebar
│   │   └── 📄 Header.tsx          # Application header
│   ├── 📁 Auth/                   # Authentication components
│   │   ├── 📄 LoginForm.tsx       # Login form
│   │   ├── 📄 RegisterForm.tsx    # Registration form
│   │   └── 📄 ProtectedRoute.tsx  # Route protection
│   ├── 📁 Documents/              # Document-related components
│   │   ├── 📄 DocumentUpload.tsx  # File upload component
│   │   ├── 📄 DocumentPreview.tsx # Document preview
│   │   └── 📄 RedactionEditor.tsx # Redaction editing
│   ├── 📁 UI/                     # UI components
│   │   ├── 📄 Button.tsx          # Custom button component
│   │   ├── 📄 Modal.tsx           # Modal dialog
│   │   ├── 📄 Loading.tsx         # Loading states
│   │   └── 📄 Toast.tsx           # Toast notifications
│   └── 📁 Charts/                 # Analytics components
│       ├── 📄 RedactionChart.tsx  # Redaction statistics
│       └── 📄 ComplianceChart.tsx # Compliance metrics
├── 📁 pages/                      # Page Components
│   ├── 📄 Dashboard.tsx           # Main dashboard
│   ├── 📄 DocumentUpload.tsx      # Upload page
│   ├── 📄 DocumentReview.tsx      # Review page
│   ├── 📄 DocumentHistory.tsx     # History page
│   ├── 📄 Analytics.tsx           # Analytics page
│   ├── 📄 Settings.tsx            # Settings page
│   └── 📁 Auth/                   # Authentication pages
│       ├── 📄 Login.tsx           # Login page
│       └── 📄 Register.tsx        # Registration page
├── 📁 hooks/                      # Custom React Hooks
│   ├── 📄 useAuth.ts              # Authentication hook
│   ├── 📄 useDocuments.ts         # Document management hook
│   ├── 📄 useRedactions.ts        # Redaction operations hook
│   └── 📄 useApi.ts               # API communication hook
├── 📁 services/                   # API Services
│   ├── 📄 api.ts                  # API client configuration
│   ├── 📄 auth.ts                 # Authentication API
│   ├── 📄 documents.ts            # Documents API
│   ├── 📄 redactions.ts           # Redactions API
│   └── 📄 exports.ts              # Exports API
├── 📁 contexts/                   # React Contexts
│   ├── 📄 AuthContext.tsx         # Authentication context
│   └── 📄 ThemeContext.tsx        # Theme management
├── 📁 utils/                      # Utility Functions
│   ├── 📄 constants.ts            # Application constants
│   ├── 📄 helpers.ts              # Helper functions
│   ├── 📄 validators.ts           # Form validation
│   └── 📄 formatters.ts           # Data formatting
├── 📁 types/                      # TypeScript Type Definitions
│   ├── 📄 auth.ts                 # Authentication types
│   ├── 📄 documents.ts            # Document types
│   ├── 📄 redactions.ts           # Redaction types
│   └── 📄 api.ts                  # API response types
├── 📁 styles/                     # Styling
│   ├── 📄 globals.css             # Global styles
│   └── 📄 components.css          # Component-specific styles
└── 📄 App.tsx                     # Main application component
```

### Configuration Files

```
frontend/
├── 📄 package.json                # Node.js dependencies
├── 📄 vite.config.ts              # Vite configuration
├── 📄 tailwind.config.js          # Tailwind CSS configuration
├── 📄 tsconfig.json               # TypeScript configuration
├── 📄 Dockerfile                  # Frontend Docker image
├── 📄 env.example                 # Environment variables template
└── 📄 .env                        # Local environment variables
```

## 🐳 Docker Configuration

### Development Environment

```
docker-compose.yml                 # Main Docker Compose file
├── 📁 backend/
│   └── 📄 Dockerfile              # Backend container
├── 📁 frontend/
│   └── 📄 Dockerfile              # Frontend container
└── 📁 nginx/                      # Production web server
    ├── 📄 nginx.conf              # Nginx configuration
    └── 📁 ssl/                    # SSL certificates
```

## 🔄 CI/CD Pipeline (`.github/workflows/`)

```
.github/workflows/
└── 📄 ci.yml                      # GitHub Actions workflow
    ├── Backend testing
    ├── Frontend testing
    ├── Security scanning
    ├── Docker image building
    └── Deployment automation
```

## 📊 Database Schema

### Core Tables

1. **users** - User accounts and authentication
2. **documents** - Uploaded document metadata
3. **redactions** - Detected sensitive information
4. **audit_logs** - Compliance and activity tracking
5. **processing_jobs** - Background job management
6. **export_jobs** - Export operation tracking
7. **team_collaborations** - Multi-user document review
8. **compliance_reports** - Analytics and reporting

## 🔐 Security Architecture

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, User, Reviewer)
- Password hashing with bcrypt
- Rate limiting and request validation

### Data Protection
- File encryption at rest
- Secure file upload validation
- Automatic file deletion after retention period
- Audit logging for compliance

## 🤖 AI/ML Architecture

### Redaction Engine
- **spaCy NER** - Base entity recognition
- **BERT Transformers** - Advanced context understanding
- **Custom Regex Patterns** - Specific format detection
- **Confidence Scoring** - Quality assessment
- **Multi-language Support** - Internationalization ready

### Model Pipeline
1. Text extraction from documents
2. Entity detection with multiple models
3. Confidence scoring and filtering
4. Context analysis and validation
5. Redaction application and logging

## 📱 User Interface Design

### Design System
- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS with custom design tokens
- **UI Library**: Custom components with Framer Motion
- **Theme**: Dark/Light mode support
- **Responsive**: Mobile-first design approach

### Key Features
- Drag-and-drop file upload
- Real-time document preview
- Interactive redaction editing
- Progress tracking and notifications
- Analytics dashboard
- Team collaboration tools

## 🚀 Deployment Architecture

### Development
- Docker Compose for local development
- Hot reload for both frontend and backend
- Shared volumes for code changes
- Health checks for all services

### Production
- AWS ECS/Fargate for container orchestration
- AWS RDS for PostgreSQL database
- AWS S3 for file storage
- AWS ElastiCache for Redis
- CloudFront for CDN
- Route 53 for DNS management

## 📈 Monitoring & Observability

### Application Monitoring
- Structured logging with structlog
- Error tracking with Sentry
- Performance metrics with Prometheus
- Health check endpoints
- Request tracing and correlation

### Infrastructure Monitoring
- AWS CloudWatch for infrastructure metrics
- Container health monitoring
- Database performance tracking
- File storage usage monitoring

## 🔧 Development Workflow

### Local Development
1. Run `./setup.sh` to initialize environment
2. Configure environment variables
3. Start services with `./start-docker.sh`
4. Access application at http://localhost:3000

### Code Quality
- ESLint and Prettier for frontend
- Black, isort, and flake8 for backend
- TypeScript strict mode
- Automated testing with Jest and pytest
- Code coverage reporting

### Git Workflow
- Feature branch development
- Pull request reviews
- Automated CI/CD pipeline
- Semantic versioning
- Release automation

This structure provides a scalable, maintainable, and secure foundation for the AutoRedactAI platform, with clear separation of concerns and modern development practices. 