#!/usr/bin/env python3
"""
HEIC2TXT Batch Processor with Custom Words Support

Enhanced batch processor that supports domain-specific custom words
for improved Apple Vision OCR recognition.
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
    """Convert HEIC file to PNG using macOS sips command."""
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

def preprocess_image_for_ocr(image_path: str) -> str:
    """Preprocess image for better OCR recognition."""
    try:
        from utils.image_utils import preprocess_image_for_ocr as utils_preprocess
        return utils_preprocess(image_path, "/tmp", save_images=True)
    except Exception as e:
        print(f"❌ Image preprocessing error: {e}")
        return image_path

def process_image_with_custom_words(image_path: str, custom_words: List[str], output_dir: str) -> dict:
    """Process a single image with custom words and orientation testing."""
    
    print(f"📷 Processing: {os.path.basename(image_path)}")
    
    # Convert HEIC to PNG
    png_path = image_path.replace('.heic', '.png').replace('.HEIC', '.png')
    if not convert_heic_to_png(image_path, png_path):
        return {"success": False, "error": "HEIC conversion failed"}
    
    # Preprocess image
    preprocessed_path = preprocess_image_for_ocr(png_path)
    
    # Initialize OCR with custom words
    try:
        from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
        from utils.text_utils import save_text_to_file
        from PIL import Image
        
        ocr = AppleVisionOCREngine(language="en", custom_words=custom_words)
        
        # Load preprocessed image
        image = Image.open(preprocessed_path)
        
        # Test different orientations
        print("🔄 Testing orientations: 0°, 90°, 180°, 270°...")
        
        orientations = [
            (0, "0°"),
            (90, "90°"),
            (180, "180°"),
            (270, "270°")
        ]
        
        best_text = ""
        best_orientation = 0
        best_rotation = 0
        orientation_results = []
        
        for rotation, label in orientations:
            # Rotate image
            if rotation > 0:
                rotated_image = image.rotate(-rotation, expand=True)
            else:
                rotated_image = image
            
            # Extract text (fast mode for orientation testing)
            text = ocr.extract_text_fast(rotated_image)
            
            # Count meaningful characters (excluding whitespace and special chars)
            meaningful_chars = len([c for c in text if c.isalnum()])
            orientation_results.append((meaningful_chars, text, rotation, label))
            
            print(f"   {label}: {meaningful_chars} meaningful characters")
            
            # Keep track of best result
            if meaningful_chars > len([c for c in best_text if c.isalnum()]):
                best_text = text
                best_orientation = rotation
                best_rotation = rotation
        
        # Find best orientation
        best_result = max(orientation_results, key=lambda x: x[0])
        best_text = best_result[1]
        best_rotation = best_result[2]
        best_label = best_result[3]
        
        print(f"🎯 Best orientation: {best_label} ({best_result[0]} characters)")
        
        # Rotate image to best orientation if needed
        if best_rotation > 0:
            print(f"🔄 Rotating image by {best_rotation}° for better text recognition...")
            final_image = image.rotate(-best_rotation, expand=True)
            
            # Save rotated image
            rotated_path = preprocessed_path.replace('.png', f'_rotated_{best_rotation}deg.png')
            final_image.save(rotated_path)
            print(f"💾 Saved rotated image: {os.path.basename(rotated_path)}")
        else:
            final_image = image
        
        # Final text extraction with best orientation
        final_text = ocr.extract_text(final_image)
        
        if not final_text.strip():
            return {"success": False, "error": "No text detected"}
        
        # Save text to file
        output_file = Path(output_dir) / f"{Path(image_path).stem}.txt"
        success = save_text_to_file(final_text, str(output_file))
        
        if not success:
            return {"success": False, "error": "Could not save text file"}
        
        # Count custom words found
        words_found = []
        for word in custom_words:
            if word.lower() in final_text.lower():
                words_found.append(word)
        
        print(f"✅ Apple Vision OCR extracted {len(final_text)} characters")
        print(f"🎯 Custom words found: {len(words_found)}/{len(custom_words)}")
        
        # Clean up temporary files
        try:
            os.unlink(png_path)
            if preprocessed_path != png_path:
                os.unlink(preprocessed_path)
        except:
            pass
        
        return {
            "success": True,
            "text_length": len(final_text),
            "words_found": words_found,
            "words_found_count": len(words_found),
            "output_file": str(output_file),
            "best_orientation": best_rotation
        }
        
    except Exception as e:
        return {"success": False, "error": f"OCR processing error: {e}"}

def batch_process_with_custom_words(input_dir: str, output_dir: str, custom_words: List[str], 
                                  combination_name: str) -> None:
    """Process all HEIC files in a directory with custom words."""
    
    print(f"🚀 Batch Processing with {combination_name}")
    print("=" * 60)
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📝 Custom words: {len(custom_words)} terms")
    print(f"   Sample: {', '.join(custom_words[:10])}...")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Find all HEIC files
    input_path = Path(input_dir)
    heic_files = list(input_path.glob("*.heic")) + list(input_path.glob("*.HEIC"))
    
    if not heic_files:
        print("❌ No HEIC files found in input directory")
        return
    
    print(f"📊 Found {len(heic_files)} HEIC files to process")
    print()
    
    # Process files
    successful = 0
    failed = 0
    total_words_found = 0
    total_processing_time = 0
    
    for i, heic_file in enumerate(heic_files, 1):
        print(f"[{i}/{len(heic_files)}] Processing: {heic_file.name}")
        
        import time
        start_time = time.time()
        
        result = process_image_with_custom_words(str(heic_file), custom_words, output_dir)
        
        processing_time = time.time() - start_time
        total_processing_time += processing_time
        
        if result["success"]:
            successful += 1
            total_words_found += result["words_found_count"]
            
            print(f"   ✅ Success: {result['text_length']} chars, "
                  f"{processing_time:.3f}s, "
                  f"{result['words_found_count']} custom words found")
            
            if result["words_found"]:
                print(f"   🎯 Found: {', '.join(result['words_found'][:5])}")
                if len(result["words_found"]) > 5:
                    print(f"   ... and {len(result['words_found']) - 5} more")
        else:
            failed += 1
            print(f"   ❌ Failed: {result['error']}")
        
        print()
    
    # Summary
    print("📊 Batch Processing Summary")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total time: {total_processing_time:.2f}s")
    print(f"⏱️  Average time per file: {total_processing_time/len(heic_files):.3f}s")
    print(f"🎯 Total custom words found: {total_words_found}")
    print(f"📁 Text files saved to: {output_dir}")

def main():
    """Main function for batch processing with custom words."""
    
    if len(sys.argv) < 4:
        print("Usage: python3 heic2txt_batch_custom.py <input_dir> <output_dir> <combination_name>")
        print("Example: python3 heic2txt_batch_custom.py /path/to/images /path/to/output terraform_ansible_postgresql")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    combination_name = sys.argv[3]
    
    # Get custom words based on combination name
    try:
        from domain_specific_custom_words import get_domain_specific_words
        
        # Map combination names to domains
        combination_map = {
            'terraform_ansible_postgresql': ['terraform', 'ansible', 'postgresql'],
            'terraform_ansible_aws_postgresql': ['terraform', 'ansible', 'aws', 'postgresql'],
            'terraform_ansible_aws': ['terraform', 'ansible', 'aws'],
            'terraform_ansible_aws_mysql': ['terraform', 'ansible', 'aws', 'mysql'],
            'terraform_ansible': ['terraform', 'ansible']
        }
        
        if combination_name not in combination_map:
            print(f"❌ Unknown combination: {combination_name}")
            print(f"Available combinations: {', '.join(combination_map.keys())}")
            sys.exit(1)
        
        domains = combination_map[combination_name]
        custom_words = get_domain_specific_words(domains)
        
        print(f"🎯 Using combination: {combination_name}")
        print(f"📝 Domains: {', '.join(domains)}")
        print(f"📊 Custom words: {len(custom_words)} terms")
        print()
        
        # Run batch processing
        batch_process_with_custom_words(input_dir, output_dir, custom_words, combination_name)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure domain_specific_custom_words.py is available")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
