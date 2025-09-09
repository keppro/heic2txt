#!/usr/bin/env python3
"""
Comprehensive test script to compare Apple Vision vs EasyOCR performance.
Uses the same methodology as EasyOCR optimization testing.
"""

import os
import sys
import time
import json
from pathlib import Path
from PIL import Image
import difflib

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from heic2txt import HEIC2TXT
from utils.text_utils import calculate_text_similarity

def test_ocr_engine(engine_name, image_path, ground_truth_path, language="en", preprocessing=False):
    """
    Test a specific OCR engine with the given image and ground truth.
    
    Args:
        engine_name: Name of the OCR engine ('easyocr' or 'apple_vision')
        image_path: Path to the test image
        ground_truth_path: Path to the ground truth text file
        language: Language code for OCR
        preprocessing: Whether to apply preprocessing
        
    Returns:
        dict: Test results including similarity, time, and extracted text
    """
    print(f"\n{'='*60}")
    print(f"Testing {engine_name.upper()} {'with' if preprocessing else 'without'} preprocessing")
    print(f"{'='*60}")
    
    try:
        # Initialize OCR engine
        start_time = time.time()
        heic2txt = HEIC2TXT(engine=engine_name, language=language)
        init_time = time.time() - start_time
        
        print(f"✅ {engine_name.upper()} initialized in {init_time:.2f}s")
        
        # Load and process image
        start_time = time.time()
        
        # First, resize image if needed (always apply this step)
        from heic2txt_batch import resize_image_if_needed
        resized_image_path = resize_image_if_needed(image_path, max_size=4000)
        
        # Load the (potentially resized) image
        image = Image.open(resized_image_path)
        
        # Apply additional preprocessing if requested
        if preprocessing:
            from utils.image_utils import preprocess_image_for_ocr
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                temp_path = tmp_file.name
            image.save(temp_path)
            preprocessed_path = preprocess_image_for_ocr(temp_path, os.path.dirname(temp_path), False)
            image = Image.open(preprocessed_path)
            os.unlink(temp_path)
            if preprocessed_path != temp_path:
                os.unlink(preprocessed_path)
        
        # Extract text
        extracted_text = heic2txt.ocr.extract_text(image)
        extraction_time = time.time() - start_time
        
        print(f"✅ Text extracted in {extraction_time:.2f}s")
        print(f"📝 Extracted text length: {len(extracted_text)} characters")
        
        # Load ground truth
        with open(ground_truth_path, 'r', encoding='utf-8') as f:
            ground_truth = f.read().strip()
        
        # Calculate similarity
        similarity = calculate_text_similarity(extracted_text, ground_truth)
        
        print(f"📊 Similarity: {similarity:.2f}%")
        print(f"⏱️  Total time: {init_time + extraction_time:.2f}s")
        
        return {
            'engine': engine_name,
            'preprocessing': preprocessing,
            'similarity': similarity,
            'init_time': init_time,
            'extraction_time': extraction_time,
            'total_time': init_time + extraction_time,
            'extracted_text': extracted_text,
            'text_length': len(extracted_text),
            'success': True
        }
        
    except Exception as e:
        print(f"❌ Error testing {engine_name}: {str(e)}")
        return {
            'engine': engine_name,
            'preprocessing': preprocessing,
            'similarity': 0.0,
            'init_time': 0.0,
            'extraction_time': 0.0,
            'total_time': 0.0,
            'extracted_text': '',
            'text_length': 0,
            'success': False,
            'error': str(e)
        }

def run_comprehensive_test():
    """Run comprehensive Apple Vision vs EasyOCR comparison test."""
    
    # Test configuration
    test_image = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518.HEIC"
    ground_truth = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518.txt"
    language = "en"
    
    print("🔬 Apple Vision vs EasyOCR Comprehensive Test")
    print("=" * 60)
    print(f"Test image: {test_image}")
    print(f"Ground truth: {ground_truth}")
    print(f"Language: {language}")
    
    # Check if files exist
    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}")
        return
    
    if not os.path.exists(ground_truth):
        print(f"❌ Ground truth not found: {ground_truth}")
        return
    
    # Convert HEIC to PNG for testing
    print("\n🔄 Converting HEIC to PNG...")
    png_path = test_image.replace('.HEIC', '_test.png')
    
    try:
        # Use sips to convert HEIC to PNG
        import subprocess
        result = subprocess.run(['sips', '-s', 'format', 'png', test_image, '--out', png_path], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed to convert HEIC: {result.stderr}")
            return
        print(f"✅ Converted to: {png_path}")
    except Exception as e:
        print(f"❌ Error converting HEIC: {str(e)}")
        return
    
    # Test configurations
    test_configs = [
        {'engine': 'easyocr', 'preprocessing': False},
        {'engine': 'easyocr', 'preprocessing': True},
        {'engine': 'apple_vision', 'preprocessing': False},
        {'engine': 'apple_vision', 'preprocessing': True},
    ]
    
    results = []
    
    # Run all tests
    for config in test_configs:
        result = test_ocr_engine(
            engine_name=config['engine'],
            image_path=png_path,
            ground_truth_path=ground_truth,
            language=language,
            preprocessing=config['preprocessing']
        )
        results.append(result)
    
    # Clean up test PNG
    try:
        os.unlink(png_path)
    except:
        pass
    
    # Display results summary
    print(f"\n{'='*80}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    
    print(f"{'Engine':<12} {'Preprocessing':<12} {'Similarity':<10} {'Time (s)':<10} {'Success':<8}")
    print("-" * 80)
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{result['engine']:<12} {str(result['preprocessing']):<12} {result['similarity']:<10.2f} {result['total_time']:<10.2f} {status:<8}")
    
    # Find best results
    successful_results = [r for r in results if r['success']]
    
    if successful_results:
        best_overall = max(successful_results, key=lambda x: x['similarity'])
        fastest = min(successful_results, key=lambda x: x['total_time'])
        
        print(f"\n🏆 BEST OVERALL ACCURACY:")
        print(f"   {best_overall['engine'].upper()} {'with' if best_overall['preprocessing'] else 'without'} preprocessing")
        print(f"   Similarity: {best_overall['similarity']:.2f}%")
        print(f"   Time: {best_overall['total_time']:.2f}s")
        
        print(f"\n⚡ FASTEST:")
        print(f"   {fastest['engine'].upper()} {'with' if fastest['preprocessing'] else 'without'} preprocessing")
        print(f"   Similarity: {fastest['similarity']:.2f}%")
        print(f"   Time: {fastest['total_time']:.2f}s")
        
        # Compare engines directly
        easyocr_results = [r for r in successful_results if r['engine'] == 'easyocr']
        apple_vision_results = [r for r in successful_results if r['engine'] == 'apple_vision']
        
        if easyocr_results and apple_vision_results:
            print(f"\n🔍 ENGINE COMPARISON:")
            
            # Compare without preprocessing
            easyocr_no_prep = next((r for r in easyocr_results if not r['preprocessing']), None)
            apple_vision_no_prep = next((r for r in apple_vision_results if not r['preprocessing']), None)
            
            if easyocr_no_prep and apple_vision_no_prep:
                print(f"\n   Without Preprocessing:")
                print(f"   EasyOCR:     {easyocr_no_prep['similarity']:.2f}% ({easyocr_no_prep['total_time']:.2f}s)")
                print(f"   Apple Vision: {apple_vision_no_prep['similarity']:.2f}% ({apple_vision_no_prep['total_time']:.2f}s)")
                
                if easyocr_no_prep['similarity'] > apple_vision_no_prep['similarity']:
                    diff = easyocr_no_prep['similarity'] - apple_vision_no_prep['similarity']
                    print(f"   🏆 EasyOCR is {diff:.2f}% more accurate")
                elif apple_vision_no_prep['similarity'] > easyocr_no_prep['similarity']:
                    diff = apple_vision_no_prep['similarity'] - easyocr_no_prep['similarity']
                    print(f"   🏆 Apple Vision is {diff:.2f}% more accurate")
                else:
                    print(f"   🤝 Both engines have equal accuracy")
            
            # Compare with preprocessing
            easyocr_with_prep = next((r for r in easyocr_results if r['preprocessing']), None)
            apple_vision_with_prep = next((r for r in apple_vision_results if r['preprocessing']), None)
            
            if easyocr_with_prep and apple_vision_with_prep:
                print(f"\n   With Preprocessing:")
                print(f"   EasyOCR:     {easyocr_with_prep['similarity']:.2f}% ({easyocr_with_prep['total_time']:.2f}s)")
                print(f"   Apple Vision: {apple_vision_with_prep['similarity']:.2f}% ({apple_vision_with_prep['total_time']:.2f}s)")
                
                if easyocr_with_prep['similarity'] > apple_vision_with_prep['similarity']:
                    diff = easyocr_with_prep['similarity'] - apple_vision_with_prep['similarity']
                    print(f"   🏆 EasyOCR is {diff:.2f}% more accurate")
                elif apple_vision_with_prep['similarity'] > easyocr_with_prep['similarity']:
                    diff = apple_vision_with_prep['similarity'] - easyocr_with_prep['similarity']
                    print(f"   🏆 Apple Vision is {diff:.2f}% more accurate")
                else:
                    print(f"   🤝 Both engines have equal accuracy")
    
    # Save detailed results
    results_file = "apple_vision_vs_easyocr_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    run_comprehensive_test()
