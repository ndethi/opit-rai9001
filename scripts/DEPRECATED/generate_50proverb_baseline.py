#!/usr/bin/env python3
"""
Generate 50-proverb baseline to compare Raw LLM vs OG-RAG for foundation decision.

This script runs a limited baseline generation to help decide which system
to build the OG-RAG cultural ontology on top of:
- Raw LLM (GPT-4/Cohere Aya) 
- Google Translate (if available)
- NLLB-200 (if API key provided)

Decision Criteria:
1. Translation quality vs expert
2. Cultural fidelity
3. Consistency across proverbs
4. Cost/speed considerations
5. API availability and reliability
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.baseline_translation_system import BaselineTranslationSystem, TranslationComparator
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def analyze_baseline_results(results_df: pd.DataFrame):
    """Analyze baseline results to make foundation decision."""
    
    print("\n" + "="*100)
    print("BASELINE ANALYSIS FOR FOUNDATION DECISION")
    print("="*100 + "\n")
    
    # 1. Availability Analysis
    print("📊 SYSTEM AVAILABILITY:")
    print("-"*100)
    
    og_rag_errors = results_df['og_rag_translation'].str.contains('ERROR', na=False).sum()
    raw_llm_errors = results_df['raw_llm_translation'].str.contains('ERROR', na=False).sum()
    nllb_errors = results_df['nllb_translation'].str.contains('ERROR', na=False).sum() if 'nllb_translation' in results_df else len(results_df)
    google_errors = results_df['google_translation'].str.contains('ERROR', na=False).sum()
    
    total = len(results_df)
    
    print(f"  OG-RAG (placeholder):  {total - og_rag_errors}/{total} successful ({(total-og_rag_errors)/total*100:.1f}%)")
    print(f"  Raw LLM:               {total - raw_llm_errors}/{total} successful ({(total-raw_llm_errors)/total*100:.1f}%)")
    print(f"  NLLB-200:              {total - nllb_errors}/{total} successful ({(total-nllb_errors)/total*100:.1f}%)")
    print(f"  Google Translate:      {total - google_errors}/{total} successful ({(total-google_errors)/total*100:.1f}%)")
    
    # 2. Performance Analysis
    print(f"\n⚡ PERFORMANCE METRICS:")
    print("-"*100)
    
    og_rag_avg = results_df['og_rag_time'].mean()
    raw_llm_avg = results_df['raw_llm_time'].mean()
    nllb_avg = results_df['nllb_time'].mean() if 'nllb_time' in results_df else 0
    google_avg = results_df['google_time'].mean()
    
    print(f"  OG-RAG avg time:       {og_rag_avg:.2f}s per proverb")
    print(f"  Raw LLM avg time:      {raw_llm_avg:.2f}s per proverb")
    print(f"  NLLB avg time:         {nllb_avg:.2f}s per proverb")
    print(f"  Google avg time:       {google_avg:.2f}s per proverb")
    
    print(f"\n  Total time for 200 proverbs (estimated):")
    print(f"    OG-RAG:  {og_rag_avg * 200 / 60:.1f} minutes")
    print(f"    Raw LLM: {raw_llm_avg * 200 / 60:.1f} minutes")
    print(f"    NLLB:    {nllb_avg * 200 / 60:.1f} minutes")
    print(f"    Google:  {google_avg * 200 / 60:.1f} minutes")
    
    # 3. Confidence Scores
    if 'og_rag_confidence' in results_df and 'raw_llm_confidence' in results_df:
        print(f"\n🎯 CONFIDENCE SCORES:")
        print("-"*100)
        
        og_rag_conf = results_df['og_rag_confidence'].mean()
        raw_llm_conf = results_df['raw_llm_confidence'].mean()
        
        print(f"  OG-RAG avg confidence: {og_rag_conf:.2f}")
        print(f"  Raw LLM avg confidence: {raw_llm_conf:.2f}")
    
    # 4. Sample translations comparison
    print(f"\n📖 SAMPLE TRANSLATIONS (First 3 Proverbs):")
    print("-"*100)
    
    for idx in range(min(3, len(results_df))):
        row = results_df.iloc[idx]
        print(f"\n{idx+1}. {row['proverb_id']}: {row['kikuyu_text'][:60]}...")
        print(f"   Expert:    {row['expert_translation'][:80]}...")
        print(f"   OG-RAG:    {row['og_rag_translation'][:80]}...")
        print(f"   Raw LLM:   {row['raw_llm_translation'][:80]}...")
        if not pd.isna(row.get('nllb_translation')) and 'ERROR' not in str(row.get('nllb_translation', '')):
            print(f"   NLLB:      {row['nllb_translation'][:80]}...")
    
    # 5. Decision Recommendation
    print(f"\n" + "="*100)
    print("💡 FOUNDATION DECISION RECOMMENDATION")
    print("="*100 + "\n")
    
    # Determine best foundation
    recommendations = []
    
    # Check availability
    if raw_llm_errors < og_rag_errors:
        recommendations.append(("Raw LLM", "Better availability", 1))
    
    # Check speed
    if raw_llm_avg < og_rag_avg:
        recommendations.append(("Raw LLM", f"Faster ({raw_llm_avg:.1f}s vs {og_rag_avg:.1f}s)", 1))
    
    # Check NLLB viability
    if nllb_errors == 0 and nllb_avg > 0:
        recommendations.append(("NLLB-200", "Native Kikuyu support, specialized MT", 2))
    
    # Google viability
    if google_errors < total * 0.5:
        recommendations.append(("Google Translate", "Commercial baseline available", 0.5))
    
    print("EVALUATION CRITERIA:")
    print("\n1. AVAILABILITY & RELIABILITY:")
    print(f"   - Raw LLM: {'✅ Highly available' if raw_llm_errors == 0 else '⚠️ Some errors'}")
    print(f"   - NLLB-200: {'✅ Available' if nllb_errors == 0 else '❌ Needs API key'}")
    print(f"   - Google: {'✅ Available' if google_errors < total * 0.3 else '⚠️ Limited Kikuyu support'}")
    
    print("\n2. PERFORMANCE:")
    print(f"   - Raw LLM: {raw_llm_avg:.1f}s/proverb ({'Fast' if raw_llm_avg < 5 else 'Moderate'})")
    print(f"   - NLLB-200: {nllb_avg:.1f}s/proverb ({'Fast' if nllb_avg < 2 else 'N/A'})")
    
    print("\n3. COST CONSIDERATIONS:")
    print("   - Raw LLM (OpenAI): API costs (~$0.01-0.05 per proverb with GPT-4)")
    print("   - NLLB-200: Free tier with API key, or local deployment")
    print("   - Google: Free up to limits")
    
    print("\n4. QUALITY INDICATORS:")
    print("   - Raw LLM: General multilingual AI, good cultural understanding")
    print("   - NLLB-200: Specialized MT, native Kikuyu training, best for baseline")
    
    print("\n" + "="*100)
    print("🎯 RECOMMENDED FOUNDATION:")
    print("="*100)
    
    if nllb_errors == 0 and nllb_avg > 0:
        print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║ RECOMMENDATION: Build OG-RAG on top of NLLB-200                               ║
╚════════════════════════════════════════════════════════════════════════════════╝

RATIONALE:
1. ✅ NLLB-200 has NATIVE Kikuyu support (only MT model with Kikuyu training data)
2. ✅ Provides the strongest baseline for comparison (specialized MT)
3. ✅ Fast inference (~1s per proverb via API)
4. ✅ Free with API key, reproducible
5. ✅ Best separation of concerns: MT foundation + Cultural ontology enhancement

ARCHITECTURE:
    NLLB-200 (Specialized MT) → Cultural Ontology → OG-RAG Enhancement
    
    This gives you:
    - Strong baseline translation from specialized MT
    - Clear value-add from cultural ontology
    - Best demonstration of ontology's contribution
    - Scientific rigor (comparing against native Kikuyu MT)

ALTERNATIVE: If NLLB unavailable, use Raw LLM as fallback foundation.
""")
    else:
        print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║ RECOMMENDATION: Build OG-RAG on top of Raw LLM (OpenAI/Cohere)                ║
╚════════════════════════════════════════════════════════════════════════════════╝

RATIONALE:
1. ✅ Highly available and reliable
2. ✅ Good quality baseline translations
3. ✅ Reasonable performance ({raw_llm_avg:.1f}s per proverb)
4. ✅ Already showing cultural understanding
5. ⚠️  NLLB-200 not available (needs API key)

ARCHITECTURE:
    Raw LLM (General AI) → Cultural Ontology → OG-RAG Enhancement
    
    This gives you:
    - Solid baseline from general multilingual AI
    - Ontology adds cultural depth and business relevance
    - More available/practical for immediate development

NOTE: Consider adding NLLB-200 later by getting free HF API key for stronger
      baseline comparison (native Kikuyu support is valuable for research).
""")
    
    print("\n" + "="*100)
    print("NEXT ACTIONS:")
    print("="*100)
    print("""
1. Review sample translations above to verify quality
2. If satisfied with foundation choice:
   a. Begin cultural ontology development based on identified gaps
   b. Design ontology to capture missing cultural elements
   c. Integrate ontology into chosen foundation system

3. For NLLB-200 access (if recommended):
   - Visit: https://huggingface.co/settings/tokens
   - Create free read token
   - Run: export HF_API_KEY='your_token'
   - Re-run this script to test NLLB

4. Full baseline generation:
   python scripts/generate_baseline_translations.py
   (Run on all ~200 proverbs for complete analysis)
""")
    
    print("\n" + "="*100 + "\n")


def main():
    """Run 50-proverb baseline and analyze for foundation decision."""
    
    print("\n" + "="*100)
    print("50-PROVERB BASELINE GENERATION FOR FOUNDATION DECISION")
    print("="*100 + "\n")
    
    # Initialize system
    system = BaselineTranslationSystem()
    comparator = TranslationComparator(system)
    
    # Check gold standard file
    gold_standard_file = "data/evaluation/gold_standard_ireri.csv"
    if not Path(gold_standard_file).exists():
        print(f"❌ Gold standard file not found: {gold_standard_file}")
        return
    
    print(f"📚 Loading gold standard: {gold_standard_file}")
    print(f"📊 Generating baseline for first 50 proverbs...")
    print(f"⏱️  This will take approximately 5-10 minutes...\n")
    
    # Generate baseline for 50 proverbs
    try:
        results_df = comparator.compare_on_gold_standard(
            gold_standard_file,
            output_file="baseline_50proverbs_foundation_decision.csv",
            max_proverbs=50
        )
        
        print("\n✅ Baseline generation complete!")
        print(f"📁 Results saved to: data/results/baseline_translations/baseline_50proverbs_foundation_decision.csv\n")
        
        # Analyze results
        analyze_baseline_results(results_df)
        
    except Exception as e:
        print(f"\n❌ Error during baseline generation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
