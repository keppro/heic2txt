#!/usr/bin/env python3
"""
OCR Engine Orientation Test with Preprocessing
==============================================

This script tests both EasyOCR and Apple Vision OCR engines with different
image orientations, both with and without preprocessing.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from PIL import Image
from typing import Dict, List, Tuple, Any

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from heic2txt import HEIC2TXT
from utils.text_utils import calculate_text_similarity, normalize_text_for_comparison
from utils.image_utils import preprocess_image_for_ocr


def convert_heic_to_png(heic_path: str, output_path: str) -> bool:
    """Convert HEIC file to PNG using sips command."""
    try:
        result = subprocess.run([
            'sips', '-s', 'format', 'png', heic_path, '--out', output_path
        ], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error converting HEIC: {e}")
        return False


def load_ground_truth(ground_truth_path: str) -> str:
    """Load ground truth text from file."""
    try:
        with open(ground_truth_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ Error loading ground truth: {e}")
        return ""


def create_orientation_variants(image_path: str) -> List[Tuple[str, str, int]]:
    """Create different orientation variants of the image."""
    print("🔄 Creating orientation variants...")
    
    variants = []
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Load original image
    image = Image.open(image_path)
    print(f"   📏 Original image size: {image.size}")
    
    # Create different orientations
    orientations = [
        (0, "original", "No rotation"),
        (90, "rotated_90", "Rotated 90° clockwise"),
        (180, "rotated_180", "Rotated 180°"),
        (270, "rotated_270", "Rotated 270° clockwise")
    ]
    
    for angle, suffix, description in orientations:
        # Rotate image
        if angle != 0:
            rotated = image.rotate(-angle, expand=True)  # PIL uses counter-clockwise
        else:
            rotated = image.copy()
        
        # Save rotated image
        variant_path = f"/tmp/{base_name}_{suffix}.png"
        rotated.save(variant_path)
        
        variants.append((variant_path, description, angle))
        print(f"   ✅ Created {suffix}: {rotated.size} ({description})")
    
    return variants


def test_engine_orientation_with_preprocessing(engine_name: str, image_path: str, orientation_desc: str, 
                                             ground_truth: str, use_preprocessing: bool, language: str = "en") -> Dict:
    """Test a specific engine with a specific orientation and preprocessing option."""
    print(f"\n🔬 Testing {engine_name.upper()} - {orientation_desc} {'(with preprocessing)' if use_preprocessing else '(no preprocessing)'}")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        # Initialize the engine
        init_start = time.time()
        heic2txt = HEIC2TXT(engine=engine_name, language=language)
        init_time = time.time() - init_start
        
        # Load and prepare image
        image = Image.open(image_path)
        print(f"   📏 Original image size: {image.size}")
        
        if use_preprocessing:
            # Apply preprocessing
            print("   🔄 Applying preprocessing...")
            preprocessed_path = preprocess_image_for_ocr(image_path, "/tmp", save_images=True)
            image = Image.open(preprocessed_path)
            print(f"   📏 Preprocessed image size: {image.size}")
        else:
            print("   ⏭️  Skipping preprocessing")
        
        # Extract text
        extract_start = time.time()
        text = heic2txt.ocr.extract_text(image)
        extract_time = time.time() - extract_start
        
        # Calculate similarity
        similarity = calculate_text_similarity(ground_truth, text) if text else 0.0
        
        total_time = time.time() - start_time
        
        result = {
            'engine': engine_name,
            'orientation': orientation_desc,
            'preprocessing': use_preprocessing,
            'image_size': image.size,
            'text_length': len(text),
            'similarity': similarity,
            'init_time': init_time,
            'extract_time': extract_time,
            'total_time': total_time,
            'success': len(text) > 0,
            'extracted_text': text[:100] + "..." if len(text) > 100 else text
        }
        
        print(f"   ⏱️  Init time: {init_time:.3f}s")
        print(f"   ⏱️  Extract time: {extract_time:.3f}s")
        print(f"   ⏱️  Total time: {total_time:.3f}s")
        print(f"   📝 Text length: {len(text)} characters")
        print(f"   📊 Similarity: {similarity:.2f}%")
        print(f"   📄 Text preview: {text[:50]}..." if text else "   📄 Text: (none)")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {
            'engine': engine_name,
            'orientation': orientation_desc,
            'preprocessing': use_preprocessing,
            'image_size': (0, 0),
            'text_length': 0,
            'similarity': 0.0,
            'init_time': 0.0,
            'extract_time': 0.0,
            'total_time': 0.0,
            'success': False,
            'error': str(e)
        }


def main():
    """Main test function."""
    print("🔬 OCR Engine Orientation Test with Preprocessing")
    print("=" * 70)
    
    # Test configuration
    heic_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518.HEIC"
    ground_truth_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518.txt"
    language = "en"
    
    print(f"Test image: {heic_path}")
    print(f"Ground truth: {ground_truth_path}")
    print(f"Language: {language}")
    
    # Convert HEIC to PNG
    print("\n🔄 Converting HEIC to PNG...")
    png_path = heic_path.replace('.HEIC', '_orientation_preprocessing_test.png')
    if not convert_heic_to_png(heic_path, png_path):
        print("❌ Failed to convert HEIC file")
        return
    
    print(f"✅ Converted to: {png_path}")
    
    # Load ground truth
    ground_truth = load_ground_truth(ground_truth_path)
    if not ground_truth:
        print("❌ No ground truth available")
        return
    
    print(f"📄 Ground truth: '{ground_truth}' ({len(ground_truth)} chars)")
    
    # Create orientation variants
    variants = create_orientation_variants(png_path)
    
    # Test configurations
    engines = ['easyocr', 'apple_vision']
    preprocessing_options = [False, True]
    
    results = []
    
    # Test each engine with each orientation and preprocessing option
    for engine in engines:
        print(f"\n{'='*70}")
        print(f"Testing {engine.upper()} ENGINE")
        print(f"{'='*70}")
        
        for variant_path, orientation_desc, angle in variants:
            for use_preprocessing in preprocessing_options:
                result = test_engine_orientation_with_preprocessing(
                    engine, variant_path, orientation_desc, ground_truth, use_preprocessing, language
                )
                results.append(result)
    
    # Print summary
    print("\n" + "=" * 120)
    print("📊 ORIENTATION + PREPROCESSING TEST RESULTS SUMMARY")
    print("=" * 120)
    
    # Group results by engine and preprocessing
    easyocr_no_prep = [r for r in results if r['engine'] == 'easyocr' and not r['preprocessing']]
    easyocr_with_prep = [r for r in results if r['engine'] == 'easyocr' and r['preprocessing']]
    apple_vision_no_prep = [r for r in results if r['engine'] == 'apple_vision' and not r['preprocessing']]
    apple_vision_with_prep = [r for r in results if r['engine'] == 'apple_vision' and r['preprocessing']]
    
    print(f"\n🏆 EASYOCR - NO PREPROCESSING:")
    print(f"{'Orientation':<20} {'Success':<8} {'Similarity':<10} {'Time (s)':<10} {'Text Length':<12}")
    print("-" * 70)
    for result in easyocr_no_prep:
        status = "✅" if result['success'] else "❌"
        print(f"{result['orientation']:<20} {status:<8} {result['similarity']:<10.2f} "
              f"{result['total_time']:<10.3f} {result['text_length']:<12}")
    
    print(f"\n🏆 EASYOCR - WITH PREPROCESSING:")
    print(f"{'Orientation':<20} {'Success':<8} {'Similarity':<10} {'Time (s)':<10} {'Text Length':<12}")
    print("-" * 70)
    for result in easyocr_with_prep:
        status = "✅" if result['success'] else "❌"
        print(f"{result['orientation']:<20} {status:<8} {result['similarity']:<10.2f} "
              f"{result['total_time']:<10.3f} {result['text_length']:<12}")
    
    print(f"\n🍎 APPLE VISION - NO PREPROCESSING:")
    print(f"{'Orientation':<20} {'Success':<8} {'Similarity':<10} {'Time (s)':<10} {'Text Length':<12}")
    print("-" * 70)
    for result in apple_vision_no_prep:
        status = "✅" if result['success'] else "❌"
        print(f"{result['orientation']:<20} {status:<8} {result['similarity']:<10.2f} "
              f"{result['total_time']:<10.3f} {result['text_length']:<12}")
    
    print(f"\n🍎 APPLE VISION - WITH PREPROCESSING:")
    print(f"{'Orientation':<20} {'Success':<8} {'Similarity':<10} {'Time (s)':<10} {'Text Length':<12}")
    print("-" * 70)
    for result in apple_vision_with_prep:
        status = "✅" if result['success'] else "❌"
        print(f"{result['orientation']:<20} {status:<8} {result['similarity']:<10.2f} "
              f"{result['total_time']:<10.3f} {result['text_length']:<12}")
    
    # Find best results
    all_results = [easyocr_no_prep, easyocr_with_prep, apple_vision_no_prep, apple_vision_with_prep]
    best_results = []
    
    for group in all_results:
        if group:
            best = max(group, key=lambda x: x['similarity'])
            best_results.append(best)
    
    overall_best = max(best_results, key=lambda x: x['similarity'])
    
    print(f"\n🎯 BEST OVERALL RESULT:")
    print(f"   {overall_best['engine'].upper()} - {overall_best['orientation']} - {'With' if overall_best['preprocessing'] else 'No'} Preprocessing")
    print(f"   Similarity: {overall_best['similarity']:.2f}%")
    print(f"   Time: {overall_best['total_time']:.3f}s")
    
    # Preprocessing impact analysis
    print(f"\n📈 PREPROCESSING IMPACT ANALYSIS:")
    
    for engine in engines:
        no_prep_results = [r for r in results if r['engine'] == engine and not r['preprocessing']]
        with_prep_results = [r for r in results if r['engine'] == engine and r['preprocessing']]
        
        if no_prep_results and with_prep_results:
            no_prep_avg = sum(r['similarity'] for r in no_prep_results) / len(no_prep_results)
            with_prep_avg = sum(r['similarity'] for r in with_prep_results) / len(with_prep_results)
            
            print(f"\n   {engine.upper()}:")
            print(f"     No preprocessing average: {no_prep_avg:.2f}%")
            print(f"     With preprocessing average: {with_prep_avg:.2f}%")
            print(f"     Preprocessing impact: {with_prep_avg - no_prep_avg:+.2f}%")
    
    # Orientation analysis
    print(f"\n📈 ORIENTATION ANALYSIS:")
    
    for engine in engines:
        for use_preprocessing in preprocessing_options:
            engine_results = [r for r in results if r['engine'] == engine and r['preprocessing'] == use_preprocessing]
            if engine_results:
                successful_orientations = [r for r in engine_results if r['success']]
                
                print(f"\n   {engine.upper()} - {'With' if use_preprocessing else 'No'} Preprocessing:")
                print(f"     Successful orientations: {len(successful_orientations)}/{len(engine_results)}")
                
                if successful_orientations:
                    avg_similarity = sum(r['similarity'] for r in successful_orientations) / len(successful_orientations)
                    print(f"     Average similarity: {avg_similarity:.2f}%")
                    
                    best_orientation = max(successful_orientations, key=lambda x: x['similarity'])
                    print(f"     Best orientation: {best_orientation['orientation']} ({best_orientation['similarity']:.2f}%)")
    
    # Save detailed results
    results_file = "orientation_preprocessing_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    try:
        os.unlink(png_path)
        for variant_path, _, _ in variants:
            os.unlink(variant_path)
        print("   ✅ Cleanup complete")
    except Exception as e:
        print(f"   ⚠️  Cleanup warning: {e}")


if __name__ == "__main__":
    main()
