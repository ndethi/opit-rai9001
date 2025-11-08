#!/usr/bin/env python3
"""
Simple BLEU Score Calculator
Calculates BLEU scores without requiring scipy
"""

import csv
import json
from pathlib import Path
import sacrebleu

def calculate_bleu_scores(evaluation_csv, output_dir):
    """Calculate BLEU scores from evaluation CSV."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    print(f"📊 Reading evaluation data from: {evaluation_csv}")
    
    with open(evaluation_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"✅ Found {len(rows)} proverbs to evaluate")
    
    for i, row in enumerate(rows, 1):
        proverb_id = row.get('proverb_id', f'proverb_{i}')
        kikuyu = row.get('kikuyu_text', '')
        expert_trans = row.get('expert_translation', '')
        ograg_trans = row.get('ograg_translation', '')
        
        if not expert_trans or not ograg_trans:
            print(f"⚠️  Skipping {proverb_id}: missing translation")
            continue
        
        # Calculate BLEU score
        bleu = sacrebleu.sentence_bleu(ograg_trans, [expert_trans])
        
        result = {
            'proverb_id': proverb_id,
            'kikuyu_text': kikuyu,
            'expert_translation': expert_trans,
            'ograg_translation': ograg_trans,
            'bleu_score': round(bleu.score, 2)
        }
        results.append(result)
        
        if i % 10 == 0:
            print(f"   Processed {i}/{len(rows)} proverbs...")
    
    # Calculate summary statistics
    bleu_scores = [r['bleu_score'] for r in results]
    avg_bleu = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0
    min_bleu = min(bleu_scores) if bleu_scores else 0
    max_bleu = max(bleu_scores) if bleu_scores else 0
    
    summary = {
        'total_proverbs': len(results),
        'average_bleu': round(avg_bleu, 2),
        'min_bleu': round(min_bleu, 2),
        'max_bleu': round(max_bleu, 2)
    }
    
    # Write per-proverb results
    per_proverb_file = output_dir / 'ograg_bleu_scores_per_proverb.csv'
    with open(per_proverb_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['proverb_id', 'kikuyu_text', 'expert_translation', 'ograg_translation', 'bleu_score'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✅ Wrote per-proverb results to: {per_proverb_file}")
    
    # Write summary
    summary_file = output_dir / 'ograg_bleu_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Wrote summary to: {summary_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 BLEU SCORE SUMMARY")
    print("="*60)
    print(f"Total Proverbs Evaluated: {summary['total_proverbs']}")
    print(f"Average BLEU Score:       {summary['average_bleu']}")
    print(f"Minimum BLEU Score:       {summary['min_bleu']}")
    print(f"Maximum BLEU Score:       {summary['max_bleu']}")
    print("="*60)
    
    return summary

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python simple_bleu_calculator.py <evaluation_csv> <output_dir>")
        sys.exit(1)
    
    evaluation_csv = sys.argv[1]
    output_dir = sys.argv[2]
    
    calculate_bleu_scores(evaluation_csv, output_dir)
