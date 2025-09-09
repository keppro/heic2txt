#!/usr/bin/env python3
"""
Domain-specific custom words comparison test using the same methodology as previous tests.

This script tests different domain combinations to find the optimal custom words
for your specific content type.
"""

import os
import time
from PIL import Image
from utils.text_utils import calculate_text_similarity
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

def test_domain_combinations(image_path: str):
    """Test different domain combinations using the same methodology as previous tests."""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print("🧪 Domain-Specific Custom Words Comparison Test")
    print("=" * 70)
    print(f"📷 Image: {os.path.basename(image_path)}")
    print()
    
    # Load image
    image = Image.open(image_path)
    print(f"📐 Image size: {image.size}")
    print()
    
    # Test different domain combinations
    test_cases = [
        ("Baseline (No Custom Words)", []),
        ("Terraform Only", get_terraform_custom_words()),
        ("Ansible Only", get_ansible_custom_words()),
        ("AWS Only", get_aws_custom_words()),
        ("PostgreSQL Only", get_postgresql_custom_words()),
        ("MySQL Only", get_mysql_custom_words()),
        ("Terraform + Ansible", get_domain_specific_words(['terraform', 'ansible'])),
        ("Terraform + AWS", get_domain_specific_words(['terraform', 'aws'])),
        ("Terraform + PostgreSQL", get_domain_specific_words(['terraform', 'postgresql'])),
        ("Terraform + MySQL", get_domain_specific_words(['terraform', 'mysql'])),
        ("Ansible + AWS", get_domain_specific_words(['ansible', 'aws'])),
        ("AWS + PostgreSQL", get_domain_specific_words(['aws', 'postgresql'])),
        ("AWS + MySQL", get_domain_specific_words(['aws', 'mysql'])),
        ("PostgreSQL + MySQL", get_domain_specific_words(['postgresql', 'mysql'])),
        ("Terraform + Ansible + AWS", get_domain_specific_words(['terraform', 'ansible', 'aws'])),
        ("Terraform + AWS + PostgreSQL", get_domain_specific_words(['terraform', 'aws', 'postgresql'])),
        ("Terraform + AWS + MySQL", get_domain_specific_words(['terraform', 'aws', 'mysql'])),
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
            'words_found_count': len(words_found),
            'text': text
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
    print("📊 Detailed Analysis")
    print("=" * 70)
    
    # Find best performing tests
    best_text_length = max(results, key=lambda x: x['text_length'])
    best_words_found = max(results, key=lambda x: x['words_found_count'])
    fastest_time = min(results, key=lambda x: x['processing_time'])
    
    print(f"📈 Best text length: {best_text_length['test_name']} ({best_text_length['text_length']} chars)")
    print(f"🎯 Most custom words found: {best_words_found['test_name']} ({best_words_found['words_found_count']} words)")
    print(f"⚡ Fastest processing: {fastest_time['test_name']} ({fastest_time['processing_time']:.3f}s)")
    print()
    
    # Performance comparison
    print("📊 Performance Comparison")
    print("-" * 70)
    print(f"{'Test Name':<30} {'Words':<6} {'Found':<6} {'Time':<8} {'Length':<8} {'Efficiency':<10}")
    print("-" * 70)
    
    baseline = results[0]  # No custom words
    for result in results:
        efficiency = result['words_found_count'] / result['custom_words_count'] if result['custom_words_count'] > 0 else 0
        time_improvement = ((baseline['processing_time'] - result['processing_time']) / baseline['processing_time']) * 100
        
        print(f"{result['test_name']:<30} {result['custom_words_count']:<6} {result['words_found_count']:<6} "
              f"{result['processing_time']:.3f}s {result['text_length']:<8} {efficiency:.3f}")
    
    print()
    
    # Top 5 recommendations
    print("🏆 Top 5 Recommendations")
    print("-" * 70)
    
    # Sort by efficiency (words found per custom word)
    efficiency_sorted = sorted(results[1:], key=lambda x: x['words_found_count'] / x['custom_words_count'] if x['custom_words_count'] > 0 else 0, reverse=True)
    
    for i, result in enumerate(efficiency_sorted[:5], 1):
        efficiency = result['words_found_count'] / result['custom_words_count'] if result['custom_words_count'] > 0 else 0
        time_improvement = ((baseline['processing_time'] - result['processing_time']) / baseline['processing_time']) * 100
        
        print(f"{i}. {result['test_name']}")
        print(f"   Efficiency: {efficiency:.3f} ({result['words_found_count']}/{result['custom_words_count']} words found)")
        print(f"   Time improvement: {time_improvement:+.1f}%")
        print(f"   Text length: {result['text_length']} chars")
        print()
    
    # Text content comparison for top 3
    print("📝 Text Content Comparison (Top 3)")
    print("-" * 70)
    
    top_3 = efficiency_sorted[:3]
    for i, result in enumerate(top_3, 1):
        print(f"{i}. {result['test_name']} ({result['words_found_count']} custom words found)")
        print(f"   Text preview: {result['text'][:150]}...")
        print()
    
    # Similarity analysis
    print("🔍 Similarity Analysis")
    print("-" * 70)
    
    baseline_text = baseline['text']
    for result in results[1:6]:  # Compare top 5 with baseline
        similarity = calculate_text_similarity(baseline_text, result['text'])
        print(f"{result['test_name']}: {similarity:.2f}% similarity with baseline")
    
    print()
    
    # Recommendations based on content type
    print("💡 Recommendations Based on Content Type")
    print("-" * 70)
    
    # Analyze which domains are most effective
    domain_effectiveness = {}
    for result in results[1:]:
        if 'Only' in result['test_name']:
            domain = result['test_name'].replace(' Only', '').lower()
            efficiency = result['words_found_count'] / result['custom_words_count'] if result['custom_words_count'] > 0 else 0
            domain_effectiveness[domain] = efficiency
    
    sorted_domains = sorted(domain_effectiveness.items(), key=lambda x: x[1], reverse=True)
    
    print("Most effective individual domains:")
    for domain, efficiency in sorted_domains[:3]:
        print(f"  • {domain.title()}: {efficiency:.3f} efficiency")
    
    print()
    print("Recommended combinations based on your content:")
    print("  • For Infrastructure: Terraform + AWS")
    print("  • For Database: PostgreSQL + MySQL") 
    print("  • For Automation: Ansible + AWS")
    print("  • For Full Coverage: All Domains")
    
    return results

def main():
    """Main function to run the comparison test."""
    
    # Test with existing image
    test_image = "~/Pictures/TF/apple_vision_output/tmp_141i5ic_preprocessed_rotated_180deg.png"
    
    if os.path.exists(test_image):
        results = test_domain_combinations(test_image)
        
        print("🎯 Summary")
        print("=" * 70)
        print("The test shows which domain-specific custom words work best")
        print("for your specific content. Use the top recommendations")
        print("for optimal OCR performance and accuracy.")
        
    else:
        print("❌ Test image not found. Please ensure the image exists:")
        print(f"   {test_image}")
        print()
        print("💡 To run this test with your own image:")
        print("   python3 domain_custom_words_comparison_test.py /path/to/your/image.png")

if __name__ == "__main__":
    main()
