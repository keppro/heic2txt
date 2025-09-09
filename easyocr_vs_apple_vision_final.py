#!/usr/bin/env python3
"""
Final Comprehensive Test: EasyOCR vs Apple Vision
================================================

This script performs a comprehensive comparison between EasyOCR and Apple Vision
OCR engines, testing both with and without preprocessing to determine the best
performing engine for the HEIC to text conversion pipeline.
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
from heic2txt_batch import resize_image_if_needed


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


def test_engine(engine_name: str, image: Image.Image, language: str = "en") -> Tuple[str, float, float]:
    """
    Test a specific OCR engine.
    
    Args:
        engine_name: Name of the engine ('easyocr' or 'apple_vision')
        image: PIL Image object
        language: Language code
        
    Returns:
        Tuple of (extracted_text, similarity_score, processing_time)
    """
    print(f"\n{'='*60}")
    print(f"Testing {engine_name.upper()}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Initialize the engine
        init_start = time.time()
        heic2txt = HEIC2TXT(engine=engine_name, language=language)
        init_time = time.time() - init_start
        print(f"✅ {engine_name.upper()} initialized in {init_time:.2f}s")
        
        # Extract text
        extract_start = time.time()
        text = heic2txt.ocr.extract_text(image)
        extract_time = time.time() - extract_start
        print(f"✅ Text extracted in {extract_time:.2f}s")
        
        total_time = time.time() - start_time
        print(f"📝 Extracted text length: {len(text)} characters")
        
        return text, 0.0, total_time  # Similarity will be calculated later
        
    except Exception as e:
        print(f"❌ {engine_name.upper()} failed: {e}")
        return "", 0.0, 0.0


def main():
    """Main test function."""
    print("🔬 Final Comprehensive OCR Test: EasyOCR vs Apple Vision")
    print("="*60)
    
    # Test configuration
    heic_path = "~/Pictures/TF/IMG_7518.HEIC"
    ground_truth_path = "~/Pictures/TF/IMG_7518.txt"
    language = "en"
    
    print(f"Test image: {heic_path}")
    print(f"Ground truth: {ground_truth_path}")
    print(f"Language: {language}")
    
    # Convert HEIC to PNG
    print("\n🔄 Converting HEIC to PNG...")
    png_path = heic_path.replace('.HEIC', '_final_test.png')
    if not convert_heic_to_png(heic_path, png_path):
        print("❌ Failed to convert HEIC file")
        return
    
    print(f"✅ Converted to: {png_path}")
    
    # Load ground truth
    ground_truth = load_ground_truth(ground_truth_path)
    if not ground_truth:
        print("❌ No ground truth available")
        return
    
    print(f"📄 Ground truth length: {len(ground_truth)} characters")
    
    # Test configurations
    test_configs = [
        ("easyocr", False, "EasyOCR without preprocessing"),
        ("easyocr", True, "EasyOCR with preprocessing"),
        ("apple_vision", False, "Apple Vision without preprocessing"),
        ("apple_vision", True, "Apple Vision with preprocessing"),
    ]
    
    results = []
    
    for engine, use_preprocessing, description in test_configs:
        print(f"\n{'='*60}")
        print(f"Testing {description.upper()}")
        print(f"{'='*60}")
        
        # Load and prepare image
        image = Image.open(png_path)
        print(f"🖼️  Original image size: {image.size}")
        
        # Apply preprocessing if requested
        if use_preprocessing:
            print("🔄 Applying preprocessing...")
            preprocessed_path = preprocess_image_for_ocr(png_path, "/tmp", save_images=True)
            image = Image.open(preprocessed_path)
            print(f"🖼️  Preprocessed image size: {image.size}")
        else:
            # Just resize to fit within limits
            resized_path = resize_image_if_needed(png_path, max_size=4000)
            image = Image.open(resized_path)
            print(f"🖼️  Resized image size: {image.size}")
        
        # Test the engine
        text, similarity, total_time = test_engine(engine, image, language)
        
        # Calculate similarity with ground truth
        if text:
            similarity = calculate_text_similarity(ground_truth, text)
            print(f"📊 Similarity: {similarity:.2f}%")
        else:
            print("📊 Similarity: 0.00% (no text extracted)")
        
        print(f"⏱️  Total time: {total_time:.2f}s")
        
        # Store results
        results.append({
            "engine": engine,
            "preprocessing": use_preprocessing,
            "description": description,
            "text_length": len(text),
            "similarity": similarity,
            "time": total_time,
            "success": len(text) > 0
        })
    
    # Print summary
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS SUMMARY")
    print("="*80)
    print(f"{'Engine':<12} {'Preprocessing':<12} {'Similarity':<10} {'Time (s)':<10} {'Success':<8}")
    print("-" * 80)
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{result['engine']:<12} {str(result['preprocessing']):<12} "
              f"{result['similarity']:<10.2f} {result['time']:<10.2f} {status:<8}")
    
    # Find best results
    best_overall = max(results, key=lambda x: x["similarity"])
    fastest = min(results, key=lambda x: x["time"])
    
    print(f"\n🏆 BEST OVERALL ACCURACY:")
    print(f"   {best_overall['description']}")
    print(f"   Similarity: {best_overall['similarity']:.2f}%")
    print(f"   Time: {best_overall['time']:.2f}s")
    
    print(f"\n⚡ FASTEST:")
    print(f"   {fastest['description']}")
    print(f"   Similarity: {fastest['similarity']:.2f}%")
    print(f"   Time: {fastest['time']:.2f}s")
    
    # Engine comparison
    print(f"\n🔍 ENGINE COMPARISON:")
    
    easyocr_results = [r for r in results if r['engine'] == 'easyocr']
    apple_vision_results = [r for r in results if r['engine'] == 'apple_vision']
    
    print(f"\n   Without Preprocessing:")
    easyocr_no_prep = next((r for r in easyocr_results if not r['preprocessing']), None)
    apple_vision_no_prep = next((r for r in apple_vision_results if not r['preprocessing']), None)
    
    if easyocr_no_prep and apple_vision_no_prep:
        diff = easyocr_no_prep['similarity'] - apple_vision_no_prep['similarity']
        winner = "EasyOCR" if diff > 0 else "Apple Vision"
        print(f"   EasyOCR:     {easyocr_no_prep['similarity']:.2f}% ({easyocr_no_prep['time']:.2f}s)")
        print(f"   Apple Vision: {apple_vision_no_prep['similarity']:.2f}% ({apple_vision_no_prep['time']:.2f}s)")
        print(f"   🏆 {winner} is {abs(diff):.2f}% more accurate")
    
    print(f"\n   With Preprocessing:")
    easyocr_prep = next((r for r in easyocr_results if r['preprocessing']), None)
    apple_vision_prep = next((r for r in apple_vision_results if r['preprocessing']), None)
    
    if easyocr_prep and apple_vision_prep:
        diff = easyocr_prep['similarity'] - apple_vision_prep['similarity']
        winner = "EasyOCR" if diff > 0 else "Apple Vision"
        print(f"   EasyOCR:     {easyocr_prep['similarity']:.2f}% ({easyocr_prep['time']:.2f}s)")
        print(f"   Apple Vision: {apple_vision_prep['similarity']:.2f}% ({apple_vision_prep['time']:.2f}s)")
        print(f"   🏆 {winner} is {abs(diff):.2f}% more accurate")
    
    # Save detailed results
    results_file = "easyocr_vs_apple_vision_final_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    # Cleanup
    try:
        os.unlink(png_path)
    except:
        pass


if __name__ == "__main__":
    main()
