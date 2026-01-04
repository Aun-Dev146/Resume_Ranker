# DEPLOYMENT.md

# Deployment Guide for Resume Ranker

## Local Development Setup

### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd Resume_Ranker

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.db import init_db; init_db()"

# Run server
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run streamlit_app.py
```

---

## Docker Deployment

### Quick Start

```bash
docker-compose up --build
```

Access:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- Docs: http://localhost:8000/docs

### Production Deployment

1. **Update docker-compose.yml** for production:

```yaml
services:
  backend:
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/resumes
  frontend:
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
```

2. **Use a reverse proxy** (Nginx):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://frontend:8501;
        proxy_set_header Host $host;
    }
}
```

3. **Use managed database** (PostgreSQL):

```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@db-host:5432/resume_ranker
```

---

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `DATABASE_URL` (PostgreSQL)
- [ ] Use environment-specific `.env` files
- [ ] Setup SSL/TLS certificates
- [ ] Configure CORS origins properly
- [ ] Setup logging and monitoring
- [ ] Backup database regularly
- [ ] Scale backend with load balancer
- [ ] Setup automated health checks
- [ ] Configure rate limiting

---

## Database Migration to PostgreSQL

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/resume_ranker

# Initialize database (models will be created automatically)
python -c "from app.db import init_db; init_db()"
```

---

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

```bash
curl http://localhost:8000/health
```

---

## Scaling Considerations

1. **Horizontal Scaling**: Use multiple backend instances behind a load balancer
2. **Caching**: Add Redis for caching embeddings
3. **Vector Database**: Consider Milvus or Pinecone for large-scale vector search
4. **Async Processing**: Use Celery for background ranking tasks

---

## Troubleshooting

### Port Conflicts
```bash
# Find process using port 8000
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

### Database Issues
```bash
# Reset database
rm resumes.db

# Reinitialize
python -c "from app.db import init_db; init_db()"
```

### Memory Issues
- Reduce batch size in embeddings
- Use smaller embedding model
- Implement pagination for large result sets

---

## Performance Optimization

### 1. Embedding Optimization
```python
# Use GPU if available
import torch
if torch.cuda.is_available():
    MODEL_DEVICE = "cuda"
else:
    MODEL_DEVICE = "cpu"
```

### 2. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_embedding(text: str):
    return embedder.embed_text(text)
```

### 3. Database Indexing
```python
# Create index on frequently queried columns
Index('idx_resume_id', Resume.id)
Index('idx_job_id', JobDescription.id)
```

---

## Backup & Recovery

### Database Backup
```bash
# SQLite
cp resumes.db resumes.db.backup

# PostgreSQL
pg_dump resume_ranker > backup.sql
```

### Restore
```bash
# PostgreSQL
psql resume_ranker < backup.sql
```

---

## CI/CD Pipeline

Example GitHub Actions workflow:

```yaml
name: Tests & Deploy

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r backend/requirements.txt
          python backend/tests/test_embeddings.py
      
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          docker-compose up -d
```

---

## Support

For issues or questions, please refer to README.md or create an issue on GitHub.
