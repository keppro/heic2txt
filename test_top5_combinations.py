#!/usr/bin/env python3
"""
Test the top 5 custom word combinations on all images in the TF directory.

This script runs the batch processor with the 5 best performing custom word
combinations identified from our previous tests.
"""

import os
import time
import subprocess
from pathlib import Path
from domain_specific_custom_words import get_domain_specific_words

def get_top5_combinations():
    """Get the top 5 custom word combinations based on our tests."""
    return [
        {
            'name': 'Terraform_Ansible_PostgreSQL',
            'description': 'Terraform + Ansible + PostgreSQL (Best Efficiency)',
            'domains': ['terraform', 'ansible', 'postgresql'],
            'expected_efficiency': 0.051,
            'expected_words': 27
        },
        {
            'name': 'Terraform_Ansible_AWS_PostgreSQL',
            'description': 'Terraform + Ansible + AWS + PostgreSQL (Most Words Found)',
            'domains': ['terraform', 'ansible', 'aws', 'postgresql'],
            'expected_efficiency': 0.050,
            'expected_words': 38
        },
        {
            'name': 'Terraform_Ansible_AWS',
            'description': 'Terraform + Ansible + AWS (Good Balance)',
            'domains': ['terraform', 'ansible', 'aws'],
            'expected_efficiency': 0.045,
            'expected_words': 19
        },
        {
            'name': 'Terraform_Ansible_AWS_MySQL',
            'description': 'Terraform + Ansible + AWS + MySQL (Comprehensive)',
            'domains': ['terraform', 'ansible', 'aws', 'mysql'],
            'expected_efficiency': 0.037,
            'expected_words': 39
        },
        {
            'name': 'Terraform_Ansible',
            'description': 'Terraform + Ansible (Fastest Processing)',
            'domains': ['terraform', 'ansible'],
            'expected_efficiency': 0.034,
            'expected_words': 6
        }
    ]

def run_batch_processing(combination, input_dir, output_dir):
    """Run batch processing with a specific custom word combination."""
    
    print(f"🚀 Processing with {combination['description']}")
    print(f"📝 Domains: {', '.join(combination['domains'])}")
    print(f"🎯 Expected efficiency: {combination['expected_efficiency']}")
    print(f"📊 Expected words found: {combination['expected_words']}")
    print("-" * 60)
    
    # Get custom words for this combination
    custom_words = get_domain_specific_words(combination['domains'])
    print(f"📝 Custom words: {len(custom_words)} terms")
    print(f"   Sample: {', '.join(custom_words[:10])}...")
    print()
    
    # Create output directory
    full_output_dir = f"{output_dir}_{combination['name']}"
    Path(full_output_dir).mkdir(parents=True, exist_ok=True)
    
    # Run batch processing
    start_time = time.time()
    
    try:
        # Use the custom batch processor with custom words
        cmd = [
            'python3', 'heic2txt_batch_custom.py',
            input_dir,
            full_output_dir,
            combination['name']
        ]
        
        print(f"🔄 Running: {' '.join(cmd)}")
        print()
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        processing_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Successfully processed in {processing_time:.2f}s")
            
            # Count output files
            txt_files = list(Path(full_output_dir).glob('*.txt'))
            png_files = list(Path(full_output_dir).glob('*.png'))
            
            print(f"📄 Text files created: {len(txt_files)}")
            print(f"🖼️  PNG files created: {len(png_files)}")
            
            # Show sample results
            if txt_files:
                sample_file = txt_files[0]
                with open(sample_file, 'r') as f:
                    sample_text = f.read()
                
                print(f"📝 Sample text from {sample_file.name}:")
                print(f"   Length: {len(sample_text)} characters")
                print(f"   Preview: {sample_text[:100]}...")
                
                # Count custom words found in sample
                words_found = []
                for word in custom_words:
                    if word.lower() in sample_text.lower():
                        words_found.append(word)
                
                print(f"🎯 Custom words found in sample: {len(words_found)}/{len(custom_words)}")
                if words_found:
                    print(f"   Found: {', '.join(words_found[:8])}")
                    if len(words_found) > 8:
                        print(f"   ... and {len(words_found) - 8} more")
            
            return {
                'success': True,
                'processing_time': processing_time,
                'txt_files': len(txt_files),
                'png_files': len(png_files),
                'words_found': len(words_found) if 'words_found' in locals() else 0,
                'output_dir': full_output_dir
            }
            
        else:
            print(f"❌ Error processing: {result.stderr}")
            return {
                'success': False,
                'error': result.stderr,
                'processing_time': processing_time
            }
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Processing timed out after 5 minutes")
        return {
            'success': False,
            'error': 'Timeout',
            'processing_time': 300
        }
    except Exception as e:
        print(f"❌ Exception: {e}")
        return {
            'success': False,
            'error': str(e),
            'processing_time': time.time() - start_time
        }

def main():
    """Main function to test all top 5 combinations."""
    
    print("🧪 Testing Top 5 Custom Word Combinations")
    print("=" * 70)
    
    input_dir = "/Volumes/UserDisk/Users/keppro/Pictures/TF"
    base_output_dir = "/Volumes/UserDisk/Users/keppro/Pictures/TF/top5_test"
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        return
    
    # Count input images
    heic_files = list(Path(input_dir).glob("*.heic")) + list(Path(input_dir).glob("*.HEIC"))
    print(f"📷 Found {len(heic_files)} HEIC images to process")
    print()
    
    if len(heic_files) == 0:
        print("❌ No HEIC files found in input directory")
        return
    
    # Get top 5 combinations
    combinations = get_top5_combinations()
    
    print(f"🎯 Testing {len(combinations)} combinations:")
    for i, combo in enumerate(combinations, 1):
        print(f"  {i}. {combo['description']}")
    print()
    
    # Test each combination
    results = []
    
    for i, combination in enumerate(combinations, 1):
        print(f"🔍 Test {i}/{len(combinations)}: {combination['name']}")
        print("=" * 70)
        
        result = run_batch_processing(combination, input_dir, base_output_dir)
        result['combination'] = combination
        results.append(result)
        
        print()
        print("✅ Test completed")
        print()
    
    # Summary
    print("📊 Final Summary")
    print("=" * 70)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed tests: {len(failed_tests)}/{len(results)}")
    print()
    
    if successful_tests:
        print("🏆 Top Performing Combinations:")
        print("-" * 50)
        
        # Sort by processing time (fastest first)
        successful_tests.sort(key=lambda x: x['processing_time'])
        
        for i, result in enumerate(successful_tests, 1):
            combo = result['combination']
            print(f"{i}. {combo['description']}")
            print(f"   Processing time: {result['processing_time']:.2f}s")
            print(f"   Text files: {result['txt_files']}")
            print(f"   PNG files: {result['png_files']}")
            print(f"   Custom words found: {result['words_found']}")
            print(f"   Output: {result['output_dir']}")
            print()
    
    if failed_tests:
        print("❌ Failed Tests:")
        print("-" * 50)
        for result in failed_tests:
            combo = result['combination']
            print(f"• {combo['description']}: {result.get('error', 'Unknown error')}")
        print()
    
    print("🎯 Recommendations:")
    print("-" * 50)
    print("1. Use the fastest processing combination for speed")
    print("2. Use the combination with most custom words found for accuracy")
    print("3. Use the combination with best efficiency for balance")
    print("4. Check the output directories for detailed results")
    print()
    print("📁 Output directories:")
    for result in successful_tests:
        print(f"  • {result['output_dir']}")

if __name__ == "__main__":
    main()
