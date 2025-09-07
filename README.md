# HEIC2TXT - OCR Image to Text Converter

A Python-based OCR tool that extracts text from HEIC images and saves them as text files.

## Features

- **HEIC Support**: Convert HEIC images to text using OCR
- **Batch Processing**: Process multiple images at once
- **Multiple OCR Engines**: Support for Tesseract and EasyOCR
- **Text Preprocessing**: Clean and format extracted text
- **Progress Tracking**: Real-time progress updates
- **Error Handling**: Robust error handling and logging

## Requirements

- Python 3.8+
- Tesseract OCR engine
- ImageMagick (for HEIC conversion)

## Installation

1. Install system dependencies:

```bash
# macOS
brew install tesseract imagemagick

# Ubuntu/Debian
sudo apt-get install tesseract-ocr imagemagick

# Windows
# Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Download and install ImageMagick from: https://imagemagick.org/script/download.php#windows
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Convert single HEIC image
python heic2txt.py input.heic

# Convert multiple images
python heic2txt.py *.heic

# Convert with specific output directory
python heic2txt.py input.heic --output ./text_files/

# Batch convert all HEIC files in a directory
python heic2txt.py --batch ./images/ --output ./text_files/
```

### Advanced Usage

```bash
# Use specific OCR engine
python heic2txt.py input.heic --engine easyocr

# Set OCR language
python heic2txt.py input.heic --language eng+spa

# Enable text preprocessing
python heic2txt.py input.heic --preprocess

# Verbose output
python heic2txt.py input.heic --verbose
```

## Project Structure

```
heic2txt/
├── heic2txt.py          # Main OCR script
├── ocr_engines/         # OCR engine implementations
│   ├── tesseract_ocr.py
│   └── easyocr_engine.py
├── utils/               # Utility functions
│   ├── image_utils.py
│   └── text_utils.py
├── tests/               # Test files
├── examples/            # Example images and outputs
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
└── README.md           # This file
```

## Supported Formats

- **Input**: HEIC, HEIF
- **Output**: TXT, MD (Markdown)

## OCR Engines

1. **Tesseract** (Default)
   - Fast and reliable
   - Multiple language support
   - Good for printed text

2. **EasyOCR**
   - Better for handwritten text
   - More accurate for complex layouts
   - Slower but more precise

## Examples

Check the `examples/` directory for sample HEIC images and their corresponding text outputs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
