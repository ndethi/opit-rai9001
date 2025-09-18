# thiLLMo Evaluation Framework

Comprehensive LLM as a Judge evaluation system for Kikuyu proverb translation quality assessment with cultural authenticity, translation accuracy, business relevance, and fluency evaluation.

## Overview

The evaluation framework provides automated assessment of translation quality using culturally-specialized Large Language Models (LLMs) as judges. It supports multiple providers, ensemble evaluation, statistical analysis, and correlation with expert human assessments.

## Key Components

### 1. Dynamic LLM Configuration (`llm_config.py`)
Environment-based configuration system supporting multiple LLM providers with fallback options.

**Supported Providers**:
- **Cohere** (Primary): Command R+ model optimized for cultural evaluation
- **OpenAI** (Fallback): GPT-4 Turbo for comprehensive assessment  
- **Anthropic** (Fallback): Claude 3 Opus for nuanced cultural understanding
- **Google** (Optional): Gemini 1.5 Pro for additional perspective

**Features**:
- Environment variable configuration via `.env` file
- Automatic provider failover and load balancing
- Cost tracking and API rate limiting
- Cultural evaluation specialization flags

### 2. LLM Judge Evaluator (`llm_judge.py`)
Core evaluation engine implementing culturally-aware assessment prompts and scoring.

**Evaluation Dimensions**:
- **Cultural Faithfulness** (40%): Preservation of traditional wisdom and cultural context
- **Translation Accuracy** (30%): Linguistic correctness and semantic fidelity
- **Business Relevance** (20%): Modern professional application potential
- **Overall Fluency** (10%): Natural English expression and readability

**Features**:
- Async evaluation for concurrent processing
- JSON-structured evaluation responses
- Confidence scoring and detailed feedback
- Single and ensemble evaluation modes

### 3. Comparative Evaluation Pipeline (`comparative_pipeline.py`)
Complete pipeline for comparing OG-RAG vs Raw LLM translation systems.

**Capabilities**:
- Batch evaluation of benchmark datasets
- Statistical significance testing
- Visualization generation (box plots, radar charts, distributions)
- Expert correlation analysis
- Comprehensive reporting with recommendations

## Quick Start

### 1. Environment Setup

```bash
# Copy and configure environment file
cp .env.example .env

# Add your API keys
COHERE_API_KEY=your_cohere_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Configure evaluation settings
LLM_JUDGE_PRIMARY_PROVIDER=cohere
LLM_JUDGE_FALLBACK_PROVIDERS=openai,anthropic
ENABLE_ENSEMBLE_EVALUATION=true
ENSEMBLE_MODEL_COUNT=3
```

### 2. Basic Usage

```python
from src.evaluation import LLMJudgeEvaluator, ComparativeEvaluationPipeline

# Single evaluation
evaluator = LLMJudgeEvaluator()
result = await evaluator.evaluate_single_translation(
    kikuyu_proverb="Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ",
    english_translation="A visitor is like a vessel that should be filled with water",
    system_type="og_rag"
)

print(f"Weighted Score: {result.weighted_score}/5.0")
print(f"Cultural Faithfulness: {result.evaluation_criteria.cultural_faithfulness}/5.0")

# Comparative evaluation
pipeline = ComparativeEvaluationPipeline("data/evaluation/benchmark.csv")
results = await pipeline.run_comparative_evaluation(sample_size=50, enable_ensemble=True)
```

### 3. Command Line Interface

```bash
# Test configuration
python scripts/run_llm_evaluation.py --mode config --show-summary

# Single evaluation
python scripts/run_llm_evaluation.py --mode single \
    --kikuyu "Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ" \
    --translation "A visitor is like a vessel that should be filled with water" \
    --system og_rag

# Comparative evaluation
python scripts/run_llm_evaluation.py --mode comparative \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --enable-ensemble --sample-size 100
```

## Configuration Options

### Environment Variables

```bash
# LLM Provider Configuration
LLM_JUDGE_PRIMARY_PROVIDER=cohere              # Primary evaluation provider
LLM_JUDGE_FALLBACK_PROVIDERS=openai,anthropic  # Comma-separated fallbacks
LLM_JUDGE_COHERE_MODEL=command-r-plus          # Cohere model selection
LLM_JUDGE_OPENAI_MODEL=gpt-4-turbo             # OpenAI model selection
LLM_JUDGE_ANTHROPIC_MODEL=claude-3-opus-20240229  # Anthropic model selection

# Evaluation Parameters
LLM_JUDGE_TEMPERATURE=0.3                      # Generation temperature
LLM_JUDGE_MAX_TOKENS=1500                      # Maximum response tokens
LLM_JUDGE_TIMEOUT=30                           # API timeout seconds

# Framework Configuration
EVALUATION_MODE=comprehensive                   # Evaluation thoroughness
CULTURAL_EVAL_WEIGHT=0.4                       # Cultural dimension weight
TRANSLATION_EVAL_WEIGHT=0.3                    # Accuracy dimension weight
BUSINESS_EVAL_WEIGHT=0.2                       # Business dimension weight
FLUENCY_EVAL_WEIGHT=0.1                        # Fluency dimension weight
ENABLE_ENSEMBLE_EVALUATION=true                # Multi-model evaluation
ENSEMBLE_MODEL_COUNT=3                         # Number of ensemble models
```

## Evaluation Process

### 1. Cultural Assessment
Evaluates preservation of traditional Kikuyu wisdom and cultural context in English translations.

**Criteria**:
- Cultural concepts preserved
- Traditional context maintained
- Metaphorical meaning captured
- Cultural authenticity respected

### 2. Translation Accuracy
Assesses linguistic correctness and semantic fidelity of the translation.

**Criteria**:
- Semantic equivalence
- Grammatical correctness
- Vocabulary appropriateness
- Idiomatic naturalness

### 3. Business Relevance
Evaluates applicability in modern business and professional contexts.

**Criteria**:
- Modern context applicability
- Business scenario relevance
- Professional appropriateness
- Practical utility

### 4. Overall Fluency
Assesses natural English expression and readability for target audience.

**Criteria**:
- Natural expression
- Readability and flow
- Coherence
- Target audience appropriateness

## Statistical Analysis

The framework provides comprehensive statistical analysis including:

- **Descriptive Statistics**: Mean, median, standard deviation, confidence intervals
- **Significance Testing**: Paired t-tests for system comparisons
- **Effect Size**: Cohen's d for practical significance assessment
- **Correlation Analysis**: Pearson and Spearman correlations with expert assessments
- **Inter-rater Reliability**: Agreement measures across multiple LLM judges

## Visualization

Automated generation of evaluation visualizations:

- **Box Plots**: Score distribution comparisons
- **Radar Charts**: Multi-dimensional assessment profiles
- **Scatter Plots**: Correlation analyses
- **Histograms**: Score frequency distributions
- **Heatmaps**: Correlation matrices

## Expert Integration

The framework integrates with human expert evaluations for validation:

```python
# Analyze correlation with expert assessments
expert_correlation = pipeline._analyze_expert_correlation(evaluation_results)
print(f"Overall correlation: {expert_correlation['overall_correlation']}")
```

**Expert Data Format**:
- `proverb_id`: Unique identifier linking to benchmark
- `expert_cultural_faithfulness`: Cultural assessment score (1-5)
- `expert_translation_accuracy`: Accuracy assessment score (1-5)
- `expert_business_relevance`: Business relevance score (1-5)
- `expert_overall_fluency`: Fluency assessment score (1-5)
- `expert_detailed_feedback`: Qualitative feedback

## Output Formats

### JSON Reports
```json
{
  "evaluation_metadata": {
    "timestamp": "2025-09-18T10:30:00",
    "total_evaluations": 50,
    "llm_configuration": {...}
  },
  "statistical_analysis": {
    "overall_scores": {...},
    "dimension_analysis": {...},
    "statistical_tests": {...}
  },
  "key_findings": [...],
  "recommendations": [...]
}
```

### CSV Data Export
Structured data for further analysis with columns for all evaluation dimensions, scores, and metadata.

### Visualization Files
- PNG/SVG charts for presentations
- Interactive HTML plots for detailed exploration
- Publication-ready figures

## Performance Considerations

- **Rate Limiting**: Automatic API rate limiting to prevent quota exhaustion
- **Concurrent Processing**: Async evaluation for improved throughput
- **Error Handling**: Graceful degradation with provider fallbacks
- **Caching**: Optional result caching for repeated evaluations
- **Cost Optimization**: Token usage tracking and cost estimation

## Best Practices

1. **Configuration Validation**: Always test configuration before large evaluations
2. **Sample Testing**: Start with small samples to validate setup
3. **Ensemble Usage**: Use ensemble evaluation for important assessments
4. **Expert Validation**: Regularly validate against expert assessments
5. **Statistical Rigor**: Ensure adequate sample sizes for statistical significance
6. **Cultural Sensitivity**: Review evaluation prompts for cultural appropriateness

## Troubleshooting

### Common Issues

**API Key Configuration**:
```bash
# Verify API keys are properly set
python scripts/run_llm_evaluation.py --mode config
```

**Provider Failures**:
- Check internet connectivity
- Verify API key validity
- Review rate limiting status
- Use fallback providers

**Evaluation Errors**:
- Validate input data format
- Check prompt encoding issues
- Review model response parsing
- Enable verbose logging for debugging

### Logging

Enable detailed logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When contributing to the evaluation framework:

1. **Test Coverage**: Ensure comprehensive test coverage for new features
2. **Documentation**: Update this README and inline documentation
3. **Cultural Sensitivity**: Review changes for cultural appropriateness
4. **Performance**: Consider API costs and processing efficiency
5. **Compatibility**: Maintain backwards compatibility where possible

## Citation

If using this evaluation framework in research, please cite:

```bibtex
@misc{kibaki2025thillmo_evaluation,
  title={thiLLMo: LLM as a Judge Evaluation Framework for Culturally Faithful Kikuyu Proverb Translation},
  author={Kibaki, Charles Watson Ndethi},
  year={2025},
  institution={Open Institute of Technology},
  course={MSc Responsible AI - RAI9001}
}
```