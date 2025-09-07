"""Tesseract OCR engine implementation."""

import pytesseract
from PIL import Image
from typing import Optional


class TesseractOCR:
    """Tesseract OCR engine for text extraction."""
    
    def __init__(self, language: str = "eng"):
        """
        Initialize Tesseract OCR engine.
        
        Args:
            language: Language code for OCR (e.g., 'eng', 'spa', 'fra')
        """
        self.language = language
        self._validate_tesseract()
    
    def _validate_tesseract(self) -> None:
        """Validate that Tesseract is installed and accessible."""
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(
                "Tesseract OCR is not installed or not in PATH. "
                "Please install it from https://github.com/tesseract-ocr/tesseract"
            ) from e
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from PIL Image using Tesseract.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        try:
            # Configure Tesseract options
            config = f'--oem 3 --psm 6 -l {self.language}'
            
            # Extract text
            text = pytesseract.image_to_string(image, config=config)
            
            return text.strip()
            
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR failed: {str(e)}") from e
    
    def get_available_languages(self) -> list:
        """
        Get list of available languages for Tesseract.
        
        Returns:
            List of available language codes
        """
        try:
            return pytesseract.get_languages()
        except Exception:
            return ['eng']  # Default to English if detection fails
