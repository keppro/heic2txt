#!/usr/bin/env python3
"""
Test domain-specific custom words with Apple Vision OCR.

This script demonstrates how to use the comprehensive custom word lists
for Terraform, Ansible, AWS, PostgreSQL, and MySQL content.
"""

import os
import time
from PIL import Image
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from domain_specific_custom_words import (
    get_terraform_custom_words,
    get_ansible_custom_words, 
    get_aws_custom_words,
    get_postgresql_custom_words,
    get_mysql_custom_words,
    get_domain_specific_words,
    get_combined_custom_words
)

def test_domain_custom_words(image_path: str):
    """Test different domain-specific custom word sets."""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print("🧪 Testing Domain-Specific Custom Words")
    print("=" * 60)
    print(f"📷 Image: {os.path.basename(image_path)}")
    print()
    
    # Load image
    image = Image.open(image_path)
    print(f"📐 Image size: {image.size}")
    print()
    
    # Test different domain combinations
    test_cases = [
        ("No Custom Words", []),
        ("Terraform Only", get_terraform_custom_words()),
        ("Ansible Only", get_ansible_custom_words()),
        ("AWS Only", get_aws_custom_words()),
        ("PostgreSQL Only", get_postgresql_custom_words()),
        ("MySQL Only", get_mysql_custom_words()),
        ("Terraform + AWS", get_domain_specific_words(['terraform', 'aws'])),
        ("All Domains", get_combined_custom_words())
    ]
    
    results = []
    
    for test_name, custom_words in test_cases:
        print(f"🔍 Testing: {test_name}")
        print(f"📝 Custom words: {len(custom_words)} terms")
        
        # Initialize OCR with custom words
        start_time = time.time()
        ocr = AppleVisionOCREngine(language='en', custom_words=custom_words)
        text = ocr.extract_text(image)
        processing_time = time.time() - start_time
        
        # Count custom words found
        words_found = []
        if custom_words:
            for word in custom_words:
                if word.lower() in text.lower():
                    words_found.append(word)
        
        result = {
            'test_name': test_name,
            'custom_words_count': len(custom_words),
            'text_length': len(text),
            'processing_time': processing_time,
            'words_found': words_found,
            'words_found_count': len(words_found)
        }
        results.append(result)
        
        print(f"   ⏱️  Time: {processing_time:.3f}s")
        print(f"   📄 Text length: {len(text)} characters")
        print(f"   🎯 Custom words found: {len(words_found)}/{len(custom_words)}")
        if words_found:
            print(f"   📝 Found: {', '.join(words_found[:5])}")
            if len(words_found) > 5:
                print(f"   ... and {len(words_found) - 5} more")
        print()
    
    # Analysis
    print("📊 Analysis")
    print("=" * 60)
    
    # Find best performing test
    best_text_length = max(results, key=lambda x: x['text_length'])
    best_words_found = max(results, key=lambda x: x['words_found_count'])
    fastest_time = min(results, key=lambda x: x['processing_time'])
    
    print(f"📈 Best text length: {best_text_length['test_name']} ({best_text_length['text_length']} chars)")
    print(f"🎯 Most custom words found: {best_words_found['test_name']} ({best_words_found['words_found_count']} words)")
    print(f"⚡ Fastest processing: {fastest_time['test_name']} ({fastest_time['processing_time']:.3f}s)")
    print()
    
    # Show text samples
    print("📝 Text Content Samples:")
    print("-" * 60)
    for result in results[:3]:  # Show first 3 results
        print(f"{result['test_name']}:")
        print(f"  {result['text_length']} chars, {result['words_found_count']} custom words found")
        print(f"  Preview: {result['text_length'] and results[0]['text_length'] and results[0]['text_length'] and '...' or 'No text'}")
        print()

def demonstrate_usage():
    """Demonstrate how to use domain-specific custom words."""
    
    print("🎯 Domain-Specific Custom Words Usage Guide")
    print("=" * 60)
    print()
    
    print("📚 Available Domains:")
    print("-" * 30)
    print("• Terraform: Infrastructure as Code")
    print("• Ansible: Configuration Management")
    print("• AWS: Amazon Web Services")
    print("• PostgreSQL: Database Management")
    print("• MySQL: Database Management")
    print()
    
    print("🔧 Basic Usage:")
    print("-" * 30)
    print("```python")
    print("from domain_specific_custom_words import get_domain_specific_words")
    print("from ocr_engines.apple_vision_ocr import AppleVisionOCREngine")
    print("")
    print("# Get words for specific domains")
    print("custom_words = get_domain_specific_words(['terraform', 'aws'])")
    print("ocr = AppleVisionOCREngine(language='en', custom_words=custom_words)")
    print("```")
    print()
    
    print("🎯 Domain-Specific Examples:")
    print("-" * 30)
    
    # Terraform example
    terraform_words = get_terraform_custom_words()
    print(f"Terraform ({len(terraform_words)} words):")
    print(f"  Sample: {', '.join(terraform_words[:8])}...")
    print()
    
    # AWS example
    aws_words = get_aws_custom_words()
    print(f"AWS ({len(aws_words)} words):")
    print(f"  Sample: {', '.join(aws_words[:8])}...")
    print()
    
    # Combined example
    combined_words = get_domain_specific_words(['terraform', 'ansible', 'aws'])
    print(f"Terraform + Ansible + AWS ({len(combined_words)} words):")
    print(f"  Sample: {', '.join(combined_words[:8])}...")
    print()
    
    print("💡 Best Practices:")
    print("-" * 30)
    print("✅ Choose domains relevant to your content")
    print("✅ Start with 1-2 domains, add more as needed")
    print("✅ Test with sample images first")
    print("✅ Monitor performance and accuracy")
    print("❌ Don't use all domains if not needed")
    print("❌ Avoid too many custom words (>500)")
    print()

if __name__ == "__main__":
    # Demonstrate usage
    demonstrate_usage()
    
    # Test with existing image if available
    test_image = "~/Pictures/TF/apple_vision_output/tmp_141i5ic_preprocessed_rotated_180deg.png"
    
    if os.path.exists(test_image):
        test_domain_custom_words(test_image)
    else:
        print("ℹ️  No test image available. Run with a sample image to test custom words.")
        print(f"   Expected image: {test_image}")
