#!/usr/bin/env python3
"""
Quick Metrics Calculation - BLEU scores only
Runs quickly without LLM-as-judge calls
"""

import csv
import json
from pathlib import Path
from sacrebleu.metrics import BLEU
import numpy as np
from scipy import stats

def calculate_bleu(reference: str, hypothesis: str) -> float:
    """Calculate BLEU score."""
    if not hypothesis or not reference:
        return 0.0
    bleu = BLEU()
    score = bleu.sentence_score(hypothesis, [reference])
    return score.score

def main():
    # Load evaluation data
    eval_file = Path("data/results/ograg_translations/ograg_evaluation_100proverbs.csv")
    
    print(f"Loading evaluation from: {eval_file}")
    
    metrics = []
    bleu_scores = {'raw': [], 'trad_rag': [], 'ograg': []}
    
    with open(eval_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            proverb_id = row['proverb_id']
            expert = row['expert_translation']
            raw = row['raw_translation']
            trad = row['trad_rag_translation']
            ograg = row['ograg_translation']
            
            # Calculate BLEU
            bleu_raw = calculate_bleu(expert, raw)
            bleu_trad = calculate_bleu(expert, trad)
            bleu_ograg = calculate_bleu(expert, ograg)
            
            bleu_scores['raw'].append(bleu_raw)
            bleu_scores['trad_rag'].append(bleu_trad)
            bleu_scores['ograg'].append(bleu_ograg)
            
            metrics.append({
                'proverb_id': proverb_id,
                'bleu_raw': bleu_raw,
                'bleu_trad_rag': bleu_trad,
                'bleu_ograg': bleu_ograg
            })
    
    # Calculate statistics
    print(f"\n{'='*70}")
    print(f"BLEU SCORE ANALYSIS - {len(metrics)} proverbs")
    print(f"{'='*70}\n")
    
    for method in ['raw', 'trad_rag', 'ograg']:
        scores = bleu_scores[method]
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        median_score = np.median(scores)
        
        print(f"{method.upper()}")
        print(f"  Mean:   {mean_score:.2f}")
        print(f"  Std:    {std_score:.2f}")
        print(f"  Median: {median_score:.2f}")
        print(f"  Min:    {min(scores):.2f}")
        print(f"  Max:    {max(scores):.2f}")
        print()
    
    # Statistical comparisons
    print(f"\n{'='*70}")
    print(f"STATISTICAL COMPARISONS")
    print(f"{'='*70}\n")
    
    # Raw vs OG-RAG
    t_stat, p_value = stats.ttest_rel(bleu_scores['raw'], bleu_scores['ograg'])
    cohens_d = (np.mean(bleu_scores['ograg']) - np.mean(bleu_scores['raw'])) / np.std(bleu_scores['raw'])
    
    print(f"Raw GPT-4 vs OG-RAG:")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Cohen's d: {cohens_d:.4f}")
    print(f"  Significant: {'YES' if p_value < 0.05 else 'NO'} (α=0.05)")
    print()
    
    # Raw vs Traditional RAG
    t_stat2, p_value2 = stats.ttest_rel(bleu_scores['raw'], bleu_scores['trad_rag'])
    cohens_d2 = (np.mean(bleu_scores['trad_rag']) - np.mean(bleu_scores['raw'])) / np.std(bleu_scores['raw'])
    
    print(f"Raw GPT-4 vs Traditional RAG:")
    print(f"  t-statistic: {t_stat2:.4f}")
    print(f"  p-value: {p_value2:.4f}")
    print(f"  Cohen's d: {cohens_d2:.4f}")
    print(f"  Significant: {'YES' if p_value2 < 0.05 else 'NO'} (α=0.05)")
    print()
    
    # Save results
    output_dir = Path("data/results")
    
    # Per-proverb metrics
    per_proverb_file = output_dir / "quick_bleu_metrics_per_proverb.csv"
    with open(per_proverb_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['proverb_id', 'bleu_raw', 'bleu_trad_rag', 'bleu_ograg'])
        writer.writeheader()
        writer.writerows(metrics)
    
    print(f"✅ Saved per-proverb metrics to: {per_proverb_file}")
    
    # Summary
    summary = {
        'n_proverbs': len(metrics),
        'bleu_raw': {
            'mean': float(np.mean(bleu_scores['raw'])),
            'std': float(np.std(bleu_scores['raw'])),
            'median': float(np.median(bleu_scores['raw']))
        },
        'bleu_trad_rag': {
            'mean': float(np.mean(bleu_scores['trad_rag'])),
            'std': float(np.std(bleu_scores['trad_rag'])),
            'median': float(np.median(bleu_scores['trad_rag']))
        },
        'bleu_ograg': {
            'mean': float(np.mean(bleu_scores['ograg'])),
            'std': float(np.std(bleu_scores['ograg'])),
            'median': float(np.median(bleu_scores['ograg']))
        },
        'statistical_tests': {
            'raw_vs_ograg': {
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'cohens_d': float(cohens_d),
                'significant': p_value < 0.05
            },
            'raw_vs_trad_rag': {
                't_statistic': float(t_stat2),
                'p_value': float(p_value2),
                'cohens_d': float(cohens_d2),
                'significant': p_value2 < 0.05
            }
        }
    }
    
    summary_file = output_dir / "quick_bleu_metrics_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Saved summary to: {summary_file}\n")

if __name__ == "__main__":
    main()
