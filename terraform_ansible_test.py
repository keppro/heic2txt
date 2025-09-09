#!/usr/bin/env python3
"""
Test Terraform and Ansible custom words combinations.

This script focuses on testing combinations that include both Terraform and Ansible
to find the optimal configuration for infrastructure and automation content.
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

def test_terraform_ansible_combinations(image_path: str):
    """Test combinations that include both Terraform and Ansible."""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print("🧪 Terraform + Ansible Custom Words Test")
    print("=" * 70)
    print(f"📷 Image: {os.path.basename(image_path)}")
    print()
    
    # Load image
    image = Image.open(image_path)
    print(f"📐 Image size: {image.size}")
    print()
    
    # Test combinations that include both Terraform and Ansible
    test_cases = [
        ("Baseline (No Custom Words)", []),
        ("Terraform Only", get_terraform_custom_words()),
        ("Ansible Only", get_ansible_custom_words()),
        ("Terraform + Ansible", get_domain_specific_words(['terraform', 'ansible'])),
        ("Terraform + Ansible + AWS", get_domain_specific_words(['terraform', 'ansible', 'aws'])),
        ("Terraform + Ansible + PostgreSQL", get_domain_specific_words(['terraform', 'ansible', 'postgresql'])),
        ("Terraform + Ansible + MySQL", get_domain_specific_words(['terraform', 'ansible', 'mysql'])),
        ("Terraform + Ansible + AWS + PostgreSQL", get_domain_specific_words(['terraform', 'ansible', 'aws', 'postgresql'])),
        ("Terraform + Ansible + AWS + MySQL", get_domain_specific_words(['terraform', 'ansible', 'aws', 'mysql'])),
        ("Terraform + Ansible + PostgreSQL + MySQL", get_domain_specific_words(['terraform', 'ansible', 'postgresql', 'mysql'])),
        ("All Domains (Including Terraform + Ansible)", get_combined_custom_words())
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
            print(f"   📝 Found: {', '.join(words_found[:8])}")
            if len(words_found) > 8:
                print(f"   ... and {len(words_found) - 8} more")
        print()
    
    # Analysis
    print("📊 Terraform + Ansible Analysis")
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
    print(f"{'Test Name':<40} {'Words':<6} {'Found':<6} {'Time':<8} {'Efficiency':<10} {'Improvement':<12}")
    print("-" * 70)
    
    baseline = results[0]  # No custom words
    for result in results:
        efficiency = result['words_found_count'] / result['custom_words_count'] if result['custom_words_count'] > 0 else 0
        time_improvement = ((baseline['processing_time'] - result['processing_time']) / baseline['processing_time']) * 100
        
        print(f"{result['test_name']:<40} {result['custom_words_count']:<6} {result['words_found_count']:<6} "
              f"{result['processing_time']:.3f}s {efficiency:.3f}      {time_improvement:+.1f}%")
    
    print()
    
    # Focus on Terraform + Ansible combinations
    print("🎯 Terraform + Ansible Focused Analysis")
    print("-" * 70)
    
    terraform_ansible_results = [r for r in results if 'Terraform + Ansible' in r['test_name'] or r['test_name'] == 'All Domains (Including Terraform + Ansible)']
    
    print("Terraform + Ansible Combinations:")
    for result in terraform_ansible_results:
        efficiency = result['words_found_count'] / result['custom_words_count'] if result['custom_words_count'] > 0 else 0
        time_improvement = ((baseline['processing_time'] - result['processing_time']) / baseline['processing_time']) * 100
        
        print(f"  • {result['test_name']}")
        print(f"    Efficiency: {efficiency:.3f} ({result['words_found_count']}/{result['custom_words_count']} words)")
        print(f"    Time improvement: {time_improvement:+.1f}%")
        print(f"    Processing time: {result['processing_time']:.3f}s")
        print()
    
    # Top recommendations
    print("🏆 Top Recommendations (Including Terraform + Ansible)")
    print("-" * 70)
    
    # Sort by efficiency
    efficiency_sorted = sorted(results[1:], key=lambda x: x['words_found_count'] / x['custom_words_count'] if x['custom_words_count'] > 0 else 0, reverse=True)
    
    for i, result in enumerate(efficiency_sorted[:5], 1):
        efficiency = result['words_found_count'] / result['custom_words_count'] if result['custom_words_count'] > 0 else 0
        time_improvement = ((baseline['processing_time'] - result['processing_time']) / baseline['processing_time']) * 100
        
        print(f"{i}. {result['test_name']}")
        print(f"   Efficiency: {efficiency:.3f} ({result['words_found_count']}/{result['custom_words_count']} words found)")
        print(f"   Time improvement: {time_improvement:+.1f}%")
        print(f"   Processing time: {result['processing_time']:.3f}s")
        print()
    
    # Custom words breakdown
    print("📝 Custom Words Breakdown")
    print("-" * 70)
    
    # Analyze which domains contribute most to the Terraform + Ansible combinations
    terraform_words = get_terraform_custom_words()
    ansible_words = get_ansible_custom_words()
    aws_words = get_aws_custom_words()
    postgresql_words = get_postgresql_custom_words()
    mysql_words = get_mysql_custom_words()
    
    print("Domain word counts:")
    print(f"  • Terraform: {len(terraform_words)} words")
    print(f"  • Ansible: {len(ansible_words)} words")
    print(f"  • AWS: {len(aws_words)} words")
    print(f"  • PostgreSQL: {len(postgresql_words)} words")
    print(f"  • MySQL: {len(mysql_words)} words")
    print()
    
    # Show sample words from each domain
    print("Sample words from each domain:")
    print(f"  • Terraform: {', '.join(terraform_words[:8])}...")
    print(f"  • Ansible: {', '.join(ansible_words[:8])}...")
    print(f"  • AWS: {', '.join(aws_words[:8])}...")
    print(f"  • PostgreSQL: {', '.join(postgresql_words[:8])}...")
    print(f"  • MySQL: {', '.join(mysql_words[:8])}...")
    print()
    
    # Final recommendation
    print("💡 Final Recommendation")
    print("-" * 70)
    
    best_terraform_ansible = max(terraform_ansible_results, key=lambda x: x['words_found_count'] / x['custom_words_count'] if x['custom_words_count'] > 0 else 0)
    
    print(f"Best Terraform + Ansible combination: {best_terraform_ansible['test_name']}")
    print(f"  • Custom words: {best_terraform_ansible['custom_words_count']}")
    print(f"  • Words found: {best_terraform_ansible['words_found_count']}")
    print(f"  • Efficiency: {best_terraform_ansible['words_found_count'] / best_terraform_ansible['custom_words_count']:.3f}")
    print(f"  • Time improvement: {((baseline['processing_time'] - best_terraform_ansible['processing_time']) / baseline['processing_time']) * 100:+.1f}%")
    print()
    
    print("Code implementation:")
    if "All Domains" in best_terraform_ansible['test_name']:
        print("```python")
        print("custom_words = get_combined_custom_words()")
        print("```")
    else:
        domains = []
        if "Terraform" in best_terraform_ansible['test_name']:
            domains.append("'terraform'")
        if "Ansible" in best_terraform_ansible['test_name']:
            domains.append("'ansible'")
        if "AWS" in best_terraform_ansible['test_name']:
            domains.append("'aws'")
        if "PostgreSQL" in best_terraform_ansible['test_name']:
            domains.append("'postgresql'")
        if "MySQL" in best_terraform_ansible['test_name']:
            domains.append("'mysql'")
        
        print("```python")
        print(f"custom_words = get_domain_specific_words([{', '.join(domains)}])")
        print("```")
    
    return results

def main():
    """Main function to run the Terraform + Ansible test."""
    
    # Test with existing image
    test_image = "/Volumes/UserDisk/Users/keppro/Pictures/TF/apple_vision_output/tmp_141i5ic_preprocessed_rotated_180deg.png"
    
    if os.path.exists(test_image):
        results = test_terraform_ansible_combinations(test_image)
        
        print("🎯 Summary")
        print("=" * 70)
        print("The test shows the best Terraform + Ansible combinations")
        print("for your infrastructure and automation content.")
        print("Use the recommended configuration for optimal performance.")
        
    else:
        print("❌ Test image not found. Please ensure the image exists:")
        print(f"   {test_image}")

if __name__ == "__main__":
    main()
