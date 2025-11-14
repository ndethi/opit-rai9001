#!/usr/bin/env python3
"""
Run Cultural Fidelity Evaluation on OG-RAG 100-Proverb Results

Executes comprehensive cultural metrics analysis on the completed evaluation,
providing cultural authenticity, translation fidelity, and quality assessments
beyond BLEU scores.

Author: Nixon Dethi
Date: November 14, 2025
"""

import pandas as pd
import sys
from pathlib import Path
import logging
from typing import Dict, List
import json
from datetime import datetime
from tqdm import tqdm

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.evaluation.cultural_metrics import (
    CulturalTranslationMetrics,
    CulturalMetricsConfig,
    CulturalEvaluationResult
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CulturalFidelityEvaluator:
    """Run cultural fidelity evaluation on translation results."""
    
    def __init__(self, config: CulturalMetricsConfig = None):
        """Initialize cultural fidelity evaluator."""
        self.config = config or CulturalMetricsConfig()
        logger.info("Initializing Cultural Fidelity Evaluator...")
        self.metrics = CulturalTranslationMetrics(self.config)
        logger.info("✅ Cultural metrics system loaded")
    
    def evaluate_translation(self, 
                           proverb_id: str,
                           kikuyu_text: str,
                           expert_translation: str,
                           translation: str,
                           system_name: str) -> Dict:
        """Evaluate a single translation for cultural fidelity."""
        
        try:
            # Calculate cultural authenticity
            cultural_result = self.metrics.calculate_cultural_authenticity_score(
                translation=translation,
                expert_translation=expert_translation,
                cultural_context="",  # Can enhance with ontology context later
                og_rag_context=""
            )
            
            # Calculate translation fidelity
            fidelity_result = self.metrics.calculate_translation_fidelity(
                translation=translation,
                expert_translation=expert_translation
            )
            
            # Calculate overall quality score
            cultural_auth = cultural_result.get('cultural_authenticity', 0.0)
            overall_fidelity = fidelity_result.get('overall_fidelity', 0.0)
            
            overall_quality = (
                cultural_auth * self.config.cultural_weight +
                overall_fidelity * self.config.fidelity_weight
            )
            
            # Determine quality grade
            if overall_quality >= 0.9:
                grade = 'A'
            elif overall_quality >= 0.8:
                grade = 'B'
            elif overall_quality >= 0.7:
                grade = 'C'
            elif overall_quality >= 0.6:
                grade = 'D'
            else:
                grade = 'F'
            
            # Generate recommendations
            recommendations = []
            if cultural_auth < 0.6:
                recommendations.append("Low cultural authenticity - review cultural concept preservation")
            if overall_fidelity < 0.5:
                recommendations.append("Low translation fidelity - significant deviation from expert translation")
            if cultural_result.get('kikuyu_analysis', {}).get('concept_preservation', 0) < 0.5:
                recommendations.append("Cultural concepts not well preserved - check metaphor/idiom handling")
            
            return {
                'proverb_id': proverb_id,
                'kikuyu_text': kikuyu_text,
                'system': system_name,
                'translation': translation,
                'expert_translation': expert_translation,
                'cultural_authenticity': cultural_auth,
                'semantic_similarity': cultural_result.get('semantic_similarity', 0.0),
                'context_preservation': cultural_result.get('context_preservation', 0.0),
                'translation_fidelity': overall_fidelity,
                'rouge1_f': fidelity_result.get('rouge1_f', 0.0),
                'rouge2_f': fidelity_result.get('rouge2_f', 0.0),
                'rougeL_f': fidelity_result.get('rougeL_f', 0.0),
                'word_overlap': fidelity_result.get('word_overlap', 0.0),
                'structural_similarity': fidelity_result.get('structural_similarity', 0.0),
                'overall_quality': overall_quality,
                'quality_grade': grade,
                'recommendations': '; '.join(recommendations) if recommendations else 'Good quality translation',
                'evaluation_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error evaluating {proverb_id} ({system_name}): {e}")
            return {
                'proverb_id': proverb_id,
                'system': system_name,
                'error': str(e)
            }
    
    def evaluate_dataset(self, input_file: str, output_file: str) -> pd.DataFrame:
        """Evaluate entire dataset for cultural fidelity."""
        
        logger.info(f"Loading evaluation data from: {input_file}")
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} proverbs")
        
        all_results = []
        
        # Evaluate each translation system
        systems = [
            ('raw_translation', 'Raw GPT-4'),
            ('trad_rag_translation', 'Traditional RAG'),
            ('ograg_translation', 'OG-RAG')
        ]
        
        total_evaluations = len(df) * len(systems)
        
        with tqdm(total=total_evaluations, desc="Evaluating translations") as pbar:
            for idx, row in df.iterrows():
                proverb_id = row['proverb_id']
                kikuyu_text = row['kikuyu_text']
                expert_translation = row['expert_translation']
                
                for translation_col, system_name in systems:
                    translation = row.get(translation_col, '')
                    
                    if pd.isna(translation) or not translation:
                        logger.warning(f"Missing translation for {proverb_id} ({system_name})")
                        pbar.update(1)
                        continue
                    
                    result = self.evaluate_translation(
                        proverb_id=proverb_id,
                        kikuyu_text=kikuyu_text,
                        expert_translation=expert_translation,
                        translation=translation,
                        system_name=system_name
                    )
                    
                    all_results.append(result)
                    pbar.update(1)
        
        # Create results DataFrame
        results_df = pd.DataFrame(all_results)
        
        # Save results
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(output_path, index=False)
        logger.info(f"✅ Results saved to: {output_path}")
        
        # Generate summary statistics
        self._generate_summary_report(results_df, output_path.parent)
        
        return results_df
    
    def _generate_summary_report(self, results_df: pd.DataFrame, output_dir: Path):
        """Generate summary report of cultural fidelity evaluation."""
        
        logger.info("Generating summary report...")
        
        summary = {}
        
        for system in results_df['system'].unique():
            system_data = results_df[results_df['system'] == system]
            
            summary[system] = {
                'total_evaluations': len(system_data),
                'cultural_authenticity': {
                    'mean': system_data['cultural_authenticity'].mean(),
                    'std': system_data['cultural_authenticity'].std(),
                    'min': system_data['cultural_authenticity'].min(),
                    'max': system_data['cultural_authenticity'].max()
                },
                'translation_fidelity': {
                    'mean': system_data['translation_fidelity'].mean(),
                    'std': system_data['translation_fidelity'].std(),
                    'min': system_data['translation_fidelity'].min(),
                    'max': system_data['translation_fidelity'].max()
                },
                'overall_quality': {
                    'mean': system_data['overall_quality'].mean(),
                    'std': system_data['overall_quality'].std(),
                    'min': system_data['overall_quality'].min(),
                    'max': system_data['overall_quality'].max()
                },
                'grade_distribution': system_data['quality_grade'].value_counts().to_dict()
            }
        
        # Save summary
        summary_file = output_dir / 'cultural_evaluation_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, indent=2, fp=f)
        
        logger.info(f"✅ Summary saved to: {summary_file}")
        
        # Print summary to console
        print("\n" + "=" * 80)
        print("CULTURAL FIDELITY EVALUATION SUMMARY")
        print("=" * 80)
        
        for system, stats in summary.items():
            print(f"\n📊 {system}")
            print(f"   Cultural Authenticity: {stats['cultural_authenticity']['mean']:.3f} ± {stats['cultural_authenticity']['std']:.3f}")
            print(f"   Translation Fidelity:  {stats['translation_fidelity']['mean']:.3f} ± {stats['translation_fidelity']['std']:.3f}")
            print(f"   Overall Quality:       {stats['overall_quality']['mean']:.3f} ± {stats['overall_quality']['std']:.3f}")
            print(f"   Grade Distribution:    {stats['grade_distribution']}")
        
        print("\n" + "=" * 80)
        
        # Statistical comparison
        print("\n📈 COMPARATIVE ANALYSIS")
        print("=" * 80)
        
        raw_quality = summary['Raw GPT-4']['overall_quality']['mean']
        trad_quality = summary['Traditional RAG']['overall_quality']['mean']
        ograg_quality = summary['OG-RAG']['overall_quality']['mean']
        
        ograg_improvement_vs_raw = ((ograg_quality - raw_quality) / raw_quality) * 100
        ograg_improvement_vs_trad = ((ograg_quality - trad_quality) / trad_quality) * 100
        
        print(f"OG-RAG vs Raw GPT-4:       {ograg_improvement_vs_raw:+.1f}% ({ograg_quality:.3f} vs {raw_quality:.3f})")
        print(f"OG-RAG vs Traditional RAG: {ograg_improvement_vs_trad:+.1f}% ({ograg_quality:.3f} vs {trad_quality:.3f})")
        print("=" * 80)


def main():
    """Main execution function."""
    
    print("=" * 80)
    print("🎯 CULTURAL FIDELITY EVALUATION - OG-RAG 100 Proverbs")
    print("=" * 80)
    print()
    
    # Input/output files
    input_file = "data/results/ograg_translations/ograg_evaluation_100proverbs.csv"
    output_file = "data/results/cultural_evaluation_100proverbs.csv"
    
    # Verify input file exists
    if not Path(input_file).exists():
        print(f"❌ Error: Input file not found: {input_file}")
        return 1
    
    try:
        # Initialize evaluator
        evaluator = CulturalFidelityEvaluator()
        
        # Run evaluation
        print(f"📂 Input:  {input_file}")
        print(f"📂 Output: {output_file}")
        print()
        
        results_df = evaluator.evaluate_dataset(input_file, output_file)
        
        print()
        print("=" * 80)
        print("✅ CULTURAL FIDELITY EVALUATION COMPLETE")
        print("=" * 80)
        print(f"\n✨ Evaluated {len(results_df)} translations")
        print(f"📁 Results saved to: {output_file}")
        print(f"📊 Summary saved to: data/results/cultural_evaluation_summary.json")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
