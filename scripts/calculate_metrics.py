#!/usr/bin/env python3
"""
OG-RAG Metrics Calculation Script
==================================

Computes evaluation metrics comparing three translation approaches:
1. Raw GPT-4 (baseline)
2. Traditional RAG
3. OG-RAG

Metrics:
- BLEU scores (all 100 proverbs)
- Cultural fidelity via LLM-as-judge (20-proverb sample)
- Statistical tests (paired t-tests, Cohen's d)

Author: Research Team
Date: November 7, 2025
"""

import os
import csv
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import random
from datetime import datetime

# External dependencies
try:
    from sacrebleu.metrics import BLEU
except ImportError:
    print("ERROR: sacrebleu not installed. Run: pip install sacrebleu")
    exit(1)

try:
    import numpy as np
    from scipy import stats
except ImportError:
    print("ERROR: numpy/scipy not installed. Run: pip install numpy scipy")
    exit(1)

# OpenAI for LLM-as-judge
try:
    from openai import OpenAI
    from decouple import config
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("WARNING: OpenAI not available. LLM-as-judge disabled.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProverbMetrics:
    """Metrics for one proverb across all methods."""
    proverb_id: str
    kikuyu_text: str
    expert_translation: str
    
    # BLEU scores
    bleu_raw: float
    bleu_trad_rag: float
    bleu_ograg: float
    
    # Cultural fidelity (LLM-as-judge, 0-1 scale)
    cultural_fidelity_raw: Optional[float] = None
    cultural_fidelity_trad_rag: Optional[float] = None
    cultural_fidelity_ograg: Optional[float] = None
    
    # Failure flags (translation empty or very short)
    failed_raw: bool = False
    failed_trad_rag: bool = False
    failed_ograg: bool = False


@dataclass
class AggregateMetrics:
    """Aggregate statistics across all proverbs."""
    n_proverbs: int
    
    # BLEU
    bleu_raw_mean: float
    bleu_raw_std: float
    bleu_trad_mean: float
    bleu_trad_std: float
    bleu_ograg_mean: float
    bleu_ograg_std: float
    
    # Cultural fidelity
    cultural_raw_mean: Optional[float] = None
    cultural_raw_std: Optional[float] = None
    cultural_trad_mean: Optional[float] = None
    cultural_trad_std: Optional[float] = None
    cultural_ograg_mean: Optional[float] = None
    cultural_ograg_std: Optional[float] = None
    
    # Failure rates
    failure_rate_raw: float = 0.0
    failure_rate_trad: float = 0.0
    failure_rate_ograg: float = 0.0
    
    # Statistical tests (Raw vs OG-RAG on BLEU)
    bleu_ttest_pvalue: Optional[float] = None
    bleu_cohens_d: Optional[float] = None
    
    # Cultural fidelity tests
    cultural_ttest_pvalue: Optional[float] = None
    cultural_cohens_d: Optional[float] = None


class MetricsCalculator:
    """Calculate evaluation metrics from OG-RAG evaluation results."""
    
    def __init__(
        self,
        evaluation_csv: str,
        sample_size: int = 20,
        openai_api_key: Optional[str] = None
    ):
        """
        Initialize metrics calculator.
        
        Args:
            evaluation_csv: Path to ograg_evaluation_100proverbs.csv
            sample_size: Number of proverbs for LLM-as-judge (default 20)
            openai_api_key: OpenAI API key (or from .env)
        """
        self.evaluation_csv = Path(evaluation_csv)
        self.sample_size = sample_size
        self.bleu = BLEU()
        
        # OpenAI client for LLM-as-judge
        self.openai_client = None
        if HAS_OPENAI:
            api_key = openai_api_key or config('OPENAI_API_KEY', default=None) or os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
                logger.info("✅ OpenAI client initialized for LLM-as-judge")
            else:
                logger.warning("⚠️ No OpenAI API key found. Skipping LLM-as-judge.")
        
        self.proverb_metrics: List[ProverbMetrics] = []
        
    def load_evaluation_results(self) -> List[Dict]:
        """Load evaluation CSV."""
        logger.info(f"Loading evaluation results from {self.evaluation_csv}")
        
        with open(self.evaluation_csv, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        logger.info(f"✅ Loaded {len(rows)} proverbs")
        return rows
    
    def calculate_bleu(self, hypothesis: str, reference: str) -> float:
        """
        Calculate BLEU score for one translation.
        
        Args:
            hypothesis: Translated text
            reference: Expert translation
            
        Returns:
            BLEU score (0-100)
        """
        if not hypothesis or not reference:
            return 0.0
        
        # sacrebleu expects lists
        score = self.bleu.sentence_score(hypothesis, [reference])
        return score.score
    
    def is_failed_translation(self, translation: str) -> bool:
        """
        Detect obvious translation failures.
        
        Args:
            translation: Translation to check
            
        Returns:
            True if failed
        """
        if not translation:
            return True
        
        # Very short translations likely failed
        if len(translation.strip()) < 5:
            return True
        
        # Contains error markers
        error_markers = ['error', 'failed', 'unable', 'cannot translate']
        if any(marker in translation.lower() for marker in error_markers):
            return True
        
        return False
    
    def judge_cultural_fidelity(
        self,
        kikuyu_text: str,
        translation: str,
        expert_translation: str,
        expert_meaning: str = ""
    ) -> Tuple[float, str]:
        """
        Use GPT-4 as judge to score cultural fidelity (0-1).
        
        Args:
            kikuyu_text: Original Kikuyu proverb
            translation: Translation to evaluate
            expert_translation: Expert reference
            expert_meaning: Optional cultural meaning
            
        Returns:
            (score, explanation)
        """
        if not self.openai_client:
            return None, "LLM judge not available"
        
        prompt = f"""You are an expert evaluator of Kikuyu proverb translations.

Rate the CULTURAL FIDELITY of the following translation on a scale of 0.0 to 1.0:

Original Kikuyu: {kikuyu_text}
Expert Translation: {expert_translation}
{f'Cultural Meaning: {expert_meaning}' if expert_meaning else ''}

Translation to Evaluate: {translation}

Cultural Fidelity Scale:
- 1.0 = Perfect: Preserves all cultural meaning, metaphors, and nuances
- 0.7-0.9 = Good: Captures main cultural meaning with minor losses
- 0.4-0.6 = Partial: Some cultural meaning preserved but significant losses
- 0.1-0.3 = Poor: Minimal cultural meaning preserved
- 0.0 = Failed: Completely wrong or missing cultural context

Respond with ONLY a JSON object:
{{"score": <0.0-1.0>, "explanation": "<brief explanation>"}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a precise evaluator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistency
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(result_text)
            score = float(result.get('score', 0.0))
            explanation = result.get('explanation', '')
            
            # Clamp to [0, 1]
            score = max(0.0, min(1.0, score))
            
            return score, explanation
            
        except Exception as e:
            logger.error(f"LLM judge error: {e}")
            return None, f"Error: {e}"
    
    def calculate_all_metrics(self, use_llm_judge: bool = True) -> None:
        """
        Calculate all metrics for all proverbs.
        
        Args:
            use_llm_judge: Whether to use LLM-as-judge (costs $)
        """
        rows = self.load_evaluation_results()
        
        # Sample for LLM judge (stratified by length)
        sampled_indices = set()
        if use_llm_judge and self.openai_client:
            # Sort by kikuyu text length for stratification
            sorted_indices = sorted(
                range(len(rows)),
                key=lambda i: len(rows[i].get('kikuyu_text', ''))
            )
            
            # Sample evenly across length distribution
            step = len(rows) // self.sample_size
            sampled_indices = set(sorted_indices[i * step] for i in range(self.sample_size))
            logger.info(f"📊 Selected {len(sampled_indices)} proverbs for LLM-as-judge")
        
        logger.info("Calculating metrics for all proverbs...")
        
        for idx, row in enumerate(rows):
            proverb_id = row['proverb_id']
            kikuyu_text = row['kikuyu_text']
            expert_translation = row.get('expert_translation', '')
            expert_meaning = row.get('expert_cultural_meaning', '')
            
            raw_trans = row.get('raw_translation', '')
            trad_trans = row.get('trad_rag_translation', '')
            ograg_trans = row.get('ograg_translation', '')
            
            # Skip if no expert translation
            if not expert_translation:
                logger.warning(f"⚠️ No expert translation for {proverb_id}, skipping")
                continue
            
            # Calculate BLEU
            bleu_raw = self.calculate_bleu(raw_trans, expert_translation)
            bleu_trad = self.calculate_bleu(trad_trans, expert_translation)
            bleu_ograg = self.calculate_bleu(ograg_trans, expert_translation)
            
            # Failure detection
            failed_raw = self.is_failed_translation(raw_trans)
            failed_trad = self.is_failed_translation(trad_trans)
            failed_ograg = self.is_failed_translation(ograg_trans)
            
            # LLM-as-judge (only for sampled proverbs)
            cultural_raw = None
            cultural_trad = None
            cultural_ograg = None
            
            if idx in sampled_indices:
                logger.info(f"Judging cultural fidelity for {proverb_id} ({idx+1}/{len(rows)})")
                
                cultural_raw, _ = self.judge_cultural_fidelity(
                    kikuyu_text, raw_trans, expert_translation, expert_meaning
                )
                cultural_trad, _ = self.judge_cultural_fidelity(
                    kikuyu_text, trad_trans, expert_translation, expert_meaning
                )
                cultural_ograg, _ = self.judge_cultural_fidelity(
                    kikuyu_text, ograg_trans, expert_translation, expert_meaning
                )
            
            metrics = ProverbMetrics(
                proverb_id=proverb_id,
                kikuyu_text=kikuyu_text,
                expert_translation=expert_translation,
                bleu_raw=bleu_raw,
                bleu_trad_rag=bleu_trad,
                bleu_ograg=bleu_ograg,
                cultural_fidelity_raw=cultural_raw,
                cultural_fidelity_trad_rag=cultural_trad,
                cultural_fidelity_ograg=cultural_ograg,
                failed_raw=failed_raw,
                failed_trad_rag=failed_trad,
                failed_ograg=failed_ograg
            )
            
            self.proverb_metrics.append(metrics)
        
        logger.info(f"✅ Calculated metrics for {len(self.proverb_metrics)} proverbs")
    
    def compute_aggregate_statistics(self) -> AggregateMetrics:
        """Compute aggregate statistics and statistical tests."""
        logger.info("Computing aggregate statistics...")
        
        if not self.proverb_metrics:
            raise ValueError("No metrics calculated. Run calculate_all_metrics() first.")
        
        # Extract BLEU scores
        bleu_raw = [m.bleu_raw for m in self.proverb_metrics]
        bleu_trad = [m.bleu_trad_rag for m in self.proverb_metrics]
        bleu_ograg = [m.bleu_ograg for m in self.proverb_metrics]
        
        # Extract cultural fidelity (only non-None)
        cultural_raw = [m.cultural_fidelity_raw for m in self.proverb_metrics if m.cultural_fidelity_raw is not None]
        cultural_trad = [m.cultural_fidelity_trad_rag for m in self.proverb_metrics if m.cultural_fidelity_trad_rag is not None]
        cultural_ograg = [m.cultural_fidelity_ograg for m in self.proverb_metrics if m.cultural_fidelity_ograg is not None]
        
        # Failure rates
        n = len(self.proverb_metrics)
        failure_rate_raw = sum(m.failed_raw for m in self.proverb_metrics) / n
        failure_rate_trad = sum(m.failed_trad_rag for m in self.proverb_metrics) / n
        failure_rate_ograg = sum(m.failed_ograg for m in self.proverb_metrics) / n
        
        # Statistical tests - BLEU (Raw vs OG-RAG)
        bleu_ttest = stats.ttest_rel(bleu_raw, bleu_ograg)
        bleu_cohens_d = self.cohens_d_paired(bleu_raw, bleu_ograg)
        
        # Cultural fidelity tests (if available)
        cultural_ttest_pvalue = None
        cultural_cohens_d = None
        if len(cultural_raw) > 1 and len(cultural_ograg) > 1:
            cultural_ttest = stats.ttest_rel(cultural_raw, cultural_ograg)
            cultural_ttest_pvalue = cultural_ttest.pvalue
            cultural_cohens_d = self.cohens_d_paired(cultural_raw, cultural_ograg)
        
        agg = AggregateMetrics(
            n_proverbs=n,
            bleu_raw_mean=np.mean(bleu_raw),
            bleu_raw_std=np.std(bleu_raw, ddof=1),
            bleu_trad_mean=np.mean(bleu_trad),
            bleu_trad_std=np.std(bleu_trad, ddof=1),
            bleu_ograg_mean=np.mean(bleu_ograg),
            bleu_ograg_std=np.std(bleu_ograg, ddof=1),
            cultural_raw_mean=np.mean(cultural_raw) if cultural_raw else None,
            cultural_raw_std=np.std(cultural_raw, ddof=1) if cultural_raw else None,
            cultural_trad_mean=np.mean(cultural_trad) if cultural_trad else None,
            cultural_trad_std=np.std(cultural_trad, ddof=1) if cultural_trad else None,
            cultural_ograg_mean=np.mean(cultural_ograg) if cultural_ograg else None,
            cultural_ograg_std=np.std(cultural_ograg, ddof=1) if cultural_ograg else None,
            failure_rate_raw=failure_rate_raw,
            failure_rate_trad=failure_rate_trad,
            failure_rate_ograg=failure_rate_ograg,
            bleu_ttest_pvalue=bleu_ttest.pvalue,
            bleu_cohens_d=bleu_cohens_d,
            cultural_ttest_pvalue=cultural_ttest_pvalue,
            cultural_cohens_d=cultural_cohens_d
        )
        
        logger.info("✅ Aggregate statistics computed")
        return agg
    
    @staticmethod
    def cohens_d_paired(x, y):
        """Calculate Cohen's d for paired samples."""
        diff = np.array(x) - np.array(y)
        return np.mean(diff) / np.std(diff, ddof=1)
    
    def save_results(self, output_dir: str = "data/results") -> Tuple[str, str]:
        """
        Save metrics to CSV files.
        
        Args:
            output_dir: Output directory
            
        Returns:
            (per_proverb_csv, summary_csv)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Per-proverb metrics
        per_proverb_csv = output_path / "ograg_metrics_per_proverb.csv"
        with open(per_proverb_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'proverb_id', 'kikuyu_text', 'expert_translation',
                'bleu_raw', 'bleu_trad_rag', 'bleu_ograg',
                'cultural_fidelity_raw', 'cultural_fidelity_trad_rag', 'cultural_fidelity_ograg',
                'failed_raw', 'failed_trad_rag', 'failed_ograg'
            ])
            writer.writeheader()
            for m in self.proverb_metrics:
                writer.writerow(asdict(m))
        
        logger.info(f"✅ Saved per-proverb metrics to {per_proverb_csv}")
        
        # Aggregate summary
        agg = self.compute_aggregate_statistics()
        summary_csv = output_path / "ograg_metrics_summary.csv"
        with open(summary_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(asdict(agg).keys()))
            writer.writeheader()
            writer.writerow(asdict(agg))
        
        logger.info(f"✅ Saved aggregate summary to {summary_csv}")
        
        # Also save as JSON for easy reading
        summary_json = output_path / "ograg_metrics_summary.json"
        with open(summary_json, 'w') as f:
            json.dump(asdict(agg), f, indent=2)
        
        return str(per_proverb_csv), str(summary_csv)


def main():
    parser = argparse.ArgumentParser(description="Calculate OG-RAG evaluation metrics")
    parser.add_argument(
        '--evaluation-csv',
        default='data/results/ograg_translations/ograg_evaluation_100proverbs.csv',
        help='Path to evaluation CSV'
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        default=20,
        help='Number of proverbs for LLM-as-judge (default: 20)'
    )
    parser.add_argument(
        '--no-llm-judge',
        action='store_true',
        help='Skip LLM-as-judge (BLEU only)'
    )
    parser.add_argument(
        '--output-dir',
        default='data/results',
        help='Output directory for results'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 70)
    logger.info("OG-RAG METRICS CALCULATION")
    logger.info("=" * 70)
    logger.info(f"Evaluation CSV: {args.evaluation_csv}")
    logger.info(f"Sample size for LLM-as-judge: {args.sample_size}")
    logger.info(f"LLM-as-judge: {'disabled' if args.no_llm_judge else 'enabled'}")
    logger.info("=" * 70)
    
    # Initialize calculator
    calculator = MetricsCalculator(
        evaluation_csv=args.evaluation_csv,
        sample_size=args.sample_size
    )
    
    # Calculate metrics
    calculator.calculate_all_metrics(use_llm_judge=not args.no_llm_judge)
    
    # Save results
    per_proverb_csv, summary_csv = calculator.save_results(output_dir=args.output_dir)
    
    # Print summary
    agg = calculator.compute_aggregate_statistics()
    
    logger.info("\n" + "=" * 70)
    logger.info("RESULTS SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Proverbs analyzed: {agg.n_proverbs}")
    logger.info("")
    logger.info("BLEU Scores (mean ± std):")
    logger.info(f"  Raw GPT-4:        {agg.bleu_raw_mean:.2f} ± {agg.bleu_raw_std:.2f}")
    logger.info(f"  Traditional RAG:  {agg.bleu_trad_mean:.2f} ± {agg.bleu_trad_std:.2f}")
    logger.info(f"  OG-RAG:          {agg.bleu_ograg_mean:.2f} ± {agg.bleu_ograg_std:.2f}")
    logger.info("")
    logger.info(f"BLEU improvement (OG-RAG vs Raw): {agg.bleu_ograg_mean - agg.bleu_raw_mean:.2f}")
    logger.info(f"Statistical test (Raw vs OG-RAG):")
    logger.info(f"  p-value: {agg.bleu_ttest_pvalue:.4f}")
    logger.info(f"  Cohen's d: {agg.bleu_cohens_d:.3f}")
    logger.info("")
    
    if agg.cultural_ograg_mean is not None:
        logger.info("Cultural Fidelity (0-1 scale, mean ± std):")
        logger.info(f"  Raw GPT-4:        {agg.cultural_raw_mean:.3f} ± {agg.cultural_raw_std:.3f}")
        logger.info(f"  Traditional RAG:  {agg.cultural_trad_mean:.3f} ± {agg.cultural_trad_std:.3f}")
        logger.info(f"  OG-RAG:          {agg.cultural_ograg_mean:.3f} ± {agg.cultural_ograg_std:.3f}")
        logger.info("")
        logger.info(f"Cultural fidelity improvement: {agg.cultural_ograg_mean - agg.cultural_raw_mean:.3f}")
        if agg.cultural_ttest_pvalue:
            logger.info(f"Statistical test (Raw vs OG-RAG):")
            logger.info(f"  p-value: {agg.cultural_ttest_pvalue:.4f}")
            logger.info(f"  Cohen's d: {agg.cultural_cohens_d:.3f}")
        logger.info("")
    
    logger.info("Failure Rates:")
    logger.info(f"  Raw GPT-4:        {agg.failure_rate_raw*100:.1f}%")
    logger.info(f"  Traditional RAG:  {agg.failure_rate_trad*100:.1f}%")
    logger.info(f"  OG-RAG:          {agg.failure_rate_ograg*100:.1f}%")
    logger.info("=" * 70)
    logger.info(f"\n✅ Results saved to {args.output_dir}")
    logger.info(f"   Per-proverb: {per_proverb_csv}")
    logger.info(f"   Summary: {summary_csv}")


if __name__ == '__main__':
    main()
