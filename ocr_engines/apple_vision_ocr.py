#!/usr/bin/env python3
"""
Apple Vision OCR Engine

This module provides OCR functionality using Apple's Vision framework
via PyObjC bindings.
"""

import os
import tempfile
from typing import List, Tuple, Optional
from PIL import Image
import objc
from Vision import VNRecognizeTextRequest, VNImageRequestHandler
from Foundation import NSData, NSURL


class AppleVisionOCREngine:
    """
    Apple Vision OCR Engine implementation using PyObjC.
    
    This implementation uses Apple's native Vision framework for OCR,
    which provides high-quality text recognition on macOS.
    """
    
    def __init__(self, language: str = "en", custom_words: List[str] = None):
        """
        Initialize the Apple Vision OCR engine.
        
        Args:
            language: Language code for OCR (e.g., 'en', 'es', 'fr')
            custom_words: List of custom words to improve recognition accuracy
        """
        self.language = language
        self.custom_words = custom_words or []
        self.engine_name = "Apple Vision"
        print(f"🔍 Initializing {self.engine_name} OCR engine (language: {language})")
        if self.custom_words:
            print(f"📝 Using {len(self.custom_words)} custom words for improved recognition")
        
        # Configure the text recognition request with optimized parameters
        self.text_request = VNRecognizeTextRequest.alloc().init()
        self.text_request.setRecognitionLevel_(0)  # VNRequestTextRecognitionLevelFast (optimized)
        self.text_request.setUsesLanguageCorrection_(False)  # Optimized: False works better
        self.text_request.setMinimumTextHeight_(0.02)  # Optimized: 0.02 works best
        self.text_request.setAutomaticallyDetectsLanguage_(True)  # Optimized: Auto-detect works better
        self.text_request.setUsesCPUOnly_(False)  # Enable GPU acceleration
        print("🚀 GPU acceleration enabled")
        
        # Set custom words if provided
        if self.custom_words:
            try:
                # Convert Python list to NSArray
                from Foundation import NSArray
                custom_words_array = NSArray.arrayWithArray_(self.custom_words)
                self.text_request.setCustomWords_(custom_words_array)
                print(f"✅ Set {len(self.custom_words)} custom words")
            except Exception as e:
                print(f"⚠️  Warning: Could not set custom words: {e}")
        
        # Set language if supported
        if language != "en":
            try:
                self.text_request.setRecognitionLanguages_([language])
            except Exception as e:
                print(f"⚠️  Warning: Could not set language to {language}: {e}")
                print("   Falling back to English")
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from an image using Apple Vision.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        print("🔍 Extracting text with Apple Vision OCR...")
        
        try:
            # Convert PIL image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name, 'PNG')
                temp_path = temp_file.name
            
            # Create NSURL from file path
            file_url = NSURL.fileURLWithPath_(temp_path)
            
            # Create image request handler
            request_handler = VNImageRequestHandler.alloc().initWithURL_options_(file_url, None)
            
            # Perform text recognition
            error = None
            success = request_handler.performRequests_error_([self.text_request], error)
            
            if not success:
                print("❌ Apple Vision OCR failed")
                return ""
            
            # Extract text from results
            text_results = self.text_request.results()
            if not text_results:
                print("ℹ️  No text detected in image")
                return ""
            
            # Combine all detected text
            extracted_text = ""
            for observation in text_results:
                if hasattr(observation, 'topCandidates_'):
                    candidates = observation.topCandidates_(1)
                    if candidates and len(candidates) > 0:
                        candidate = candidates[0]
                        if hasattr(candidate, 'string'):
                            extracted_text += candidate.string() + "\n"
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            print(f"✅ Apple Vision OCR extracted {len(extracted_text)} characters")
            return extracted_text.strip()
            
        except Exception as e:
            print(f"❌ Apple Vision OCR error: {e}")
            return ""
    
    def extract_text_fast(self, image: Image.Image) -> str:
        """
        Fast text extraction for orientation testing (no verbose output).
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        
        try:
            # Convert PIL image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name, 'PNG')
                temp_path = temp_file.name
            
            # Create NSURL from file path
            file_url = NSURL.fileURLWithPath_(temp_path)
            
            # Create image request handler
            request_handler = VNImageRequestHandler.alloc().initWithURL_options_(file_url, None)
            
            # Perform text recognition
            error = None
            success = request_handler.performRequests_error_([self.text_request], error)
            
            if not success:
                return ""
            
            # Extract text from results
            text_results = self.text_request.results()
            if not text_results:
                return ""
            
            # Combine all detected text
            extracted_text = ""
            for observation in text_results:
                if hasattr(observation, 'topCandidates_'):
                    candidates = observation.topCandidates_(1)
                    if candidates and len(candidates) > 0:
                        candidate = candidates[0]
                        if hasattr(candidate, 'string'):
                            extracted_text += candidate.string() + "\n"
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return extracted_text.strip()
            
        except Exception as e:
            return ""
    
    def extract_text_with_confidence(self, image: Image.Image) -> List[Tuple[str, float]]:
        """
        Extract text with confidence scores using Apple Vision.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of tuples containing (text, confidence_score)
        """
        print("🔍 Extracting text with confidence using Apple Vision OCR...")
        
        try:
            # Convert PIL image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name, 'PNG')
                temp_path = temp_file.name
            
            # Create NSURL from file path
            file_url = NSURL.fileURLWithPath_(temp_path)
            
            # Create image request handler
            request_handler = VNImageRequestHandler.alloc().initWithURL_options_(file_url, None)
            
            # Perform text recognition
            error = None
            success = request_handler.performRequests_error_([self.text_request], error)
            
            if not success:
                print("❌ Apple Vision OCR failed")
                return []
            
            # Extract text with confidence from results
            text_results = self.text_request.results()
            if not text_results:
                print("ℹ️  No text detected in image")
                return []
            
            # Combine all detected text with confidence scores
            results = []
            for observation in text_results:
                if hasattr(observation, 'topCandidates_'):
                    candidates = observation.topCandidates_(1)
                    if candidates and len(candidates) > 0:
                        candidate = candidates[0]
                        if hasattr(candidate, 'string') and hasattr(candidate, 'confidence'):
                            text = candidate.string()
                            confidence = candidate.confidence()
                            results.append((text, float(confidence)))
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            print(f"✅ Apple Vision OCR extracted {len(results)} text regions")
            return results
            
        except Exception as e:
            print(f"❌ Apple Vision OCR error: {e}")
            return []
    
    def update_custom_words(self, custom_words: List[str]) -> None:
        """
        Update the custom words for improved recognition.
        
        Args:
            custom_words: List of custom words to improve recognition accuracy
        """
        self.custom_words = custom_words
        if self.custom_words:
            try:
                from Foundation import NSArray
                custom_words_array = NSArray.arrayWithArray_(self.custom_words)
                self.text_request.setCustomWords_(custom_words_array)
                print(f"✅ Updated custom words: {len(self.custom_words)} words")
            except Exception as e:
                print(f"⚠️  Warning: Could not update custom words: {e}")
        else:
            try:
                self.text_request.setCustomWords_(None)
                print("✅ Cleared custom words")
            except Exception as e:
                print(f"⚠️  Warning: Could not clear custom words: {e}")
    
    def is_available(self) -> bool:
        """
        Check if Apple Vision OCR is available.
        
        Returns:
            True if available, False otherwise
        """
        try:
            # Test if we can create a basic request
            test_request = VNRecognizeTextRequest.alloc().init()
            return test_request is not None
        except Exception:
            return False