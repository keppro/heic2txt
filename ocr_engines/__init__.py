"""OCR engines package for HEIC2TXT."""

from .tesseract_ocr import TesseractOCR
from .easyocr_engine import EasyOCREngine

__all__ = ['TesseractOCR', 'EasyOCREngine']
