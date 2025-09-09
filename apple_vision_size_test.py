#!/usr/bin/env python3
"""
Apple Vision Image Size Limitation Test
======================================

This script tests Apple Vision OCR with different image sizes to determine
if there are any size limitations or performance impacts.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from PIL import Image
import tempfile

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from heic2txt import HEIC2TXT
from utils.text_utils import calculate_text_similarity


def create_test_images():
    """Create test images of different sizes."""
    print("🖼️  Creating test images of different sizes...")
    
    # Test sizes: small, medium, large, very large
    test_sizes = [
        (500, 500, "small"),
        (1000, 1000, "medium"), 
        (2000, 2000, "large"),
        (4000, 4000, "very_large"),
        (6000, 6000, "extra_large"),
        (8000, 8000, "huge")
    ]
    
    test_images = []
    
    for width, height, name in test_sizes:
        # Create a simple test image with text
        img = Image.new('RGB', (width, height), color='white')
        
        # Add some text-like patterns (simplified)
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw some text patterns
        text = f"TEST IMAGE {name.upper()}\nSize: {width}x{height}\nApple Vision OCR Test"
        
        # Calculate text position (center)
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 6  # Approximate
            text_height = 20
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill='black', font=font)
        
        # Save test image
        filename = f"test_{name}_{width}x{height}.png"
        img.save(filename)
        test_images.append((filename, width, height, name))
        print(f"   ✅ Created {filename} ({width}x{height})")
    
    return test_images


def test_apple_vision_with_size(image_path, width, height, name):
    """Test Apple Vision OCR with a specific image size."""
    print(f"\n🔬 Testing {name} image ({width}x{height})...")
    
    try:
        # Load image
        image = Image.open(image_path)
        print(f"   📏 Image loaded: {image.size}")
        
        # Test Apple Vision
        start_time = time.time()
        
        heic2txt = HEIC2TXT(engine='apple_vision', language='en')
        text = heic2txt.ocr.extract_text(image)
        
        processing_time = time.time() - start_time
        
        print(f"   ⏱️  Processing time: {processing_time:.3f}s")
        print(f"   📝 Text extracted: {len(text)} characters")
        print(f"   📄 Text preview: {text[:100]}..." if text else "   📄 Text: (none)")
        
        return {
            'size': f"{width}x{height}",
            'name': name,
            'width': width,
            'height': height,
            'text_length': len(text),
            'processing_time': processing_time,
            'success': len(text) > 0,
            'text': text
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {
            'size': f"{width}x{height}",
            'name': name,
            'width': width,
            'height': height,
            'text_length': 0,
            'processing_time': 0,
            'success': False,
            'error': str(e)
        }


def test_with_different_max_dimensions():
    """Test Apple Vision with different maximum processing dimensions."""
    print("\n🔧 Testing with different maximum processing dimensions...")
    
    from Vision import VNRecognizeTextRequest
    from Foundation import NSURL
    import tempfile
    
    # Create a large test image
    large_img = Image.new('RGB', (4000, 4000), color='white')
    from PIL import ImageDraw
    draw = ImageDraw.Draw(large_img)
    draw.text((100, 100), "LARGE IMAGE TEST\n4000x4000 pixels\nApple Vision OCR", fill='black')
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        large_img.save(temp_file.name, 'PNG')
        temp_path = temp_file.name
    
    # Test different maximum dimensions
    max_dims = [0, 1000, 2000, 4000, 6000, 8000]
    
    for max_dim in max_dims:
        print(f"\n   Testing with max dimension: {max_dim}")
        
        try:
            # Create request with custom max dimension
            request = VNRecognizeTextRequest.alloc().init()
            if max_dim > 0:
                request.setMaximumProcessingDimensionOnTheLongSide_(max_dim)
            
            # Test with the large image
            file_url = NSURL.fileURLWithPath_(temp_path)
            from Vision import VNImageRequestHandler
            request_handler = VNImageRequestHandler.alloc().initWithURL_options_(file_url, None)
            
            start_time = time.time()
            error = None
            success = request_handler.performRequests_error_([request], error)
            processing_time = time.time() - start_time
            
            if success:
                text_results = request.results()
                text = ""
                if text_results:
                    for observation in text_results:
                        if hasattr(observation, 'topCandidates_'):
                            candidates = observation.topCandidates_(1)
                            if candidates and len(candidates) > 0:
                                candidate = candidates[0]
                                if hasattr(candidate, 'string'):
                                    text += candidate.string() + "\n"
                
                print(f"     ✅ Success: {len(text)} chars in {processing_time:.3f}s")
                print(f"     📄 Text: {text[:50]}..." if text else "     📄 Text: (none)")
            else:
                print(f"     ❌ Failed to process image")
                
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    # Cleanup
    os.unlink(temp_path)


def main():
    """Main test function."""
    print("🔬 Apple Vision Image Size Limitation Test")
    print("=" * 60)
    
    # Create test images
    test_images = create_test_images()
    
    print(f"\n🧪 Testing {len(test_images)} different image sizes...")
    
    results = []
    
    # Test each image size
    for image_path, width, height, name in test_images:
        result = test_apple_vision_with_size(image_path, width, height, name)
        results.append(result)
    
    # Print results summary
    print("\n" + "=" * 80)
    print("📊 SIZE LIMITATION TEST RESULTS")
    print("=" * 80)
    print(f"{'Size':<15} {'Name':<12} {'Success':<8} {'Time (s)':<10} {'Text Length':<12} {'Notes'}")
    print("-" * 80)
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        notes = ""
        if result['width'] > 4000 or result['height'] > 4000:
            notes = "Large size"
        if 'error' in result:
            notes = f"Error: {result['error'][:20]}..."
        
        print(f"{result['size']:<15} {result['name']:<12} {status:<8} "
              f"{result['processing_time']:<10.3f} {result['text_length']:<12} {notes}")
    
    # Test with different maximum processing dimensions
    test_with_different_max_dimensions()
    
    # Analysis
    print("\n📈 ANALYSIS:")
    
    successful_sizes = [r for r in results if r['success']]
    failed_sizes = [r for r in results if not r['success']]
    
    if successful_sizes:
        max_successful_size = max(successful_sizes, key=lambda x: max(x['width'], x['height']))
        print(f"   ✅ Largest successful size: {max_successful_size['size']}")
    
    if failed_sizes:
        min_failed_size = min(failed_sizes, key=lambda x: max(x['width'], x['height']))
        print(f"   ❌ Smallest failed size: {min_failed_size['size']}")
    
    # Performance analysis
    if successful_sizes:
        times = [r['processing_time'] for r in successful_sizes]
        print(f"   ⏱️  Processing time range: {min(times):.3f}s - {max(times):.3f}s")
        
        # Check if processing time scales with image size
        sizes = [max(r['width'], r['height']) for r in successful_sizes]
        if len(sizes) > 1:
            import numpy as np
            correlation = np.corrcoef(sizes, times)[0, 1]
            print(f"   📊 Size-time correlation: {correlation:.3f}")
    
    # Cleanup test images
    print("\n🧹 Cleaning up test images...")
    for image_path, _, _, _ in test_images:
        try:
            os.unlink(image_path)
            print(f"   🗑️  Deleted {image_path}")
        except:
            pass


if __name__ == "__main__":
    main()
