#!/usr/bin/env python3
"""
HEIC2TXT - OCR Image to Text Converter

A command-line tool that extracts text from HEIC images using OCR
and saves the results as text files.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

import click
from tqdm import tqdm

from ocr_engines.tesseract_ocr import TesseractOCR
from ocr_engines.easyocr_engine import EasyOCREngine
from ocr_engines.paddle_ocr import PaddleOCREngine
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from utils.image_utils import convert_heic_to_pil, is_heic_file
from utils.text_utils import preprocess_text, save_text_to_file


class HEIC2TXT:
    """Main class for HEIC to text conversion."""
    
    def __init__(self, engine: str = "tesseract", language: str = "eng", 
                 preprocess: bool = False, verbose: bool = False, custom_words: List[str] = None):
        """
        Initialize the HEIC2TXT converter.
        
        Args:
            engine: OCR engine to use ('tesseract', 'easyocr', 'paddleocr', or 'apple_vision')
            language: Language code for OCR
            preprocess: Whether to preprocess extracted text
            verbose: Enable verbose output
            custom_words: List of custom words to improve recognition (Apple Vision only)
        """
        self.engine = engine
        self.language = language
        self.preprocess = preprocess
        self.verbose = verbose
        self.custom_words = custom_words
        
        # Initialize OCR engine
        if engine == "easyocr":
            self.ocr = EasyOCREngine(language=language)
        elif engine == "tesseract":
            self.ocr = TesseractOCR(language=language)
        elif engine == "paddleocr":
            self.ocr = PaddleOCREngine(language=language)
        elif engine == "apple_vision":
            self.ocr = AppleVisionOCREngine(language=language, custom_words=custom_words)
        else:
            raise ValueError(f"Unsupported OCR engine: {engine}")
    
    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """
        Convert a single HEIC file to text.
        
        Args:
            input_path: Path to input HEIC file
            output_path: Path to output text file (optional)
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            if not is_heic_file(input_path):
                print(f"Warning: {input_path} is not a HEIC file")
                return False
            
            if self.verbose:
                print(f"Processing: {input_path}")
            
            # Convert HEIC to PIL Image
            image = convert_heic_to_pil(input_path)
            if image is None:
                print(f"Error: Could not convert {input_path}")
                return False
            
            # Extract text using OCR
            text = self.ocr.extract_text(image)
            if not text.strip():
                print(f"Warning: No text found in {input_path}")
                return False
            
            # Preprocess text if requested
            if self.preprocess:
                text = preprocess_text(text)
            
            # Determine output path
            if output_path is None:
                input_file = Path(input_path)
                output_path = input_file.with_suffix('.txt')
            
            # Save text to file
            success = save_text_to_file(text, output_path)
            if success and self.verbose:
                print(f"Saved text to: {output_path}")
            
            return success
            
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}")
            return False
    
    def convert_batch(self, input_dir: str, output_dir: str) -> None:
        """
        Convert all HEIC files in a directory.
        
        Args:
            input_dir: Directory containing HEIC files
            output_dir: Directory to save text files
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            print(f"Error: Input directory {input_dir} does not exist")
            return
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all HEIC files
        heic_files = list(input_path.glob("*.heic")) + list(input_path.glob("*.HEIC"))
        
        if not heic_files:
            print(f"No HEIC files found in {input_dir}")
            return
        
        print(f"Found {len(heic_files)} HEIC files to process")
        
        # Process files with progress bar
        successful = 0
        for heic_file in tqdm(heic_files, desc="Converting HEIC files"):
            output_file = output_path / f"{heic_file.stem}.txt"
            if self.convert_file(str(heic_file), str(output_file)):
                successful += 1
        
        print(f"Successfully converted {successful}/{len(heic_files)} files")


@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('--batch', '-b', type=click.Path(exists=True), 
              help='Batch process all HEIC files in directory')
@click.option('--output', '-o', type=click.Path(), 
              help='Output directory or file path')
@click.option('--engine', '-e', type=click.Choice(['tesseract', 'easyocr']), 
              default='tesseract', help='OCR engine to use')
@click.option('--language', '-l', default='eng', 
              help='Language code for OCR (e.g., eng, spa, fra)')
@click.option('--preprocess', '-p', is_flag=True, 
              help='Preprocess extracted text')
@click.option('--verbose', '-v', is_flag=True, 
              help='Enable verbose output')
def main(input_files, batch, output, engine, language, preprocess, verbose):
    """
    HEIC2TXT - Convert HEIC images to text using OCR.
    
    Examples:
        heic2txt.py image.heic
        heic2txt.py *.heic --output ./text_files/
        heic2txt.py --batch ./images/ --output ./text_files/
    """
    if not input_files and not batch:
        click.echo("Error: Please provide input files or use --batch option")
        sys.exit(1)
    
    # Initialize converter
    converter = HEIC2TXT(
        engine=engine,
        language=language,
        preprocess=preprocess,
        verbose=verbose
    )
    
    if batch:
        # Batch processing
        if not output:
            output = batch
        converter.convert_batch(batch, output)
    else:
        # Single file processing
        for input_file in input_files:
            converter.convert_file(input_file, output)


if __name__ == "__main__":
    main()
