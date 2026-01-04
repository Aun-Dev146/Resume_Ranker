# backend/app/utils.py
import re
from typing import List


def preprocess_text(text: str) -> str:
    """
    Preprocess text by cleaning and normalizing
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove special characters but keep basic punctuation
    text = text.strip()
    return text


def calculate_percentile(score: float, all_scores: List[float]) -> float:
    """
    Calculate percentile ranking for a score
    
    Args:
        score: The score to rank
        all_scores: List of all scores
        
    Returns:
        Percentile rank (0-100)
    """
    if not all_scores:
        return 0.0
    
    sorted_scores = sorted(all_scores)
    position = sum(1 for s in sorted_scores if s < score)
    percentile = (position / len(all_scores)) * 100
    return round(percentile, 2)


def format_score(score: float) -> str:
    """
    Format score for display
    
    Args:
        score: Numerical score
        
    Returns:
        Formatted score string
    """
    return f"{score:.4f}" if isinstance(score, float) else str(score)


def validate_file_extension(filename: str) -> bool:
    """
    Validate if file has supported extension
    
    Args:
        filename: Name of file
        
    Returns:
        True if extension is supported
    """
    supported_extensions = [".pdf", ".docx"]
    return any(filename.lower().endswith(ext) for ext in supported_extensions)


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
 
