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
        Extract text from PIL Image using Tesseract with optimized parameters.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        try:
            # Preprocess image for better OCR
            processed_image = self._preprocess_image(image)
            
            # Try multiple optimized configurations and pick the best one
            configs = [
                # Configuration 1: Single uniform block - good for documents
                f'--oem 3 --psm 6 -l {self.language}',
                
                # Configuration 2: Automatic page segmentation - good for mixed content
                f'--oem 3 --psm 3 -l {self.language}',
                
                # Configuration 3: Single text line - good for single lines
                f'--oem 3 --psm 13 -l {self.language}',
                
                # Configuration 4: Single word - good for individual words
                f'--oem 3 --psm 8 -l {self.language}',
                
                # Configuration 5: Single character - good for individual characters
                f'--oem 3 --psm 10 -l {self.language}',
                
                # Configuration 6: Sparse text - good for sparse text
                f'--oem 3 --psm 11 -l {self.language}',
                
                # Configuration 7: Raw line - good for raw text lines
                f'--oem 3 --psm 13 -l {self.language}',
            ]
            
            best_text = ""
            best_score = -float('inf')
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config).strip()
                    
                    if not text:
                        continue
                    
                    # Score the text quality based on readability
                    score = self._score_text_quality(text)
                    
                    if score > best_score:
                        best_score = score
                        best_text = text
                        
                except Exception as e:
                    continue
            
            # If no good result found, try with original image
            if not best_text.strip():
                for config in configs[:3]:  # Try first 3 configs with original image
                    try:
                        text = pytesseract.image_to_string(image, config=config).strip()
                        if text:
                            score = self._score_text_quality(text)
                            if score > best_score:
                                best_score = score
                                best_text = text
                    except Exception:
                        continue
            
            return best_text.strip()
            
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR failed: {str(e)}") from e
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image object
        """
        try:
            import cv2
            import numpy as np
            
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply morphological operations to clean up the image
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Convert back to PIL Image
            return Image.fromarray(cleaned)
            
        except ImportError:
            # If OpenCV is not available, return original image
            return image
        except Exception:
            # If preprocessing fails, return original image
            return image
    
    def _score_text_quality(self, text: str) -> float:
        """
        Score text quality based on readability and meaningful content.
        
        Args:
            text: Text to score
            
        Returns:
            Quality score (higher is better)
        """
        if not text.strip():
            return -float('inf')
        
        # Count meaningful characters (letters, numbers, common punctuation)
        meaningful_chars = sum(1 for c in text if c.isalnum() or c in '.,!?;:()[]{}"\'@#$%^&*+-=<>/\\|_~` ')
        
        # Count gibberish characters and symbols
        gibberish_chars = sum(1 for c in text if c in '=|°§±×÷∞≤≥≠≈∑∏∫∂∇∆√∝∈∉⊂⊃∪∩∧∨¬→←↑↓↔↕↖↗↘↙')
        
        # Count special symbols that are often OCR errors
        special_chars = sum(1 for c in text if c in '|°§±×÷∞≤≥≠≈∑∏∫∂∇∆√∝∈∉⊂⊃∪∩∧∨¬→←↑↓↔↕↖↗↘↙')
        
        # Count words (sequences of meaningful characters)
        words = [w for w in text.split() if w.strip() and len(w) > 1 and any(c.isalnum() for c in w)]
        word_count = len(words)
        
        # Count lines with meaningful content
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        meaningful_lines = sum(1 for line in lines if any(c.isalnum() for c in line))
        
        # Calculate base score
        score = meaningful_chars * 1.0
        
        # Heavy penalty for gibberish and special symbols
        score -= gibberish_chars * 5.0
        score -= special_chars * 3.0
        
        # Bonus for having words
        score += word_count * 3.0
        
        # Bonus for meaningful lines
        score += meaningful_lines * 2.0
        
        # Penalty for too many single characters
        single_chars = sum(1 for w in text.split() if len(w.strip()) == 1)
        if single_chars > len(text.split()) * 0.6:  # More than 60% single characters
            score -= single_chars * 2.0
        
        # Penalty for very short text (likely errors)
        if len(text.strip()) < 10:
            score -= 10.0
        
        # Bonus for reasonable text length
        if len(text.strip()) > 50:
            score += 5.0
        
        return score
    
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
