#!/usr/bin/env python3
"""
OCR Engine Orientation Test
===========================

This script tests both EasyOCR and Apple Vision OCR engines with different
image orientations to determine how well they handle rotated images.
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
        (270, "rotated_270", "Rotated 270° clockwise"),
        (-90, "rotated_neg90", "Rotated 90° counter-clockwise")
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


def test_engine_orientation(engine_name: str, image_path: str, orientation_desc: str, 
                          ground_truth: str, language: str = "en") -> Dict:
    """Test a specific engine with a specific orientation."""
    print(f"\n🔬 Testing {engine_name.upper()} - {orientation_desc}")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # Initialize the engine
        init_start = time.time()
        heic2txt = HEIC2TXT(engine=engine_name, language=language)
        init_time = time.time() - init_start
        
        # Load image
        image = Image.open(image_path)
        print(f"   📏 Image size: {image.size}")
        
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
    print("🔬 OCR Engine Orientation Test")
    print("=" * 60)
    
    # Test configuration
    heic_path = "~/Pictures/TF/IMG_7518.HEIC"
    ground_truth_path = "~/Pictures/TF/IMG_7518.txt"
    language = "en"
    
    print(f"Test image: {heic_path}")
    print(f"Ground truth: {ground_truth_path}")
    print(f"Language: {language}")
    
    # Convert HEIC to PNG
    print("\n🔄 Converting HEIC to PNG...")
    png_path = heic_path.replace('.HEIC', '_orientation_test.png')
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
    
    results = []
    
    # Test each engine with each orientation
    for engine in engines:
        print(f"\n{'='*60}")
        print(f"Testing {engine.upper()} ENGINE")
        print(f"{'='*60}")
        
        for variant_path, orientation_desc, angle in variants:
            result = test_engine_orientation(engine, variant_path, orientation_desc, ground_truth, language)
            results.append(result)
    
    # Print summary
    print("\n" + "=" * 100)
    print("📊 ORIENTATION TEST RESULTS SUMMARY")
    print("=" * 100)
    
    # Group results by engine
    easyocr_results = [r for r in results if r['engine'] == 'easyocr']
    apple_vision_results = [r for r in results if r['engine'] == 'apple_vision']
    
    print(f"\n🏆 EASYOCR RESULTS:")
    print(f"{'Orientation':<20} {'Success':<8} {'Similarity':<10} {'Time (s)':<10} {'Text Length':<12}")
    print("-" * 70)
    for result in easyocr_results:
        status = "✅" if result['success'] else "❌"
        print(f"{result['orientation']:<20} {status:<8} {result['similarity']:<10.2f} "
              f"{result['total_time']:<10.3f} {result['text_length']:<12}")
    
    print(f"\n🍎 APPLE VISION RESULTS:")
    print(f"{'Orientation':<20} {'Success':<8} {'Similarity':<10} {'Time (s)':<10} {'Text Length':<12}")
    print("-" * 70)
    for result in apple_vision_results:
        status = "✅" if result['success'] else "❌"
        print(f"{result['orientation']:<20} {status:<8} {result['similarity']:<10.2f} "
              f"{result['total_time']:<10.3f} {result['text_length']:<12}")
    
    # Find best results for each engine
    easyocr_best = max(easyocr_results, key=lambda x: x['similarity'])
    apple_vision_best = max(apple_vision_results, key=lambda x: x['similarity'])
    
    print(f"\n🎯 BEST RESULTS:")
    print(f"   EasyOCR: {easyocr_best['similarity']:.2f}% similarity with {easyocr_best['orientation']}")
    print(f"   Apple Vision: {apple_vision_best['similarity']:.2f}% similarity with {apple_vision_best['orientation']}")
    
    # Orientation analysis
    print(f"\n📈 ORIENTATION ANALYSIS:")
    
    for engine in engines:
        engine_results = [r for r in results if r['engine'] == engine]
        successful_orientations = [r for r in engine_results if r['success']]
        
        print(f"\n   {engine.upper()}:")
        print(f"     Successful orientations: {len(successful_orientations)}/{len(engine_results)}")
        
        if successful_orientations:
            avg_similarity = sum(r['similarity'] for r in successful_orientations) / len(successful_orientations)
            print(f"     Average similarity: {avg_similarity:.2f}%")
            
            best_orientation = max(successful_orientations, key=lambda x: x['similarity'])
            worst_orientation = min(successful_orientations, key=lambda x: x['similarity'])
            
            print(f"     Best orientation: {best_orientation['orientation']} ({best_orientation['similarity']:.2f}%)")
            print(f"     Worst orientation: {worst_orientation['orientation']} ({worst_orientation['similarity']:.2f}%)")
    
    # Overall comparison
    print(f"\n🔍 ENGINE COMPARISON:")
    if easyocr_best['similarity'] > apple_vision_best['similarity']:
        winner = "EasyOCR"
        margin = easyocr_best['similarity'] - apple_vision_best['similarity']
    else:
        winner = "Apple Vision"
        margin = apple_vision_best['similarity'] - easyocr_best['similarity']
    
    print(f"   🏆 {winner} wins by {margin:.2f}% similarity")
    print(f"   EasyOCR best: {easyocr_best['similarity']:.2f}% ({easyocr_best['orientation']})")
    print(f"   Apple Vision best: {apple_vision_best['similarity']:.2f}% ({apple_vision_best['orientation']})")
    
    # Speed comparison
    easyocr_avg_time = sum(r['total_time'] for r in easyocr_results) / len(easyocr_results)
    apple_vision_avg_time = sum(r['total_time'] for r in apple_vision_results) / len(apple_vision_results)
    
    print(f"\n⚡ SPEED COMPARISON:")
    print(f"   EasyOCR average time: {easyocr_avg_time:.3f}s")
    print(f"   Apple Vision average time: {apple_vision_avg_time:.3f}s")
    
    if easyocr_avg_time < apple_vision_avg_time:
        speed_winner = "EasyOCR"
        speed_margin = apple_vision_avg_time - easyocr_avg_time
    else:
        speed_winner = "Apple Vision"
        speed_margin = easyocr_avg_time - apple_vision_avg_time
    
    print(f"   🏆 {speed_winner} is {speed_margin:.3f}s faster on average")
    
    # Save detailed results
    results_file = "orientation_test_results.json"
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
