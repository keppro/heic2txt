"""Tests for HEIC2TXT package."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from heic2txt import HEIC2TXT
from utils.image_utils import is_heic_file
from utils.text_utils import preprocess_text, save_text_to_file


class TestHEIC2TXT:
    """Test cases for HEIC2TXT class."""
    
    def test_init_tesseract(self):
        """Test initialization with Tesseract engine."""
        with patch('ocr_engines.tesseract_ocr.TesseractOCR'):
            converter = HEIC2TXT(engine="tesseract", language="eng")
            assert converter.engine == "tesseract"
            assert converter.language == "eng"
    
    def test_init_easyocr(self):
        """Test initialization with EasyOCR engine."""
        with patch('ocr_engines.easyocr_engine.EasyOCREngine'):
            converter = HEIC2TXT(engine="easyocr", language="en")
            assert converter.engine == "easyocr"
            assert converter.language == "en"
    
    def test_init_invalid_engine(self):
        """Test initialization with invalid engine."""
        with pytest.raises(ValueError):
            HEIC2TXT(engine="invalid")
    
    @patch('heic2txt.convert_heic_to_pil')
    @patch('ocr_engines.tesseract_ocr.TesseractOCR')
    def test_convert_file_success(self, mock_ocr, mock_convert, mock_is_heic, mock_save):
        """Test successful file conversion."""
        # Mock image conversion
        mock_image = Mock()
        mock_convert.return_value = mock_image
        
        # Mock OCR
        mock_ocr_instance = Mock()
        mock_ocr_instance.extract_text.return_value = "Sample text"
        mock_ocr.return_value = mock_ocr_instance
        
        # Mock file operations
        mock_is_heic.return_value = True
        mock_save.return_value = True
            
        converter = HEIC2TXT(engine="tesseract")
        result = converter.convert_file("test.heic")
            
        assert result is True
        mock_convert.assert_called_once_with("test.heic")
        mock_ocr_instance.extract_text.assert_called_once_with(mock_image)
    
    @patch('heic2txt.is_heic_file')
    def test_convert_file_not_heic(self, mock_is_heic):
        """Test conversion of non-HEIC file."""
        mock_is_heic.return_value = False
        
        converter = HEIC2TXT(engine="tesseract")
        result = converter.convert_file("test.jpg")
        
        assert result is False


class TestImageUtils:
    """Test cases for image utility functions."""
    
    def test_is_heic_file_valid(self):
        """Test HEIC file detection with valid file."""
        with tempfile.NamedTemporaryFile(suffix='.heic', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            assert is_heic_file(tmp_path) is True
        finally:
            os.unlink(tmp_path)
    
    def test_is_heic_file_invalid_extension(self):
        """Test HEIC file detection with invalid extension."""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            assert is_heic_file(tmp_path) is False
        finally:
            os.unlink(tmp_path)
    
    def test_is_heic_file_nonexistent(self):
        """Test HEIC file detection with nonexistent file."""
        assert is_heic_file("nonexistent.heic") is False


class TestTextUtils:
    """Test cases for text utility functions."""
    
    def test_preprocess_text(self):
        """Test text preprocessing."""
        input_text = "  Hello    world  \n\n\n  Test  "
        expected = "Hello world Test"
        result = preprocess_text(input_text)
        assert result == expected
    
    def test_preprocess_empty_text(self):
        """Test preprocessing of empty text."""
        assert preprocess_text("") == ""
        assert preprocess_text(None) is None
    
    def test_save_text_to_file(self):
        """Test saving text to file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "test.txt")
            text = "Sample text content"
            
            result = save_text_to_file(text, output_path)


if __name__ == "__main__":
    pytest.main([__file__])
