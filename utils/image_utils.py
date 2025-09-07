"""Image utility functions for HEIC2TXT."""

import pyheif
from PIL import Image
from pathlib import Path
from typing import Optional


def is_heic_file(file_path: str) -> bool:
    """
    Check if a file is a HEIC/HEIF image.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is HEIC/HEIF, False otherwise
    """
    file_path = Path(file_path)
    
    # Check file extension
    heic_extensions = {'.heic', '.heif', '.HEIC', '.HEIF'}
    if file_path.suffix not in heic_extensions:
        return False
    
    # Check if file exists
    if not file_path.exists():
        return False
    
    return True


def convert_heic_to_pil(file_path: str) -> Optional[Image.Image]:
    """
    Convert HEIC file to PIL Image.
    
    Args:
        file_path: Path to HEIC file
        
    Returns:
        PIL Image object or None if conversion fails
    """
    try:
        # Read HEIC file
        heif_file = pyheif.read(file_path)
        
        # Convert to PIL Image
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        
        return image
        
    except Exception as e:
        print(f"Error converting HEIC file {file_path}: {str(e)}")
        return None


def convert_heic_to_jpeg(heic_path: str, jpeg_path: str) -> bool:
    """
    Convert HEIC file to JPEG format.
    
    Args:
        heic_path: Path to input HEIC file
        jpeg_path: Path to output JPEG file
        
    Returns:
        True if conversion successful, False otherwise
    """
    try:
        # Convert HEIC to PIL Image
        image = convert_heic_to_pil(heic_path)
        if image is None:
            return False
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as JPEG
        image.save(jpeg_path, 'JPEG', quality=95)
        return True
        
    except Exception as e:
        print(f"Error converting HEIC to JPEG: {str(e)}")
        return False


def get_image_info(file_path: str) -> Optional[dict]:
    """
    Get basic information about a HEIC image.
    
    Args:
        file_path: Path to HEIC file
        
    Returns:
        Dictionary with image info or None if error
    """
    try:
        heif_file = pyheif.read(file_path)
        
        return {
            'width': heif_file.size[0],
            'height': heif_file.size[1],
            'mode': heif_file.mode,
            'has_alpha': heif_file.mode in ['RGBA', 'LA'],
            'stride': heif_file.stride
        }
        
    except Exception as e:
        print(f"Error getting image info: {str(e)}")
        return None
