#!/usr/bin/env python3
"""
Guide and examples for using custom words with Apple Vision OCR.

This script demonstrates how to effectively use custom words to improve
OCR recognition accuracy for different types of content.
"""

import os
import time
from typing import List, Dict
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from utils.text_utils import calculate_text_similarity

def get_terraform_custom_words() -> List[str]:
    """Get custom words for Terraform/infrastructure content."""
    return [
        # Terraform core
        "terraform", "provider", "resource", "variable", "output", "module",
        "data", "locals", "for_each", "count", "depends_on", "lifecycle",
        
        # AWS services
        "aws", "ec2", "s3", "rds", "lambda", "apigateway", "cloudfront",
        "cloudwatch", "iam", "kms", "secrets", "ssm", "parameter", "store",
        "vpc", "subnet", "security_group", "route_table", "internet_gateway",
        "nat_gateway", "load_balancer", "autoscaling", "elasticache",
        "redshift", "dynamodb", "sqs", "sns", "eventbridge", "stepfunctions",
        
        # File extensions and formats
        "tf", "tfvars", "tfstate", "hcl", "json", "yaml", "yml",
        
        # Common technical terms
        "configuration", "infrastructure", "deployment", "environment",
        "production", "staging", "development", "testing", "monitoring",
        "logging", "metrics", "alerting", "backup", "recovery", "disaster",
        "scalability", "availability", "reliability", "performance",
        "security", "compliance", "governance", "policy", "access",
        "authentication", "authorization", "encryption", "decryption"
    ]

def get_programming_custom_words() -> List[str]:
    """Get custom words for programming/code content."""
    return [
        # Programming languages
        "python", "javascript", "typescript", "java", "go", "rust", "swift",
        "kotlin", "php", "ruby", "cpp", "csharp", "scala", "clojure",
        
        # Frameworks and libraries
        "react", "vue", "angular", "nodejs", "express", "django", "flask",
        "spring", "hibernate", "jpa", "jdbc", "mybatis", "struts",
        "laravel", "symfony", "codeigniter", "cakephp", "zend",
        "rails", "sinatra", "hanami", "grape", "padrino",
        "tornado", "fastapi", "bottle", "cherrypy", "pyramid",
        
        # Common programming terms
        "function", "method", "class", "object", "array", "string", "integer",
        "boolean", "null", "undefined", "exception", "error", "warning",
        "debug", "trace", "log", "console", "print", "return", "import",
        "export", "require", "include", "namespace", "package", "library",
        "framework", "api", "rest", "graphql", "soap", "grpc", "websocket",
        "http", "https", "tcp", "udp", "ip", "dns", "ssl", "tls"
    ]

def get_medical_custom_words() -> List[str]:
    """Get custom words for medical/healthcare content."""
    return [
        # Medical terms
        "patient", "diagnosis", "treatment", "therapy", "medication", "dosage",
        "prescription", "symptoms", "condition", "disease", "disorder",
        "syndrome", "infection", "inflammation", "tumor", "cancer", "benign",
        "malignant", "metastasis", "remission", "relapse", "prognosis",
        
        # Body systems
        "cardiovascular", "respiratory", "digestive", "nervous", "muscular",
        "skeletal", "endocrine", "immune", "lymphatic", "urinary", "reproductive",
        
        # Medical procedures
        "surgery", "biopsy", "radiology", "mri", "ct", "xray", "ultrasound",
        "endoscopy", "colonoscopy", "mammography", "echocardiogram",
        
        # Medications
        "antibiotic", "antiviral", "antifungal", "analgesic", "antipyretic",
        "antihistamine", "anticoagulant", "diuretic", "beta", "blocker",
        "ace", "inhibitor", "statin", "insulin", "cortisol", "adrenaline"
    ]

def get_legal_custom_words() -> List[str]:
    """Get custom words for legal content."""
    return [
        # Legal terms
        "plaintiff", "defendant", "attorney", "counsel", "judge", "court",
        "jury", "trial", "hearing", "motion", "objection", "sustained",
        "overruled", "evidence", "testimony", "witness", "deposition",
        "subpoena", "warrant", "indictment", "arraignment", "plea",
        "guilty", "not", "guilty", "nolo", "contendere", "verdict",
        "sentence", "probation", "parole", "appeal", "conviction",
        
        # Legal documents
        "contract", "agreement", "lease", "deed", "will", "trust",
        "power", "of", "attorney", "affidavit", "petition", "complaint",
        "answer", "counterclaim", "cross", "claim", "third", "party",
        "interrogatories", "requests", "for", "production", "admissions"
    ]

def test_custom_words_effectiveness(image_path: str, custom_words: List[str], 
                                  content_type: str) -> Dict:
    """Test the effectiveness of custom words on a specific image."""
    
    if not os.path.exists(image_path):
        return {"error": f"Image not found: {image_path}"}
    
    print(f"🧪 Testing {content_type} custom words")
    print(f"📷 Image: {os.path.basename(image_path)}")
    print(f"📝 Custom words: {len(custom_words)} terms")
    print("-" * 50)
    
    # Load image
    from PIL import Image
    image = Image.open(image_path)
    
    # Test without custom words
    start_time = time.time()
    ocr_basic = AppleVisionOCREngine(language="en", custom_words=None)
    text_basic = ocr_basic.extract_text(image)
    time_basic = time.time() - start_time
    
    # Test with custom words
    start_time = time.time()
    ocr_enhanced = AppleVisionOCREngine(language="en", custom_words=custom_words)
    text_enhanced = ocr_enhanced.extract_text(image)
    time_enhanced = time.time() - start_time
    
    # Calculate metrics
    similarity = calculate_text_similarity(text_basic, text_enhanced)
    
    # Count custom words found
    words_found = []
    for word in custom_words:
        if word.lower() in text_enhanced.lower():
            words_found.append(word)
    
    results = {
        "content_type": content_type,
        "text_basic": text_basic,
        "text_enhanced": text_enhanced,
        "time_basic": time_basic,
        "time_enhanced": time_enhanced,
        "similarity": similarity,
        "words_found": words_found,
        "length_basic": len(text_basic),
        "length_enhanced": len(text_enhanced)
    }
    
    print(f"📊 Results:")
    print(f"   Text length: {len(text_basic)} → {len(text_enhanced)} chars")
    print(f"   Processing time: {time_basic:.3f}s → {time_enhanced:.3f}s")
    print(f"   Similarity: {similarity:.2f}%")
    print(f"   Custom words found: {len(words_found)}/{len(custom_words)}")
    if words_found:
        print(f"   Found: {', '.join(words_found[:10])}")
    print()
    
    return results

def demonstrate_custom_words_usage():
    """Demonstrate how to use custom words effectively."""
    
    print("🎯 Custom Words Guide for Apple Vision OCR")
    print("=" * 60)
    print()
    
    print("📚 What are custom words?")
    print("-" * 30)
    print("Custom words are domain-specific terms that help Apple Vision OCR")
    print("recognize text more accurately. They work by providing context")
    print("about expected vocabulary in your documents.")
    print()
    
    print("🔧 How to use custom words:")
    print("-" * 30)
    print("1. Initialize with custom words:")
    print("   ocr = AppleVisionOCREngine(language='en', custom_words=['terraform', 'aws'])")
    print()
    print("2. Update custom words dynamically:")
    print("   ocr.update_custom_words(['new', 'words', 'list'])")
    print()
    print("3. Clear custom words:")
    print("   ocr.update_custom_words([])")
    print()
    
    print("💡 Best practices:")
    print("-" * 30)
    print("✅ Include domain-specific terminology")
    print("✅ Add technical jargon and acronyms")
    print("✅ Include proper nouns and names")
    print("✅ Add file extensions and formats")
    print("✅ Include common abbreviations")
    print("✅ Keep the list focused and relevant")
    print("❌ Don't include too many generic words")
    print("❌ Don't include misspelled words")
    print("❌ Don't make the list too long (>100 words)")
    print()
    
    print("📊 Expected improvements:")
    print("-" * 30)
    print("• Better recognition of technical terms")
    print("• Improved accuracy for domain-specific content")
    print("• Faster processing (usually)")
    print("• More consistent results")
    print("• Better handling of acronyms and abbreviations")
    print()
    
    # Test with different custom word sets
    test_image = "~/Pictures/TF/apple_vision_output/tmp_141i5ic_preprocessed_rotated_180deg.png"
    
    if os.path.exists(test_image):
        print("🧪 Testing different custom word sets:")
        print("=" * 60)
        
        # Test Terraform words
        terraform_words = get_terraform_custom_words()
        test_custom_words_effectiveness(test_image, terraform_words, "Terraform")
        
        # Test programming words
        programming_words = get_programming_custom_words()
        test_custom_words_effectiveness(test_image, programming_words, "Programming")
        
        # Test with no custom words
        test_custom_words_effectiveness(test_image, [], "No Custom Words")
    
    print("🎯 Example implementations:")
    print("=" * 60)
    
    print("For Terraform documents:")
    print("```python")
    print("terraform_words = ['terraform', 'provider', 'resource', 'aws', 'ec2', 's3']")
    print("ocr = AppleVisionOCREngine(language='en', custom_words=terraform_words)")
    print("```")
    print()
    
    print("For code documentation:")
    print("```python")
    print("code_words = ['function', 'class', 'method', 'api', 'json', 'python']")
    print("ocr = AppleVisionOCREngine(language='en', custom_words=code_words)")
    print("```")
    print()
    
    print("For medical documents:")
    print("```python")
    print("medical_words = ['patient', 'diagnosis', 'treatment', 'medication']")
    print("ocr = AppleVisionOCREngine(language='en', custom_words=medical_words)")
    print("```")

if __name__ == "__main__":
    demonstrate_custom_words_usage()
