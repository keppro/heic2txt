#!/usr/bin/env python3
"""
Debug script to check preprocessing results
"""

import cv2
import numpy as np
from PIL import Image

def preprocess_image_for_ocr(image_path):
    """Apply preprocessing: invert colors, thresholding, noise cleaning"""
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not load image")
        
        print(f"Original image shape: {img.shape}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"Grayscale image shape: {gray.shape}")
        
        # Invert colors (white -> black, blue -> white)
        inverted = cv2.bitwise_not(gray)
        print(f"Inverted image shape: {inverted.shape}")
        
        # Apply thresholding to get clean monochrome
        _, thresh = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"Thresholded image shape: {thresh.shape}")
        
        # Clean up noise with morphological operations
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        print(f"Cleaned image shape: {cleaned.shape}")
        
        # Resize if too large (OCR works better with smaller images)
        height, width = cleaned.shape
        max_side = 4000
        if max(height, width) > max_side:
            scale = max_side / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            cleaned = cv2.resize(cleaned, (new_width, new_height), interpolation=cv2.INTER_AREA)
            print(f"Resized image shape: {cleaned.shape}")
        
        # Save preprocessed image for inspection
        cv2.imwrite("/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518_preprocessed_debug.png", cleaned)
        print("💾 Saved preprocessed image for inspection")
        
        return cleaned
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def main():
    png_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518_test.png"
    
    print("🔍 Debugging preprocessing...")
    result = preprocess_image_for_ocr(png_path)
    
    if result is not None:
        print("✅ Preprocessing completed successfully")
        print(f"Final image shape: {result.shape}")
        print(f"Image dtype: {result.dtype}")
        print(f"Min value: {result.min()}, Max value: {result.max()}")
    else:
        print("❌ Preprocessing failed")

if __name__ == "__main__":
    main()
