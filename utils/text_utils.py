"""Text utility functions for HEIC2TXT."""

import difflib
import re
from pathlib import Path
from typing import Optional


def preprocess_text(text: str) -> str:
    """
    Preprocess extracted text to improve readability.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Preprocessed text
    """
    if not text:
        return text
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Fix common OCR errors
    text = fix_common_ocr_errors(text)
    
    # Remove excessive line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    return text


def fix_common_ocr_errors(text: str) -> str:
    """
    Fix common OCR recognition errors.
    
    Args:
        text: Text with potential OCR errors
        
    Returns:
        Text with common errors fixed
    """
    # Common character substitutions
    replacements = {
        '0': 'O',  # Zero to O in words
        '1': 'I',  # One to I in words
        '5': 'S',  # Five to S in words
        '8': 'B',  # Eight to B in words
    }
    
    # Apply replacements (be careful not to break numbers)
    for old, new in replacements.items():
        # Only replace if it's part of a word (not standalone)
        text = re.sub(rf'\b{old}\b', new, text)
    
    # Fix common word errors
    word_replacements = {
        'rn': 'm',  # rn often misread as m
        'cl': 'd',  # cl often misread as d
        'vv': 'w',  # vv often misread as w
    }
    
    for old, new in word_replacements.items():
        text = text.replace(old, new)
    
    return text


def save_text_to_file(text: str, output_path: str) -> bool:
    """
    Save text to file.
    
    Args:
        text: Text content to save
        output_path: Path to output file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        output_file = Path(output_path)
        
        # Create parent directories if they don't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write text to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return True
        
    except Exception as e:
        print(f"Error saving text to file {output_path}: {str(e)}")
        return False


def save_text_to_markdown(text: str, output_path: str, title: str = None) -> bool:
    """
    Save text to Markdown file with optional title.
    
    Args:
        text: Text content to save
        output_path: Path to output Markdown file
        title: Optional title for the document
        
    Returns:
        True if successful, False otherwise
    """
    try:
        output_file = Path(output_path)
        
        # Create parent directories if they don't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare markdown content
        markdown_content = ""
        if title:
            markdown_content += f"# {title}\n\n"
        
        markdown_content += text
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return True
        
    except Exception as e:
        print(f"Error saving text to Markdown file {output_path}: {str(e)}")
        return False


def clean_text_for_ocr(text: str) -> str:
    """
    Clean text specifically for OCR processing.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return text
    
    # Remove special characters that might confuse OCR
    text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts using multiple methods.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
        
    Returns:
        Similarity score as percentage (0-100)
    """
    if not text1 and not text2:
        return 100.0
    if not text1 or not text2:
        return 0.0
    
    # Normalize texts for comparison
    text1_norm = normalize_text_for_comparison(text1)
    text2_norm = normalize_text_for_comparison(text2)
    
    if text1_norm == text2_norm:
        return 100.0
    
    # Calculate similarity using difflib
    similarity = difflib.SequenceMatcher(None, text1_norm, text2_norm).ratio()
    
    # Convert to percentage
    return similarity * 100.0


def normalize_text_for_comparison(text: str) -> str:
    """
    Normalize text for comparison by removing extra whitespace and converting to lowercase.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text
