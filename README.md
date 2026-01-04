# Resume Ranker 📄

An AI-powered resume ranking system that uses semantic similarity matching to rank resumes against job descriptions.

## Features ✨

- **Document Upload**: Support for PDF and DOCX resume files
- **Job Description Management**: Upload job descriptions as text or files
- **AI Embeddings**: Uses sentence-transformers for semantic understanding
- **Ranking System**: Ranks resumes based on semantic similarity to job description
- **Web Interface**: User-friendly Streamlit frontend
- **REST API**: FastAPI backend with full endpoints
- **Database**: SQLAlchemy ORM with SQLite storage
- **Docker Support**: Fully containerized with Docker Compose

## Architecture 🏗️

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                     │
│         - Upload Resumes & Job Descriptions                │
│         - Rank & View Results                              │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP Requests
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│  - REST API Endpoints                                       │
│  - Text Extraction (PDF/DOCX)                              │
│  - Embeddings Generation                                    │
│  - Similarity Scoring                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │ Database ORM
                  ▼
┌─────────────────────────────────────────────────────────────┐
│            Database (SQLite / SQLAlchemy)                   │
│  - Resumes Table                                            │
│  - Job Descriptions Table                                   │
│  - Ranking Results Table                                    │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack 🛠️

- **Backend**: FastAPI, uvicorn, SQLAlchemy
- **Frontend**: Streamlit, Pandas
- **AI/ML**: sentence-transformers, scikit-learn, numpy
- **Document Processing**: python-docx, pdfminer.six
- **Database**: SQLite (default), supports PostgreSQL
- **Infrastructure**: Docker, Docker Compose

## Installation & Setup 🚀

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
cd Resume_Ranker

# Build and start services
docker-compose up --build

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run streamlit_app.py
```

## API Endpoints 📡

### Resume Management
- `POST /upload-resume` - Upload a resume file
- `GET /resumes` - List all resumes
- `DELETE /resume/{resume_id}` - Delete a resume

### Job Description Management
- `POST /upload-job-description` - Upload job description
- `GET /jobs` - List all job descriptions
- `DELETE /job/{job_id}` - Delete a job description

### Ranking
- `POST /rank-resumes` - Rank all resumes against a job
- `GET /results` - Get ranking results

### Health & Info
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation

## Usage Guide 📖

### Step 1: Upload Resumes
1. Go to the "Upload" tab
2. Click "Choose resume files"
3. Select one or more PDF/DOCX files
4. Enter candidate names (optional)
5. Files will be automatically processed

### Step 2: Upload Job Description
1. In the "Upload" tab, enter:
   - Job Title
   - Company (optional)
   - Job Description (text) OR upload a file
2. Click "Upload Job Description"

### Step 3: Rank Resumes
1. Go to the "Rank" tab
2. Click "Start Ranking"
3. View results as a sorted table with scores

### Step 4: View Results
1. Go to the "Results" tab
2. View score distribution and statistics
3. Download results as CSV

## Project Structure 📂

```
Resume_Ranker/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api.py               # API endpoints
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── db.py                # Database setup
│   │   ├── embeddings.py        # Embedding generation
│   │   ├── text_extract.py      # PDF/DOCX extraction
│   │   └── utils.py             # Utility functions
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Docker image for backend
│   └── tests/                   # Test files
├── frontend/
│   ├── streamlit_app.py         # Streamlit UI
│   ├── requirements.txt         # Frontend dependencies
│   └── Dockerfile               # Docker image for frontend
├── scripts/
│   └── test_embedding.py        # Embedding test script
├── docker-compose.yml           # Multi-container orchestration
└── README.md                    # This file
```

## File Descriptions 📝

### Backend Files

**models.py** - Database Models
- `Resume`: Stores resume documents with content
- `JobDescription`: Stores job posting details
- `RankingResult`: Stores similarity scores and rankings

**db.py** - Database Configuration
- SQLAlchemy engine and session setup
- Database initialization
- Dependency injection for sessions

**api.py** - REST API Endpoints
- File upload handling
- Text extraction integration
- Ranking calculation and storage
- Result retrieval endpoints

**main.py** - FastAPI Application
- App initialization
- CORS configuration
- Route registration
- Health checks

**embeddings.py** - AI Embeddings
- Loads sentence-transformers model (all-MiniLM-L6-v2)
- Converts text to embeddings
- L2 normalization for cosine similarity

**text_extract.py** - Document Processing
- PDF text extraction
- DOCX text extraction
- File format validation

**utils.py** - Helper Functions
- Text preprocessing
- Score formatting
- Percentile calculation
- File validation

### Frontend Files

**streamlit_app.py** - User Interface
- Three-tab interface (Upload, Rank, Results)
- File upload widgets
- Results visualization with charts
- CSV export functionality

## Configuration 🔧

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///./resumes.db

# API
API_BASE_URL=http://localhost:8000

# Model
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Model Selection

To use different embedding models, edit `backend/app/embeddings.py`:

```python
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"  # Larger, more accurate
# or
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"   # Smaller, faster
```

## Performance Considerations ⚡

- **Embedding Model**: all-MiniLM-L6-v2 is CPU-friendly (~22MB)
- **Batch Processing**: Embeddings are generated on-the-fly
- **Database**: SQLite for development, PostgreSQL for production
- **Vector Search**: Uses cosine similarity (dot product of L2-normalized vectors)

## Troubleshooting 🐛

### Docker Issues
```bash
# Remove containers and volumes
docker-compose down -v

# Rebuild images
docker-compose up --build
```

### API Connection Issues
- Ensure backend is running on port 8000
- Check firewall settings
- Verify API URL in frontend config

### File Upload Issues
- Ensure file format is PDF or DOCX
- Check file permissions
- Verify disk space

## Future Enhancements 🚀

- [ ] Advanced filtering and search
- [ ] Multi-language support
- [ ] Custom embedding models
- [ ] Batch processing
- [ ] User authentication
- [ ] Advanced analytics dashboard
- [ ] Resume parsing and skill extraction
- [ ] Job matching feedback system

## Contributing 🤝

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for resume ranking
 
