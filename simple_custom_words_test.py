#!/usr/bin/env python3
"""
Simple test script to demonstrate custom words improvement with Apple Vision OCR.
"""

import os
import time
from PIL import Image
from utils.text_utils import calculate_text_similarity
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine

def test_custom_words():
    """Test custom words with a simple example."""
    
    # Use an existing PNG file from the batch processing
    image_path = "~/Pictures/TF/apple_vision_output/tmp_141i5ic_preprocessed_rotated_180deg.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print("🧪 Testing Custom Words with Apple Vision OCR")
    print("=" * 50)
    
    # Load image
    print(f"📷 Loading image: {os.path.basename(image_path)}")
    image = Image.open(image_path)
    print(f"📐 Image size: {image.size}")
    print()
    
    # Define custom words for technical content
    custom_words = [
        # Common technical terms
        "terraform", "provider", "resource", "variable", "output", "module",
        "aws", "configuration", "infrastructure", "deployment", "environment",
        "security", "group", "subnet", "vpc", "instance", "database",
        "api", "gateway", "lambda", "cloudfront", "s3", "rds", "ec2",
        "json", "yaml", "hcl", "tf", "tfvars", "tfstate",
        "function", "method", "class", "object", "array", "string",
        "error", "warning", "debug", "log", "console", "import",
        "cloud", "serverless", "microservices", "rest", "graphql",
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch"
    ]
    
    print(f"📝 Custom words: {len(custom_words)} technical terms")
    print(f"   Sample: {', '.join(custom_words[:10])}...")
    print()
    
    # Test 1: Without custom words
    print("🔍 Test 1: WITHOUT custom words")
    print("-" * 30)
    
    start_time = time.time()
    ocr_basic = AppleVisionOCREngine(language="en", custom_words=None)
    text_basic = ocr_basic.extract_text(image)
    time_basic = time.time() - start_time
    
    print(f"⏱️  Time: {time_basic:.3f}s")
    print(f"📄 Length: {len(text_basic)} characters")
    print(f"📝 Preview: {text_basic[:150]}...")
    print()
    
    # Test 2: With custom words
    print("🔍 Test 2: WITH custom words")
    print("-" * 30)
    
    start_time = time.time()
    ocr_enhanced = AppleVisionOCREngine(language="en", custom_words=custom_words)
    text_enhanced = ocr_enhanced.extract_text(image)
    time_enhanced = time.time() - start_time
    
    print(f"⏱️  Time: {time_enhanced:.3f}s")
    print(f"📄 Length: {len(text_enhanced)} characters")
    print(f"📝 Preview: {text_enhanced[:150]}...")
    print()
    
    # Test 3: Dynamic update
    print("🔍 Test 3: Dynamic custom words update")
    print("-" * 30)
    
    ocr_dynamic = AppleVisionOCREngine(language="en", custom_words=None)
    
    # Without custom words
    start_time = time.time()
    text_dynamic_1 = ocr_dynamic.extract_text(image)
    time_dynamic_1 = time.time() - start_time
    
    print(f"📝 Without custom words: {len(text_dynamic_1)} chars in {time_dynamic_1:.3f}s")
    
    # Update with custom words
    ocr_dynamic.update_custom_words(custom_words)
    
    # With custom words
    start_time = time.time()
    text_dynamic_2 = ocr_dynamic.extract_text(image)
    time_dynamic_2 = time.time() - start_time
    
    print(f"📝 With custom words: {len(text_dynamic_2)} chars in {time_dynamic_2:.3f}s")
    print()
    
    # Analysis
    print("📊 Analysis")
    print("=" * 50)
    
    similarity = calculate_text_similarity(text_basic, text_enhanced)
    
    print(f"📈 Text length comparison:")
    print(f"   Basic:     {len(text_basic)} characters")
    print(f"   Enhanced:  {len(text_enhanced)} characters")
    print(f"   Difference: {len(text_enhanced) - len(text_basic):+d} characters")
    print()
    
    print(f"⏱️  Time comparison:")
    print(f"   Basic:     {time_basic:.3f}s")
    print(f"   Enhanced:  {time_enhanced:.3f}s")
    print(f"   Difference: {time_enhanced - time_basic:+.3f}s")
    print()
    
    print(f"🔍 Text similarity: {similarity:.2f}%")
    print()
    
    # Check for technical terms
    technical_terms_found = []
    for term in custom_words[:20]:
        if term.lower() in text_enhanced.lower():
            technical_terms_found.append(term)
    
    print(f"🎯 Technical terms detected: {len(technical_terms_found)}")
    if technical_terms_found:
        print(f"   Found: {', '.join(technical_terms_found)}")
    print()
    
    # Show the difference in text content
    print("📝 Text Content Comparison:")
    print("-" * 50)
    print("BASIC (without custom words):")
    print(text_basic[:300])
    print()
    print("ENHANCED (with custom words):")
    print(text_enhanced[:300])
    
    return {
        'text_basic': text_basic,
        'text_enhanced': text_enhanced,
        'time_basic': time_basic,
        'time_enhanced': time_enhanced,
        'similarity': similarity,
        'technical_terms_found': technical_terms_found
    }

if __name__ == "__main__":
    results = test_custom_words()
