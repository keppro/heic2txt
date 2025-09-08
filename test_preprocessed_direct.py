#!/usr/bin/env python3
"""
Test EasyOCR directly on preprocessed image with different parameters
"""

import easyocr
import cv2
import numpy as np

def test_preprocessed_image():
    # Load the preprocessed image
    img_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518_preprocessed_debug.png"
    
    # Initialize EasyOCR
    reader = easyocr.Reader(['en'], gpu=True)
    
    # Load image
    img = cv2.imread(img_path)
    print(f"Image shape: {img.shape}")
    print(f"Image dtype: {img.dtype}")
    print(f"Min value: {img.min()}, Max value: {img.max()}")
    
    # Test with different parameters
    print("\n" + "="*50)
    print("TESTING DIFFERENT EASYOCR PARAMETERS")
    print("="*50)
    
    # Test 1: Default parameters
    print("\n1. Default parameters:")
    try:
        results = reader.readtext(img)
        text_parts = [text for (bbox, text, confidence) in results if confidence > 0.5]
        print(f"   Found {len(text_parts)} text blocks")
        print(f"   First few: {text_parts[:5]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Lower thresholds
    print("\n2. Lower thresholds (0.3, 0.2, 0.3):")
    try:
        results = reader.readtext(img, text_threshold=0.3, low_text=0.2, link_threshold=0.3)
        text_parts = [text for (bbox, text, confidence) in results if confidence > 0.3]
        print(f"   Found {len(text_parts)} text blocks")
        print(f"   First few: {text_parts[:5]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Very low thresholds
    print("\n3. Very low thresholds (0.1, 0.1, 0.1):")
    try:
        results = reader.readtext(img, text_threshold=0.1, low_text=0.1, link_threshold=0.1)
        text_parts = [text for (bbox, text, confidence) in results if confidence > 0.1]
        print(f"   Found {len(text_parts)} text blocks")
        print(f"   First few: {text_parts[:5]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: With paragraph=True
    print("\n4. With paragraph=True:")
    try:
        results = reader.readtext(img, paragraph=True)
        text_parts = [text for (bbox, text, confidence) in results if confidence > 0.5]
        print(f"   Found {len(text_parts)} text blocks")
        print(f"   First few: {text_parts[:5]}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_preprocessed_image()
