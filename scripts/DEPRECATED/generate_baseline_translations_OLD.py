#!/usr/bin/env python3
"""
Clean Baseline Translation Generation Script

Generates baseline translations for Kikuyu proverbs with SEPARATED systems:
1. OpenAI GPT-4 (General Multilingual LLM)
2. Cohere Aya-23 (African Language Optimized LLM)
3. NLLB-200 (Specialized MT with Native Kikuyu Support)
4. Google Translate (Commercial Baseline - No Kikuyu Support)

Output: ONE row per proverb (no duplicates, no confusion)

Usage:
    python generate_baseline_translations.py [--max-proverbs N] [--output filename.csv]
    
Examples:
    # Process all proverbs
    python generate_baseline_translations.py
    
    # Test with 10 proverbs
    python generate_baseline_translations.py --max-proverbs 10
    
    # Process 50 proverbs with custom output
    python generate_baseline_translations.py --max-proverbs 50 --output my_baseline.csv
"""

import sys
import os
import argparse
from pathlib import Path
import pandas as pd
import logging
import time
import json
from datetime import datetime
from typing import Dict
from dataclasses import dataclass, asdict

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate baseline translations for thesis evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all proverbs from gold standard
  python generate_baseline_translations.py
  
  # Test with limited proverbs
  python generate_baseline_translations.py --max-proverbs 10
  
  # Custom output file
  python generate_baseline_translations.py --output my_results.csv
  
  # Use alternative gold standard file
  python generate_baseline_translations.py --input data/evaluation/alternative_gold.csv

Environment Variables Required:
  OPENAI_API_KEY      - For OG-RAG and Raw LLM translations
  GOOGLE_API_KEY      - Optional, for Gemini alternative
  
Additional Setup:
  pip install googletrans==4.0.0-rc1  # For Google Translate baseline
        """
    )
    
    parser.add_argument(
        '--input',
        type=str,
        default='data/evaluation/gold_standard_ireri.csv',
        help='Path to gold standard CSV file (default: data/evaluation/gold_standard_ireri.csv)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output filename (default: auto-generated with timestamp)'
    )
    
    parser.add_argument(
        '--max-proverbs',
        type=int,
        default=None,
        help='Limit number of proverbs to process (useful for testing)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file'
    )
    
    return parser.parse_args()


def check_prerequisites():
    """Check that required setup is complete."""
    issues = []
    
    # Check API keys
    import os
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('COHERE_API_KEY'):
        issues.append("❌ OPENAI_API_KEY or COHERE_API_KEY not set - required for Raw LLM")
    else:
        if os.getenv('OPENAI_API_KEY'):
            logger.info("✓ OpenAI API key found")
        if os.getenv('COHERE_API_KEY'):
            logger.info("✓ Cohere API key found")
    
    # Check if requests library is available for NLLB API
    try:
        import requests
        logger.info("✓ NLLB-200 API available (via winstxnhdw/nllb-api - no auth required)")
    except ImportError:
        issues.append("⚠️  requests library not installed - NLLB-200 baseline unavailable")
        issues.append("   Install with: pip install requests")
    
    # Check Google Translate library (optional, using deep-translator now)
    try:
        from deep_translator import GoogleTranslator
        logger.info("✓ deep-translator library available")
    except ImportError:
        issues.append("⚠️  deep-translator not installed - Google Translate baseline unavailable")
        issues.append("   Install with: pip install deep-translator")
    
    return issues


def main():
    """Main execution function."""
    args = parse_arguments()
    
    print("\n" + "="*80)
    print("BASELINE TRANSLATION GENERATION FOR THESIS EVALUATION")
    print("="*80)
    print("\nPurpose: Generate translations across multiple systems to validate")
    print("         the hypothesis that OG-RAG provides superior cultural preservation")
    print("\nSystems:")
    print("  1. OG-RAG: Ontology-enhanced RAG with cultural knowledge (placeholder)")
    print("  2. Raw LLM: General multilingual AI without cultural enhancement")
    print("  3. NLLB-200: Specialized MT with native Kikuyu support")
    print("  4. Google Translate: Commercial baseline (reference)")
    print("="*80 + "\n")
    
    # Check prerequisites
    issues = check_prerequisites()
    if issues:
        print("Setup Issues Detected:\n")
        for issue in issues:
            print(f"  {issue}")
        print("\nPlease resolve these issues before proceeding.")
        
        # Ask if user wants to continue anyway
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"\n❌ Error: Gold standard file not found: {args.input}")
        print("Please ensure the gold standard dataset exists.")
        return
    
    print(f"✓ Gold standard file: {args.input}")
    
    if args.max_proverbs:
        print(f"✓ Processing limit: {args.max_proverbs} proverbs (testing mode)")
    else:
        print("✓ Processing: ALL proverbs")
    
    print("\nInitializing translation systems...")
    
    # Initialize system
    try:
        translation_system = BaselineTranslationSystem(config_file=args.config)
        comparator = TranslationComparator(translation_system)
    except Exception as e:
        print(f"\n❌ Failed to initialize translation systems: {e}")
        return
    
    print("\nStarting baseline translation generation...")
    print("This may take several minutes depending on the number of proverbs.\n")
    
    try:
        # Generate translations
        results_df = comparator.compare_on_gold_standard(
            gold_standard_file=args.input,
            output_file=args.output,
            max_proverbs=args.max_proverbs
        )
        
        print("\n" + "="*80)
        print("✅ SUCCESS: Baseline translations generated")
        print("="*80)
        print(f"\nProcessed: {len(results_df)} proverbs")
        print(f"Output directory: data/results/baseline_translations/")
        print("\nNext Steps:")
        print("  1. Review the generated translations")
        print("  2. Run evaluation metrics (BLEU, ROUGE, METEOR)")
        print("  3. Perform cultural authenticity assessment")
        print("  4. Conduct LLM-as-a-Judge evaluation")
        print("  5. Generate comparative analysis and visualizations")
        print("\nSee README.md for detailed evaluation workflow.")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        print("Partial results may have been saved to data/results/baseline_translations/")
    except Exception as e:
        print(f"\n❌ Error during translation generation: {e}")
        logger.exception("Detailed error:")
        return


if __name__ == "__main__":
    main()
