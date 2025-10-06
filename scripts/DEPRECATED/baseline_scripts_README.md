# Deprecated Baseline Translation Scripts

**Date Deprecated:** October 7, 2025  
**Reason:** Script consolidation - replaced by single unified `generate_baseline_translations.py`

## Deprecated Files

### 1. `generate_baseline_translations_OLD.py`
- **Original Purpose:** Initial baseline translation script with mixed "Raw LLM" system
- **Issues:** 
  - Mixed OpenAI and Cohere responses in single "raw_llm" column (couldn't distinguish which was which)
  - Generated 401 rows for 50 proverbs (~8x duplication)
  - Included confusing "OG-RAG" placeholder (just OpenAI with cultural prompt)
- **Replaced By:** `generate_baseline_translations.py` with separated systems

### 2. `generate_clean_baseline_OLD.py`
- **Original Purpose:** Clean baseline generator with separated OpenAI/Cohere/NLLB/Google systems
- **Status:** Working implementation, consolidated into main script
- **Replaced By:** `generate_baseline_translations.py` (functionality merged)

### 3. `generate_50proverb_baseline.py`
- **Original Purpose:** Quick test script for 50-proverb baseline generation
- **Issues:** Hardcoded to 50 proverbs, no command-line flexibility
- **Replaced By:** `generate_baseline_translations.py --max-proverbs 50`

### 4. `generate_baseline_translations_partial.py`
- **Original Purpose:** Partial implementation during development
- **Status:** Incomplete, superseded by full implementation
- **Replaced By:** `generate_baseline_translations.py`

## Current Implementation

**Active Script:** `scripts/generate_baseline_translations.py`

**Features:**
- ✅ Separated systems: OpenAI | Cohere | NLLB | Google (no mixing)
- ✅ ONE row per proverb (no duplicates)
- ✅ Command-line arguments: `--max-proverbs`, `--output`, `--input`
- ✅ Incremental saving every 10 proverbs
- ✅ Summary statistics generation
- ✅ Clear structure for analysis

**Usage Examples:**
```bash
# Process all proverbs
python scripts/generate_baseline_translations.py

# Test with 10 proverbs
python scripts/generate_baseline_translations.py --max-proverbs 10

# Process 50 proverbs with custom output
python scripts/generate_baseline_translations.py --max-proverbs 50 --output my_baseline.csv
```

## Migration Path

If you need to reference old behavior:
1. Check these deprecated scripts for historical implementation
2. Review git history for detailed change evolution
3. Consult `docs/development/BASELINE_REDESIGN_PROPOSAL.md` for design decisions

## Output Structure Comparison

### OLD (deprecated):
- 401 rows for 50 proverbs
- Mixed OpenAI/Cohere in "raw_llm" column
- OG-RAG placeholder confusion
- Difficult to analyze

### NEW (current):
- 50 rows for 50 proverbs (1:1 mapping)
- Separated columns: `openai_translation`, `cohere_translation`, `nllb_translation`, `google_translation`
- Clear system attribution with reasoning and confidence scores
- Analysis-ready structure

## Related Documentation

- `docs/development/BASELINE_REDESIGN_PROPOSAL.md` - Comprehensive redesign rationale
- `data/evaluation/gold_standard_ireri.csv` - Input gold standard
- `data/results/baseline_translations/` - Output directory for clean baselines
