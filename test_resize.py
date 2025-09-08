#!/usr/bin/env python3
"""Test resize function"""

def resize_image_if_needed(image_path: str, max_size: int = 4000) -> str:
    """
    Resize image if any side exceeds max_size, maintaining aspect ratio.
    
    Args:
        image_path: Path to input image file
        max_size: Maximum size for any side (default: 4000)
        
    Returns:
        Path to resized image file (original path if no resize needed)
    """
    try:
        from PIL import Image
        import os
        
        # Load the image
        img = Image.open(image_path)
        width, height = img.size
        max_side = max(width, height)
        
        print(f"🔄 Checking image size: {width}x{height}, max_side={max_side}")
        
        if max_side <= max_size:
            print(f"🔄 Image size {width}x{height} is within limits")
            return image_path
        
        # Calculate new dimensions
        scale_factor = max_size / max_side
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        print(f"�� Resizing image with scale factor {scale_factor:.4f}")
        print(f"🔄 Resizing from {width}x{height} to {new_width}x{new_height}")
        
        # Resize image
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save resized image
        base_name = os.path.splitext(image_path)[0]
        resized_path = f"{base_name}_resized.png"
        resized_img.save(resized_path)
        
        print(f"✅ Image resized and saved to {os.path.basename(resized_path)}")
        return resized_path
        
    except Exception as e:
        print(f"⚠️  Image resize failed: {e}")
        return image_path

# Test with the actual image
test_path = "/Volumes/UserDisk/Users/keppro/Pictures/TF/IMG_7518_test.png"
if __name__ == "__main__":
    result = resize_image_if_needed(test_path, max_size=4000)
    print(f"Result: {result}")
