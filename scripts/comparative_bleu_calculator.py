#!/usr/bin/env python3
"""
Comparative BLEU Score Calculator
==================================
Compares three translation methods against expert translations:
1. Raw GPT-4 (baseline)
2. Traditional RAG
3. OG-RAG (ontology-grounded)

Calculates BLEU scores for each method to demonstrate improvement.
"""

import csv
import json
from pathlib import Path
import sacrebleu

def calculate_comparative_bleu(evaluation_csv, output_dir):
    """Calculate BLEU scores for all three translation methods."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("🔬 COMPARATIVE BLEU SCORE ANALYSIS")
    print("="*70)
    print(f"\n📊 Reading evaluation data from: {evaluation_csv}\n")
    
    with open(evaluation_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"✅ Found {len(rows)} proverbs to evaluate\n")
    
    # Storage for per-proverb results
    results = []
    
    # Accumulators for each method
    raw_bleu_scores = []
    trad_rag_bleu_scores = []
    ograg_bleu_scores = []
    
    for i, row in enumerate(rows, 1):
        proverb_id = row.get('proverb_id', f'proverb_{i}')
        kikuyu = row.get('kikuyu_text', '')
        expert_trans = row.get('expert_translation', '')
        raw_trans = row.get('raw_translation', '')
        trad_rag_trans = row.get('trad_rag_translation', '')
        ograg_trans = row.get('ograg_translation', '')
        
        if not expert_trans:
            print(f"⚠️  Skipping {proverb_id}: missing expert translation")
            continue
        
        # Calculate BLEU for each method (only if translation exists)
        raw_bleu = None
        trad_rag_bleu = None
        ograg_bleu = None
        
        if raw_trans and raw_trans.strip():
            raw_bleu = sacrebleu.sentence_bleu(raw_trans, [expert_trans]).score
            raw_bleu_scores.append(raw_bleu)
        
        if trad_rag_trans and trad_rag_trans.strip():
            trad_rag_bleu = sacrebleu.sentence_bleu(trad_rag_trans, [expert_trans]).score
            trad_rag_bleu_scores.append(trad_rag_bleu)
        
        if ograg_trans and ograg_trans.strip():
            ograg_bleu = sacrebleu.sentence_bleu(ograg_trans, [expert_trans]).score
            ograg_bleu_scores.append(ograg_bleu)
        
        result = {
            'proverb_id': proverb_id,
            'kikuyu_text': kikuyu,
            'expert_translation': expert_trans,
            'raw_translation': raw_trans,
            'raw_bleu': round(raw_bleu, 2) if raw_bleu is not None else None,
            'trad_rag_translation': trad_rag_trans,
            'trad_rag_bleu': round(trad_rag_bleu, 2) if trad_rag_bleu is not None else None,
            'ograg_translation': ograg_trans,
            'ograg_bleu': round(ograg_bleu, 2) if ograg_bleu is not None else None
        }
        results.append(result)
        
        if i % 10 == 0:
            print(f"   Processed {i}/{len(rows)} proverbs...")
    
    print(f"\n✅ Completed processing all proverbs\n")
    
    # Calculate summary statistics for each method
    def calc_stats(scores, name):
        if not scores:
            return {
                'method': name,
                'count': 0,
                'average': 0.0,
                'min': 0.0,
                'max': 0.0,
                'median': 0.0
            }
        
        sorted_scores = sorted(scores)
        median = sorted_scores[len(sorted_scores) // 2]
        
        return {
            'method': name,
            'count': len(scores),
            'average': round(sum(scores) / len(scores), 2),
            'min': round(min(scores), 2),
            'max': round(max(scores), 2),
            'median': round(median, 2)
        }
    
    raw_stats = calc_stats(raw_bleu_scores, 'Raw GPT-4')
    trad_rag_stats = calc_stats(trad_rag_bleu_scores, 'Traditional RAG')
    ograg_stats = calc_stats(ograg_bleu_scores, 'OG-RAG')
    
    # Calculate improvements
    raw_to_ograg_improvement = ograg_stats['average'] - raw_stats['average']
    trad_to_ograg_improvement = ograg_stats['average'] - trad_rag_stats['average']
    
    summary = {
        'total_proverbs_evaluated': len(results),
        'methods': [raw_stats, trad_rag_stats, ograg_stats],
        'improvements': {
            'ograg_vs_raw': {
                'absolute': round(raw_to_ograg_improvement, 2),
                'percentage': round((raw_to_ograg_improvement / raw_stats['average'] * 100) if raw_stats['average'] > 0 else 0, 2)
            },
            'ograg_vs_trad_rag': {
                'absolute': round(trad_to_ograg_improvement, 2),
                'percentage': round((trad_to_ograg_improvement / trad_rag_stats['average'] * 100) if trad_rag_stats['average'] > 0 else 0, 2)
            }
        },
        'best_method': max([raw_stats, trad_rag_stats, ograg_stats], key=lambda x: x['average'])['method']
    }
    
    # Write per-proverb comparative results
    per_proverb_file = output_dir / 'comparative_bleu_scores.csv'
    with open(per_proverb_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['proverb_id', 'kikuyu_text', 'expert_translation', 
                      'raw_translation', 'raw_bleu',
                      'trad_rag_translation', 'trad_rag_bleu',
                      'ograg_translation', 'ograg_bleu']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✅ Wrote per-proverb results to: {per_proverb_file}\n")
    
    # Write summary JSON
    summary_file = output_dir / 'comparative_bleu_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Wrote summary to: {summary_file}\n")
    
    # Print beautiful summary table
    print("="*70)
    print("📊 COMPARATIVE BLEU SCORE RESULTS")
    print("="*70)
    print()
    print(f"{'Method':<20} {'Count':<8} {'Avg':<8} {'Min':<8} {'Max':<8} {'Median':<8}")
    print("-"*70)
    
    for stats in [raw_stats, trad_rag_stats, ograg_stats]:
        print(f"{stats['method']:<20} {stats['count']:<8} "
              f"{stats['average']:<8.2f} {stats['min']:<8.2f} "
              f"{stats['max']:<8.2f} {stats['median']:<8.2f}")
    
    print("="*70)
    print()
    print("📈 IMPROVEMENTS")
    print("-"*70)
    print(f"OG-RAG vs Raw GPT-4:      {raw_to_ograg_improvement:+.2f} points "
          f"({summary['improvements']['ograg_vs_raw']['percentage']:+.1f}%)")
    print(f"OG-RAG vs Traditional RAG: {trad_to_ograg_improvement:+.2f} points "
          f"({summary['improvements']['ograg_vs_trad_rag']['percentage']:+.1f}%)")
    print("="*70)
    print()
    print(f"🏆 BEST METHOD: {summary['best_method']}")
    print("="*70)
    
    return summary

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python comparative_bleu_calculator.py <evaluation_csv> <output_dir>")
        sys.exit(1)
    
    evaluation_csv = sys.argv[1]
    output_dir = sys.argv[2]
    
    calculate_comparative_bleu(evaluation_csv, output_dir)
    
    print("\n✅ Comparative BLEU analysis complete!")
    print("\nNext steps:")
    print("1. Review comparative_bleu_scores.csv for per-proverb details")
    print("2. Add semantic similarity analysis")
    print("3. Select qualitative examples for discussion")
