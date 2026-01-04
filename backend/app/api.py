# backend/app/api.py
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import numpy as np

from .db import get_db
from .models import Resume, JobDescription, RankingResult
from .embeddings import Embedder
from .text_extract import extract_text
from .utils import validate_file_extension, truncate_text

router = APIRouter()
embedder = Embedder()

# Store current job description ID for ranking
current_job_id = None


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    candidate_name: str = None,
    db: Session = Depends(get_db)
):
    """
    Upload and process a resume file (PDF or DOCX)
    """
    # Validate file extension
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Only PDF and DOCX are supported."
        )
    
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
        
        # Extract text
        resume_text = extract_text(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Save to database
        resume = Resume(
            filename=file.filename,
            candidate_name=candidate_name or file.filename.split('.')[0],
            content=resume_text
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {
            "id": resume.id,
            "filename": resume.filename,
            "candidate_name": resume.candidate_name,
            "preview": truncate_text(resume_text, 200)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload-job-description")
async def upload_job_description(
    job_title: str,
    company: str = None,
    content: str = None,
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Upload job description either as text or file
    """
    global current_job_id
    
    job_content = content
    
    # If file is provided, extract text from it
    if file:
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Only PDF and DOCX are supported."
            )
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
                contents = await file.read()
                tmp.write(contents)
                tmp_path = tmp.name
            
            job_content = extract_text(tmp_path)
            os.unlink(tmp_path)
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    if not job_content:
        raise HTTPException(status_code=400, detail="Job description content is required")
    
    try:
        # Save to database
        job = JobDescription(
            job_title=job_title,
            company=company,
            content=job_content
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        current_job_id = job.id
        
        return {
            "id": job.id,
            "job_title": job.job_title,
            "company": job.company,
            "preview": truncate_text(job_content, 200)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rank-resumes")
async def rank_resumes(job_id: int = None, db: Session = Depends(get_db)):
    """
    Rank all resumes against a job description
    """
    job_id = job_id or current_job_id
    
    if not job_id:
        raise HTTPException(status_code=400, detail="Job description ID is required")
    
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Get all resumes
    resumes = db.query(Resume).all()
    if not resumes:
        raise HTTPException(status_code=404, detail="No resumes found")
    
    # Generate embeddings
    job_embedding = embedder.embed_text(job.content)[0]
    
    results = []
    scores = []
    
    for resume in resumes:
        resume_embedding = embedder.embed_text(resume.content)[0]
        similarity_score = float(np.dot(job_embedding, resume_embedding))
        scores.append(similarity_score)
        
        results.append({
            "resume_id": resume.id,
            "candidate_name": resume.candidate_name,
            "filename": resume.filename,
            "similarity_score": similarity_score
        })
    
    # Sort by score descending and add ranks
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    # Delete existing results for this job
    db.query(RankingResult).filter(RankingResult.job_id == job_id).delete()
    
    # Save ranking results to database
    for rank, result in enumerate(results, 1):
        ranking = RankingResult(
            resume_id=result["resume_id"],
            job_id=job_id,
            similarity_score=result["similarity_score"],
            rank=rank
        )
        db.add(ranking)
        result["rank"] = rank
    
    db.commit()
    
    return {
        "job_id": job_id,
        "job_title": job.job_title,
        "total_resumes": len(results),
        "rankings": results
    }


@router.get("/results")
async def get_results(job_id: int = None, db: Session = Depends(get_db)):
    """
    Get ranking results for a specific job
    """
    job_id = job_id or current_job_id
    
    if not job_id:
        raise HTTPException(status_code=400, detail="Job description ID is required")
    
    results = db.query(RankingResult).filter(
        RankingResult.job_id == job_id
    ).order_by(RankingResult.rank).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No ranking results found")
    
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    
    return {
        "job_id": job_id,
        "job_title": job.job_title,
        "total_results": len(results),
        "rankings": [
            {
                "rank": r.rank,
                "resume_id": r.resume_id,
                "similarity_score": r.similarity_score
            }
            for r in results
        ]
    }


@router.get("/resumes")
async def list_resumes(db: Session = Depends(get_db)):
    """
    List all uploaded resumes
    """
    resumes = db.query(Resume).all()
    return {
        "total": len(resumes),
        "resumes": [
            {
                "id": r.id,
                "filename": r.filename,
                "candidate_name": r.candidate_name,
                "created_at": r.created_at
            }
            for r in resumes
        ]
    }


@router.get("/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    """
    List all job descriptions
    """
    jobs = db.query(JobDescription).all()
    return {
        "total": len(jobs),
        "jobs": [
            {
                "id": j.id,
                "job_title": j.job_title,
                "company": j.company,
                "created_at": j.created_at
            }
            for j in jobs
        ]
    }


@router.delete("/resume/{resume_id}")
async def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Delete a resume
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    db.delete(resume)
    db.commit()
    
    return {"message": "Resume deleted successfully"}


@router.delete("/job/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job description
    """
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Also delete associated ranking results
    db.query(RankingResult).filter(RankingResult.job_id == job_id).delete()
    db.delete(job)
    db.commit()
    
    return {"message": "Job description deleted successfully"}
 
