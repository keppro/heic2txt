#!/usr/bin/env python3
"""
Batch processing example with custom words for Apple Vision OCR.

This script demonstrates how to process multiple images with domain-specific
custom words to improve OCR accuracy.
"""

import os
import time
from pathlib import Path
from typing import List, Dict
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from utils.image_utils import convert_heic_to_pil, preprocess_image_for_ocr
from utils.text_utils import save_text_to_file

def get_terraform_custom_words() -> List[str]:
    """Get custom words optimized for Terraform/infrastructure content."""
    return [
        # Terraform core terms
        "terraform", "provider", "resource", "variable", "output", "module",
        "data", "locals", "for_each", "count", "depends_on", "lifecycle",
        "backend", "state", "workspace", "environment", "configuration",
        
        # AWS services and resources
        "aws", "ec2", "s3", "rds", "lambda", "apigateway", "cloudfront",
        "cloudwatch", "iam", "kms", "secrets", "ssm", "parameter", "store",
        "vpc", "subnet", "security_group", "route_table", "internet_gateway",
        "nat_gateway", "load_balancer", "autoscaling", "elasticache",
        "redshift", "dynamodb", "sqs", "sns", "eventbridge", "stepfunctions",
        "ecs", "eks", "fargate", "ecr", "codebuild", "codepipeline",
        "codedeploy", "cloudformation", "systems_manager", "config",
        
        # File extensions and formats
        "tf", "tfvars", "tfstate", "hcl", "json", "yaml", "yml", "toml",
        
        # Common technical terms
        "infrastructure", "deployment", "production", "staging", "development",
        "monitoring", "logging", "metrics", "alerting", "backup", "recovery",
        "scalability", "availability", "reliability", "performance",
        "security", "compliance", "governance", "policy", "access",
        "authentication", "authorization", "encryption", "decryption",
        "network", "firewall", "bastion", "nat", "vpn", "directconnect"
    ]

def process_image_with_custom_words(image_path: str, custom_words: List[str], 
                                  output_dir: str) -> Dict:
    """Process a single image with custom words."""
    
    print(f"📷 Processing: {os.path.basename(image_path)}")
    
    # Convert HEIC to PIL Image
    image = convert_heic_to_pil(image_path)
    if image is None:
        return {"success": False, "error": "Could not convert HEIC image"}
    
    # Preprocess image
    preprocessed_image = preprocess_image_for_ocr(image)
    
    # Initialize OCR with custom words
    ocr = AppleVisionOCREngine(language="en", custom_words=custom_words)
    
    # Extract text
    start_time = time.time()
    text = ocr.extract_text(preprocessed_image)
    processing_time = time.time() - start_time
    
    if not text.strip():
        return {"success": False, "error": "No text detected"}
    
    # Save text to file
    output_file = Path(output_dir) / f"{Path(image_path).stem}.txt"
    success = save_text_to_file(text, str(output_file))
    
    if not success:
        return {"success": False, "error": "Could not save text file"}
    
    # Count custom words found
    words_found = []
    for word in custom_words:
        if word.lower() in text.lower():
            words_found.append(word)
    
    return {
        "success": True,
        "text_length": len(text),
        "processing_time": processing_time,
        "words_found": words_found,
        "output_file": str(output_file)
    }

def batch_process_with_custom_words(input_dir: str, output_dir: str, 
                                  custom_words: List[str]) -> None:
    """Process all HEIC files in a directory with custom words."""
    
    print("🚀 Batch Processing with Custom Words")
    print("=" * 50)
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📝 Custom words: {len(custom_words)} terms")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Find all HEIC files
    input_path = Path(input_dir)
    heic_files = list(input_path.glob("*.heic")) + list(input_path.glob("*.HEIC"))
    
    if not heic_files:
        print("❌ No HEIC files found in input directory")
        return
    
    print(f"📊 Found {len(heic_files)} HEIC files to process")
    print()
    
    # Process files
    successful = 0
    failed = 0
    total_time = 0
    total_words_found = 0
    
    for i, heic_file in enumerate(heic_files, 1):
        print(f"[{i}/{len(heic_files)}] Processing: {heic_file.name}")
        
        result = process_image_with_custom_words(str(heic_file), custom_words, output_dir)
        
        if result["success"]:
            successful += 1
            total_time += result["processing_time"]
            total_words_found += len(result["words_found"])
            
            print(f"   ✅ Success: {result['text_length']} chars, "
                  f"{result['processing_time']:.3f}s, "
                  f"{len(result['words_found'])} custom words found")
            
            if result["words_found"]:
                print(f"   🎯 Found: {', '.join(result['words_found'][:5])}")
                if len(result["words_found"]) > 5:
                    print(f"   ... and {len(result['words_found']) - 5} more")
        else:
            failed += 1
            print(f"   ❌ Failed: {result['error']}")
        
        print()
    
    # Summary
    print("📊 Batch Processing Summary")
    print("=" * 50)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total time: {total_time:.2f}s")
    print(f"⏱️  Average time per file: {total_time/len(heic_files):.3f}s")
    print(f"🎯 Total custom words found: {total_words_found}")
    print(f"📁 Text files saved to: {output_dir}")

def main():
    """Main function to run batch processing with custom words."""
    
    # Configuration
    input_directory = "/Volumes/UserDisk/Users/keppro/Pictures/TF"
    output_directory = "/Volumes/UserDisk/Users/keppro/Pictures/TF/custom_words_output"
    
    # Get custom words for Terraform content
    custom_words = get_terraform_custom_words()
    
    print("🎯 Apple Vision OCR with Custom Words")
    print("=" * 50)
    print(f"📝 Using {len(custom_words)} Terraform/Infrastructure custom words")
    print(f"   Sample: {', '.join(custom_words[:10])}...")
    print()
    
    # Run batch processing
    batch_process_with_custom_words(input_directory, output_directory, custom_words)
    
    print()
    print("💡 Tips for using custom words:")
    print("-" * 40)
    print("• Custom words help Apple Vision recognize domain-specific terms")
    print("• They work best with technical content and proper nouns")
    print("• Keep the list focused on your specific use case")
    print("• Update custom words based on your content analysis")
    print("• Test with a few images first to optimize your word list")

if __name__ == "__main__":
    main()
