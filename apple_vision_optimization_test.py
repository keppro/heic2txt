#!/usr/bin/env python3
"""
Apple Vision OCR Parameter Optimization Test
===========================================

This script systematically tests different Apple Vision OCR parameters
to find the optimal configuration for maximum accuracy and performance.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from PIL import Image
from typing import Dict, List, Tuple, Any
from itertools import product

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


class OptimizedAppleVisionOCREngine:
    """Apple Vision OCR Engine with configurable parameters."""
    
    def __init__(self, 
                 recognition_level: int = 1,
                 uses_language_correction: bool = True,
                 minimum_text_height: float = 0.0,
                 custom_words: List[str] = None,
                 automatically_detects_language: bool = False,
                 uses_cpu_only: bool = False,
                 language: str = "en"):
        """
        Initialize Apple Vision OCR with configurable parameters.
        
        Args:
            recognition_level: 0=Fast, 1=Accurate
            uses_language_correction: Enable language correction
            minimum_text_height: Minimum text height (0.0 = no minimum)
            custom_words: List of custom words to recognize
            automatically_detects_language: Auto-detect language
            uses_cpu_only: Force CPU-only processing
            language: Language code
        """
        self.recognition_level = recognition_level
        self.uses_language_correction = uses_language_correction
        self.minimum_text_height = minimum_text_height
        self.custom_words = custom_words or []
        self.automatically_detects_language = automatically_detects_language
        self.uses_cpu_only = uses_cpu_only
        self.language = language
        
        # Import Vision framework
        from Vision import VNRecognizeTextRequest, VNImageRequestHandler
        from Foundation import NSURL
        
        # Configure the text recognition request
        self.text_request = VNRecognizeTextRequest.alloc().init()
        self.text_request.setRecognitionLevel_(recognition_level)
        self.text_request.setUsesLanguageCorrection_(uses_language_correction)
        self.text_request.setMinimumTextHeight_(minimum_text_height)
        self.text_request.setAutomaticallyDetectsLanguage_(automatically_detects_language)
        self.text_request.setUsesCPUOnly_(uses_cpu_only)
        
        # Set custom words if provided
        if custom_words:
            self.text_request.setCustomWords_(custom_words)
        
        # Set language if not auto-detecting
        if not automatically_detects_language and language != "en":
            try:
                self.text_request.setRecognitionLanguages_([language])
            except Exception as e:
                print(f"⚠️  Warning: Could not set language to {language}: {e}")
    
    def extract_text(self, image: Image.Image) -> str:
        """Extract text from image using configured parameters."""
        import tempfile
        from Vision import VNImageRequestHandler
        from Foundation import NSURL
        
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
            print(f"❌ Apple Vision OCR error: {e}")
            return ""


def test_parameter_combination(params: Dict, image: Image.Image, ground_truth: str) -> Dict:
    """Test a specific parameter combination."""
    print(f"\n🔬 Testing: {params}")
    
    start_time = time.time()
    
    try:
        # Create engine with these parameters
        engine = OptimizedAppleVisionOCREngine(**params)
        
        # Extract text
        text = engine.extract_text(image)
        
        # Calculate similarity
        similarity = calculate_text_similarity(ground_truth, text) if text else 0.0
        
        # Calculate time
        total_time = time.time() - start_time
        
        result = {
            **params,
            'text_length': len(text),
            'similarity': similarity,
            'time': total_time,
            'success': len(text) > 0,
            'extracted_text': text[:100] + "..." if len(text) > 100 else text
        }
        
        print(f"   📊 Similarity: {similarity:.2f}%")
        print(f"   ⏱️  Time: {total_time:.3f}s")
        print(f"   📝 Text: {text[:50]}..." if text else "   📝 Text: (none)")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {
            **params,
            'text_length': 0,
            'similarity': 0.0,
            'time': 0.0,
            'success': False,
            'error': str(e)
        }


def main():
    """Main optimization function."""
    print("🔬 Apple Vision OCR Parameter Optimization Test")
    print("=" * 60)
    
    # Test configuration
    heic_path = "~/Pictures/TF/IMG_7518.HEIC"
    ground_truth_path = "~/Pictures/TF/IMG_7518.txt"
    
    print(f"Test image: {heic_path}")
    print(f"Ground truth: {ground_truth_path}")
    
    # Convert HEIC to PNG
    print("\n🔄 Converting HEIC to PNG...")
    png_path = heic_path.replace('.HEIC', '_optimization_test.png')
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
    
    # Prepare image with preprocessing (since it worked best)
    print("\n🔄 Applying preprocessing...")
    preprocessed_path = preprocess_image_for_ocr(png_path, "/tmp", save_images=True)
    image = Image.open(preprocessed_path)
    print(f"🖼️  Preprocessed image size: {image.size}")
    
    # Define parameter ranges to test
    parameter_ranges = {
        'recognition_level': [0, 1],  # Fast vs Accurate
        'uses_language_correction': [True, False],
        'minimum_text_height': [0.0, 0.01, 0.02, 0.05],  # Different minimum heights
        'automatically_detects_language': [True, False],
        'uses_cpu_only': [True, False],
        'custom_words': [None, ['TF', 'IMG', '7518']],  # Custom words from the image
        'language': ['en', 'en_US']
    }
    
    # Generate all combinations
    param_names = list(parameter_ranges.keys())
    param_values = list(parameter_ranges.values())
    
    print(f"\n🧪 Testing {len(list(product(*param_values)))} parameter combinations...")
    
    results = []
    best_similarity = 0.0
    best_params = None
    
    # Test each combination
    for i, combination in enumerate(product(*param_values)):
        params = dict(zip(param_names, combination))
        
        print(f"\n--- Test {i+1}/{len(list(product(*param_values)))} ---")
        
        result = test_parameter_combination(params, image, ground_truth)
        results.append(result)
        
        # Track best result
        if result['similarity'] > best_similarity:
            best_similarity = result['similarity']
            best_params = params.copy()
            print(f"   🏆 NEW BEST: {best_similarity:.2f}%")
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 OPTIMIZATION RESULTS SUMMARY")
    print("=" * 80)
    
    # Sort by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    print(f"\n🏆 TOP 10 RESULTS:")
    print(f"{'Rank':<4} {'Similarity':<10} {'Time (s)':<8} {'Success':<8} {'Parameters'}")
    print("-" * 80)
    
    for i, result in enumerate(results[:10]):
        status = "✅" if result['success'] else "❌"
        params_str = ", ".join([f"{k}={v}" for k, v in result.items() 
                               if k not in ['similarity', 'time', 'success', 'text_length', 'extracted_text', 'error']])
        print(f"{i+1:<4} {result['similarity']:<10.2f} {result['time']:<8.3f} {status:<8} {params_str}")
    
    # Best overall result
    if best_params:
        print(f"\n🎯 BEST CONFIGURATION:")
        print(f"   Similarity: {best_similarity:.2f}%")
        print(f"   Parameters:")
        for key, value in best_params.items():
            print(f"     {key}: {value}")
    
    # Parameter analysis
    print(f"\n📈 PARAMETER ANALYSIS:")
    
    # Analyze each parameter's impact
    for param_name in param_names:
        if param_name in ['custom_words', 'language']:  # Skip complex parameters
            continue
            
        print(f"\n   {param_name.upper()}:")
        
        # Group results by this parameter
        param_groups = {}
        for result in results:
            value = result.get(param_name, 'N/A')
            if value not in param_groups:
                param_groups[value] = []
            param_groups[value].append(result['similarity'])
        
        # Calculate average similarity for each value
        for value, similarities in param_groups.items():
            avg_similarity = sum(similarities) / len(similarities)
            print(f"     {value}: {avg_similarity:.2f}% (n={len(similarities)})")
    
    # Save detailed results
    results_file = "apple_vision_optimization_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    # Cleanup
    try:
        os.unlink(png_path)
        if png_path != preprocessed_path:
            os.unlink(preprocessed_path)
    except:
        pass


if __name__ == "__main__":
    main()
