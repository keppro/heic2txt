#!/usr/bin/env python3
"""
PaddleOCR engine for text extraction.
"""

import warnings
warnings.filterwarnings('ignore')

try:
    from paddleocr import PaddleOCR
    import torch
    import numpy as np
    from PIL import Image
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False

class PaddleOCREngine:
    """PaddleOCR engine for text extraction."""
    
    def __init__(self, language: str = "en"):
        """
        Initialize PaddleOCR engine.
        
        Args:
            language: Language code for OCR (e.g., 'en', 'es', 'fr')
        """
        if not PADDLEOCR_AVAILABLE:
            raise RuntimeError("PaddleOCR is not installed. Please install it with: pip install paddlepaddle paddleocr")
        
        self.language = language
        self.ocr = None
        self._initialize_ocr()
    
    def _initialize_ocr(self) -> None:
        """Initialize the PaddleOCR engine."""
        try:
            # Convert language code if needed
            lang_code = self._convert_language_code(self.language)
            
            # Detect GPU availability
            use_gpu = self._detect_gpu_availability()
            
            # Initialize PaddleOCR
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=lang_code,
                text_det_limit_side_len=4000,  # Set to our max size to prevent internal resizing
                text_det_limit_type='max'      # Use max side length limit
            )
            
            if use_gpu:
                print("🚀 Using GPU acceleration for PaddleOCR")
            else:
                print("💻 Using CPU processing for PaddleOCR")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize PaddleOCR: {str(e)}") from e
    
    def _detect_gpu_availability(self) -> bool:
        """
        Detect if GPU acceleration is available for PaddlePaddle.
        
        Returns:
            True if GPU is available, False otherwise
        """
        try:
            import paddle
            # Check if PaddlePaddle is compiled with CUDA support
            if paddle.is_compiled_with_cuda():
                print("🚀 PaddlePaddle compiled with CUDA support")
                return True
            
            # Check if PaddlePaddle supports MPS (Apple Silicon)
            if hasattr(paddle, 'is_compiled_with_mps') and paddle.is_compiled_with_mps():
                print("🚀 PaddlePaddle compiled with MPS support")
                return True
            
            # Check available devices
            available_devices = paddle.get_device()
            if 'gpu' in available_devices.lower() or 'mps' in available_devices.lower():
                print(f"🚀 GPU device available: {available_devices}")
                return True
                
        except Exception as e:
            print(f"⚠️  Error detecting GPU: {e}")
        
        print("💻 PaddlePaddle is CPU-only (no GPU support available)")
        return False
    
    def _convert_language_code(self, language: str) -> str:
        """
        Convert language code to PaddleOCR format.
        
        Args:
            language: Language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            PaddleOCR language code
        """
        # PaddleOCR uses different language codes
        lang_map = {
            'en': 'en',
            'es': 'es',
            'fr': 'fr',
            'de': 'german',
            'it': 'it',
            'pt': 'pt',
            'ru': 'ru',
            'ja': 'japan',
            'ko': 'korean',
            'zh': 'ch',
            'chinese': 'ch'
        }
        
        return lang_map.get(language.lower(), 'en')
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from PIL Image using PaddleOCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        try:
            # Convert PIL Image to numpy array
            img_array = np.array(image)
            
            # Extract text with bounding boxes
            results = self.ocr.ocr(img_array)
            
            # Combine all text
            text_parts = []
            if results and results[0]:
                for line in results[0]:
                    if line and len(line) >= 2:
                        text = line[1][0]  # Extract text from result
                        confidence = line[1][1]  # Extract confidence
                        if confidence > 0.5:  # Filter low confidence results
                            text_parts.append(text)
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            raise RuntimeError(f"PaddleOCR failed: {str(e)}") from e
