# Quick Start Guide for Resume Ranker

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Or Python 3.11+ for local development

### Option 1: Docker (Fastest Way)

#### Windows:
```bash
cd Resume_Ranker
start.bat
```

#### Linux/Mac:
```bash
cd Resume_Ranker
chmod +x start.sh
./start.sh
```

Then open:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

### Option 2: Local Development

#### Start Backend:
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

#### Start Frontend (new terminal):
```bash
cd frontend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 📖 How to Use

1. **Upload Resumes**
   - Click "Upload" tab
   - Select PDF/DOCX resume files
   - Enter candidate names (optional)

2. **Upload Job Description**
   - Enter job title & company
   - Paste job description or upload file
   - Click "Upload Job Description"

3. **Rank Resumes**
   - Click "Rank" tab
   - Click "Start Ranking"
   - View results sorted by similarity score

4. **Download Results**
   - Click "Results" tab
   - View charts and statistics
   - Download as CSV

---

## 🔧 Troubleshooting

**Port already in use:**
```bash
# Change ports in docker-compose.yml
# Or kill the process using the port
```

**Docker issues:**
```bash
# Clean up
docker-compose down -v
docker-compose up --build
```

**Backend not responding:**
- Check if backend container is running: `docker ps`
- View logs: `docker logs resume-ranker-backend`

---

## 📊 API Examples

### Upload Resume:
```bash
curl -X POST "http://localhost:8000/upload-resume" \
  -F "file=@resume.pdf" \
  -F "candidate_name=John Doe"
```

### Upload Job Description:
```bash
curl -X POST "http://localhost:8000/upload-job-description" \
  -F "job_title=Senior Developer" \
  -F "company=Tech Corp" \
  -F "content=Job description text..."
```

### Rank Resumes:
```bash
curl -X POST "http://localhost:8000/rank-resumes" \
  -F "job_id=1"
```

### Get Results:
```bash
curl -X GET "http://localhost:8000/results?job_id=1"
```

---

## 📚 Documentation

Full documentation is in `README.md`

---

Need help? Check the logs or open an issue!
