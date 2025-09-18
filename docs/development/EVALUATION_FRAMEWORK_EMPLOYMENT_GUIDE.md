# Evaluation Framework Employment Guide

**How to Process Expert Feedback and Deploy the thiLLMo Evaluation Benchmark**

This guide documents the complete workflow for processing expert feedback and employing the evaluation framework to assess OG-RAG vs Raw LLM translation quality.

## Table of Contents

1. [Overview](#overview)
2. [Data Processing Pipeline](#data-processing-pipeline)
3. [Expert Feedback Integration](#expert-feedback-integration)
4. [Comparative Analysis](#comparative-analysis)
5. [Statistical Validation](#statistical-validation)
6. [Results Interpretation](#results-interpretation)
7. [Benchmark Publication](#benchmark-publication)
8. [Framework Deployment](#framework-deployment)

## Overview

The evaluation framework employment process involves:
1. **Expert Feedback Collection** → Raw evaluation data from cultural experts
2. **Data Processing** → Clean, validate, and structure expert assessments
3. **System Comparison** → Generate OG-RAG and Raw LLM translations for evaluation
4. **Statistical Analysis** → Calculate quality metrics and significance tests
5. **Results Interpretation** → Generate insights and recommendations
6. **Benchmark Publication** → Create reusable benchmark dataset for research community

## Data Processing Pipeline

### Step 1: Expert Feedback Integration

Once expert evaluations are collected, integrate them into the benchmark structure:

```bash
# Process expert feedback into benchmark dataset
python scripts/process_expert_feedback.py \
    --expert-evaluations data/evaluation/collected/expert_evaluations.xlsx \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --output-file data/evaluation/processed/expert_validated_benchmark.csv
```

**Required Expert Data Fields**:
- `proverb_id`: Links to benchmark dataset
- `expert_translation`: Expert's preferred translation
- `expert_cultural_explanation`: Cultural meaning explanation
- `expert_business_application`: Modern business relevance
- `expert_cultural_faithfulness`: Score 1-5
- `expert_translation_accuracy`: Score 1-5
- `expert_business_relevance`: Score 1-5
- `expert_overall_fluency`: Score 1-5

### Step 2: LLM as a Judge Evaluation

The evaluation framework includes automated LLM-based assessment for scalable evaluation:

#### Configuration Setup

Configure LLM providers in `.env` file:

```bash
# LLM as a Judge Configuration
LLM_JUDGE_PRIMARY_PROVIDER=cohere
LLM_JUDGE_FALLBACK_PROVIDERS=openai,anthropic
LLM_JUDGE_COHERE_MODEL=command-r-plus
LLM_JUDGE_OPENAI_MODEL=gpt-4-turbo
LLM_JUDGE_ANTHROPIC_MODEL=claude-3-opus-20240229
LLM_JUDGE_TEMPERATURE=0.3
LLM_JUDGE_MAX_TOKENS=1500

# Evaluation Framework Configuration
EVALUATION_MODE=comprehensive
CULTURAL_EVAL_WEIGHT=0.4
TRANSLATION_EVAL_WEIGHT=0.3
BUSINESS_EVAL_WEIGHT=0.2
FLUENCY_EVAL_WEIGHT=0.1
ENABLE_ENSEMBLE_EVALUATION=true
ENSEMBLE_MODEL_COUNT=3
```

#### Running LLM Evaluations

```bash
# Test configuration
python scripts/run_llm_evaluation.py --mode config --show-summary

# Single translation evaluation
python scripts/run_llm_evaluation.py --mode single \
    --kikuyu "Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ" \
    --translation "A visitor is like a vessel that should be filled with water" \
    --system og_rag

# Comparative evaluation
python scripts/run_llm_evaluation.py --mode comparative \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --sample-size 50 --enable-ensemble

# Full pipeline evaluation
python scripts/run_llm_evaluation.py --mode pipeline \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --output-dir outputs/evaluation/full_run
```

#### LLM Judge Features

**Cultural Evaluation Specialization**:
- Culturally-aware prompts for Kikuyu proverb assessment
- Traditional wisdom preservation evaluation
- Cross-cultural understanding validation

**Multi-Model Ensemble**:
- Primary Cohere model with OpenAI/Anthropic fallbacks
- Ensemble evaluation for robust assessment
- Inter-model agreement analysis

**Comprehensive Scoring**:
- Cultural Faithfulness (40%)
- Translation Accuracy (30%)
- Business Relevance (20%)
- Overall Fluency (10%)

#### Integration with Expert Evaluation

```python
# Analyze correlation between LLM and expert assessments
from src.evaluation.comparative_pipeline import ComparativeEvaluationPipeline

pipeline = ComparativeEvaluationPipeline(
    benchmark_file="data/evaluation/benchmark/translation_evaluation_benchmark.csv"
)

# Run comprehensive evaluation with expert correlation
results = await pipeline.run_comparative_evaluation(
    sample_size=100,
    enable_ensemble=True
)

# Extract correlation analysis
expert_correlation = results['expert_correlation']
print(f"Overall correlation: {expert_correlation.get('overall_correlation', 'N/A')}")
```
- `expert_evaluator_id`: Expert identifier
- `evaluation_date`: Assessment timestamp

### Step 2: System Translation Generation

Generate translations from both systems for comparative evaluation:

```bash
# Generate OG-RAG translations
python scripts/generate_og_rag_translations.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --ontology-uri bolt://localhost:7687 \
    --output-file data/evaluation/system_outputs/og_rag_translations.csv

# Generate Raw LLM translations  
python scripts/generate_raw_llm_translations.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --model-name gpt-4 \
    --output-file data/evaluation/system_outputs/raw_llm_translations.csv
```

### Step 3: Data Validation and Quality Control

Validate collected data for completeness and consistency:

```bash
# Validate expert feedback quality
python scripts/validate_evaluation_data.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --min-expert-score 3.0 \
    --min-inter-rater-agreement 0.7 \
    --output-report data/evaluation/reports/data_validation_report.md
```

**Quality Control Checks**:
- Expert score completeness (no missing values)
- Score range validation (1-5 scale adherence)
- Inter-rater reliability calculation
- Outlier detection and flagging
- Expert consistency validation

## Expert Feedback Integration

### Data Integration Script Structure

Create `scripts/process_expert_feedback.py`:

```python
#!/usr/bin/env python3
"""Process expert feedback for evaluation benchmark deployment."""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

class ExpertFeedbackProcessor:
    """Process and integrate expert evaluations into benchmark framework."""
    
    def __init__(self, expert_data_file: str, benchmark_file: str):
        self.expert_df = pd.read_excel(expert_data_file)
        self.benchmark_df = pd.read_csv(benchmark_file)
        
    def integrate_expert_feedback(self) -> pd.DataFrame:
        """Integrate expert evaluations into benchmark structure."""
        
        # Merge expert feedback with benchmark structure
        integrated_df = self.benchmark_df.merge(
            self.expert_df,
            on='proverb_id',
            how='left',
            suffixes=('_benchmark', '_expert')
        )
        
        # Calculate overall expert scores
        integrated_df['expert_overall_score'] = (
            0.4 * integrated_df['expert_cultural_faithfulness'] +
            0.3 * integrated_df['expert_translation_accuracy'] +
            0.2 * integrated_df['expert_business_relevance'] +
            0.1 * integrated_df['expert_overall_fluency']
        )
        
        return integrated_df
    
    def calculate_inter_rater_reliability(self) -> float:
        """Calculate inter-rater reliability for multiple experts."""
        # Implementation for Krippendorff's alpha or ICC
        pass
    
    def generate_gold_standard(self) -> pd.DataFrame:
        """Create gold standard dataset from high-quality expert evaluations."""
        
        # Filter high-quality evaluations (score >= 4.0)
        gold_standard = self.integrated_df[
            self.integrated_df['expert_overall_score'] >= 4.0
        ].copy()
        
        return gold_standard
```

### Quality Metrics Calculation

Implement comprehensive quality assessment:

```python
def calculate_evaluation_metrics(df: pd.DataFrame) -> dict:
    """Calculate comprehensive evaluation metrics."""
    
    metrics = {
        'primary_metrics': {
            'cultural_faithfulness_mean': df['expert_cultural_faithfulness'].mean(),
            'translation_accuracy_mean': df['expert_translation_accuracy'].mean(),
            'business_relevance_mean': df['expert_business_relevance'].mean(),
            'overall_fluency_mean': df['expert_overall_fluency'].mean(),
            'overall_quality_mean': df['expert_overall_score'].mean()
        },
        'quality_distribution': {
            'excellent_scores': len(df[df['expert_overall_score'] >= 4.5]),
            'good_scores': len(df[df['expert_overall_score'] >= 4.0]),
            'acceptable_scores': len(df[df['expert_overall_score'] >= 3.0]),
            'poor_scores': len(df[df['expert_overall_score'] < 3.0])
        },
        'expert_consistency': {
            'cultural_faithfulness_std': df['expert_cultural_faithfulness'].std(),
            'translation_accuracy_std': df['expert_translation_accuracy'].std(),
            'score_variance': df['expert_overall_score'].var()
        }
    }
    
    return metrics
```

## Comparative Analysis

### System Performance Comparison

Once both expert feedback and system translations are collected:

```bash
# Run comprehensive comparative analysis
python scripts/run_comparative_analysis.py \
    --expert-benchmark data/evaluation/processed/expert_validated_benchmark.csv \
    --og-rag-translations data/evaluation/system_outputs/og_rag_translations.csv \
    --raw-llm-translations data/evaluation/system_outputs/raw_llm_translations.csv \
    --output-dir data/evaluation/analysis \
    --generate-report
```

### Statistical Analysis Framework

```python
#!/usr/bin/env python3
"""Comprehensive statistical analysis of translation quality comparison."""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class TranslationQualityAnalyzer:
    """Analyze and compare translation quality across systems."""
    
    def __init__(self, benchmark_file: str):
        self.df = pd.read_csv(benchmark_file)
    
    def compare_systems(self) -> dict:
        """Compare OG-RAG vs Raw LLM performance."""
        
        # Calculate system scores (when expert evaluates both systems)
        og_rag_scores = self.df['og_rag_expert_score'].dropna()
        raw_llm_scores = self.df['raw_llm_expert_score'].dropna()
        
        comparison = {
            'og_rag_mean': og_rag_scores.mean(),
            'raw_llm_mean': raw_llm_scores.mean(),
            'difference': og_rag_scores.mean() - raw_llm_scores.mean(),
            'og_rag_std': og_rag_scores.std(),
            'raw_llm_std': raw_llm_scores.std(),
            'effect_size': self.calculate_cohens_d(og_rag_scores, raw_llm_scores),
            'significance_test': stats.ttest_rel(og_rag_scores, raw_llm_scores)
        }
        
        return comparison
    
    def calculate_cohens_d(self, group1: pd.Series, group2: pd.Series) -> float:
        """Calculate Cohen's d effect size."""
        pooled_std = np.sqrt(((len(group1) - 1) * group1.var() + 
                             (len(group2) - 1) * group2.var()) / 
                            (len(group1) + len(group2) - 2))
        return (group1.mean() - group2.mean()) / pooled_std
    
    def cultural_preservation_analysis(self) -> dict:
        """Analyze cultural preservation effectiveness."""
        
        cultural_analysis = {
            'og_rag_cultural_score': self.df['og_rag_cultural_faithfulness'].mean(),
            'raw_llm_cultural_score': self.df['raw_llm_cultural_faithfulness'].mean(),
            'cultural_advantage': (
                self.df['og_rag_cultural_faithfulness'].mean() - 
                self.df['raw_llm_cultural_faithfulness'].mean()
            ),
            'cultural_preservation_rate': len(
                self.df[self.df['og_rag_cultural_faithfulness'] >= 4.0]
            ) / len(self.df),
            'traditional_context_coverage': self.analyze_traditional_coverage()
        }
        
        return cultural_analysis
    
    def business_relevance_assessment(self) -> dict:
        """Assess modern business application quality."""
        
        business_analysis = {
            'og_rag_business_score': self.df['og_rag_business_relevance'].mean(),
            'raw_llm_business_score': self.df['raw_llm_business_relevance'].mean(),
            'business_advantage': (
                self.df['og_rag_business_relevance'].mean() - 
                self.df['raw_llm_business_relevance'].mean()
            ),
            'modern_applicability_rate': len(
                self.df[self.df['og_rag_business_relevance'] >= 4.0]
            ) / len(self.df)
        }
        
        return business_analysis
```

## Statistical Validation

### Significance Testing Protocol

```python
def run_statistical_validation(df: pd.DataFrame) -> dict:
    """Run comprehensive statistical validation of results."""
    
    validation_results = {
        'sample_size_adequacy': {
            'total_cases': len(df),
            'power_analysis': calculate_statistical_power(df),
            'effect_size_detectable': calculate_minimum_detectable_effect(df)
        },
        'normality_tests': {
            'og_rag_normality': stats.shapiro(df['og_rag_expert_score'].dropna()),
            'raw_llm_normality': stats.shapiro(df['raw_llm_expert_score'].dropna())
        },
        'comparative_tests': {
            'paired_t_test': stats.ttest_rel(
                df['og_rag_expert_score'].dropna(),
                df['raw_llm_expert_score'].dropna()
            ),
            'wilcoxon_signed_rank': stats.wilcoxon(
                df['og_rag_expert_score'].dropna(),
                df['raw_llm_expert_score'].dropna()
            ),
            'effect_size_confidence_interval': calculate_effect_size_ci(df)
        },
        'reliability_validation': {
            'inter_rater_reliability': calculate_krippendorff_alpha(df),
            'internal_consistency': calculate_cronbach_alpha(df),
            'test_retest_reliability': calculate_test_retest(df)
        }
    }
    
    return validation_results
```

### Quality Threshold Validation

```python
def validate_quality_thresholds(df: pd.DataFrame) -> dict:
    """Validate achievement of quality targets."""
    
    threshold_validation = {
        'cultural_faithfulness_target': {
            'target': 4.2,
            'achieved': df['og_rag_cultural_faithfulness'].mean(),
            'met': df['og_rag_cultural_faithfulness'].mean() >= 4.2
        },
        'translation_accuracy_target': {
            'target': 4.0,
            'achieved': df['og_rag_translation_accuracy'].mean(),
            'met': df['og_rag_translation_accuracy'].mean() >= 4.0
        },
        'overall_quality_target': {
            'target': 4.0,
            'achieved': df['og_rag_expert_score'].mean(),
            'met': df['og_rag_expert_score'].mean() >= 4.0
        },
        'inter_rater_reliability_target': {
            'target': 0.7,
            'achieved': calculate_inter_rater_reliability(df),
            'met': calculate_inter_rater_reliability(df) >= 0.7
        }
    }
    
    return threshold_validation
```

## Results Interpretation

### Performance Interpretation Framework

```python
def interpret_results(analysis_results: dict) -> dict:
    """Generate comprehensive interpretation of evaluation results."""
    
    interpretation = {
        'performance_summary': {
            'og_rag_advantage': analysis_results['comparison']['difference'] > 0,
            'practical_significance': analysis_results['comparison']['effect_size'] > 0.5,
            'statistical_significance': analysis_results['comparison']['significance_test'][1] < 0.05,
            'confidence_level': 1 - analysis_results['comparison']['significance_test'][1]
        },
        'cultural_preservation': {
            'cultural_faithfulness_superior': (
                analysis_results['cultural_analysis']['cultural_advantage'] > 0.5
            ),
            'traditional_context_preserved': (
                analysis_results['cultural_analysis']['cultural_preservation_rate'] > 0.8
            ),
            'cultural_authenticity_maintained': (
                analysis_results['cultural_analysis']['og_rag_cultural_score'] >= 4.0
            )
        },
        'business_applicability': {
            'modern_relevance_achieved': (
                analysis_results['business_analysis']['og_rag_business_score'] >= 4.0
            ),
            'business_advantage_demonstrated': (
                analysis_results['business_analysis']['business_advantage'] > 0.3
            ),
            'practical_utility_confirmed': (
                analysis_results['business_analysis']['modern_applicability_rate'] > 0.7
            )
        },
        'research_implications': generate_research_implications(analysis_results),
        'recommendations': generate_recommendations(analysis_results)
    }
    
    return interpretation
```

### Visualization and Reporting

```bash
# Generate comprehensive evaluation report with visualizations
python scripts/generate_evaluation_report.py \
    --analysis-results data/evaluation/analysis/comparative_analysis_results.json \
    --output-format html \
    --include-visualizations \
    --output-file data/evaluation/reports/thiLLMo_evaluation_report.html
```

## Benchmark Publication

### Research Dataset Preparation

```bash
# Prepare benchmark for research publication
python scripts/prepare_research_benchmark.py \
    --validated-benchmark data/evaluation/processed/expert_validated_benchmark.csv \
    --system-outputs data/evaluation/system_outputs/ \
    --analysis-results data/evaluation/analysis/ \
    --output-dir data/evaluation/publication/ \
    --anonymize-experts \
    --include-metadata
```

### Publication Package Contents

The research publication package includes:

1. **Benchmark Dataset**: `kikuyu_proverbs_translation_benchmark.csv`
2. **Expert Evaluations**: `expert_quality_assessments.csv`
3. **System Outputs**: `og_rag_translations.csv`, `raw_llm_translations.csv`
4. **Analysis Results**: `comparative_analysis_results.json`
5. **Metadata**: `benchmark_metadata.json`
6. **Documentation**: `benchmark_usage_guide.md`
7. **Evaluation Report**: `evaluation_results_report.pdf`

### Citation and Usage Guidelines

Create citation format and usage guidelines:

```markdown
## Citation

If you use this benchmark in your research, please cite:

```bibtex
@dataset{ndethi2025kikuyu,
  title={thiLLMo: Kikuyu Proverbs Translation Quality Benchmark},
  author={Ndethi, Charles Watson Kibaki},
  year={2025},
  institution={Open Institute of Technology},
  url={https://github.com/ndethi/opit-rai9001}
}
```

## Usage Guidelines

This benchmark enables researchers to:
- Evaluate cultural translation quality for low-resource languages
- Compare ontology-grounded vs raw LLM translation approaches
- Assess preservation of cultural meaning in AI translation
- Develop culturally-aware translation systems
```

## Framework Deployment

### Production Deployment Workflow

```bash
# Deploy evaluation framework for ongoing quality assessment
python scripts/deploy_evaluation_framework.py \
    --benchmark-file data/evaluation/publication/kikuyu_proverbs_translation_benchmark.csv \
    --deployment-env production \
    --monitoring-enabled \
    --api-endpoint https://api.thillmo.org/evaluate
```

### Continuous Evaluation Pipeline

```python
#!/usr/bin/env python3
"""Continuous evaluation pipeline for production translation system."""

class ContinuousEvaluationPipeline:
    """Deploy evaluation framework for ongoing quality monitoring."""
    
    def __init__(self, benchmark_file: str):
        self.benchmark = pd.read_csv(benchmark_file)
        self.quality_thresholds = self.load_quality_thresholds()
    
    def evaluate_new_translation(self, kikuyu_text: str, translation: str) -> dict:
        """Evaluate new translation against benchmark standards."""
        
        # Find similar proverbs in benchmark
        similar_proverbs = self.find_similar_proverbs(kikuyu_text)
        
        # Apply learned quality criteria
        quality_score = self.predict_quality_score(translation, similar_proverbs)
        
        # Check against thresholds
        quality_assessment = self.assess_quality(quality_score)
        
        return {
            'translation': translation,
            'quality_score': quality_score,
            'cultural_faithfulness': quality_assessment['cultural_faithfulness'],
            'translation_accuracy': quality_assessment['translation_accuracy'],
            'business_relevance': quality_assessment['business_relevance'],
            'meets_standards': quality_score >= self.quality_thresholds['minimum'],
            'recommendations': quality_assessment['recommendations']
        }
    
    def monitor_system_performance(self) -> dict:
        """Monitor ongoing translation system performance."""
        
        # Collect recent translations
        recent_translations = self.get_recent_translations()
        
        # Evaluate against benchmark
        performance_metrics = self.calculate_performance_metrics(recent_translations)
        
        # Alert if quality degrades
        alerts = self.check_quality_alerts(performance_metrics)
        
        return {
            'performance_metrics': performance_metrics,
            'quality_trends': self.analyze_quality_trends(),
            'alerts': alerts,
            'recommendations': self.generate_system_recommendations()
        }
```

## Command-Line Interface

### Complete Evaluation Workflow

```bash
#!/bin/bash
# complete_evaluation_workflow.sh

# Step 1: Process expert feedback
echo "Processing expert feedback..."
python scripts/process_expert_feedback.py \
    --expert-evaluations data/evaluation/collected/expert_evaluations.xlsx \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv

# Step 2: Generate system translations
echo "Generating system translations..."
python scripts/generate_system_translations.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --systems og_rag,raw_llm

# Step 3: Run comparative analysis
echo "Running comparative analysis..."
python scripts/run_comparative_analysis.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --output-dir data/evaluation/analysis

# Step 4: Generate evaluation report
echo "Generating evaluation report..."
python scripts/generate_evaluation_report.py \
    --analysis-results data/evaluation/analysis/comparative_analysis_results.json \
    --output-format html,pdf

# Step 5: Prepare publication package
echo "Preparing publication package..."
python scripts/prepare_research_benchmark.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --output-dir data/evaluation/publication

echo "✅ Complete evaluation workflow finished!"
echo "📊 Results available in: data/evaluation/analysis/"
echo "📚 Publication package: data/evaluation/publication/"
```

## Quality Assurance Checklist

Before deploying evaluation results:

### Data Quality Validation
- [ ] Expert feedback completeness verified (>95% fields populated)
- [ ] Score range validation passed (all scores within 1-5 scale)
- [ ] Inter-rater reliability achieved (≥0.7 agreement)
- [ ] Outlier detection and validation completed
- [ ] Missing data patterns analyzed and addressed

### Statistical Validation
- [ ] Sample size adequacy confirmed (power analysis ≥0.8)
- [ ] Normality assumptions tested and addressed
- [ ] Appropriate statistical tests selected and executed
- [ ] Effect size calculations completed with confidence intervals
- [ ] Multiple comparison corrections applied where needed

### Results Validation
- [ ] Quality thresholds achievement verified
- [ ] Cultural preservation effectiveness confirmed
- [ ] Business relevance appropriateness validated
- [ ] Statistical significance and practical significance both achieved
- [ ] Results reproducibility verified

### Publication Readiness
- [ ] Data anonymization completed
- [ ] Metadata documentation comprehensive
- [ ] Usage guidelines and citations prepared
- [ ] Ethical considerations addressed
- [ ] Research contribution clearly articulated

---

*This comprehensive guide ensures systematic and rigorous employment of the thiLLMo evaluation framework for validating culturally faithful AI translation quality.*