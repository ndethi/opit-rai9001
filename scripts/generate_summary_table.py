"""
Generate summary statistics table for thesis.

Author: Nixon Dethi
Date: November 13, 2025
"""

import pandas as pd
from pathlib import Path

def main():
    """Generate summary table."""
    print("📊 Generating summary statistics table...")
    
    # Load metrics
    metrics_path = Path("data/results/quick_bleu_metrics_per_proverb.csv")
    metrics_df = pd.read_csv(metrics_path)
    
    # Create output directory
    output_dir = Path("data/results/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Method labels
    LABELS = {
        'raw': 'Raw GPT-4',
        'trad_rag': 'Traditional RAG',
        'ograg': 'OG-RAG'
    }
    
    # Calculate summary statistics
    methods = ['raw', 'trad_rag', 'ograg']
    summary_data = []
    
    for method in methods:
        data = metrics_df[f'bleu_{method}']
        summary_data.append({
            'Method': LABELS[method],
            'Mean': f'{data.mean():.2f}',
            'Std Dev': f'{data.std():.2f}',
            'Median': f'{data.median():.2f}',
            'Min': f'{data.min():.2f}',
            'Max': f'{data.max():.2f}',
            'Q1': f'{data.quantile(0.25):.2f}',
            'Q3': f'{data.quantile(0.75):.2f}'
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Save as CSV
    csv_path = output_dir / 'summary_statistics_table.csv'
    summary_df.to_csv(csv_path, index=False)
    print(f"✅ CSV saved: {csv_path}")
    
    # Save as LaTeX
    latex_table = summary_df.to_latex(
        index=False, 
        caption='BLEU Score Summary Statistics for 100 Kikuyu Wealth Proverbs', 
        label='tab:bleu_summary',
        column_format='l|ccccccc',
        position='htbp'
    )
    
    tex_path = output_dir / 'summary_statistics_table.tex'
    with open(tex_path, 'w') as f:
        f.write(latex_table)
    print(f"✅ LaTeX saved: {tex_path}")
    
    # Print to console
    print("\n" + "="*70)
    print("SUMMARY STATISTICS TABLE")
    print("="*70)
    print(summary_df.to_string(index=False))
    print("="*70)

if __name__ == "__main__":
    main()
