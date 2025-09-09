#!/usr/bin/env python3
"""
EasyOCR Parameter Optimization Script

This script performs grid search optimization over EasyOCR parameters:
- text_threshold: Controls text detection confidence
- low_text: Controls low text detection threshold  
- link_threshold: Controls text linking threshold

The script tests different parameter combinations and measures accuracy
by comparing OCR output with ground truth text files.
"""

import os
import sys
import itertools
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
import tempfile

# Add current directory to path
sys.path.append('.')

from heic2txt_batch import convert_heic_to_png, preprocess_image_for_ocr
from ocr_engines.easyocr_engine import EasyOCREngine
from PIL import Image
import difflib


def setup_logging(log_dir: str) -> logging.Logger:
    """Setup logging for the optimization process."""
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger('easyocr_optimization')
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # File handler
    log_file = os.path.join(log_dir, f'easyocr_optimization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def load_ground_truth(test_dir: str) -> Dict[str, str]:
    """Load ground truth text files."""
    ground_truth = {}
    
    for file_path in Path(test_dir).glob("*.txt"):
        if not file_path.name.endswith('_comparison.log'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:  # Only include non-empty files
                        # Extract base name (remove .txt extension)
                        base_name = file_path.stem
                        ground_truth[base_name] = content
            except Exception as e:
                print(f"Warning: Could not load {file_path}: {e}")
    
    return ground_truth


def calculate_text_similarity(text1: str, text2: str) -> Dict[str, float]:
    """Calculate various similarity metrics between two texts."""
    if not text1 and not text2:
        return {'exact_match': 1.0, 'sequence_ratio': 1.0, 'character_ratio': 1.0, 'word_ratio': 1.0}
    
    if not text1 or not text2:
        return {'exact_match': 0.0, 'sequence_ratio': 0.0, 'character_ratio': 0.0, 'word_ratio': 0.0}
    
    # Exact match
    exact_match = 1.0 if text1.strip() == text2.strip() else 0.0
    
    # Sequence matcher ratio
    sequence_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    
    # Character-level similarity
    char_ratio = difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    # Word-level similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if words1 or words2:
        word_ratio = len(words1.intersection(words2)) / len(words1.union(words2))
    else:
        word_ratio = 1.0
    
    return {
        'exact_match': exact_match,
        'sequence_ratio': sequence_ratio,
        'character_ratio': char_ratio,
        'word_ratio': word_ratio
    }


def test_easyocr_parameters(heic_path: str, ground_truth: str, 
                           text_threshold: float, low_text: float, link_threshold: float,
                           logger: logging.Logger) -> Dict:
    """Test EasyOCR with specific parameters on a single image."""
    try:
        # Convert HEIC to PNG
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_png:
            png_path = tmp_png.name
        
        if not convert_heic_to_png(heic_path, png_path):
            return {'success': False, 'error': 'HEIC conversion failed'}
        
        # Preprocess image
        preprocessed_path = preprocess_image_for_ocr(png_path)
        
        # Initialize EasyOCR with custom parameters
        ocr_engine = EasyOCREngine(
            language='en',
            text_threshold=text_threshold,
            low_text=low_text,
            link_threshold=link_threshold
        )
        
        # Load and process image
        img = Image.open(preprocessed_path)
        
        # Extract text
        ocr_text = ocr_engine.extract_text(img)
        
        # Calculate similarity metrics
        similarity_metrics = calculate_text_similarity(ground_truth, ocr_text)
        
        # Cleanup
        os.unlink(png_path)
        if preprocessed_path != png_path:
            os.unlink(preprocessed_path)
        
        return {
            'success': True,
            'ocr_text': ocr_text,
            'ground_truth': ground_truth,
            'similarity_metrics': similarity_metrics,
            'text_length': len(ocr_text),
            'ground_truth_length': len(ground_truth)
        }
        
    except Exception as e:
        logger.error(f"Error testing parameters {text_threshold}, {low_text}, {link_threshold}: {e}")
        return {'success': False, 'error': str(e)}


def run_parameter_optimization(test_dir: str, output_dir: str, 
                              max_files: int = 10) -> None:
    """Run parameter optimization on test files."""
    
    # Setup logging
    logger = setup_logging(output_dir)
    logger.info("Starting EasyOCR parameter optimization")
    
    # Load ground truth
    logger.info("Loading ground truth files...")
    ground_truth = load_ground_truth(test_dir)
    logger.info(f"Loaded {len(ground_truth)} ground truth files")
    
    if not ground_truth:
        logger.error("No ground truth files found!")
        return
    
    # Get HEIC files that have corresponding ground truth
    heic_files = []
    for base_name, truth_text in ground_truth.items():
        heic_path = os.path.join(test_dir, f"{base_name}.HEIC")
        if os.path.exists(heic_path):
            heic_files.append((heic_path, base_name, truth_text))
    
    # Limit number of files for testing
    heic_files = heic_files[:max_files]
    logger.info(f"Testing on {len(heic_files)} files")
    
    # Define parameter ranges
    text_thresholds = [0.4, 0.5, 0.6, 0.7]
    low_texts = [0.2, 0.3, 0.4, 0.5]
    link_thresholds = [0.4, 0.5, 0.6, 0.7]
    
    # Generate all parameter combinations
    param_combinations = list(itertools.product(text_thresholds, low_texts, link_thresholds))
    logger.info(f"Testing {len(param_combinations)} parameter combinations")
    
    # Results storage
    all_results = []
    best_combination = None
    best_score = 0.0
    
    # Test each parameter combination
    for i, (text_thresh, low_text, link_thresh) in enumerate(param_combinations):
        logger.info(f"Testing combination {i+1}/{len(param_combinations)}: "
                   f"text_threshold={text_thresh}, low_text={low_text}, link_threshold={link_thresh}")
        
        combination_results = []
        total_sequence_ratio = 0.0
        total_word_ratio = 0.0
        successful_tests = 0
        
        for heic_path, base_name, ground_truth_text in heic_files:
            logger.info(f"  Testing {base_name}...")
            
            result = test_easyocr_parameters(
                heic_path, ground_truth_text, 
                text_thresh, low_text, link_thresh, logger
            )
            
            if result['success']:
                combination_results.append({
                    'file': base_name,
                    'result': result
                })
                
                # Accumulate metrics
                total_sequence_ratio += result['similarity_metrics']['sequence_ratio']
                total_word_ratio += result['similarity_metrics']['word_ratio']
                successful_tests += 1
                
                # Log detailed comparison
                logger.info(f"    Sequence ratio: {result['similarity_metrics']['sequence_ratio']:.3f}")
                logger.info(f"    Word ratio: {result['similarity_metrics']['word_ratio']:.3f}")
                logger.info(f"    OCR length: {result['text_length']}, Ground truth length: {result['ground_truth_length']}")
                
                # Log text differences
                if result['similarity_metrics']['sequence_ratio'] < 0.8:  # Only log significant differences
                    logger.info(f"    Ground truth: {ground_truth_text[:100]}...")
                    logger.info(f"    OCR result:   {result['ocr_text'][:100]}...")
            else:
                logger.error(f"    Failed: {result.get('error', 'Unknown error')}")
        
        # Calculate average metrics for this combination
        if successful_tests > 0:
            avg_sequence_ratio = total_sequence_ratio / successful_tests
            avg_word_ratio = total_word_ratio / successful_tests
            combined_score = (avg_sequence_ratio + avg_word_ratio) / 2
            
            combination_summary = {
                'parameters': {
                    'text_threshold': text_thresh,
                    'low_text': low_text,
                    'link_threshold': link_thresh
                },
                'avg_sequence_ratio': avg_sequence_ratio,
                'avg_word_ratio': avg_word_ratio,
                'combined_score': combined_score,
                'successful_tests': successful_tests,
                'total_tests': len(heic_files),
                'detailed_results': combination_results
            }
            
            all_results.append(combination_summary)
            
            # Check if this is the best combination so far
            if combined_score > best_score:
                best_score = combined_score
                best_combination = combination_summary
                logger.info(f"  New best combination! Score: {combined_score:.3f}")
            else:
                logger.info(f"  Score: {combined_score:.3f}")
        else:
            logger.error(f"  No successful tests for this combination")
    
    # Save results
    results_file = os.path.join(output_dir, 'optimization_results.json')
    with open(results_file, 'w') as f:
        json.dump({
            'best_combination': best_combination,
            'all_results': all_results,
            'test_files': [f[1] for f in heic_files],
            'parameter_ranges': {
                'text_thresholds': text_thresholds,
                'low_texts': low_texts,
                'link_thresholds': link_thresholds
            }
        }, f, indent=2)
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("OPTIMIZATION SUMMARY")
    logger.info("="*60)
    
    if best_combination:
        logger.info(f"Best parameters:")
        logger.info(f"  text_threshold: {best_combination['parameters']['text_threshold']}")
        logger.info(f"  low_text: {best_combination['parameters']['low_text']}")
        logger.info(f"  link_threshold: {best_combination['parameters']['link_threshold']}")
        logger.info(f"  Combined score: {best_combination['combined_score']:.3f}")
        logger.info(f"  Average sequence ratio: {best_combination['avg_sequence_ratio']:.3f}")
        logger.info(f"  Average word ratio: {best_combination['avg_word_ratio']:.3f}")
        logger.info(f"  Successful tests: {best_combination['successful_tests']}/{best_combination['total_tests']}")
    else:
        logger.error("No successful parameter combinations found!")
    
    # Sort all results by combined score
    sorted_results = sorted(all_results, key=lambda x: x['combined_score'], reverse=True)
    logger.info(f"\nTop 5 parameter combinations:")
    for i, result in enumerate(sorted_results[:5]):
        params = result['parameters']
        logger.info(f"  {i+1}. text_threshold={params['text_threshold']}, "
                   f"low_text={params['low_text']}, link_threshold={params['link_threshold']} "
                   f"(score: {result['combined_score']:.3f})")
    
    logger.info(f"\nDetailed results saved to: {results_file}")


if __name__ == "__main__":
    # Configuration
    test_directory = "~/Pictures/TF"
    output_directory = "./optimization_results"
    max_test_files = 5  # Start with 5 files for initial testing
    
    print(f"Starting EasyOCR parameter optimization...")
    print(f"Test directory: {test_directory}")
    print(f"Output directory: {output_directory}")
    print(f"Max test files: {max_test_files}")
    
    run_parameter_optimization(test_directory, output_directory, max_test_files)