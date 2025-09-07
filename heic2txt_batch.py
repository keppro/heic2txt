#!/usr/bin/env python3
"""
HEIC2TXT Batch Processor with HEIC Conversion, Auto-Rotation, Image Preprocessing, and OCR Engine Comparison

A comprehensive wrapper script that converts HEIC files to PNG using macOS sips,
preprocesses images with color inversion and thresholding, then processes them with OCR
to extract text with automatic orientation detection and comparison between different OCR engines.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def convert_heic_to_png(heic_path: str, png_path: str) -> bool:
    """
    Convert HEIC file to PNG using macOS sips command.
    
    Args:
        heic_path: Path to input HEIC file
        png_path: Path to output PNG file
        
    Returns:
        True if conversion successful, False otherwise
    """
    try:
        result = subprocess.run([
            'sips', '-s', 'format', 'png', heic_path, '--out', png_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(png_path):
            return True
        else:
            print(f"❌ sips conversion failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ sips conversion timed out for {heic_path}")
        return False
    except Exception as e:
        print(f"❌ sips conversion error: {e}")
        return False

def preprocess_image_for_ocr(png_path: str, output_dir: str = None, save_images: bool = False) -> str:
    """
    Preprocess PNG image for better OCR results with color inversion and thresholding.
    
    Args:
        png_path: Path to input PNG file
        
    Returns:
        Path to preprocessed PNG file
    print(f"🔄 Starting preprocessing for {png_path}")
    """
    try:
        from PIL import Image, ImageOps
        import cv2
        import numpy as np
        import os
        
        # Load the image
        img = Image.open(png_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to OpenCV format
        img_array = np.array(img)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Step 1: Invert colors (white → black, black → white)
        print(f"🔄 Inverting colors...")
        inverted = cv2.bitwise_not(gray)
        
        # Step 2: Apply adaptive thresholding for clean monochrome
        print(f"🔄 Applying thresholding...")
        # Use adaptive thresholding to handle varying lighting
        thresh = cv2.adaptiveThreshold(
            inverted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Step 3: Apply morphological operations to clean up noise
        print(f"🔄 Cleaning up noise...")
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Step 4: Optional - apply additional noise reduction
        # Remove small noise using opening operation
        kernel_small = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel_small)
        
        # Convert back to PIL Image
        processed_img = Image.fromarray(cleaned)
        
        # Save preprocessed image
        base_name = os.path.splitext(png_path)[0]
        preprocessed_path = f"{base_name}_preprocessed.png"
        processed_img.save(preprocessed_path)
        # Also save to output directory if provided
        if output_dir and save_images:
            preprocessed_save_path = os.path.join(output_dir, f"{os.path.basename(base_name)}_preprocessed.png")
            processed_img.save(preprocessed_save_path)
            print(f"💾 Saved preprocessed image to output directory: {os.path.basename(preprocessed_save_path)}")
        
        print(f"✅ Image preprocessed and saved to {os.path.basename(preprocessed_path)}")
        return preprocessed_path
        
    except ImportError:
        print(f"⚠️  OpenCV not available, skipping preprocessing")
        return png_path
    except Exception as e:
        print(f"⚠️  Preprocessing failed: {e}, using original image")
        return png_path

def detect_text_orientation(png_path: str, engine: str = 'easyocr', language: str = 'en') -> int:
    """
    Detect the best orientation for text in the image by trying all 4 rotations.
    
    Args:
        png_path: Path to PNG file
        engine: OCR engine to use
        language: Language code for OCR
        
    Returns:
        Best rotation angle (0, 90, 180, 270)
    """
    try:
        from heic2txt import HEIC2TXT
        from PIL import Image
        
        # Create converter
        converter = HEIC2TXT(engine=engine, language=language)
        
        # Load image
        img = Image.open(png_path)
        
        best_angle = 0
        best_text_length = 0
        
        print(f"🔄 Testing orientations: 0°, 90°, 180°, 270°...")
        
        # Try all 4 orientations
        for angle in [0, 90, 180, 270]:
            try:
                # Rotate image
                rotated_img = img.rotate(-angle, expand=True)
                
                # Extract text
                text = converter.ocr.extract_text(rotated_img)
                
                # Count meaningful characters (letters, numbers, spaces)
                meaningful_chars = sum(1 for c in text if c.isalnum() or c.isspace())
                
                print(f"   {angle}°: {meaningful_chars} meaningful characters")
                
                if meaningful_chars > best_text_length:
                    best_text_length = meaningful_chars
                    best_angle = angle
                    
            except Exception as e:
                print(f"   {angle}°: Error - {e}")
                continue
        
        print(f"🎯 Best orientation: {best_angle}° ({best_text_length} characters)")
        return best_angle
        
    except Exception as e:
        print(f"⚠️  Orientation detection failed: {e}")
        return 0

def extract_text_from_png(png_path: str, engine: str = 'easyocr', language: str = 'en', auto_rotate: bool = True, output_dir: str = None, save_images: bool = False) -> str:
    """
    Extract text from PNG file using OCR with optional auto-rotation.
    
    Args:
        png_path: Path to PNG file
        engine: OCR engine to use ('easyocr' or 'tesseract')
        language: Language code for OCR
        auto_rotate: Whether to automatically detect and correct text orientation
        
    Returns:
        Extracted text
    """
    try:
        from heic2txt import HEIC2TXT
        from PIL import Image
        
        # Create converter
        converter = HEIC2TXT(engine=engine, language=language)
        
        # Load PNG image
        img = Image.open(png_path)
        
        if auto_rotate:
            # Detect best orientation
            best_angle = detect_text_orientation(png_path, engine, language)
            
            if best_angle != 0:
                print(f"🔄 Rotating image by {best_angle}° for better text recognition...")
                img = img.rotate(-best_angle, expand=True)
                # Save rotated image if output directory is provided
                if output_dir and save_images:
                    base_name = os.path.splitext(os.path.basename(png_path))[0]
                    rotated_save_path = os.path.join(output_dir, f"{base_name}_rotated_{best_angle}deg.png")
                    img.save(rotated_save_path)
                    print(f"💾 Saved rotated image: {os.path.basename(rotated_save_path)}")
        
        # Extract text
        text = converter.ocr.extract_text(img)
        
        return text
        
    except Exception as e:
        print(f"❌ OCR error: {e}")
        return ""

def compare_ocr_engines(png_path: str, language: str = 'en', auto_rotate: bool = True) -> dict:
    """
    Compare results from different OCR engines on the same image.
    
    Args:
        png_path: Path to PNG file
        language: Language code for OCR
        auto_rotate: Whether to use auto-rotation
        
    Returns:
        Dictionary with results from each engine
    """
    results = {}
    engines = ['easyocr', 'paddleocr']
    
    for engine in engines:
        try:
            print(f"🔍 Testing {engine.upper()}...")
            text = extract_text_from_png(png_path, engine, language, auto_rotate)
            
            # Calculate metrics
            total_chars = len(text)
            meaningful_chars = sum(1 for c in text if c.isalnum() or c.isspace())
            words = len([w for w in text.split() if w.strip()])
            lines = len([l for l in text.split('\n') if l.strip()])
            
            # Calculate text quality score
            quality_score = _calculate_text_quality(text)
            
            results[engine] = {
                'text': text,
                'total_chars': total_chars,
                'meaningful_chars': meaningful_chars,
                'words': words,
                'lines': lines,
                'quality_score': quality_score,
                'success': True
            }
            
            print(f"   ✅ {engine.upper()}: {meaningful_chars} meaningful chars, {words} words, {lines} lines, quality: {quality_score:.1f}")
            
        except Exception as e:
            print(f"   ❌ {engine.upper()}: Error - {e}")
            results[engine] = {
                'text': '',
                'total_chars': 0,
                'meaningful_chars': 0,
                'words': 0,
                'lines': 0,
                'quality_score': 0,
                'success': False,
                'error': str(e)
            }
    
    return results

def _calculate_text_quality(text: str) -> float:
    """
    Calculate text quality score based on readability and meaningful content.
    
    Args:
        text: Text to analyze
        
    Returns:
        Quality score (higher is better)
    """
    if not text.strip():
        return 0.0
    
    # Count meaningful characters (letters, numbers, common punctuation)
    meaningful_chars = sum(1 for c in text if c.isalnum() or c in '.,!?;:()[]{}"\'@#$%^&*+-=<>/\\|_~` ')
    
    # Count gibberish characters and symbols
    gibberish_chars = sum(1 for c in text if c in '=|°§±×÷∞≤≥≠≈∑∏∫∂∇∆√∝∈∉⊂⊃∪∩∧∨¬→←↑↓↔↕↖↗↘↙')
    
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
    
    # Bonus for having words
    score += word_count * 3.0
    
    # Bonus for meaningful lines
    score += meaningful_lines * 2.0
    
    # Penalty for too many single characters
    single_chars = sum(1 for w in text.split() if len(w.strip()) == 1)
    if single_chars > len(text.split()) * 0.6:  # More than 60% single characters
        score -= single_chars * 2.0
    
    # Normalize score by text length
    if len(text.strip()) > 0:
        score = score / len(text.strip()) * 100
    
    return max(0, score)

def analyze_differences(results: dict) -> dict:
    """
    Analyze differences between OCR engine results.
    
    Args:
        results: Dictionary with results from each engine
        
    Returns:
        Analysis of differences
    """
    analysis = {
        'best_engine': None,
        'best_meaningful_chars': 0,
        'differences': {},
        'summary': {}
    }
    
    # Find best performing engine based on quality score
    for engine, data in results.items():
        if data['success'] and data['quality_score'] > analysis['best_meaningful_chars']:
            analysis['best_engine'] = engine
            analysis['best_meaningful_chars'] = data['quality_score']
    
    # Compare engines
    engines = list(results.keys())
    for i, engine1 in enumerate(engines):
        for engine2 in engines[i+1:]:
            if results[engine1]['success'] and results[engine2]['success']:
                diff_key = f"{engine1}_vs_{engine2}"
                analysis['differences'][diff_key] = {
                    'meaningful_chars_diff': results[engine1]['meaningful_chars'] - results[engine2]['meaningful_chars'],
                    'words_diff': results[engine1]['words'] - results[engine2]['words'],
                    'lines_diff': results[engine1]['lines'] - results[engine2]['lines'],
                    'quality_score_diff': results[engine1]['quality_score'] - results[engine2]['quality_score'],
                    'better_engine': engine1 if results[engine1]['quality_score'] > results[engine2]['quality_score'] else engine2
                }
    
    # Summary
    successful_engines = [e for e, d in results.items() if d['success']]
    analysis['summary'] = {
        'total_engines': len(engines),
        'successful_engines': len(successful_engines),
        'best_engine': analysis['best_engine'],
        'performance_gap': max([d['quality_score'] for d in results.values() if d['success']]) - 
                          min([d['quality_score'] for d in results.values() if d['success']]) if successful_engines else 0
    }
    
    return analysis

def process_heic_file(heic_path: str, output_dir: str, engine: str = 'easyocr', language: str = 'en', auto_rotate: bool = True, compare_engines: bool = False, save_images: bool = False) -> bool:
    """
    Process a single HEIC file: convert to PNG, preprocess, extract text, save result.
    
    Args:
        heic_path: Path to HEIC file
        output_dir: Directory to save text file
        engine: OCR engine to use
        language: Language code for OCR
        auto_rotate: Whether to automatically detect and correct text orientation
        compare_engines: Whether to compare all OCR engines and log differences
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create temporary PNG file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_png:
            png_path = tmp_png.name
        
        # Convert HEIC to PNG
        print(f"🔄 Converting {os.path.basename(heic_path)} to PNG...")
        if not convert_heic_to_png(heic_path, png_path):
            return False
        
        # Preprocess image for better OCR
        print(f"🔄 Preprocessing image for OCR...")
        preprocessed_png_path = preprocess_image_for_ocr(png_path, output_dir, save_images)
        
        # Extract text from PNG
        if compare_engines:
            print(f"📊 Comparing OCR engines...")
            results = compare_ocr_engines(preprocessed_png_path, language, auto_rotate)
            analysis = analyze_differences(results)
            
            # Log comparison results
            print(f"\\n📈 COMPARISON RESULTS:")
            print(f"   �� Best engine: {analysis['best_engine'].upper()}")
            print(f"   📊 Quality gap: {analysis['summary']['performance_gap']:.1f} points")
            
            for diff_key, diff_data in analysis['differences'].items():
                engine1, engine2 = diff_key.split('_vs_')
                print(f"   🔄 {engine1.upper()} vs {engine2.upper()}:")
                print(f"      Characters: {diff_data['meaningful_chars_diff']:+d}")
                print(f"      Words: {diff_data['words_diff']:+d}")
                print(f"      Lines: {diff_data['lines_diff']:+d}")
                print(f"      Quality: {diff_data['quality_score_diff']:+.1f}")
                print(f"      Winner: {diff_data['better_engine'].upper()}")
            
            # Use the best engine's result
            if analysis['best_engine']:
                text = results[analysis['best_engine']]['text']
                used_engine = analysis['best_engine']
            else:
                text = "[No engines succeeded]"
                used_engine = "none"
        else:
            print(f"📖 Extracting text with {engine}...")
            text = extract_text_from_png(preprocessed_png_path, engine, language, auto_rotate, output_dir, save_images)
            used_engine = engine
        
        if not text.strip():
            print(f"⚠️  No text found in {os.path.basename(heic_path)}")
            text = "[No text detected]"
        
        # Save text to file
        base_name = Path(heic_path).stem
        text_file = os.path.join(output_dir, f"{base_name}.txt")
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Save comparison log if comparison was performed
        if compare_engines:
            log_file = os.path.join(output_dir, f"{base_name}_comparison.log")
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"OCR Engine Comparison Results\\n")
                f.write(f"File: {os.path.basename(heic_path)}\\n")
                f.write(f"Date: {__import__('datetime').datetime.now()}\\n")
                f.write(f"Auto-rotation: {'Enabled' if auto_rotate else 'Disabled'}\\n")
                f.write(f"Image preprocessing: Enabled\\n")
                f.write(f"\\n{'='*50}\\n\\n")
                
                for engine_name, data in results.items():
                    f.write(f"{engine_name.upper()} Results:\\n")
                    f.write(f"  Success: {data['success']}\\n")
                    f.write(f"  Total characters: {data['total_chars']}\\n")
                    f.write(f"  Meaningful characters: {data['meaningful_chars']}\\n")
                    f.write(f"  Words: {data['words']}\\n")
                    f.write(f"  Lines: {data['lines']}\\n")
                    f.write(f"  Quality score: {data.get('quality_score', 0):.1f}\\n")
                    if not data['success']:
                        f.write(f"  Error: {data.get('error', 'Unknown error')}\\n")
                    f.write(f"\\n")
                
                f.write(f"Analysis:\\n")
                f.write(f"  Best engine: {analysis['best_engine']}\\n")
                f.write(f"  Quality gap: {analysis['summary']['performance_gap']:.1f} points\\n")
                f.write(f"\\n")
                
                for diff_key, diff_data in analysis['differences'].items():
                    engine1, engine2 = diff_key.split('_vs_')
                    f.write(f"{engine1.upper()} vs {engine2.upper()}:\\n")
                    f.write(f"  Character difference: {diff_data['meaningful_chars_diff']:+d}\\n")
                    f.write(f"  Word difference: {diff_data['words_diff']:+d}\\n")
                    f.write(f"  Line difference: {diff_data['lines_diff']:+d}\\n")
                    f.write(f"  Quality difference: {diff_data.get('quality_score_diff', 0):+.1f}\\n")
                    f.write(f"  Winner: {diff_data['better_engine']}\\n")
                    f.write(f"\\n")
            
            print(f"📋 Comparison log saved to {log_file}")
        
        print(f"✅ Saved text to {text_file} (using {used_engine.upper()})")
        print(f"📄 Text preview: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {heic_path}: {e}")
        return False
    finally:
        # Clean up temporary PNG files
        if 'png_path' in locals() and os.path.exists(png_path):
            os.unlink(png_path)
        if 'preprocessed_png_path' in locals() and os.path.exists(preprocessed_png_path):
            os.unlink(preprocessed_png_path)

def main():
    """Main function to process HEIC files."""
    import argparse
    
    parser = argparse.ArgumentParser(description='HEIC2TXT Batch Processor with HEIC Conversion, Auto-Rotation, Image Preprocessing, and OCR Engine Comparison')
    parser.add_argument('input_paths', nargs='+', help='HEIC files or directories containing HEIC files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for text files')
    parser.add_argument('-e', '--engine', choices=['easyocr', 'tesseract'], default='easyocr', 
                       help='OCR engine to use')
    parser.add_argument('-l', '--language', default='en', help='Language code for OCR')
    parser.add_argument('--no-rotate', action='store_true', help='Disable automatic text orientation detection')
    parser.add_argument('--compare', action='store_true', help='Compare all OCR engines and log differences')
    parser.add_argument('--save-images', action='store_true', help='Save preprocessed and rotated images as PNG files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Find HEIC files
    heic_files = []
    for input_path in args.input_paths:
        if os.path.isfile(input_path):
            if input_path.lower().endswith('.heic'):
                heic_files.append(input_path)
            else:
                print(f"❌ {input_path} is not a HEIC file")
        elif os.path.isdir(input_path):
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith('.heic'):
                        heic_files.append(os.path.join(root, file))
        else:
            print(f"❌ {input_path} is not a valid file or directory")
    
    if not heic_files:
        print(f"❌ No HEIC files found in {args.input_paths}")
        return 1
    
    print(f"🚀 Found {len(heic_files)} HEIC files to process")
    print(f"📁 Output directory: {args.output}")
    print(f"🔧 OCR engine: {args.engine}")
    print(f"🌐 Language: {args.language}")
    print(f"🔄 Auto-rotation: {'Enabled' if not args.no_rotate else 'Disabled'}")
    print(f"🖼️  Image preprocessing: Enabled")
    print(f"💾 Save intermediate images: {"Enabled" if args.save_images else "Disabled"}")
    print(f"📊 Engine comparison: {'Enabled' if args.compare else 'Disabled'}")
    print("=" * 60)
    
    # Process files
    successful = 0
    failed = 0
    
    for i, heic_file in enumerate(heic_files, 1):
        print(f"\\n[{i}/{len(heic_files)}] Processing: {os.path.basename(heic_file)}")
        
        if process_heic_file(heic_file, args.output, args.engine, args.language, not args.no_rotate, args.compare, args.save_images):
            successful += 1
        else:
            failed += 1
    
    print("\\n" + "=" * 60)
    print(f"🎉 Processing complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Text files saved to: {args.output}")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
