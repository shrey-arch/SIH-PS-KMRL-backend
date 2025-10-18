# 🚀 KMRL Backend - Document Intelligence & Routing Hub

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Testing & Verification](#testing--verification)
- [Development](#development)
- [Future Roadmap](#future-roadmap)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

**KMRL Backend** is the central document intelligence and routing hub for Kochi Metro Rail Limited. It serves as the backbone for processing, analyzing, and distributing critical documents across the organization.

### Purpose
- **Document Intake**: Accept uploads from worker/admin/engineer apps
- **AI Processing**: Extract text and generate intelligent summaries
- **Workflow Management**: Control room review and approval system
- **Role-Based Distribution**: Deliver relevant documents to the right people

---

## ✨ Features

### ✅ Core Features (MVP)
| Feature | Status | Description |
|---------|--------|-------------|
| Document Upload | ✅ Complete | Multi-format file upload with storage |
| Text Extraction | ✅ Complete | PDF and text file content extraction |
| AI Summarization | ⚡ Partial | Intelligent document summarization |
| Control Room Review | ✅ Complete | Document approval workflow |
| Role-Based Access | ✅ Complete | Engineer/Passenger-specific document feeds |
| Public API Access | ✅ Complete | Ngrok integration for external access |

### 🔮 Future Enhancements
- Advanced AI summarization with multiple models
- Real-time notifications
- Audit trail and compliance logging
- Multi-language support (English + Malayalam)
- Advanced search capabilities
- User authentication system

---

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** - Modern Python web framework with automatic API docs
- **Uvicorn** - ASGI server for high-performance async handling
- **Pydantic** - Data validation using Python type annotations

### Database & ORM
- **SQLAlchemy** - Python SQL toolkit and Object-Relational Mapping
- **SQLite** - Lightweight, file-based database (development)

### AI & Document Processing
- **Hugging Face Transformers** - State-of-the-art NLP models
- **PyPDF2** - PDF text extraction library
- **Python-multipart** - File upload handling

### Deployment & Integration
- **Ngrok** - Secure public tunneling for demo/testing
- **Python-dotenv** - Environment variable management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd kmrl-backend
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create `.env` file in project root:
   ```env
   # Hugging Face API Key (Optional - for AI summarization)
   HF_API_KEY=your_huggingface_api_key_here
   
   # Database Configuration
   DATABASE_URL=sqlite:///./database.db
   
   # Application Settings
   APP_NAME=KMRL-Backend
   ENVIRONMENT=development
   ```

5. **Initialize Database**
   ```bash
   # The database auto-creates on first run
   python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   ```

---

## 🖥️ Running the Server

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access Points
- **Local Access**: `http://localhost:8000`
- **Network Access**: `http://[YOUR_IP]:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Public Access** (via Ngrok): `https://[YOUR_SUBDOMAIN].ngrok-free.app`

---

## 📚 API Documentation

### Available Endpoints

#### 1. **Health Check**
```http
GET /
```
**Response**: `{"message": "KMRL Backend is running!"}`

#### 2. **Document Upload**
```http
POST /upload_doc/
```
**Parameters**:
- `uploader` (query): Name of person uploading
- `file` (form-data): Document file (PDF, TXT)

**Response**: Document metadata with processing status

#### 3. **Document Approval**
```http
POST /approve_doc/{doc_id}
```
**Body**:
```json
{
  "roles": ["engineer", "passenger"]
}
```

#### 4. **Role-Based Document Retrieval**
```http
GET /docs/{role}
```
**Response**: List of approved documents for specified role

---

## 🧪 Testing & Verification

### Step-by-Step Verification

1. **Server Health Check**
   ```bash
   curl http://localhost:8000/
   # Expected: {"message":"KMRL Backend is running!"}
   ```

2. **Test File Upload**
   ```bash
   # Create test file
   echo "KMRL Maintenance Report: Signal system update completed at Edappally station." > test_doc.txt
   
   # Upload via API
   curl -X POST "http://localhost:8000/upload_doc/?uploader=test_engineer" -F "file=@test_doc.txt"
   ```

3. **Verify Database Entry**
   ```bash
   python check_db.py
   # Should show document with extracted text and summary
   ```

4. **Test Approval Workflow**
   ```bash
   # Approve document (replace ID with actual document ID)
   curl -X POST "http://localhost:8000/approve_doc/1" -H "Content-Type: application/json" -d '{"roles": ["engineer"]}'
   ```

5. **Test Role-Based Access**
   ```bash
   curl "http://localhost:8000/docs/engineer"
   # Should return approved documents for engineers
   ```

### Automated Testing Script
```bash
# Run comprehensive test suite
python test_upload.py
python test_processor.py
```

---

## 🔧 Development

### Project Structure
```
kmrl-backend/
├── main.py                 # FastAPI application entry point
├── database.py            # Database connection configuration
├── models.py              # SQLAlchemy ORM models
├── schema.py              # Pydantic request/response models
├── crud.py                # Database operations (Create, Read, Update, Delete)
├── services/
│   └── document_processor.py  # AI processing and text extraction
├── data/
│   └── uploads/           # Uploaded file storage
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

### Key Components

#### Database Models
- **Document**: Core entity storing file metadata, content, and approval status
- Fields: id, filename, uploader, raw_text, summary, roles, approved

#### Document Processing Flow
1. File uploaded via `/upload_doc/`
2. File saved to `data/uploads/`
3. Background processing extracts text and generates summary
4. Document metadata stored in database
5. Control room approves and assigns roles
6. Documents distributed via role-based endpoints

### Adding New Features

1. **New API Endpoints**: Add to `main.py`
2. **Database Changes**: Update `models.py` and `schema.py`
3. **Business Logic**: Add to `crud.py` or service modules
4. **AI Features**: Extend `services/document_processor.py`

---

## 🗺️ Future Roadmap

### Phase 1: Enhanced AI Capabilities
- [ ] Multiple summarization models (BART, T5, GPT)
- [ ] Document classification by type
- [ ] Sentiment analysis for passenger feedback
- [ ] Multi-language summarization

### Phase 2: Advanced Features
- [ ] Real-time WebSocket notifications
- [ ] Advanced search with Elasticsearch
- [ ] User authentication & authorization
- [ ] File versioning and history

### Phase 3: Enterprise Features
- [ ] Audit trail and compliance reporting
- [ ] Integration with external systems
- [ ] Advanced analytics dashboard
- [ ] Mobile-optimized APIs

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. "Can't reach this page" when accessing server
**Problem**: Using wrong URL
**Solution**: Use `http://localhost:8000` instead of `http://0.0.0.0:8000`

#### 2. Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check virtual environment
python -c "import fastapi; print('OK')"
```

#### 3. Database Connection Issues
```bash
# Recreate database
rm database.db
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

#### 4. File Upload Failures
- Check `data/uploads/` directory permissions
- Verify file size limits
- Check disk space

#### 5. Background Processing Not Working
- Check server logs for error messages
- Verify Hugging Face API key in `.env`
- Test with immediate processing as fallback

### Debug Mode
Enable detailed logging by adding debug prints to `process_document` function:
```python
def process_document(doc_id: int, file_path: str):
    print(f"DEBUG: Processing document {doc_id}")
    # ... rest of function
```

---

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- Follow PEP 8 Python style guide
- Include docstrings for all functions
- Add tests for new features
- Update documentation for API changes

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For support, email your team or create an issue in the project repository.

**Happy Coding! 🚀**

---

*Last Updated: September 2025*  
*Version: 1.0.0*  
*Built with ❤️ for KMRL during Smart India Hackathon*
