#!/usr/bin/env python3
"""
Test script for NLLB-200 integration in Baseline Translation System

This script tests the newly integrated NLLB translation capability with sample Kikuyu proverbs.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.baseline_translation_system import BaselineTranslationSystem
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_nllb_translation():
    """Test NLLB translation with sample Kikuyu proverbs."""
    
    print("\n" + "="*80)
    print("TESTING NLLB-200 INTEGRATION")
    print("="*80 + "\n")
    
    # Initialize system
    print("Initializing BaselineTranslationSystem...")
    system = BaselineTranslationSystem()
    
    # Sample Kikuyu proverbs from your gold standard
    test_proverbs = [
        {
            "id": "MW_001",
            "kikuyu": "Aikaragia mbia ta njuu ngigi.",
            "expert_en": "He looks after his money the way storks pursue locusts.",
            "meaning": "Whoever has much always wants more."
        },
        {
            "id": "MW_002",
            "kikuyu": "Andu ni indo.",
            "expert_en": "People are wealth.",
            "meaning": "Wealth emanates from people."
        },
        {
            "id": "MW_003",
            "kikuyu": "Bururi uri ngui ndungiciarikira indo.",
            "expert_en": "In an unstable country one cannot become wealthy",
            "meaning": "Political stability facilitates wealth."
        }
    ]
    
    print("\nTesting NLLB translation on sample proverbs...\n")
    
    for proverb in test_proverbs:
        print(f"\n{'='*80}")
        print(f"Proverb ID: {proverb['id']}")
        print(f"Kikuyu: {proverb['kikuyu']}")
        print(f"Expert Translation: {proverb['expert_en']}")
        print(f"Expert Meaning: {proverb['meaning']}")
        print("-"*80)
        
        try:
            # Test NLLB translation
            result = system.translate_nllb(proverb['kikuyu'])
            
            print(f"\nNLLB Translation: {result.translation}")
            print(f"Generation Time: {result.generation_time:.2f}s")
            print(f"System: {result.system_name}")
            print(f"Metadata: {result.metadata}")
            
            # Compare with expert
            print(f"\n📊 Comparison:")
            print(f"   Expert: {proverb['expert_en']}")
            print(f"   NLLB:   {result.translation}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        print("="*80)
    
    print("\n✅ NLLB Integration Test Complete!\n")


def test_all_systems_comparison():
    """Test all translation systems together (quick test with 1 proverb)."""
    
    print("\n" + "="*80)
    print("TESTING ALL SYSTEMS COMPARISON")
    print("="*80 + "\n")
    
    system = BaselineTranslationSystem()
    
    test_proverb = "Andu ni indo."  # People are wealth
    
    print(f"Test Proverb: {test_proverb}\n")
    
    try:
        # Generate translations from all systems
        results = system.generate_all_translations(test_proverb, "TEST_001")
        
        print("\n📊 TRANSLATION COMPARISON:\n")
        print("-"*80)
        
        for system_name, result in results.items():
            print(f"\n{system_name.upper()}:")
            print(f"  Translation: {result.translation[:100]}...")
            print(f"  Time: {result.generation_time:.2f}s")
            if result.confidence_score:
                print(f"  Confidence: {result.confidence_score:.2f}")
        
        print("\n" + "-"*80)
        print("\n✅ All Systems Test Complete!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🚀 Starting NLLB Integration Tests...\n")
    
    # Test 1: NLLB-only translation
    test_nllb_translation()
    
    # Test 2: All systems comparison
    test_all_systems_comparison()
    
    print("\n" + "="*80)
    print("All tests complete!")
    print("="*80 + "\n")
    
    print("\n📝 NEXT STEPS:")
    print("  1. Run full baseline generation on gold standard dataset")
    print("  2. Analyze NLLB translation quality vs expert translations")
    print("  3. Compare NLLB (specialized MT) vs Raw LLM (general AI)")
    print("  4. Identify cultural gaps for ontology development\n")
