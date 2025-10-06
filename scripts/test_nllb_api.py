#!/usr/bin/env python3
"""
Quick test of NLLB-200 API integration via winstxnhdw/nllb-api

Tests the new HTTP-based implementation to verify it works before running full baseline.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.evaluation.baseline_translation_system import BaselineTranslationSystem

def test_nllb_api():
    """Test NLLB API with a simple Kikuyu proverb."""
    print("="*80)
    print("Testing NLLB-200 API Integration")
    print("="*80)
    print()
    
    # Initialize system
    print("1. Initializing BaselineTranslationSystem...")
    system = BaselineTranslationSystem()
    
    if not system.hf_client:
        print("❌ NLLB API not available!")
        return False
    
    print("✅ NLLB API available\n")
    
    # Test translation
    test_proverb = "Nĩ waguo"  # Simple Kikuyu phrase meaning "It's yours"
    
    print(f"2. Testing translation:")
    print(f"   Kikuyu: {test_proverb}")
    print(f"   Translating via https://winstxnhdw-nllb-api.hf.space/api/v4/translator")
    print()
    
    result = system.translate_nllb(test_proverb)
    
    if result.translation.startswith("[ERROR"):
        print(f"❌ Translation failed: {result.translation}")
        return False
    
    print(f"✅ Translation successful!")
    print()
    print(f"   English: {result.translation}")
    print(f"   Time: {result.generation_time:.2f}s")
    print(f"   Confidence: {result.confidence_score}")
    print(f"   Model: {result.metadata.get('model', 'N/A')}")
    print(f"   Backend: {result.metadata.get('backend', 'N/A')}")
    print()
    print("="*80)
    print("✅ NLLB API integration working correctly!")
    print("="*80)
    return True

if __name__ == "__main__":
    success = test_nllb_api()
    sys.exit(0 if success else 1)
