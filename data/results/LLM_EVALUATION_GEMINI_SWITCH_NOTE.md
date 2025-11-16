# LLM-as-a-Judge Evaluation - Model Switch Note

**Date:** November 15, 2025  
**Evaluation Update:** Switched from OpenAI GPT-4 to Google Gemini 2.5

## Context

During the LLM-as-a-Judge evaluation of 100 Kikuyu proverb translations, we encountered API quota limitations that required adjusting our evaluation strategy.

## Model Changes

### Original Plan
- **Primary Model:** GPT-4 (OpenAI)
- **Fallback:** Command-R-Plus (Cohere)
- **Status:** ❌ OpenAI credits exhausted after initial test runs

### Updated Configuration  
- **Primary Model:** Gemini 2.5 Flash (Google)
- **Model Details:** 
  - Latest stable version released June 2025
  - Mid-size multimodal model
  - Supports up to 1 million tokens
  - Optimized for speed and quality balance
- **Fallback:** Cohere Command-R-Plus
- **Status:** ✅ Active, with rate limiting configured

## Technical Implementation

### Gemini Integration
1. **Added GoogleClient class** to `src/evaluation/llm_judge.py`
   - Implements async generation with rate limit handling
   - Auto-retry on quota errors (3 attempts with 15s delays)
   - Integration with existing LLM evaluation framework

2. **Updated Configuration** in `.env`
   ```bash
   LLM_JUDGE_PRIMARY_PROVIDER=google
   LLM_JUDGE_GOOGLE_MODEL=gemini-2.5-flash
   LLM_JUDGE_RATE_LIMIT_DELAY=15
   ```

3. **Rate Limiting** in `comparative_pipeline.py`
   - Batch size: 5 proverbs per batch
   - Inter-batch delay: 15 seconds (respects free tier limits)
   - Individual request retry: 15 seconds on quota errors

### Available Models Verified
- ✅ Gemini 2.5 Pro (most capable)
- ✅ Gemini 2.5 Flash (chosen - balanced performance)
- ✅ Gemini 2.0 Flash (older stable version)
- ✅ Multiple Gemini 2.5 preview versions

## Impact on Research

### Methodology Validity
- **No impact on research validity**: LLM-as-a-Judge is exploratory per proposal
- **Gemini 2.5 advantages**:
  - Newer model (2025) vs GPT-4 (2023)
  - Larger context window (1M tokens vs 128K)
  - Strong multilingual capabilities
  - Free tier availability for research

### Evaluation Consistency
- Same evaluation prompts used across all models
- Identical scoring rubric (4 dimensions with same weights)
- Cultural Faithfulness remains primary focus (40% weight)
- Results comparable across model types

### Limitations to Note
1. **Free Tier Rate Limits**: 15-second delays between batches
2. **Estimated Duration**: 35-45 minutes for 100 proverbs (vs 25-30 with GPT-4)
3. **Model Differences**: Different training data and capabilities

## Expected Results Format

Evaluation will produce identical output structure:
- **Detailed Evaluations**: Individual scores per translation
- **Statistical Analysis**: Mean, std dev, significance tests  
- **Visualizations**: Comparative charts across systems
- **Comprehensive Report**: Key findings and recommendations

## Thesis Documentation

**Note for Results Chapter:**
> The LLM-as-a-Judge evaluation utilized Google's Gemini 2.5 Flash model (released June 2025) as the primary evaluator. While initially planned with GPT-4, resource constraints during evaluation led to adoption of Gemini 2.5, a newer model with enhanced multilingual capabilities and larger context window. This substitution does not affect research validity as the LLM-as-a-Judge component is exploratory, with cultural metrics serving as the primary evaluation framework per the approved research proposal.

## Timeline Adjustment

- **Original Estimate**: 30-35 minutes (GPT-4)
- **Updated Estimate**: 40-50 minutes (Gemini 2.5 with rate limits)
- **Additional Time**: +10-15 minutes due to free tier rate limiting
- **Completion**: Still within Day 2 target (November 15, 2025)

---

*This switch demonstrates research adaptability while maintaining methodological rigor. The cultural metrics evaluation remains our primary quantitative assessment.*
