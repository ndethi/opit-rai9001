#!/usr/bin/env python3
"""
Partial Baseline Translation Generator

Generates translations using only the systems                 'raw_llm_translation': raw_llm.translation,
                'raw_llm_reasoning': raw_llm.cultural_meaning or raw_llm.translation,
                'raw_llm_confidence': raw_llm.confidence_score or 0.0,
                'raw_llm_time': raw_llm.generation_time or 0.0,
                'raw_llm_model': raw_llm.metadata.get('model', 'unknown') if raw_llm.metadata else 'unknown',
                'raw_llm_provider': raw_llm.metadata.get('provider', 'unknown') if raw_llm.metadata else 'unknown',
                'raw_llm_model_type': raw_llm.metadata.get('model_type', 'standard') if raw_llm.metadata else 'standard',
                
                # Google Translate
                'google_translation': google.translation,
                'google_time': google.generation_time or 0.0,
                
                # Metadata
                'generation_timestamp': datetime.now().isoformat(),
                'processing_order': idx + 1,
                'systems_included': 'raw_llm,google',
                'og_rag_status': 'pending_implementation'uire OG-RAG:
1. Raw LLM (Direct GPT-4 translation without cultural enhancement)
2. Google Translate (Commercial baseline)

This allows you to:
- Get immediate baseline results without waiting for OG-RAG implementation
- Understand where current systems fail culturally
- Identify gaps that OG-RAG needs to address
- Validate your evaluation pipeline works correctly

Usage:
    # Test with 10 proverbs
    python scripts/generate_baseline_translations_partial.py --max-proverbs 10
    
    # Process all proverbs
    python scripts/generate_baseline_translations_partial.py
    
    # Custom output
    python scripts/generate_baseline_translations_partial.py --output my_partial_baselines.csv
"""

import sys
import argparse
from pathlib import Path
import logging
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict
import time

# Add src to path - but avoid triggering __init__.py by using importlib
import os
import importlib.util

# Change to project root
project_root = Path(__file__).parent.parent
os.chdir(str(project_root))

# Direct import using importlib to bypass __init__.py
spec = importlib.util.spec_from_file_location(
    "baseline_translation_system",
    project_root / "src" / "evaluation" / "baseline_translation_system.py"
)
baseline_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline_module)
BaselineTranslationSystem = baseline_module.BaselineTranslationSystem

# Import ontology gap analyzer
spec2 = importlib.util.spec_from_file_location(
    "ontology_gap_analyzer",
    project_root / "src" / "evaluation" / "ontology_gap_analyzer.py"
)
gap_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(gap_module)
OntologyGapAnalyzer = gap_module.OntologyGapAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PartialBaselineGenerator:
    """
    Generates partial baselines (Raw LLM + Google Translate only).
    Skips OG-RAG to enable immediate progress.
    """
    
    def __init__(self):
        self.system = BaselineTranslationSystem()
        self.gap_analyzer = OntologyGapAnalyzer()
        self.output_dir = Path("data/results/baseline_translations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_partial_baselines(
        self,
        gold_standard_file: str,
        output_file: Optional[str] = None,
        max_proverbs: Optional[int] = None
    ) -> pd.DataFrame:
        """Generate translations from Raw LLM and Google Translate only."""
        
        # Load gold standard
        gold_df = pd.read_csv(gold_standard_file)
        logger.info(f"Loaded {len(gold_df)} proverbs from gold standard")
        
        if max_proverbs:
            gold_df = gold_df.head(max_proverbs)
            logger.info(f"Limited to {max_proverbs} proverbs for processing")
        
        comparison_results = []
        start_time = time.time()
        
        for idx, row in gold_df.iterrows():
            proverb_id = row.get('proverb_id', f'proverb_{idx}')
            kikuyu_text = row.get('kikuyu_text', '')
            expert_translation = row.get('expert_translation', '')
            # Handle NaN values for cultural meaning
            expert_cultural_meaning = row.get('expert_cultural_meaning', '')
            if pd.isna(expert_cultural_meaning):
                expert_cultural_meaning = ''
            else:
                expert_cultural_meaning = str(expert_cultural_meaning)
            
            if not kikuyu_text:
                logger.warning(f"Skipping row {idx}: No Kikuyu text")
                continue
            
            logger.info(f"\n[{idx+1}/{len(gold_df)}] Processing: {proverb_id}")
            logger.info(f"   Kikuyu: {kikuyu_text[:60]}...")
            
            # Generate only Raw LLM and Google Translate
            raw_llm = self.system.translate_raw_llm(kikuyu_text)
            google = self.system.translate_google(kikuyu_text)
            
            # Extract model info from metadata
            raw_llm_model = raw_llm.metadata.get('model', 'unknown') if raw_llm.metadata else 'unknown'
            raw_llm_provider = raw_llm.metadata.get('provider', 'unknown') if raw_llm.metadata else 'unknown'
            
            logger.info(f"   ✓ Raw LLM ({raw_llm_provider}/{raw_llm_model}): {raw_llm.translation[:60]}...")
            logger.info(f"   ✓ Google: {google.translation[:60]}...")
            
            # Analyze ontology gaps for raw LLM
            raw_llm_gap = self.gap_analyzer.analyze_translation_gap(
                expert_translation=expert_translation,
                machine_translation=raw_llm.translation,
                expert_cultural_meaning=expert_cultural_meaning,
                kikuyu_text=kikuyu_text
            )
            
            # Analyze ontology gaps for Google Translate (if not N/A)
            google_gap = None
            if not google.translation.startswith("[ERROR") and not google.translation.startswith("[Google"):
                google_gap = self.gap_analyzer.analyze_translation_gap(
                    expert_translation=expert_translation,
                    machine_translation=google.translation,
                    expert_cultural_meaning=expert_cultural_meaning,
                    kikuyu_text=kikuyu_text
                )
            
            # Compile comprehensive comparison record with clear structure
            comparison_record = {
                # === SOURCE DATA ===
                'proverb_id': proverb_id,
                'kikuyu_original': kikuyu_text,
                
                # === EXPERT BASELINE (Ground Truth) ===
                'expert_translation': expert_translation,
                'expert_cultural_meaning': expert_cultural_meaning,
                
                # === COHERE AYA TRANSLATION ===
                'cohere_aya_translation': raw_llm.translation if 'aya' in raw_llm_model.lower() else '',
                'cohere_aya_model': raw_llm_model if 'aya' in raw_llm_model.lower() else 'N/A',
                'cohere_aya_reasoning': raw_llm.cultural_meaning if 'aya' in raw_llm_model.lower() else '',
                'cohere_aya_confidence': raw_llm.confidence_score if 'aya' in raw_llm_model.lower() else 0.0,
                'cohere_aya_time_sec': raw_llm.generation_time if 'aya' in raw_llm_model.lower() else 0.0,
                'cohere_aya_cultural_score': raw_llm_gap.cultural_context_score if 'aya' in raw_llm_model.lower() else 0.0,
                'cohere_aya_missing_concepts': '; '.join(raw_llm_gap.missing_concepts) if 'aya' in raw_llm_model.lower() else '',
                'cohere_aya_ontology_gaps': '; '.join(raw_llm_gap.recommended_ontology_nodes) if 'aya' in raw_llm_model.lower() else '',
                
                # === OPENAI GPT TRANSLATION ===
                'openai_gpt_translation': raw_llm.translation if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else '',
                'openai_gpt_model': raw_llm_model if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else 'N/A',
                'openai_gpt_reasoning': raw_llm.cultural_meaning if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else '',
                'openai_gpt_confidence': raw_llm.confidence_score if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else 0.0,
                'openai_gpt_time_sec': raw_llm.generation_time if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else 0.0,
                'openai_gpt_cultural_score': raw_llm_gap.cultural_context_score if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else 0.0,
                'openai_gpt_missing_concepts': '; '.join(raw_llm_gap.missing_concepts) if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else '',
                'openai_gpt_ontology_gaps': '; '.join(raw_llm_gap.recommended_ontology_nodes) if 'gpt' in raw_llm_model.lower() or raw_llm_provider == 'openai' else '',
                
                # === GOOGLE TRANSLATE ===
                'google_translate': google.translation,
                'google_translate_status': 'N/A - Kikuyu not supported' if google.translation.startswith("[") else 'Available',
                'google_time_sec': google.generation_time or 0.0,
                'google_cultural_score': google_gap.cultural_context_score if google_gap else 0.0,
                'google_missing_concepts': '; '.join(google_gap.missing_concepts) if google_gap else 'N/A',
                'google_ontology_gaps': '; '.join(google_gap.recommended_ontology_nodes) if google_gap else 'N/A',
                
                # === ONTOLOGY RECOMMENDATIONS ===
                'primary_ontology_gaps': raw_llm_gap.gap_summary,
                'all_missing_concepts': '; '.join(set(raw_llm_gap.missing_concepts + (google_gap.missing_concepts if google_gap else []))),
                'all_ontology_recommendations': '; '.join(set(raw_llm_gap.recommended_ontology_nodes + (google_gap.recommended_ontology_nodes if google_gap else []))),
                
                # === METADATA ===
                'generation_timestamp': datetime.now().isoformat(),
                'processing_order': idx + 1,
                'raw_llm_provider_used': raw_llm_provider,
                'raw_llm_model_used': raw_llm_model
            }
            
            comparison_results.append(comparison_record)
            
            # Save incrementally every 10 proverbs
            if (idx + 1) % 10 == 0:
                self._save_incremental_results(comparison_results, output_file)
        
        # Create final DataFrame
        results_df = pd.DataFrame(comparison_results)
        
        # Save final results
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"translation_comparison_partial_{timestamp}.csv"
        
        output_path = self.output_dir / output_file
        results_df.to_csv(output_path, index=False)
        
        total_time = time.time() - start_time
        
        logger.info(f"\n{'='*80}")
        logger.info(f"✅ PARTIAL BASELINE GENERATION COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Processed: {len(results_df)} proverbs")
        logger.info(f"Systems: Raw LLM, Google Translate")
        logger.info(f"Total time: {total_time:.1f}s ({total_time/len(results_df):.1f}s per proverb)")
        logger.info(f"Output: {output_path}")
        logger.info(f"{'='*80}\n")
        
        # Generate summary report
        self._generate_summary_report(results_df, output_path, total_time)
        
        return results_df
    
    def _save_incremental_results(self, results: List[Dict], output_file: Optional[str]):
        """Save results incrementally to prevent data loss."""
        if output_file is None:
            output_file = "translation_comparison_partial_incremental.csv"
        
        output_path = self.output_dir / output_file
        pd.DataFrame(results).to_csv(output_path, index=False)
        logger.info(f"   💾 Incremental save: {len(results)} proverbs")
    
    def _generate_summary_report(self, results_df: pd.DataFrame, output_path: Path, total_time: float):
        """Generate summary statistics report."""
        report_path = output_path.parent / f"{output_path.stem}_summary.txt"
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("PARTIAL BASELINE TRANSLATION GENERATION SUMMARY\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Proverbs: {len(results_df)}\n")
            f.write(f"Total Time: {total_time:.1f}s ({total_time/len(results_df):.1f}s per proverb)\n\n")
            
            f.write("TRANSLATION SYSTEMS STATUS:\n")
            
            # Check which systems were actually used
            cohere_used = 'cohere_aya_translation' in results_df.columns and not results_df['cohere_aya_translation'].isna().all()
            openai_used = 'openai_gpt_translation' in results_df.columns and not results_df['openai_gpt_translation'].isna().all()
            google_used = 'google_translation' in results_df.columns and results_df['google_translation'].notna().any()
            
            if cohere_used:
                f.write("  ✅ Cohere Aya-23 - Multilingual model optimized for 100+ languages\n")
                f.write("     🌍 Specifically designed for low-resource languages including African languages\n")
            
            if openai_used:
                f.write("  ✅ OpenAI GPT - Industry standard for comparison\n")
            else:
                f.write("  ⚠️  OpenAI GPT - Not available (quota exceeded or key not set)\n")
                f.write("     💡 Add credits at https://platform.openai.com/account/billing to enable\n")
            
            if google_used:
                f.write("  ⚠️  Google Translate - Limited/No Kikuyu support\n")
            else:
                f.write("  ❌ Google Translate - Kikuyu not supported\n")
            
            f.write("\n")
            f.write("SYSTEM NOT INCLUDED (Yet):\n")
            f.write("  - OG-RAG: Pending implementation\n")
            f.write("  - Will be added when ontology-enhanced RAG system is ready\n\n")
            
            f.write("GENERATION TIME STATISTICS:\n")
            # Use new column names
            cohere_time_col = 'cohere_aya_time_sec' if 'cohere_aya_time_sec' in results_df.columns else 'openai_gpt_time_sec'
            if cohere_time_col in results_df.columns:
                avg_time = results_df[cohere_time_col].replace(0, pd.NA).mean()
                f.write(f"  Raw LLM avg time: {avg_time:.2f}s\n" if not pd.isna(avg_time) else "  Raw LLM avg time: N/A\n")
            if 'google_time_sec' in results_df.columns:
                google_avg = results_df['google_time_sec'].replace(0, pd.NA).mean()
                f.write(f"  Google avg time: {google_avg:.2f}s\n\n" if not pd.isna(google_avg) else "  Google avg time: N/A\n\n")
            
            f.write("CULTURAL PRESERVATION SCORES:\n")
            # Use cultural scores instead of confidence
            if 'cohere_aya_cultural_score' in results_df.columns:
                cohere_scores = results_df['cohere_aya_cultural_score'].replace(0, pd.NA)
                if not cohere_scores.isna().all():
                    f.write(f"  Cohere Aya avg: {cohere_scores.mean():.2f}\n")
                    f.write(f"  Cohere Aya min: {cohere_scores.min():.2f}\n")
                    f.write(f"  Cohere Aya max: {cohere_scores.max():.2f}\n")
            if 'openai_gpt_cultural_score' in results_df.columns:
                gpt_scores = results_df['openai_gpt_cultural_score'].replace(0, pd.NA)
                if not gpt_scores.isna().all():
                    f.write(f"  OpenAI GPT avg: {gpt_scores.mean():.2f}\n")
            f.write("\n")
            
            f.write("OUTPUT FILES:\n")
            f.write(f"  Main dataset: {output_path.name}\n")
            f.write(f"  Summary report: {report_path.name}\n\n")
            
            f.write("WHAT YOU CAN DO WITH THESE RESULTS:\n")
            f.write("  1. ✅ Run statistical analysis (BLEU, ROUGE, METEOR)\n")
            f.write("  2. ✅ Test cultural metrics evaluation\n")
            f.write("  3. ✅ Run LLM-as-a-Judge evaluation\n")
            f.write("  4. ✅ Identify cultural gaps and mistranslations\n")
            f.write("  5. ✅ Document what OG-RAG needs to fix\n\n")
            
            f.write("INSIGHTS TO GATHER:\n")
            f.write("  - Where does Raw LLM fail culturally?\n")
            f.write("  - What traditional wisdom gets lost?\n")
            f.write("  - Which metaphors are mistranslated?\n")
            f.write("  - What cultural context is missing?\n")
            f.write("  - What should your ontology capture?\n\n")
            
            f.write("NEXT STEPS:\n")
            f.write("  1. Analyze these baseline results\n")
            f.write("  2. Document cultural failures and gaps\n")
            f.write("  3. Design OG-RAG requirements based on findings\n")
            f.write("  4. Build OG-RAG to address identified gaps\n")
            f.write("  5. Re-run with all 3 systems for full comparison\n\n")
            
            # Add recommendation for OpenAI if not used
            if not openai_used:
                f.write("⭐ RECOMMENDATION FOR THESIS:\n")
                f.write("  OpenAI GPT-4 is considered the industry gold standard for NLP tasks.\n")
                f.write("  For academic credibility and comprehensive comparison:\n")
                f.write("  - Add $5-10 credits to OpenAI account at https://platform.openai.com/account/billing\n")
                f.write("  - Re-run baseline generation to include GPT-4 results\n")
                f.write("  - Compare: Expert vs Cohere Aya vs OpenAI GPT-4 vs Google Translate\n")
                f.write("  - This will strengthen your thesis validation significantly\n\n")
            
            f.write("TO ADD OG-RAG LATER:\n")
            f.write("  When your OG-RAG system is ready, run:\n")
            f.write("  python scripts/generate_baseline_translations.py\n")
            f.write("  (This will generate translations from all 3 systems)\n\n")
            
            f.write("="*80 + "\n")
        
        logger.info(f"📊 Summary report saved: {report_path}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate partial baseline translations (Raw LLM + Google only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with 10 proverbs
  python generate_baseline_translations_partial.py --max-proverbs 10
  
  # Process first 50 proverbs
  python generate_baseline_translations_partial.py --max-proverbs 50
  
  # Process all proverbs
  python generate_baseline_translations_partial.py
  
  # Custom output file
  python generate_baseline_translations_partial.py --output my_baselines.csv

Purpose:
  Generate baseline translations WITHOUT OG-RAG to:
  - Get immediate results today
  - Understand where current systems fail
  - Identify what OG-RAG needs to fix
  - Validate evaluation pipeline works
        """
    )
    
    parser.add_argument(
        '--input',
        type=str,
        default='data/evaluation/gold_standard_ireri.csv',
        help='Path to gold standard CSV file'
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
    
    return parser.parse_args()


def check_api_keys():
    """Check if required API keys are available."""
    import os
    
    issues = []
    
    openai_key = os.getenv('OPENAI_API_KEY')
    cohere_key = os.getenv('COHERE_API_KEY')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        if not cohere_key:
            issues.append("❌ Neither OPENAI_API_KEY nor COHERE_API_KEY set - need at least one for Raw LLM")
            issues.append("   Set in .env file or: export OPENAI_API_KEY='sk-...' or COHERE_API_KEY='...'")
        else:
            logger.info("✓ Cohere API key found (OpenAI not available)")
    else:
        logger.info("✓ OpenAI API key found")
    
    try:
        import deep_translator
        logger.info("✓ deep-translator library available")
    except ImportError:
        issues.append("⚠️  deep-translator not installed - Google Translate will be unavailable")
        issues.append("   Install with: pip install deep-translator")
    
    return issues


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Load environment variables FIRST
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\n" + "="*80)
    print("PARTIAL BASELINE TRANSLATION GENERATION")
    print("="*80)
    print("\nSystems: Raw LLM (Cohere Aya-23 🌍) + Google Translate (OG-RAG pending)")
    print("Purpose: Get immediate baseline results to inform OG-RAG design")
    print("Note: Using Cohere Aya-23 - multilingual model optimized for low-resource languages")
    print("="*80 + "\n")
    
    # Check prerequisites
    issues = check_api_keys()
    if issues:
        print("⚠️  Setup Issues Detected:\n")
        for issue in issues:
            print(f"  {issue}")
        
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
    
    print("\nInitializing partial baseline system...")
    
    try:
        generator = PartialBaselineGenerator()
        
        print("\nStarting partial baseline generation...")
        print("This generates Raw LLM + Google Translate baselines only.\n")
        
        results_df = generator.generate_partial_baselines(
            gold_standard_file=args.input,
            output_file=args.output,
            max_proverbs=args.max_proverbs
        )
        
        print("\n" + "="*80)
        print("✅ SUCCESS: Partial baselines generated")
        print("="*80)
        print(f"\nProcessed: {len(results_df)} proverbs")
        print(f"Systems: Raw LLM, Google Translate")
        print(f"Output: data/results/baseline_translations/")
        print("\nWhat You Can Do Now:")
        print("  1. ✅ Analyze where Raw LLM fails culturally")
        print("  2. ✅ Document cultural gaps and mistranslations")
        print("  3. ✅ Run statistical analysis on these baselines")
        print("  4. ✅ Test LLM-as-a-Judge evaluation")
        print("  5. ✅ Design OG-RAG based on identified gaps")
        print("\nWhen OG-RAG is Ready:")
        print("  python scripts/generate_baseline_translations.py")
        print("  (This will add OG-RAG to the comparison)")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        print("Partial results saved to data/results/baseline_translations/")
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        logger.exception("Detailed error:")


if __name__ == "__main__":
    main()
