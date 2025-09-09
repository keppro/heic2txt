# HEIC2TXT - Advanced OCR Image to Text Converter

A high-performance Python-based OCR tool that extracts text from HEIC images using multiple OCR engines with GPU acceleration and custom word recognition.

## 🚀 Key Features

- **Multiple OCR Engines**: Apple Vision (GPU-accelerated), EasyOCR, Tesseract, PaddleOCR
- **GPU Acceleration**: Apple Vision with Metal Performance Shaders (MPS) support
- **Custom Words**: Domain-specific vocabulary for improved accuracy
- **Orientation Detection**: Automatic image rotation for optimal text recognition
- **Batch Processing**: Process hundreds of images efficiently
- **HEIC Support**: Native HEIC/HEIF image processing
- **Text Preprocessing**: Advanced image enhancement and text cleaning
- **Progress Tracking**: Real-time processing updates

## 🎯 OCR Engines

### 1. Apple Vision (Recommended)
- **GPU Acceleration**: 6.92x faster than CPU processing
- **Custom Words**: Support for domain-specific terminology
- **Orientation Detection**: Automatic 0°, 90°, 180°, 270° testing
- **High Accuracy**: Optimized for technical documents
- **Native macOS**: Uses Apple's Vision framework

### 2. EasyOCR
- **GPU Support**: CUDA and MPS acceleration
- **Multi-language**: 80+ languages supported
- **Handwritten Text**: Excellent for handwritten content
- **Complex Layouts**: Handles tables and mixed content

### 3. Tesseract
- **Fast Processing**: Quick text extraction
- **Multiple Languages**: Extensive language support
- **Reliable**: Battle-tested OCR engine

### 4. PaddleOCR
- **Chinese Text**: Excellent for Chinese characters
- **Lightweight**: Minimal resource usage
- **Fast**: Quick processing times

## 📋 Requirements

- **macOS**: 10.15+ (for Apple Vision)
- **Python**: 3.8+
- **System Dependencies**:
  - Tesseract OCR
  - ImageMagick (for HEIC conversion)
  - Apple Vision framework (built-in on macOS)

## 🛠 Installation

1. **Install system dependencies**:

```bash
# macOS
brew install tesseract imagemagick

# Ubuntu/Debian
sudo apt-get install tesseract-ocr imagemagick

# Windows
# Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Download ImageMagick: https://imagemagick.org/script/download.php#windows
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Usage

```bash
# Convert single HEIC image with Apple Vision (GPU-accelerated)
python heic2txt.py input.heic --engine apple_vision

# Batch convert with custom words
python heic2txt_batch_custom.py /path/to/images /path/to/output terraform_ansible_postgresql

# Convert with orientation detection
python heic2txt.py input.heic --engine apple_vision --orientation
```

### Advanced Usage

```bash
# Use specific OCR engine
python heic2txt.py input.heic --engine easyocr

# Set OCR language
python heic2txt.py input.heic --language eng

# Enable text preprocessing
python heic2txt.py input.heic --preprocess

# Verbose output
python heic2txt.py input.heic --verbose
```

## 🎯 Custom Words Support

### Domain-Specific Vocabulary

The system includes pre-built custom word collections for:

- **Terraform**: Infrastructure as Code terminology
- **Ansible**: Configuration management terms
- **AWS**: Cloud services and resources
- **PostgreSQL**: Database terminology
- **MySQL**: Database management terms

### Using Custom Words

```python
from ocr_engines.apple_vision_ocr import AppleVisionOCREngine
from domain_specific_custom_words import get_domain_specific_words

# Get custom words for specific domains
custom_words = get_domain_specific_words(['terraform', 'aws', 'postgresql'])

# Initialize OCR with custom words
ocr = AppleVisionOCREngine(language="en", custom_words=custom_words)

# Extract text with improved accuracy
text = ocr.extract_text(image)
```

## 📊 Performance Comparison

| Engine | Speed | Accuracy | GPU Support | Custom Words |
|--------|-------|----------|-------------|--------------|
| Apple Vision | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| EasyOCR | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ❌ |
| Tesseract | ⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ❌ |
| PaddleOCR | ⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ❌ |

## 🏗 Project Structure

```
heic2txt/
├── heic2txt.py                    # Main OCR script
├── heic2txt_batch_custom.py       # Batch processing with custom words
├── ocr_engines/                   # OCR engine implementations
│   ├── apple_vision_ocr.py        # Apple Vision (GPU-accelerated)
│   ├── easyocr_engine.py          # EasyOCR with MPS support
│   ├── tesseract_ocr.py           # Tesseract OCR
│   └── paddle_ocr.py              # PaddleOCR
├── utils/                         # Utility functions
│   ├── image_utils.py             # Image processing utilities
│   └── text_utils.py              # Text processing utilities
├── domain_specific_custom_words.py # Custom word collections
├── examples/                      # Example images and outputs
├── tests/                         # Test files
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## 🎯 Supported Formats

- **Input**: HEIC, HEIF, PNG, JPEG
- **Output**: TXT, MD (Markdown)

## 🔧 Configuration

### Apple Vision Optimization

```python
# Optimized parameters for best performance
ocr = AppleVisionOCREngine(
    language="en",
    custom_words=custom_words,
    recognition_level=0,  # Fast mode
    uses_cpu_only=False,  # Enable GPU acceleration
    minimum_text_height=0.02
)
```

### EasyOCR with MPS

```python
# GPU acceleration with Apple Silicon
ocr = EasyOCREngine(
    language="en",
    gpu=True,  # Enable MPS acceleration
    model_storage_directory="./models"
)
```

## 📈 Batch Processing

### Process All Images

```bash
# Process all HEIC images in directory
python heic2txt_batch_custom.py /path/to/images /path/to/output terraform_ansible_postgresql
```

### Available Custom Word Combinations

1. **Terraform + Ansible + PostgreSQL** (Best Efficiency)
2. **Terraform + Ansible + AWS + PostgreSQL** (Most Words Found)
3. **Terraform + Ansible + AWS** (Good Balance)
4. **Terraform + Ansible + AWS + MySQL** (Comprehensive)
5. **Terraform + Ansible** (Fastest Processing)

## 🧪 Testing

```bash
# Test single image with custom words
python test_single_combination.py

# Test all custom word combinations
python test_top5_combinations.py

# Test GPU acceleration
python test_gpu_verification.py
```

## 📚 Documentation

- [Custom Words Guide](CUSTOM_WORDS_GUIDE.md)
- [Domain-Specific Custom Words](DOMAIN_CUSTOM_WORDS_SUMMARY.md)
- [Test Results](DOMAIN_TEST_RESULTS.md)
- [Terraform + Ansible Results](TERRAFORM_ANSIBLE_RESULTS.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

1. **Python Environment**: Use system Python (`/usr/bin/python3`) instead of pyenv
2. **GPU Acceleration**: Ensure Apple Vision framework is available
3. **HEIC Conversion**: Install ImageMagick for HEIC support
4. **Custom Words**: Verify domain-specific word lists are loaded

### Performance Tips

1. Use Apple Vision with GPU acceleration for best performance
2. Enable custom words for domain-specific content
3. Use orientation detection for rotated images
4. Process images in batches for efficiency