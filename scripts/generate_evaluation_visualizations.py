"""
Generate publication-ready visualizations for OG-RAG evaluation results.

Creates 7 key figures for thesis Chapter 5:
1. BLEU Score Distribution (Box Plot)
2. BLEU Score Comparison (Bar Chart with Error Bars)
3. Score Distribution (Violin Plot)
4. Per-Proverb BLEU Trends (Line Plot)
5. Statistical Significance (P-value Visualization)
6. Consistency Analysis (Variance Comparison)
7. Top/Bottom Performers (Example Cases)

Author: Nixon Dethi
Date: November 13, 2025
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for file output
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy import stats

# Set publication-quality defaults
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("colorblind")
sns.set_context("paper", font_scale=1.2)

# Color scheme
COLORS = {
    'raw': '#E74C3C',      # Red
    'trad_rag': '#F39C12', # Orange
    'ograg': '#27AE60'     # Green
}

LABELS = {
    'raw': 'Raw GPT-4',
    'trad_rag': 'Traditional RAG',
    'ograg': 'OG-RAG'
}


def load_data():
    """Load evaluation results and calculated metrics."""
    # Per-proverb BLEU metrics
    metrics_path = Path("data/results/quick_bleu_metrics_per_proverb.csv")
    metrics_df = pd.read_csv(metrics_path)
    
    # Full evaluation data with translations
    eval_path = Path("data/results/ograg_translations/ograg_evaluation_100proverbs.csv")
    eval_df = pd.read_csv(eval_path)
    
    return metrics_df, eval_df


def create_output_dir():
    """Create directory for visualizations."""
    viz_dir = Path("data/results/visualizations")
    viz_dir.mkdir(parents=True, exist_ok=True)
    return viz_dir


def fig1_boxplot(metrics_df, output_dir):
    """Figure 1: BLEU Score Distribution - Box Plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = [
        metrics_df['bleu_raw'],
        metrics_df['bleu_trad_rag'],
        metrics_df['bleu_ograg']
    ]
    
    bp = ax.boxplot(data, 
                    labels=[LABELS['raw'], LABELS['trad_rag'], LABELS['ograg']],
                    patch_artist=True,
                    showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
    
    # Color boxes
    colors = [COLORS['raw'], COLORS['trad_rag'], COLORS['ograg']]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax.set_ylabel('BLEU Score', fontsize=12, fontweight='bold')
    ax.set_title('BLEU Score Distribution Across Translation Methods\n(100 Kikuyu Wealth Proverbs)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add mean values as text
    means = [np.mean(d) for d in data]
    for i, mean in enumerate(means):
        ax.text(i+1, mean+2, f'μ={mean:.2f}', ha='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'fig1_bleu_boxplot.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig1_bleu_boxplot.pdf', bbox_inches='tight')
    print("✅ Figure 1 saved: BLEU Box Plot")
    plt.close()


def fig2_barplot(metrics_df, output_dir):
    """Figure 2: Mean BLEU Comparison - Bar Chart with Error Bars."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    methods = ['raw', 'trad_rag', 'ograg']
    means = [metrics_df[f'bleu_{m}'].mean() for m in methods]
    stds = [metrics_df[f'bleu_{m}'].std() for m in methods]
    
    x_pos = np.arange(len(methods))
    bars = ax.bar(x_pos, means, 
                  yerr=stds, 
                  color=[COLORS[m] for m in methods],
                  alpha=0.7,
                  capsize=10,
                  error_kw={'linewidth': 2})
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels([LABELS[m] for m in methods])
    ax.set_ylabel('Mean BLEU Score ± Std Dev', fontsize=12, fontweight='bold')
    ax.set_title('Average Translation Quality Comparison\n(Mean BLEU ± 1 SD)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.text(i, mean + std + 1, f'{mean:.2f}±{std:.2f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'fig2_bleu_barplot.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig2_bleu_barplot.pdf', bbox_inches='tight')
    print("✅ Figure 2 saved: Mean BLEU Bar Chart")
    plt.close()


def fig3_violinplot(metrics_df, output_dir):
    """Figure 3: Score Distribution - Violin Plot."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Reshape data for seaborn
    data_long = pd.melt(metrics_df, 
                        id_vars=['proverb_id'],
                        value_vars=['bleu_raw', 'bleu_trad_rag', 'bleu_ograg'],
                        var_name='Method', 
                        value_name='BLEU')
    
    # Rename methods
    data_long['Method'] = data_long['Method'].map({
        'bleu_raw': LABELS['raw'],
        'bleu_trad_rag': LABELS['trad_rag'],
        'bleu_ograg': LABELS['ograg']
    })
    
    sns.violinplot(data=data_long, x='Method', y='BLEU', 
                   palette=[COLORS['raw'], COLORS['trad_rag'], COLORS['ograg']],
                   inner='quartile', ax=ax)
    
    ax.set_ylabel('BLEU Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('')
    ax.set_title('BLEU Score Distribution Shape Comparison\n(Violin Plot with Quartiles)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'fig3_bleu_violinplot.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig3_bleu_violinplot.pdf', bbox_inches='tight')
    print("✅ Figure 3 saved: BLEU Violin Plot")
    plt.close()


def fig4_lineplot(metrics_df, output_dir):
    """Figure 4: Per-Proverb BLEU Trends - Line Plot."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(metrics_df))
    
    ax.plot(x, metrics_df['bleu_raw'], 
            label=LABELS['raw'], color=COLORS['raw'], alpha=0.7, linewidth=1.5)
    ax.plot(x, metrics_df['bleu_trad_rag'], 
            label=LABELS['trad_rag'], color=COLORS['trad_rag'], alpha=0.7, linewidth=1.5)
    ax.plot(x, metrics_df['bleu_ograg'], 
            label=LABELS['ograg'], color=COLORS['ograg'], alpha=0.7, linewidth=2)
    
    ax.set_xlabel('Proverb Index (MW_001 to MW_100)', fontsize=12, fontweight='bold')
    ax.set_ylabel('BLEU Score', fontsize=12, fontweight='bold')
    ax.set_title('Per-Proverb BLEU Score Trends\n(All 100 Wealth Proverbs)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'fig4_bleu_lineplot.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig4_bleu_lineplot.pdf', bbox_inches='tight')
    print("✅ Figure 4 saved: Per-Proverb Line Plot")
    plt.close()


def fig5_statistical_significance(metrics_df, output_dir):
    """Figure 5: Statistical Significance - P-value Visualization."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Paired t-tests
    raw_vs_ograg = stats.ttest_rel(metrics_df['bleu_raw'], metrics_df['bleu_ograg'])
    raw_vs_trad = stats.ttest_rel(metrics_df['bleu_raw'], metrics_df['bleu_trad_rag'])
    
    # Cohen's d effect sizes
    def cohens_d(x, y):
        return (np.mean(x) - np.mean(y)) / np.sqrt((np.std(x)**2 + np.std(y)**2) / 2)
    
    d_ograg = cohens_d(metrics_df['bleu_ograg'], metrics_df['bleu_raw'])
    d_trad = cohens_d(metrics_df['bleu_trad_rag'], metrics_df['bleu_raw'])
    
    # Left plot: P-values
    comparisons = ['Raw vs\nOG-RAG', 'Raw vs\nTrad RAG']
    p_values = [raw_vs_ograg.pvalue, raw_vs_trad.pvalue]
    colors_sig = [COLORS['ograg'], COLORS['trad_rag']]
    
    bars1 = ax1.bar(comparisons, p_values, color=colors_sig, alpha=0.7)
    ax1.axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='α=0.05')
    ax1.set_ylabel('P-value', fontsize=12, fontweight='bold')
    ax1.set_title('Statistical Significance\n(Paired t-test)', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add significance markers
    for i, (p, bar) in enumerate(zip(p_values, bars1)):
        sig_marker = '✅ Significant' if p < 0.05 else '❌ Not Significant'
        ax1.text(i, p + 0.05, f'p={p:.4f}\n{sig_marker}', 
                 ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Right plot: Effect sizes
    effect_sizes = [d_ograg, d_trad]
    bars2 = ax2.bar(comparisons, effect_sizes, color=colors_sig, alpha=0.7)
    ax2.set_ylabel("Cohen's d (Effect Size)", fontsize=12, fontweight='bold')
    ax2.set_title("Effect Size Magnitude\n(Cohen's d)", fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add effect size interpretation
    for i, (d, bar) in enumerate(zip(effect_sizes, bars2)):
        if abs(d) < 0.2:
            interpretation = 'Negligible'
        elif abs(d) < 0.5:
            interpretation = 'Small'
        elif abs(d) < 0.8:
            interpretation = 'Medium'
        else:
            interpretation = 'Large'
        
        ax2.text(i, d + 0.01, f'd={d:.3f}\n({interpretation})', 
                 ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.suptitle('Statistical Analysis: Significance and Effect Sizes', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'fig5_statistical_tests.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig5_statistical_tests.pdf', bbox_inches='tight')
    print("✅ Figure 5 saved: Statistical Significance")
    plt.close()


def fig6_variance_analysis(metrics_df, output_dir):
    """Figure 6: Consistency Analysis - Variance Comparison."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    methods = ['raw', 'trad_rag', 'ograg']
    variances = [metrics_df[f'bleu_{m}'].var() for m in methods]
    stds = [metrics_df[f'bleu_{m}'].std() for m in methods]
    
    x_pos = np.arange(len(methods))
    bars = ax.bar(x_pos, stds, 
                  color=[COLORS[m] for m in methods],
                  alpha=0.7)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels([LABELS[m] for m in methods])
    ax.set_ylabel('Standard Deviation (BLEU)', fontsize=12, fontweight='bold')
    ax.set_title('Translation Consistency Comparison\n(Lower = More Consistent)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, (std, var) in enumerate(zip(stds, variances)):
        ax.text(i, std + 0.5, f'σ={std:.2f}\nσ²={var:.2f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Highlight best consistency
    best_idx = np.argmin(stds)
    bars[best_idx].set_edgecolor('green')
    bars[best_idx].set_linewidth(3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'fig6_variance_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig6_variance_comparison.pdf', bbox_inches='tight')
    print("✅ Figure 6 saved: Variance Comparison")
    plt.close()


def fig7_example_cases(metrics_df, eval_df, output_dir):
    """Figure 7: Top/Bottom Performers - Qualitative Examples."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
    
    # Find best and worst cases for OG-RAG
    ograg_best_idx = metrics_df['bleu_ograg'].idxmax()
    ograg_worst_idx = metrics_df['bleu_ograg'].idxmin()
    
    # Find biggest improvement and degradation
    metrics_df['ograg_improvement'] = metrics_df['bleu_ograg'] - metrics_df['bleu_raw']
    best_improvement_idx = metrics_df['ograg_improvement'].idxmax()
    worst_degradation_idx = metrics_df['ograg_improvement'].idxmin()
    
    cases = [
        (ograg_best_idx, ax1, 'Best OG-RAG Performance', 'green'),
        (ograg_worst_idx, ax2, 'Worst OG-RAG Performance', 'red'),
        (best_improvement_idx, ax3, 'Largest OG-RAG Improvement', 'blue'),
        (worst_degradation_idx, ax4, 'Largest OG-RAG Degradation', 'orange')
    ]
    
    for idx, ax, title, color in cases:
        row = metrics_df.iloc[idx]
        proverb_id = row['proverb_id']
        
        # Get BLEU scores
        scores = [row['bleu_raw'], row['bleu_trad_rag'], row['bleu_ograg']]
        methods = [LABELS['raw'], LABELS['trad_rag'], LABELS['ograg']]
        colors_bar = [COLORS['raw'], COLORS['trad_rag'], COLORS['ograg']]
        
        bars = ax.bar(methods, scores, color=colors_bar, alpha=0.7)
        ax.set_ylabel('BLEU Score', fontsize=10, fontweight='bold')
        ax.set_title(f'{title}\n{proverb_id}', fontsize=11, fontweight='bold', color=color)
        ax.set_ylim(0, max(scores) + 5)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, score in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width()/2, score + 0.5, 
                   f'{score:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Rotate x labels
        ax.tick_params(axis='x', rotation=15)
    
    plt.suptitle('Qualitative Case Studies: Best and Worst Performers', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(output_dir / 'fig7_example_cases.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'fig7_example_cases.pdf', bbox_inches='tight')
    print("✅ Figure 7 saved: Example Cases")
    plt.close()


def generate_summary_table(metrics_df, output_dir):
    """Generate LaTeX-ready summary table."""
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
    summary_df.to_csv(output_dir / 'summary_statistics_table.csv', index=False)
    
    # Save as LaTeX
    latex_table = summary_df.to_latex(index=False, caption='BLEU Score Summary Statistics', 
                                       label='tab:bleu_summary')
    with open(output_dir / 'summary_statistics_table.tex', 'w') as f:
        f.write(latex_table)
    
    print("✅ Summary table saved (CSV + LaTeX)")


def main():
    """Generate all visualizations."""
    print("=" * 60)
    print("🎨 GENERATING EVALUATION VISUALIZATIONS")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading data...")
    metrics_df, eval_df = load_data()
    print(f"   Loaded {len(metrics_df)} proverbs")
    
    # Create output directory
    output_dir = create_output_dir()
    print(f"   Output directory: {output_dir}")
    
    # Generate figures
    print("\n🖼️  Generating figures...\n")
    fig1_boxplot(metrics_df, output_dir)
    fig2_barplot(metrics_df, output_dir)
    fig3_violinplot(metrics_df, output_dir)
    fig4_lineplot(metrics_df, output_dir)
    fig5_statistical_significance(metrics_df, output_dir)
    fig6_variance_analysis(metrics_df, output_dir)
    fig7_example_cases(metrics_df, eval_df, output_dir)
    
    # Generate summary table
    print("\n📊 Generating summary table...")
    generate_summary_table(metrics_df, output_dir)
    
    print("\n" + "=" * 60)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📁 Output location: {output_dir.absolute()}")
    print("\n📋 Files created:")
    print("   - fig1_bleu_boxplot.png/.pdf")
    print("   - fig2_bleu_barplot.png/.pdf")
    print("   - fig3_bleu_violinplot.png/.pdf")
    print("   - fig4_bleu_lineplot.png/.pdf")
    print("   - fig5_statistical_tests.png/.pdf")
    print("   - fig6_variance_comparison.png/.pdf")
    print("   - fig7_example_cases.png/.pdf")
    print("   - summary_statistics_table.csv/.tex")
    print("\n🎓 Ready for thesis Chapter 5!")


if __name__ == "__main__":
    main()
