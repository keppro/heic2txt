#!/usr/bin/env python3
"""
Fixed test script to compare OCR results with and without preprocessing
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
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters that might vary
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\']', '', text)
    return text.lower()

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts"""
    text1_clean = preprocess_text(text1)
    text2_clean = preprocess_text(text2)
    return SequenceMatcher(None, text1_clean, text2_clean).ratio()

def preprocess_image_for_ocr(image_path):
    """Apply preprocessing: invert colors, thresholding, noise cleaning"""
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
        
        # Resize if too large (OCR works better with smaller images)
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

def extract_text_with_easyocr(image_path, preprocessed=False):
    """Extract text using EasyOCR"""
    try:
        # Initialize EasyOCR
        reader = easyocr.Reader(['en'], gpu=True)
        
        if preprocessed:
            # Use preprocessed image
            processed_img = preprocess_image_for_ocr(image_path)
            if processed_img is None:
                return ""
            img_array = processed_img
        else:
            # Use original image
            img = Image.open(image_path)
            img_array = np.array(img)
        
        # Extract text
        results = reader.readtext(img_array, text_threshold=0.7, low_text=0.5, link_threshold=0.5)
        
        # Combine all text
        text_parts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:
                text_parts.append(text)
        
        return '\n'.join(text_parts)
    
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def main():
    # Paths
    png_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518_test.png"
    ground_truth_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518.txt"
    output_dir = "/Volumes/UserDisk/Users/keppro/Pictures/TF"
    
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
    print("OCR PREPROCESSING COMPARISON TEST (FIXED)")
    print("=" * 80)
    print(f"Testing file: {os.path.basename(png_path)}")
    print(f"Ground truth: {os.path.basename(ground_truth_path)}")
    print(f"Ground truth length: {len(ground_truth)} characters")
    print()
    
    # Test 1: Without preprocessing
    print("=" * 50)
    print("TEST 1: WITHOUT PREPROCESSING")
    print("=" * 50)
    
    print("📖 Extracting text without preprocessing...")
    text_no_preprocessing = extract_text_with_easyocr(png_path, preprocessed=False)
    
    print(f"�� Extracted text length: {len(text_no_preprocessing)} characters")
    print(f"📄 Text preview (first 200 chars): {text_no_preprocessing[:200]}...")
    
    # Calculate similarity
    similarity_no_preprocessing = calculate_similarity(ground_truth, text_no_preprocessing)
    print(f"🎯 Similarity to ground truth: {similarity_no_preprocessing:.2%}")
    
    # Save result
    output_file_no_preprocessing = os.path.join(output_dir, "IMG_7518_no_preprocessing_fixed.txt")
    with open(output_file_no_preprocessing, 'w', encoding='utf-8') as f:
        f.write(text_no_preprocessing)
    print(f"💾 Saved to: {output_file_no_preprocessing}")
    
    # Test 2: With preprocessing
    print("\n" + "=" * 50)
    print("TEST 2: WITH PREPROCESSING")
    print("=" * 50)
    
    print("📖 Extracting text with preprocessing...")
    text_with_preprocessing = extract_text_with_easyocr(png_path, preprocessed=True)
    
    print(f"📄 Extracted text length: {len(text_with_preprocessing)} characters")
    print(f"📄 Text preview (first 200 chars): {text_with_preprocessing[:200]}...")
    
    # Calculate similarity
    similarity_with_preprocessing = calculate_similarity(ground_truth, text_with_preprocessing)
    print(f"🎯 Similarity to ground truth: {similarity_with_preprocessing:.2%}")
    
    # Save result
    output_file_with_preprocessing = os.path.join(output_dir, "IMG_7518_with_preprocessing_fixed.txt")
    with open(output_file_with_preprocessing, 'w', encoding='utf-8') as f:
        f.write(text_with_preprocessing)
    print(f"💾 Saved to: {output_file_with_preprocessing}")
    
    # Comparison summary
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print(f"Without preprocessing: {similarity_no_preprocessing:.2%} similarity")
    print(f"With preprocessing:    {similarity_with_preprocessing:.2%} similarity")
    print()
    
    if similarity_with_preprocessing > similarity_no_preprocessing:
        improvement = similarity_with_preprocessing - similarity_no_preprocessing
        print(f"✅ Preprocessing IMPROVES accuracy by {improvement:.2%}")
    elif similarity_no_preprocessing > similarity_with_preprocessing:
        degradation = similarity_no_preprocessing - similarity_with_preprocessing
        print(f"❌ Preprocessing DEGRADES accuracy by {degradation:.2%}")
    else:
        print("➖ Preprocessing has NO EFFECT on accuracy")
    
    print(f"\n📊 Character count comparison:")
    print(f"Ground truth:           {len(ground_truth):,} characters")
    print(f"Without preprocessing:  {len(text_no_preprocessing):,} characters")
    print(f"With preprocessing:     {len(text_with_preprocessing):,} characters")

if __name__ == "__main__":
    main()
