"""EasyOCR engine implementation."""

import warnings
import os
import easyocr
import numpy as np
import torch
from PIL import Image
from typing import Optional, List, Tuple

# Suppress EasyOCR warnings
warnings.filterwarnings('ignore', category=UserWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class EasyOCREngine:
    """EasyOCR engine for text extraction."""
    
    def __init__(self, language: str = "en", text_threshold: float = 0.7, 
                 low_text: float = 0.5, link_threshold: float = 0.5):
        """
        Initialize EasyOCR engine.
        
        Args:
            language: Language code for OCR (e.g., 'en', 'es', 'fr')
            text_threshold: Text detection confidence threshold
            low_text: Low text detection threshold
            link_threshold: Text linking threshold
        """
        self.language = language
        self.text_threshold = text_threshold
        self.low_text = low_text
        self.link_threshold = link_threshold
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self) -> None:
        """Initialize the EasyOCR reader."""
        try:
            # Convert language code if needed
            lang_code = self._convert_language_code(self.language)
            
            # Detect GPU availability
            use_gpu = self._detect_gpu_availability()
            
            # Set PyTorch device for optimal performance
            if use_gpu:
                if torch.cuda.is_available():
                    torch.set_default_device('cuda')
                    print("🚀 Using CUDA GPU acceleration")
                elif torch.backends.mps.is_available():
                    torch.set_default_device('mps')
                    print("🚀 Using Apple Silicon GPU acceleration (MPS)")
                else:
                    print("⚠️  GPU detected but no compatible backend found, using CPU")
                    use_gpu = False
            else:
                print("💻 Using CPU processing")
            
            self.reader = easyocr.Reader([lang_code], gpu=use_gpu)
            
            # Log the actual device being used
            if hasattr(self.reader, 'device'):
                print(f"🎯 EasyOCR using device: {self.reader.device}")
            else:
                print("🎯 EasyOCR initialized successfully")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize EasyOCR: {str(e)}") from e
    
    def _detect_gpu_availability(self) -> bool:
        """
        Detect if GPU acceleration is available.
        
        Returns:
            True if GPU is available, False otherwise
        """
        # Check for CUDA (NVIDIA GPUs)
        if torch.cuda.is_available():
            return True
        
        # Check for MPS (Apple Silicon GPUs)
        if torch.backends.mps.is_available():
            return True
        
        return False
    
    def _convert_language_code(self, language: str) -> str:
        """
        Convert language code to EasyOCR format.
        
        Args:
            language: Language code (e.g., 'eng' -> 'en')
            
        Returns:
            EasyOCR language code
        """
        # Common language code mappings
        lang_map = {
            'eng': 'en',
            'spa': 'es',
            'fra': 'fr',
            'deu': 'de',
            'ita': 'it',
            'por': 'pt',
            'rus': 'ru',
            'chi_sim': 'ch_sim',
            'chi_tra': 'ch_tra',
            'jpn': 'ja',
            'kor': 'ko'
        }
        
        return lang_map.get(language, language)
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from PIL Image using EasyOCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        try:
            # Convert PIL Image to numpy array
            img_array = np.array(image)
            
            # Extract text with bounding boxes using custom parameters
            results = self.reader.readtext(
                img_array,
                text_threshold=self.text_threshold,
                low_text=self.low_text,
                link_threshold=self.link_threshold
            )
            
            # Combine all text
            text_parts = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Filter low confidence results
                    text_parts.append(text)
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            raise RuntimeError(f"EasyOCR failed: {str(e)}") from e
    
    def extract_text_with_confidence(self, image: Image.Image) -> List[Tuple[str, float]]:
        """
        Extract text with confidence scores.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of tuples (text, confidence)
        """
        try:
            img_array = np.array(image)
            results = self.reader.readtext(
                img_array,
                text_threshold=self.text_threshold,
                low_text=self.low_text,
                link_threshold=self.link_threshold
            )
            
            return [(text, confidence) for (bbox, text, confidence) in results]
            
        except Exception as e:
            raise RuntimeError(f"EasyOCR failed: {str(e)}") from e
