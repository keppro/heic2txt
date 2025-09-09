#!/usr/bin/env python3
"""
Test script to demonstrate how custom words improve Apple Vision OCR recognition.

This script shows the difference between OCR with and without custom words
using a sample image from the TF directory.
"""

import os
import sys
import time
from PIL import Image
from utils.text_utils import calculate_text_similarity
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from utils.image_utils import preprocess_image_for_ocr

def test_custom_words_improvement():
    """Test how custom words improve OCR recognition."""
    
    # Sample image from TF directory
    image_path = "~/Pictures/TF/IMG_7518.HEIC"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print("🧪 Testing Custom Words Improvement with Apple Vision OCR")
    print("=" * 60)
    
    # Load and preprocess image
    print(f"📷 Loading image: {os.path.basename(image_path)}")
    from utils.image_utils import convert_heic_to_pil
    image = convert_heic_to_pil(image_path)
    if image is None:
        print(f"❌ Could not load image: {image_path}")
        return
    preprocessed_image = preprocess_image_for_ocr(image)
    
    # Define custom words based on common Terraform/technical terms
    # These are words that might appear in your technical documents
    custom_words = [
        # Terraform specific terms
        "terraform", "provider", "resource", "variable", "output", "module",
        "aws", "azurerm", "google", "kubernetes", "docker", "container",
        "instance", "security_group", "subnet", "vpc", "route_table",
        "load_balancer", "autoscaling", "cloudfront", "s3", "rds", "ec2",
        "lambda", "api_gateway", "cloudwatch", "iam", "kms", "secrets",
        
        # Technical terms
        "configuration", "infrastructure", "deployment", "environment",
        "production", "staging", "development", "testing", "monitoring",
        "logging", "metrics", "alerting", "backup", "recovery", "disaster",
        "scalability", "availability", "reliability", "performance",
        "security", "compliance", "governance", "policy", "access",
        "authentication", "authorization", "encryption", "decryption",
        
        # Common programming terms
        "function", "method", "class", "object", "array", "string", "integer",
        "boolean", "null", "undefined", "exception", "error", "warning",
        "debug", "trace", "log", "console", "print", "return", "import",
        "export", "require", "include", "namespace", "package", "library",
        
        # File extensions and formats
        "json", "yaml", "yml", "toml", "hcl", "tf", "tfvars", "tfstate",
        "md", "txt", "log", "csv", "xml", "html", "css", "js", "py", "go",
        "java", "cpp", "c", "php", "ruby", "rust", "swift", "kotlin",
        
        # Cloud and infrastructure terms
        "cloud", "serverless", "microservices", "api", "rest", "graphql",
        "database", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "kibana", "grafana", "prometheus", "jaeger", "zipkin", "consul",
        "vault", "nomad", "consul", "etcd", "zookeeper", "kafka", "rabbitmq"
    ]
    
    print(f"📝 Custom words list: {len(custom_words)} technical terms")
    print(f"   Sample: {', '.join(custom_words[:10])}...")
    print()
    
    # Test 1: Without custom words
    print("🔍 Test 1: Apple Vision OCR WITHOUT custom words")
    print("-" * 50)
    
    start_time = time.time()
    ocr_without_custom = AppleVisionOCREngine(language="en", custom_words=None)
    text_without_custom = ocr_without_custom.extract_text(preprocessed_image)
    time_without_custom = time.time() - start_time
    
    print(f"⏱️  Processing time: {time_without_custom:.3f}s")
    print(f"📄 Text length: {len(text_without_custom)} characters")
    print(f"📝 Text preview: {text_without_custom[:100]}...")
    print()
    
    # Test 2: With custom words
    print("🔍 Test 2: Apple Vision OCR WITH custom words")
    print("-" * 50)
    
    start_time = time.time()
    ocr_with_custom = AppleVisionOCREngine(language="en", custom_words=custom_words)
    text_with_custom = ocr_with_custom.extract_text(preprocessed_image)
    time_with_custom = time.time() - start_time
    
    print(f"⏱️  Processing time: {time_with_custom:.3f}s")
    print(f"📄 Text length: {len(text_with_custom)} characters")
    print(f"📝 Text preview: {text_with_custom[:100]}...")
    print()
    
    # Test 3: Dynamic custom words update
    print("🔍 Test 3: Dynamic custom words update")
    print("-" * 50)
    
    # Start with no custom words
    ocr_dynamic = AppleVisionOCREngine(language="en", custom_words=None)
    
    # Extract text without custom words
    start_time = time.time()
    text_dynamic_1 = ocr_dynamic.extract_text(preprocessed_image)
    time_dynamic_1 = time.time() - start_time
    
    print(f"📝 Without custom words: {len(text_dynamic_1)} chars in {time_dynamic_1:.3f}s")
    
    # Update with custom words
    ocr_dynamic.update_custom_words(custom_words)
    
    # Extract text with custom words
    start_time = time.time()
    text_dynamic_2 = ocr_dynamic.extract_text(preprocessed_image)
    time_dynamic_2 = time.time() - start_time
    
    print(f"📝 With custom words: {len(text_dynamic_2)} chars in {time_dynamic_2:.3f}s")
    print()
    
    # Analysis
    print("📊 Analysis")
    print("=" * 60)
    
    # Calculate similarity between results
    similarity = calculate_text_similarity(text_without_custom, text_with_custom)
    
    print(f"📈 Text length comparison:")
    print(f"   Without custom words: {len(text_without_custom)} characters")
    print(f"   With custom words:    {len(text_with_custom)} characters")
    print(f"   Difference:           {len(text_with_custom) - len(text_without_custom):+d} characters")
    print()
    
    print(f"⏱️  Processing time comparison:")
    print(f"   Without custom words: {time_without_custom:.3f}s")
    print(f"   With custom words:    {time_with_custom:.3f}s")
    print(f"   Difference:           {time_with_custom - time_without_custom:+.3f}s")
    print()
    
    print(f"🔍 Text similarity: {similarity:.2f}%")
    print()
    
    # Check for specific technical terms
    technical_terms_found = []
    for term in custom_words[:20]:  # Check first 20 terms
        if term.lower() in text_with_custom.lower():
            technical_terms_found.append(term)
    
    print(f"🎯 Technical terms detected with custom words: {len(technical_terms_found)}")
    if technical_terms_found:
        print(f"   Found: {', '.join(technical_terms_found[:10])}")
        if len(technical_terms_found) > 10:
            print(f"   ... and {len(technical_terms_found) - 10} more")
    print()
    
    # Recommendations
    print("💡 Recommendations for using custom words:")
    print("-" * 50)
    print("1. 📚 Domain-specific terms: Add words specific to your content domain")
    print("2. 🔤 Technical jargon: Include technical terms, acronyms, and abbreviations")
    print("3. 📝 Proper nouns: Add names, places, and specific identifiers")
    print("4. 🏷️  File extensions: Include common file types (.json, .yaml, etc.)")
    print("5. 🔧 Tool names: Add names of tools, frameworks, and libraries")
    print("6. 📊 Metrics: Include measurement units, percentages, and numbers")
    print("7. 🎯 Context-specific: Tailor words to your specific use case")
    print()
    print("💡 Best practices:")
    print("- Keep the list focused and relevant to your content")
    print("- Update custom words based on analysis of OCR results")
    print("- Test with a representative sample of your images")
    print("- Monitor performance impact (usually minimal)")
    
    return {
        'text_without_custom': text_without_custom,
        'text_with_custom': text_with_custom,
        'time_without_custom': time_without_custom,
        'time_with_custom': time_with_custom,
        'similarity': similarity,
        'technical_terms_found': technical_terms_found
    }

if __name__ == "__main__":
    results = test_custom_words_improvement()
