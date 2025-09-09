#!/usr/bin/env python3
"""
Test script to verify Apple Vision GPU acceleration is working.
"""

import time
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from PIL import Image
import tempfile
import os

def test_gpu_acceleration():
    """Test if Apple Vision is using GPU acceleration."""
    
    print("🧪 Testing Apple Vision GPU Acceleration")
    print("=" * 50)
    
    # Create a simple test image with text
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a white image with black text
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 30), "GPU Test Text", fill='black', font=font)
    
    # Save test image
    test_image_path = "/tmp/gpu_test.png"
    img.save(test_image_path)
    
    print(f"📷 Created test image: {test_image_path}")
    
    # Test with CPU only
    print("\n🔍 Testing with CPU only...")
    ocr_cpu = AppleVisionOCREngine(language="en", custom_words=None)
    
    # Override to force CPU
    ocr_cpu.text_request.setUsesCPUOnly_(True)
    print("🔧 Forced CPU-only mode")
    
    start_time = time.time()
    text_cpu = ocr_cpu.extract_text(img)
    cpu_time = time.time() - start_time
    
    print(f"⏱️  CPU time: {cpu_time:.3f}s")
    print(f"📝 CPU result: '{text_cpu}'")
    
    # Test with GPU acceleration
    print("\n🚀 Testing with GPU acceleration...")
    ocr_gpu = AppleVisionOCREngine(language="en", custom_words=None)
    
    # Ensure GPU is enabled
    ocr_gpu.text_request.setUsesCPUOnly_(False)
    print("🔧 GPU acceleration enabled")
    
    start_time = time.time()
    text_gpu = ocr_gpu.extract_text(img)
    gpu_time = time.time() - start_time
    
    print(f"⏱️  GPU time: {gpu_time:.3f}s")
    print(f"📝 GPU result: '{text_gpu}'")
    
    # Compare results
    print("\n📊 Comparison:")
    print(f"   CPU time: {cpu_time:.3f}s")
    print(f"   GPU time: {gpu_time:.3f}s")
    
    if gpu_time < cpu_time:
        speedup = cpu_time / gpu_time
        print(f"   🚀 GPU is {speedup:.2f}x faster!")
    else:
        print(f"   ⚠️  GPU is not faster (might be using CPU anyway)")
    
    # Test multiple images to see if GPU is consistently faster
    print("\n🔄 Testing multiple images for consistency...")
    
    gpu_times = []
    cpu_times = []
    
    for i in range(5):
        # Create slightly different test image
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 30), f"Test {i+1}", fill='black', font=font)
        
        # CPU test
        start_time = time.time()
        ocr_cpu.extract_text(img)
        cpu_times.append(time.time() - start_time)
        
        # GPU test
        start_time = time.time()
        ocr_gpu.extract_text(img)
        gpu_times.append(time.time() - start_time)
    
    avg_cpu = sum(cpu_times) / len(cpu_times)
    avg_gpu = sum(gpu_times) / len(gpu_times)
    
    print(f"   Average CPU time: {avg_cpu:.3f}s")
    print(f"   Average GPU time: {avg_gpu:.3f}s")
    
    if avg_gpu < avg_cpu:
        speedup = avg_cpu / avg_gpu
        print(f"   🚀 GPU is consistently {speedup:.2f}x faster!")
    else:
        print(f"   ⚠️  GPU is not consistently faster")
    
    # Check Vision framework capabilities
    print("\n🔍 Checking Vision framework capabilities...")
    try:
        from Vision import VNRecognizeTextRequest
        request = VNRecognizeTextRequest.alloc().init()
        
        # Check if CPU-only is supported
        request.setUsesCPUOnly_(True)
        print("   ✅ CPU-only mode supported")
        
        # Check if GPU acceleration is supported
        request.setUsesCPUOnly_(False)
        print("   ✅ GPU acceleration supported")
        
        # Check recognition levels
        request.setRecognitionLevel_(0)  # Fast
        print("   ✅ Fast recognition level supported")
        
        request.setRecognitionLevel_(1)  # Accurate
        print("   ✅ Accurate recognition level supported")
        
    except Exception as e:
        print(f"   ❌ Error checking capabilities: {e}")
    
    # Clean up
    try:
        os.unlink(test_image_path)
    except:
        pass
    
    print("\n✅ GPU acceleration test completed")

if __name__ == "__main__":
    test_gpu_acceleration()
