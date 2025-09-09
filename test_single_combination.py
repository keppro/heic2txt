#!/usr/bin/env python3
"""
Test a single custom word combination on a subset of images.

This script tests one combination on the first 5 images to verify
the custom batch processor is working correctly.
"""

import os
import time
import subprocess
from pathlib import Path
from domain_specific_custom_words import get_domain_specific_words

def test_single_combination():
    """Test a single combination on a few images."""
    
    print("🧪 Testing Single Custom Word Combination")
    print("=" * 60)
    
    input_dir = "~/Pictures/TF"
    output_dir = "~/Pictures/TF/single_test"
    
    # Get custom words for Terraform + Ansible + PostgreSQL
    custom_words = get_domain_specific_words(['terraform', 'ansible', 'postgresql'])
    
    print(f"📝 Custom words: {len(custom_words)} terms")
    print(f"   Sample: {', '.join(custom_words[:10])}...")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Find first 5 HEIC files
    input_path = Path(input_dir)
    heic_files = list(input_path.glob("*.heic")) + list(input_path.glob("*.HEIC"))
    test_files = heic_files[:5]  # Test only first 5 files
    
    print(f"📷 Testing with {len(test_files)} images:")
    for i, file in enumerate(test_files, 1):
        print(f"  {i}. {file.name}")
    print()
    
    # Process each file individually
    results = []
    
    for i, heic_file in enumerate(test_files, 1):
        print(f"🔍 Processing {i}/{len(test_files)}: {heic_file.name}")
        print("-" * 50)
        
        # Convert HEIC to PNG
        png_path = str(heic_file).replace('.heic', '.png').replace('.HEIC', '.png')
        
        try:
            from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
            from utils.text_utils import save_text_to_file
            from PIL import Image
            import subprocess
            
            # Convert HEIC to PNG using sips
            result = subprocess.run([
                'sips', '-s', 'format', 'png', str(heic_file), '--out', png_path
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"❌ HEIC conversion failed: {result.stderr}")
                results.append({"success": False, "error": "HEIC conversion failed"})
                continue
            
            # Use the original working preprocessing
            from utils.image_utils import preprocess_image_for_ocr
            preprocessed_path = preprocess_image_for_ocr(png_path, "/tmp", save_images=True)
            preprocessed_image = Image.open(preprocessed_path)
            
            # Initialize OCR with custom words
            ocr = AppleVisionOCREngine(language="en", custom_words=custom_words)
            
            # Test orientations
            print("🔄 Testing orientations: 0°, 90°, 180°, 270°...")
            
            orientations = [(0, "0°"), (90, "90°"), (180, "180°"), (270, "270°")]
            orientation_results = []
            
            for rotation, label in orientations:
                if rotation > 0:
                    rotated_image = preprocessed_image.rotate(-rotation, expand=True)
                else:
                    rotated_image = preprocessed_image
                
                text = ocr.extract_text_fast(rotated_image)
                meaningful_chars = len([c for c in text if c.isalnum()])
                orientation_results.append((meaningful_chars, text, rotation, label))
                
                print(f"   {label}: {meaningful_chars} meaningful characters")
            
            # Find best orientation
            best_result = max(orientation_results, key=lambda x: x[0])
            best_text = best_result[1]
            best_rotation = best_result[2]
            best_label = best_result[3]
            
            print(f"🎯 Best orientation: {best_label} ({best_result[0]} characters)")
            
            # Final text extraction
            if best_rotation > 0:
                final_image = preprocessed_image.rotate(-best_rotation, expand=True)
            else:
                final_image = preprocessed_image
            
            final_text = ocr.extract_text(final_image)
            
            if not final_text.strip():
                print("⚠️  No text detected")
                results.append({"success": False, "error": "No text detected"})
                continue
            
            # Save text to file
            output_file = Path(output_dir) / f"{heic_file.stem}.txt"
            success = save_text_to_file(final_text, str(output_file))
            
            if not success:
                print("❌ Could not save text file")
                results.append({"success": False, "error": "Could not save text file"})
                continue
            
            # Count custom words found
            words_found = []
            for word in custom_words:
                if word.lower() in final_text.lower():
                    words_found.append(word)
            
            print(f"✅ Success: {len(final_text)} chars, {len(words_found)} custom words found")
            print(f"📝 Found: {', '.join(words_found[:5])}")
            if len(words_found) > 5:
                print(f"   ... and {len(words_found) - 5} more")
            
            results.append({
                "success": True,
                "text_length": len(final_text),
                "words_found": words_found,
                "words_found_count": len(words_found),
                "best_orientation": best_rotation
            })
            
            # Clean up
            try:
                os.unlink(png_path)
                os.unlink(preprocessed_path)
            except:
                pass
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({"success": False, "error": str(e)})
        
        print()
    
    # Summary
    successful = [r for r in results if r.get("success", False)]
    failed = [r for r in results if not r.get("success", False)]
    
    print("📊 Test Summary")
    print("=" * 60)
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        total_words_found = sum(r["words_found_count"] for r in successful)
        avg_words_found = total_words_found / len(successful)
        avg_text_length = sum(r["text_length"] for r in successful) / len(successful)
        
        print(f"📊 Average text length: {avg_text_length:.0f} characters")
        print(f"🎯 Average custom words found: {avg_words_found:.1f}")
        print(f"📁 Output directory: {output_dir}")
        
        print("\n🏆 Results by file:")
        for i, result in enumerate(results):
            if result.get("success"):
                print(f"  {i+1}. {test_files[i].name}: {result['text_length']} chars, {result['words_found_count']} custom words")
            else:
                print(f"  {i+1}. {test_files[i].name}: FAILED - {result.get('error', 'Unknown error')}")
    
    if failed:
        print(f"\n❌ Failed files:")
        for i, result in enumerate(failed):
            if not result.get("success"):
                print(f"  • {test_files[i].name}: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_single_combination()
