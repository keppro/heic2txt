#!/usr/bin/env python3
"""
Test with gentler preprocessing approach
"""

import os
import sys
import easyocr
import numpy as np
import cv2
from difflib import SequenceMatcher
import re
from PIL import Image

def preprocess_text(text):
    """Clean and normalize text for comparison"""
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\']', '', text)
    return text.lower()

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts"""
    text1_clean = preprocess_text(text1)
    text2_clean = preprocess_text(text2)
    return SequenceMatcher(None, text1_clean, text2_clean).ratio()

def gentle_preprocess_image(image_path):
    """Apply gentler preprocessing"""
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not load image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding instead of global thresholding
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Convert back to RGB for EasyOCR
        rgb_cleaned = cv2.cvtColor(adaptive_thresh, cv2.COLOR_GRAY2RGB)
        
        return rgb_cleaned
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def aggressive_preprocess_image(image_path):
    """Apply aggressive preprocessing (original method)"""
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not load image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Invert colors (white -> black, blue -> white)
        inverted = cv2.bitwise_not(gray)
        
        # Apply thresholding to get clean monochrome
        _, thresh = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Clean up noise with morphological operations
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        # Resize if too large
        height, width = cleaned.shape
        max_side = 4000
        if max(height, width) > max_side:
            scale = max_side / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            cleaned = cv2.resize(cleaned, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Convert back to RGB for EasyOCR
        rgb_cleaned = cv2.cvtColor(cleaned, cv2.COLOR_GRAY2RGB)
        
        return rgb_cleaned
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def extract_text_with_easyocr(image_path, preprocessing_type="none"):
    """Extract text using EasyOCR with different preprocessing"""
    try:
        # Initialize EasyOCR
        reader = easyocr.Reader(['en'], gpu=True)
        
        if preprocessing_type == "none":
            # Use original image
            img = Image.open(image_path)
            img_array = np.array(img)
        elif preprocessing_type == "gentle":
            # Use gentle preprocessing
            processed_img = gentle_preprocess_image(image_path)
            if processed_img is None:
                return ""
            img_array = processed_img
        elif preprocessing_type == "aggressive":
            # Use aggressive preprocessing
            processed_img = aggressive_preprocess_image(image_path)
            if processed_img is None:
                return ""
            img_array = processed_img
        
        # Extract text with lower thresholds for preprocessed images
        if preprocessing_type == "none":
            results = reader.readtext(img_array, text_threshold=0.7, low_text=0.5, link_threshold=0.5)
        else:
            results = reader.readtext(img_array, text_threshold=0.1, low_text=0.1, link_threshold=0.1)
        
        # Combine all text
        text_parts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.1:  # Lower confidence threshold for preprocessed
                text_parts.append(text)
        
        return '\n'.join(text_parts)
    
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def main():
    # Paths
    png_path = "~/Pictures/TF/IMG_7518_test.png"
    ground_truth_path = "~/Pictures/TF/IMG_7518.txt"
    output_dir = "~/Pictures/TF"
    
    # Check if files exist
    if not os.path.exists(png_path):
        print(f"Error: PNG file not found: {png_path}")
        return
    
    if not os.path.exists(ground_truth_path):
        print(f"Error: Ground truth file not found: {ground_truth_path}")
        return
    
    # Read ground truth
    with open(ground_truth_path, 'r', encoding='utf-8') as f:
        ground_truth = f.read()
    
    print("=" * 80)
    print("OCR PREPROCESSING COMPARISON TEST (MULTIPLE METHODS)")
    print("=" * 80)
    print(f"Testing file: {os.path.basename(png_path)}")
    print(f"Ground truth: {os.path.basename(ground_truth_path)}")
    print(f"Ground truth length: {len(ground_truth)} characters")
    print()
    
    results = {}
    
    # Test 1: No preprocessing
    print("=" * 50)
    print("TEST 1: NO PREPROCESSING")
    print("=" * 50)
    
    print("📖 Extracting text without preprocessing...")
    text_no_preprocessing = extract_text_with_easyocr(png_path, "none")
    similarity_no_preprocessing = calculate_similarity(ground_truth, text_no_preprocessing)
    results["no_preprocessing"] = (text_no_preprocessing, similarity_no_preprocessing)
    
    print(f"📄 Extracted text length: {len(text_no_preprocessing)} characters")
    print(f"🎯 Similarity to ground truth: {similarity_no_preprocessing:.2%}")
    
    # Test 2: Gentle preprocessing
    print("\n" + "=" * 50)
    print("TEST 2: GENTLE PREPROCESSING (Adaptive Threshold)")
    print("=" * 50)
    
    print("📖 Extracting text with gentle preprocessing...")
    text_gentle_preprocessing = extract_text_with_easyocr(png_path, "gentle")
    similarity_gentle_preprocessing = calculate_similarity(ground_truth, text_gentle_preprocessing)
    results["gentle_preprocessing"] = (text_gentle_preprocessing, similarity_gentle_preprocessing)
    
    print(f"📄 Extracted text length: {len(text_gentle_preprocessing)} characters")
    print(f"🎯 Similarity to ground truth: {similarity_gentle_preprocessing:.2%}")
    
    # Test 3: Aggressive preprocessing
    print("\n" + "=" * 50)
    print("TEST 3: AGGRESSIVE PREPROCESSING (Invert + OTSU)")
    print("=" * 50)
    
    print("📖 Extracting text with aggressive preprocessing...")
    text_aggressive_preprocessing = extract_text_with_easyocr(png_path, "aggressive")
    similarity_aggressive_preprocessing = calculate_similarity(ground_truth, text_aggressive_preprocessing)
    results["aggressive_preprocessing"] = (text_aggressive_preprocessing, similarity_aggressive_preprocessing)
    
    print(f"📄 Extracted text length: {len(text_aggressive_preprocessing)} characters")
    print(f"🎯 Similarity to ground truth: {similarity_aggressive_preprocessing:.2%}")
    
    # Save results
    for method, (text, similarity) in results.items():
        output_file = os.path.join(output_dir, f"IMG_7518_{method}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"💾 Saved {method} result to: {output_file}")
    
    # Comparison summary
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print(f"No preprocessing:        {results['no_preprocessing'][1]:.2%} similarity")
    print(f"Gentle preprocessing:    {results['gentle_preprocessing'][1]:.2%} similarity")
    print(f"Aggressive preprocessing: {results['aggressive_preprocessing'][1]:.2%} similarity")
    print()
    
    # Find best method
    best_method = max(results.items(), key=lambda x: x[1][1])
    print(f"🏆 BEST METHOD: {best_method[0]} with {best_method[1][1]:.2%} similarity")
    
    print(f"\n📊 Character count comparison:")
    print(f"Ground truth:            {len(ground_truth):,} characters")
    for method, (text, similarity) in results.items():
        print(f"{method:20}: {len(text):,} characters")

if __name__ == "__main__":
    main()
