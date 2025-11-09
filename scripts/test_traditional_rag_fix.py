#!/usr/bin/env python3
"""
Test Traditional RAG Fix
========================
Quick test to verify Traditional RAG no longer leaks expert translations.

Tests:
1. Load sample proverbs from CSV
2. Translate using fixed Traditional RAG
3. Check for perfect BLEU matches (should be 0)
4. Compare translations to expert translations (should NOT be identical)
"""

import sys
from pathlib import Path

# Add project root and og-rag-system to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src' / 'og-rag-system'))

import pandas as pd
from sacrebleu import sentence_bleu
from ograg_translator import OGRAGTranslator

def test_traditional_rag_fix():
    """Test that Traditional RAG no longer produces perfect matches."""
    
    print("=" * 80)
    print("TRADITIONAL RAG FIX VALIDATION TEST")
    print("=" * 80)
    
    # Load evaluation data
    eval_csv = project_root / "data/results/ograg_translations/ograg_evaluation_100proverbs.csv"
    df = pd.read_csv(eval_csv)
    
    # Select 5 test proverbs (including known perfect matchers)
    test_proverbs = [
        ("MW_001", "Aikaragia mbia ta njuu ngigi"),  # Known perfect match before
        ("MW_002", "Andũ nĩo ũtonga"),                # Known perfect match before
        ("MW_004", "Bũrũri ũtarĩ kĩhooto gũtiagĩrwo"), # Known perfect match before
        ("MW_010", "Kĩhoto kĩrĩaga igongona"),        # Random test
        ("MW_020", "Mũgunda wa ngũkũ ũthiraga na itua"), # Random test
    ]
    
    # Initialize translator
    print("\n🔧 Initializing OGRAGTranslator...")
    translator = OGRAGTranslator()
    
    print("\n📊 TEST RESULTS:")
    print("-" * 80)
    
    perfect_matches = 0
    results = []
    
    for proverb_id, kikuyu_text in test_proverbs:
        # Get expert translation from CSV
        expert_translation = df[df['proverb_id'] == proverb_id]['expert_translation'].iloc[0]
        
        # Translate with fixed Traditional RAG
        print(f"\n🔍 Testing: {proverb_id}")
        print(f"   Kikuyu: {kikuyu_text}")
        
        result = translator.translate_traditional_rag(kikuyu_text, proverb_id, k=5)
        trad_rag_translation = result.translation
        
        # Calculate BLEU
        bleu = sentence_bleu(trad_rag_translation, [expert_translation])
        
        # Check if perfect match
        is_perfect = (trad_rag_translation.strip().lower() == expert_translation.strip().lower())
        if is_perfect:
            perfect_matches += 1
        
        print(f"   Expert:      {expert_translation}")
        print(f"   Trad RAG:    {trad_rag_translation}")
        print(f"   BLEU Score:  {bleu.score:.2f}")
        print(f"   Perfect Match: {'❌ YES (LEAKAGE!)' if is_perfect else '✅ No'}")
        
        results.append({
            'proverb_id': proverb_id,
            'kikuyu': kikuyu_text,
            'expert': expert_translation,
            'trad_rag': trad_rag_translation,
            'bleu': bleu.score,
            'perfect_match': is_perfect
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 TEST SUMMARY")
    print("=" * 80)
    print(f"Proverbs tested: {len(test_proverbs)}")
    print(f"Perfect matches: {perfect_matches}")
    print(f"Average BLEU:    {sum(r['bleu'] for r in results) / len(results):.2f}")
    
    # Validation
    print("\n🎯 VALIDATION:")
    if perfect_matches == 0:
        print("✅ PASS: No perfect matches detected (data leakage fixed!)")
        avg_bleu = sum(r['bleu'] for r in results) / len(results)
        if avg_bleu < 15:
            print(f"✅ PASS: Average BLEU ({avg_bleu:.2f}) is reasonable (< 15)")
            print("\n🎉 FIX VALIDATED - Ready for full re-run!")
            return True
        else:
            print(f"⚠️  WARNING: Average BLEU ({avg_bleu:.2f}) still high (> 15)")
            print("   May still have subtle data leakage. Investigate further.")
            return False
    else:
        print(f"❌ FAIL: {perfect_matches} perfect matches detected!")
        print("   Data leakage NOT fixed. Check implementation.")
        print("\n🔍 Perfect matches:")
        for r in results:
            if r['perfect_match']:
                print(f"   - {r['proverb_id']}: {r['kikuyu']}")
        return False


if __name__ == '__main__':
    success = test_traditional_rag_fix()
    sys.exit(0 if success else 1)
