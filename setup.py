"""Setup script for HEIC2TXT package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="heic2txt",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="OCR tool that extracts text from HEIC images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/heic2txt",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "heic2txt=heic2txt:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
