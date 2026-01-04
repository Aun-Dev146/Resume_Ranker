# backend/app/text_extract.py
import os
from pathlib import Path
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document as DocxDocument


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    try:
        text = pdf_extract_text(file_path)
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file_path: Path to DOCX file
        
    Returns:
        Extracted text content
    """
    try:
        doc = DocxDocument(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_text(file_path: str) -> str:
    """
    Extract text from file based on extension
    
    Args:
        file_path: Path to file
        
    Returns:
        Extracted text content
        
    Raises:
        ValueError: If file format is not supported
    """
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
 
