#!/usr/bin/env python3
"""
Generate comprehensive summary of LLM-as-a-Judge evaluation results.
"""

import json
from pathlib import Path

# Load the latest evaluation report
report_file = 'outputs/evaluation/comparative/results/evaluation_report_20251115_134223.json'
with open(report_file) as f:
    report = json.load(f)

print("=" * 80)
print("LLM-AS-A-JUDGE EVALUATION RESULTS - GEMINI 2.5 PRO")
print("=" * 80)
print()

# Metadata
metadata = report.get('evaluation_metadata', {})
print("📊 EVALUATION DETAILS")
print("-" * 80)
print(f"Total Evaluations: {metadata.get('total_evaluations', 'N/A')}")
print(f"Model: Gemini 2.5 Pro (Google)")
print(f"Timestamp: {metadata.get('timestamp', 'N/A')}")
print()

# Overall scores
stats = report.get('statistical_analysis', {})
if 'overall_scores' in stats:
    print("📈 OVERALL WEIGHTED SCORES")
    print("-" * 80)
    overall = stats['overall_scores']
    
    og_rag = overall.get('og_rag', {})
    raw_llm = overall.get('raw_llm', {})
    
    print(f"\nOG-RAG:")
    print(f"  Mean:   {og_rag.get('mean', 0):.3f}")
    print(f"  Std:    {og_rag.get('std', 0):.3f}")
    print(f"  Median: {og_rag.get('median', 0):.3f}")
    print(f"  Range:  {og_rag.get('min', 0):.3f} - {og_rag.get('max', 0):.3f}")
    
    print(f"\nRaw GPT-4:")
    print(f"  Mean:   {raw_llm.get('mean', 0):.3f}")
    print(f"  Std:    {raw_llm.get('std', 0):.3f}")
    print(f"  Median: {raw_llm.get('median', 0):.3f}")
    print(f"  Range:  {raw_llm.get('min', 0):.3f} - {raw_llm.get('max', 0):.3f}")
    
    # Calculate difference
    diff = og_rag.get('mean', 0) - raw_llm.get('mean', 0)
    pct_diff = (diff / raw_llm.get('mean', 1)) * 100
    print(f"\n✓ OG-RAG Performance: +{diff:.3f} points ({pct_diff:+.1f}%)")
    print()

# Dimension-wise scores
if 'dimension_scores' in stats:
    print("📊 DIMENSION-WISE PERFORMANCE")
    print("-" * 80)
    
    dimensions = {
        'cultural_faithfulness': ('Cultural Faithfulness', 0.40),
        'translation_accuracy': ('Translation Accuracy', 0.30),
        'business_relevance': ('Business Relevance', 0.20),
        'overall_fluency': ('Overall Fluency', 0.10)
    }
    
    dim_scores = stats['dimension_scores']
    
    for dim_key, (dim_name, weight) in dimensions.items():
        if dim_key in dim_scores:
            data = dim_scores[dim_key]
            print(f"\n{dim_name} (Weight: {weight*100:.0f}%):")
            print("  " + "-" * 60)
            
            og = data.get('og_rag', {})
            raw = data.get('raw_llm', {})
            
            og_mean = og.get('mean', 0)
            raw_mean = raw.get('mean', 0)
            
            print(f"  OG-RAG:     {og_mean:.3f} (±{og.get('std', 0):.3f})")
            print(f"  Raw GPT-4:  {raw_mean:.3f} (±{raw.get('std', 0):.3f})")
            
            diff = og_mean - raw_mean
            pct = (diff / raw_mean * 100) if raw_mean != 0 else 0
            
            arrow = "↑" if diff > 0 else "↓" if diff < 0 else "="
            print(f"  Difference: {arrow} {diff:+.3f} ({pct:+.1f}%)")

print()

# Statistical significance
if 'significance_tests' in stats:
    print("🔬 STATISTICAL SIGNIFICANCE")
    print("-" * 80)
    
    sig_tests = stats['significance_tests']
    for test_name, test_data in sig_tests.items():
        if isinstance(test_data, dict):
            p_value = test_data.get('p_value', 1.0)
            is_sig = p_value < 0.05
            status = "✓ SIGNIFICANT" if is_sig else "✗ Not significant"
            print(f"{test_name}: p={p_value:.4f} - {status}")
    print()

# Key findings
if 'key_findings' in report:
    print("💡 KEY FINDINGS")
    print("-" * 80)
    for i, finding in enumerate(report['key_findings'], 1):
        print(f"{i}. {finding}")
    print()

# Recommendations
if 'recommendations' in report:
    print("🎯 RECOMMENDATIONS")
    print("-" * 80)
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"{i}. {rec}")
    print()

print("=" * 80)
print(f"Full report saved to: {report_file}")
print("=" * 80)
