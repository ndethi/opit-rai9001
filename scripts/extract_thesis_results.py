#!/usr/bin/env python3
"""
Extract Key Results for Thesis Writing

Generates LaTeX-ready tables and summaries from evaluation results.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_cultural_results():
    """Load cultural evaluation results."""
    summary_file = "data/results/cultural_evaluation_summary.json"
    with open(summary_file) as f:
        return json.load(f)

def load_llm_results():
    """Load LLM-as-a-Judge results."""
    results_dir = Path("outputs/evaluation/comparative/results")
    
    # Find the latest report file
    report_files = sorted(results_dir.glob("comparative_evaluation_report_*.json"))
    if report_files:
        with open(report_files[-1]) as f:
            return json.load(f)
    return None

def generate_latex_table_1(cultural_results):
    """Generate Table 5.1: Cultural Metrics Summary Statistics."""
    
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{Cultural Metrics Summary Statistics (100 Proverbs)}")
    print("\\label{tab:cultural_metrics}")
    print("\\begin{tabular}{lcccc}")
    print("\\hline")
    print("\\textbf{System} & \\textbf{Cultural Auth.} & \\textbf{Trans. Fidelity} & \\textbf{Overall Quality} & \\textbf{Grade} \\\\")
    print("\\hline")
    
    for system, metrics in cultural_results.items():
        if system == 'metadata':
            continue
        cultural_auth = f"{metrics['cultural_authenticity']['mean']:.3f} $\\pm$ {metrics['cultural_authenticity']['std']:.3f}"
        trans_fid = f"{metrics['translation_fidelity']['mean']:.3f} $\\pm$ {metrics['translation_fidelity']['std']:.3f}"
        overall_qual = f"{metrics['overall_quality']['mean']:.3f} $\\pm$ {metrics['overall_quality']['std']:.3f}"
        
        # Get most common grade from distribution
        grade_dist = metrics.get('grade_distribution', {})
        grade = max(grade_dist.items(), key=lambda x: x[1])[0] if grade_dist else 'N/A'
        
        print(f"{system} & {cultural_auth} & {trans_fid} & {overall_qual} & {grade} \\\\")
    
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")
    print()

def generate_key_statistics(cultural_results):
    """Generate key statistics summary."""
    
    print("=" * 70)
    print("KEY STATISTICS FOR THESIS")
    print("=" * 70)
    print()
    
    og_rag = cultural_results['OG-RAG']
    raw_gpt4 = cultural_results['Raw GPT-4']
    trad_rag = cultural_results['Traditional RAG']
    
    og_rag_auth = og_rag['cultural_authenticity']['mean']
    raw_gpt4_auth = raw_gpt4['cultural_authenticity']['mean']
    
    improvement = ((og_rag_auth - raw_gpt4_auth) / raw_gpt4_auth) * 100
    
    print(f"📊 CULTURAL AUTHENTICITY:")
    print(f"   OG-RAG:         {og_rag_auth:.3f} ± {og_rag['cultural_authenticity']['std']:.3f}")
    print(f"   Raw GPT-4:      {raw_gpt4_auth:.3f} ± {raw_gpt4['cultural_authenticity']['std']:.3f}")
    print(f"   Traditional RAG: {trad_rag['cultural_authenticity']['mean']:.3f} ± {trad_rag['cultural_authenticity']['std']:.3f}")
    print(f"   → IMPROVEMENT:  {improvement:.1f}%")
    print()
    
    print(f"📊 TRANSLATION FIDELITY:")
    print(f"   OG-RAG:         {og_rag['translation_fidelity']['mean']:.3f} ± {og_rag['translation_fidelity']['std']:.3f}")
    print(f"   Raw GPT-4:      {raw_gpt4['translation_fidelity']['mean']:.3f} ± {raw_gpt4['translation_fidelity']['std']:.3f}")
    print()
    
    print(f"📊 OVERALL QUALITY:")
    print(f"   OG-RAG:         {og_rag['overall_quality']['mean']:.3f} ± {og_rag['overall_quality']['std']:.3f}")
    print(f"   Raw GPT-4:      {raw_gpt4['overall_quality']['mean']:.3f} ± {raw_gpt4['overall_quality']['std']:.3f}")
    print()
    
    # Extract metadata
    metadata = cultural_results.get('metadata', {})
    print(f"📋 EVALUATION METADATA:")
    print(f"   Total Proverbs:    {metadata.get('total_proverbs', 'N/A')}")
    print(f"   Successful Evals:  {metadata.get('successful_evaluations', 'N/A')}")
    print(f"   Failed Evals:      {metadata.get('failed_evaluations', 'N/A')}")
    print()

def generate_latex_table_2():
    """Generate Table 5.2: Statistical Significance Tests."""
    
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{Statistical Significance Tests for Cultural Authenticity}")
    print("\\label{tab:statistical_tests}")
    print("\\begin{tabular}{lccc}")
    print("\\hline")
    print("\\textbf{Comparison} & \\textbf{t-statistic} & \\textbf{p-value} & \\textbf{Interpretation} \\\\")
    print("\\hline")
    print("OG-RAG vs Raw GPT-4 & TBD & TBD & Significant/Not Significant \\\\")
    print("OG-RAG vs Traditional RAG & TBD & TBD & Significant/Not Significant \\\\")
    print("Traditional RAG vs Raw GPT-4 & TBD & TBD & Significant/Not Significant \\\\")
    print("\\hline")
    print("\\multicolumn{4}{l}{\\textit{Note: Significance level $\\alpha = 0.05$}} \\\\")
    print("\\end{tabular}")
    print("\\end{table}")
    print()

def main():
    """Generate all thesis-ready results."""
    
    print("\n" + "=" * 70)
    print("THESIS RESULTS EXTRACTION")
    print("=" * 70)
    print()
    
    # Load cultural results
    print("Loading cultural evaluation results...")
    cultural_results = load_cultural_results()
    
    # Generate key statistics
    generate_key_statistics(cultural_results)
    
    # Generate LaTeX tables
    print("\n" + "=" * 70)
    print("LATEX TABLE 5.1: Cultural Metrics Summary")
    print("=" * 70)
    print()
    generate_latex_table_1(cultural_results)
    
    print("=" * 70)
    print("LATEX TABLE 5.2: Statistical Significance Tests")
    print("=" * 70)
    print()
    generate_latex_table_2()
    
    # Try to load LLM results
    print("=" * 70)
    print("LLM-AS-A-JUDGE RESULTS")
    print("=" * 70)
    llm_results = load_llm_results()
    if llm_results:
        print("✅ LLM evaluation results found!")
        print(f"   File: {sorted(Path('outputs/evaluation/comparative/results').glob('comparative_evaluation_report_*.json'))[-1]}")
    else:
        print("⚠️  LLM evaluation results not found in expected location")
    print()
    
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Copy LaTeX tables above into thesis Chapter 5")
    print("2. Copy visualizations from data/results/visualizations/ to docs/thesis/figures/")
    print("3. Reference figures in Chapter 5 using \\ref{fig:...}")
    print("4. Fill in statistical test results (t-tests)")
    print("5. Write interpretation paragraphs for each result")
    print()

if __name__ == "__main__":
    main()
