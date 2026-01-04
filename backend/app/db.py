# backend/app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base

# Database URL - using SQLite by default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resumes.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Dependency injection for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
