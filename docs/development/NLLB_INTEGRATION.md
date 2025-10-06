# NLLB-200 Integration for Baseline Translation System

## Overview

NLLB-200 (No Language Left Behind) has been integrated into the thiLLMo baseline translation system as the **specialized machine translation baseline** with native Kikuyu support.

## Why NLLB?

### Native Kikuyu Support
- **Only MT model** with actual Kikuyu (kik_Latn) training data
- Part of Meta's 200+ language multilingual model
- Specifically designed for low-resource languages
- Trained on parallel translation corpora

### Research Value
NLLB provides a critical comparison point for evaluating OG-RAG:
- **NLLB**: Specialized MT trained on Kikuyu↔English pairs
- **Raw LLM**: General AI with some Kikuyu knowledge
- **Google Translate**: Commercial standard (doesn't support Kikuyu)
- **OG-RAG**: Cultural ontology-enhanced translation (future)

## Translation System Architecture

```
Baseline Translation Systems (Flat Comparison for Gap Analysis)
├── 1. OG-RAG Placeholder - Will be enhanced with cultural ontology
├── 2. Raw LLM (GPT-4/Cohere Aya) - General multilingual AI
├── 3. NLLB-200 (Meta) - Specialized low-resource MT ← NEW
└── 4. Google Translate - Commercial baseline (reference)
```

All systems are **equal peers** in baseline comparison to identify:
- Where ALL systems fail → Critical ontology requirements
- Where only NLLB/LLM succeeds → System strengths
- What cultural elements are missing → Ontology development targets

## Implementation Details

### API vs Local Model
**Chosen: Hugging Face Inference API**

Rationale for GPU-less iMac setup:
- ✅ No local GPU required (uses HF cloud GPUs)
- ✅ No 2-6GB model download needed
- ✅ Fast inference (<1s per proverb)
- ✅ Free tier available (30k chars/month)
- ✅ Simple setup (one pip install)

### Model Selection
**Model**: `facebook/nllb-200-distilled-600M`

- Distilled version: Faster, smaller, good quality
- 600M parameters: Best balance for API usage
- Supports 200+ languages including Kikuyu (kik_Latn)

### Language Codes
- **Source**: `kik_Latn` (Kikuyu in Latin script)
- **Target**: `eng_Latn` (English in Latin script)

Based on [FLORES-200 language codes](https://github.com/facebookresearch/flores/blob/main/flores200/README.md)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install huggingface_hub
```

Or from requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. API Key (Optional)

NLLB works **without an API key** on the free tier, but for higher rate limits:

```bash
# Get free API key from https://huggingface.co/settings/tokens
export HF_API_KEY="your_huggingface_api_key"
```

Or add to `.env`:
```
HF_API_KEY=your_huggingface_api_key
```

### 3. Test Integration

```bash
python scripts/test_nllb_integration.py
```

## Usage

### Single Translation

```python
from src.evaluation.baseline_translation_system import BaselineTranslationSystem

system = BaselineTranslationSystem()
result = system.translate_nllb("Andu ni indo.")

print(result.translation)  # NLLB translation
print(result.generation_time)  # Time taken
print(result.metadata)  # Model info
```

### All Systems Comparison

```python
system = BaselineTranslationSystem()
translations = system.generate_all_translations("Andu ni indo.", "MW_002")

# Returns dict with keys: 'og_rag', 'raw_llm', 'nllb', 'google'
nllb_translation = translations['nllb'].translation
```

### Full Baseline Generation

```python
from src.evaluation.baseline_translation_system import TranslationComparator

system = BaselineTranslationSystem()
comparator = TranslationComparator(system)

# Generate baseline for all proverbs
results_df = comparator.compare_on_gold_standard(
    "data/evaluation/gold_standard_ireri.csv"
)

# Results saved to: data/results/baseline_translations/
```

## Output Data Structure

### CSV Columns Added

- `nllb_translation`: NLLB-200 translation text
- `nllb_metadata`: JSON metadata (model info, language codes)
- `nllb_time`: Generation time in seconds

### TranslationResult Fields

```python
TranslationResult(
    proverb_id="MW_002",
    kikuyu_text="Andu ni indo.",
    translation="People are wealth.",
    system_name="NLLB-200",
    cultural_meaning="Specialized MT for low-resource languages - trained on Kikuyu data",
    confidence_score=None,  # NLLB doesn't provide confidence
    generation_time=0.85,
    timestamp="2025-10-06T...",
    metadata={
        "model": "facebook/nllb-200-distilled-600M",
        "provider": "meta",
        "via": "huggingface_inference_api",
        "src_lang": "kik_Latn",
        "tgt_lang": "eng_Latn",
        "language_support": "native_kikuyu",
        "model_type": "specialized_mt"
    }
)
```

## Performance Expectations

For ~200 proverb gold standard:
- **Per proverb**: ~0.5-1.5 seconds (via HF API)
- **Total time**: ~3-5 minutes for full dataset
- **Rate limits**: Free tier sufficient for research use
- **Memory**: Minimal (API-based, no local model)

## Error Handling

### Rate Limits
If rate limited on free tier:
```
⚠️ Rate limit reached. Consider adding HF_API_KEY or waiting a moment.
```

Solution:
1. Add HF API key for higher limits
2. Wait a few minutes and retry
3. Process in smaller batches

### API Unavailable
Falls back gracefully with error result:
```
[ERROR: Hugging Face client not available]
```

System continues with other translation methods.

## Research Applications

### Gap Analysis (Pre-Ontology)
Compare where systems fail to identify ontology requirements:

```python
# After baseline generation
failures_df = results_df[
    (results_df['nllb_translation'].str.contains('ERROR')) |
    (results_df['raw_llm_translation'].str.contains('ERROR'))
]

# These failures indicate cultural gaps
```

### Quality Comparison
```python
# Compare NLLB (specialized MT) vs Raw LLM (general AI)
nllb_quality = evaluate_translations(results_df['nllb_translation'])
llm_quality = evaluate_translations(results_df['raw_llm_translation'])

# Where NLLB fails but LLM succeeds → General AI advantage
# Where LLM fails but NLLB succeeds → Specialized MT advantage
# Where BOTH fail → Ontology needed
```

### Cultural Fidelity Assessment
```python
# Evaluate cultural authenticity
from src.evaluation.cultural_metrics import CulturalFidelityMetrics

metrics = CulturalFidelityMetrics()
nllb_scores = metrics.evaluate(
    results_df['nllb_translation'],
    results_df['expert_cultural_meaning']
)

# Compare with expert translations to assess cultural gaps
```

## Next Steps

1. **Run Baseline Generation**
   ```bash
   python scripts/generate_baseline_translations.py
   ```

2. **Analyze Results**
   - Compare NLLB vs Expert translations
   - Identify where specialized MT struggles
   - Document cultural gaps for ontology

3. **Develop Ontology**
   - Use gap analysis to inform ontology structure
   - Focus on areas where all systems fail
   - Prioritize cultural elements missing from translations

4. **Enhance OG-RAG**
   - Integrate cultural ontology
   - Test if ontology fills identified gaps
   - Compare enhanced OG-RAG vs NLLB baseline

## References

- **NLLB Paper**: [No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672)
- **FLORES-200**: [Evaluation Benchmark for 200 Languages](https://github.com/facebookresearch/flores)
- **Hugging Face**: [NLLB Model Documentation](https://huggingface.co/docs/transformers/model_doc/nllb)
- **Model Card**: [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)

## Support

For issues or questions:
1. Check HF API status: https://status.huggingface.co/
2. Review error logs in `logs/`
3. Test with `scripts/test_nllb_integration.py`
4. Verify API key if using authenticated tier

---

**Integration Date**: October 6, 2025  
**Status**: ✅ Complete and Ready for Testing  
**Model**: facebook/nllb-200-distilled-600M (via HF Inference API)
