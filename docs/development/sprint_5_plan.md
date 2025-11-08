# Sprint 5: Metrics, Visualization & Documentation

**Status:** In Progress  
**Started:** November 7, 2025  
**Target Completion:** November 8, 2025

## Overview

Sprint 5 focuses on analyzing the OG-RAG evaluation results, computing comprehensive metrics, running statistical tests, generating visualizations, and documenting findings for the supervisor meeting and thesis.

## Dependencies

**Completed Prerequisites:**
- ✅ Sprint 1: Graph Retriever (413 lines)
- ✅ Sprint 2: Context Builder (474 lines)
- ✅ Sprint 3: GPT-4 Translator (530 lines)
- ✅ Sprint 4: Evaluation Execution (100 proverbs, $5.29, 14.5 min)

**Input Data:**
- `data/results/ograg_translations/ograg_evaluation_100proverbs.csv` (92KB, 100 proverbs)
- Neo4j database with 100 proverbs + translations

## Tasks & Status

### Task 1: Metrics Calculation ⏳ IN PROGRESS

**File:** `scripts/calculate_metrics.py` (600 lines)

**Implemented Features:**
- ✅ BLEU score calculation (sacrebleu) for all 100 proverbs
- ✅ LLM-as-judge for cultural fidelity (20-proverb stratified sample)
- ✅ Failure detection heuristics
- ✅ Statistical tests (paired t-test, Cohen's d)
- ✅ Per-proverb and aggregate outputs (CSV + JSON)

**Metrics Computed:**
1. **BLEU Scores** (0-100): Measures translation accuracy against expert translations
   - Raw GPT-4
   - Traditional RAG
   - OG-RAG
   
2. **Cultural Fidelity** (0-1 scale via LLM-as-judge):
   - GPT-4 evaluates preservation of cultural meaning/metaphors
   - 20-proverb representative sample (stratified by length)
   - Deterministic scoring (temperature=0.1)
   
3. **Failure Rates**: Percentage of empty/error translations per method

**Statistical Tests:**
- Paired t-tests: Raw vs OG-RAG, Traditional vs OG-RAG
- Cohen's d effect sizes
- 95% confidence intervals

**Cost Analysis:**
- BLEU calculation: $0 (local computation)
- LLM-as-judge (20 proverbs): ~$0.50 (60 API calls @ ~200 tokens each)
- **Total incremental cost:** ~$0.50

**Current Status:** Script implemented, ready to run full evaluation.

**Next Action:** Execute script and verify outputs.

**Commands:**
```bash
# Install dependencies
pip install sacrebleu numpy scipy

# Run metrics calculation
python3 scripts/calculate_metrics.py \
  --evaluation-csv data/results/ograg_translations/ograg_evaluation_100proverbs.csv \
  --sample-size 20 \
  --output-dir data/results

# Skip LLM judge (BLEU only, free)
python3 scripts/calculate_metrics.py --no-llm-judge
```

**Expected Outputs:**
- `data/results/ograg_metrics_per_proverb.csv`
- `data/results/ograg_metrics_summary.csv`
- `data/results/ograg_metrics_summary.json`

---

### Task 2: Statistical Analysis 📋 PENDING

**File:** `scripts/run_statistical_tests.py` (to be created)

**Planned Tests:**
1. Normality checks (Shapiro-Wilk)
2. Paired t-tests (parametric) or Wilcoxon (non-parametric)
3. Effect sizes: Cohen's d, Hedge's g
4. Confidence intervals (bootstrap)
5. Multiple comparison correction (Bonferroni)

**Comparisons:**
- Raw vs Traditional RAG
- Raw vs OG-RAG
- Traditional RAG vs OG-RAG

**Output:** `data/results/statistical_tests.json`

**Acceptance Criteria:**
- All p-values < 0.05 for OG-RAG superiority
- Cohen's d > 0.8 (large effect size)

---

### Task 3: Visualization 📊 PENDING

**File:** `scripts/visualize_results.py` (to be created)

**Charts to Generate:**

1. **Bar Charts** (mean with error bars):
   - BLEU scores by method
   - Cultural fidelity scores by method
   - Failure rates by method

2. **Box Plots:**
   - BLEU score distributions
   - Cultural fidelity distributions

3. **Scatter Plots:**
   - Token usage vs BLEU score
   - Token usage vs cultural fidelity

4. **Heatmap:**
   - Correlation matrix (BLEU, cultural fidelity, tokens)

5. **Example Showcase:**
   - Side-by-side translations (5-10 representative cases)

**Output Directory:** `docs/results/figures/`

**Dependencies:** `matplotlib`, `seaborn`, `pandas`

**Acceptance Criteria:**
- At least 5 publication-ready figures (300 DPI PNG + SVG)
- All charts have clear labels, legends, and titles

---

### Task 4: Documentation 📝 PENDING

**File:** `docs/results/ograg_evaluation_report.md`

**Structure:**

```markdown
# OG-RAG Evaluation Report

## Executive Summary
- Key findings (1 paragraph)
- Statistical significance
- Practical implications

## Methodology
- Dataset: 100 Kikuyu proverbs
- Methods: Raw, Traditional RAG, OG-RAG
- Metrics: BLEU, cultural fidelity, failure rates
- Statistical approach

## Results

### Quantitative Analysis
- Aggregate statistics table
- Statistical test results
- Effect sizes

### Qualitative Analysis
- 5-10 example translations
- Failure mode analysis
- Cultural preservation examples

## Discussion
- Why OG-RAG outperforms
- Limitations
- Cost-benefit trade-offs

## Figures
[Embedded visualizations]

## Conclusions
- Research questions answered
- Contributions to field
- Future work
```

**Acceptance Criteria:**
- 5-10 pages
- Publication-ready (thesis chapter draft)
- All figures embedded
- References to statistical tests

---

### Task 5: Supervisor Presentation Prep 📽️ PENDING

**File:** `presentations/weekly-updates/sprint_5_supervisor_meeting.pdf`

**Slides:**
1. Title: "OG-RAG Evaluation Results"
2. Methodology recap
3. Key quantitative results (with charts)
4. Example translations showcase
5. Statistical significance
6. Cost analysis
7. Next steps

**Acceptance Criteria:**
- 7-10 slides
- Clear visualizations
- Key findings highlighted

---

## Timeline

| Task | Duration | Depends On | Status |
|------|----------|------------|--------|
| Metrics calculation | 1 hour | Sprint 4 | ⏳ In Progress |
| Run metrics script | 5 min | Task 1 | 📋 Pending |
| Statistical tests | 1 hour | Task 2 | 📋 Pending |
| Visualization | 2 hours | Task 2 | 📋 Pending |
| Documentation | 2 hours | Task 3 | 📋 Pending |
| Presentation prep | 1 hour | Task 4 | 📋 Pending |

**Total Estimated Time:** 7-8 hours

---

## Technical Requirements

### Python Dependencies

```bash
# Core
pip install sacrebleu numpy scipy pandas

# Visualization
pip install matplotlib seaborn

# Optional (semantic similarity)
pip install sentence-transformers

# Testing
pip install pytest
```

### Environment Setup

```bash
# Create clean venv (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

pip install --upgrade pip
pip install -r requirements-sprint5.txt
```

**File:** `requirements-sprint5.txt`
```
sacrebleu>=2.3.0
numpy>=1.24.0
scipy>=1.10.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
pytest>=7.4.0
```

---

## Success Criteria

**Sprint 5 is COMPLETE when:**

1. ✅ Metrics calculated for all 100 proverbs
2. ✅ Statistical tests show OG-RAG superiority (p < 0.05, d > 0.8)
3. ✅ At least 5 publication-ready figures generated
4. ✅ Evaluation report drafted (5-10 pages)
5. ✅ Supervisor presentation ready (7-10 slides)
6. ✅ All outputs committed to Git and pushed to GitHub

**Evidence for Supervisor Meeting:**
- Significant improvement in BLEU (expected: +15-20 points)
- Significant improvement in cultural fidelity (expected: +0.3-0.4)
- Lower failure rate (expected: <5% vs 10-15%)
- Publication-ready visualizations
- Draft thesis chapter

---

## Continuation Instructions (for Different Device)

### Quick Start

1. **Pull latest code:**
   ```bash
   git pull origin dev
   ```

2. **Check current progress:**
   ```bash
   ls -lh scripts/calculate_metrics.py
   ls -lh data/results/ograg_*.csv
   ```

3. **Run metrics calculation:**
   ```bash
   python3 scripts/calculate_metrics.py --sample-size 20
   ```

4. **Check results:**
   ```bash
   cat data/results/ograg_metrics_summary.json
   ```

5. **Continue with visualization:**
   - Create `scripts/visualize_results.py`
   - Generate charts in `docs/results/figures/`

### Context Files

- **Evaluation data:** `data/results/ograg_translations/ograg_evaluation_100proverbs.csv`
- **Metrics script:** `scripts/calculate_metrics.py`
- **Sprint plan:** `docs/development/sprint_5_plan.md` (this file)
- **Progress tracking:** See todo list in conversation

### Key Decisions Made

1. **Cost-effective approach:** 20-proverb LLM-as-judge sample (~$0.50) instead of full 100 (~$2.40)
2. **Stratified sampling:** Sample distributed across proverb length to ensure representativeness
3. **BLEU for all:** Free BLEU scores computed for all 100 proverbs for statistical power
4. **Hybrid metrics:** Combine objective (BLEU) and subjective (LLM-as-judge) measures

### Expected Results (Hypotheses)

Based on Sprint 4 preliminary observations:

| Metric | Raw GPT-4 | Traditional RAG | OG-RAG | Hypothesis |
|--------|-----------|-----------------|---------|------------|
| BLEU | ~15-20 | ~40-50 | ~45-55 | OG-RAG ≈ Traditional RAG (both good) |
| Cultural Fidelity | ~0.3-0.4 | ~0.6-0.7 | ~0.7-0.9 | OG-RAG >> Raw, OG-RAG > Traditional |
| Failure Rate | ~10-15% | ~3-5% | ~1-3% | OG-RAG lowest |

---

## Blockers & Risks

**Current Blockers:**
- None (metrics script implemented)

**Potential Risks:**
1. LLM-as-judge cost if scaling to 100 proverbs ($2.40) - Mitigated by 20-sample approach
2. Statistical power with 20-sample LLM judgments - Acceptable for pilot study, can scale later
3. BLEU may not fully capture cultural fidelity - Addressed by hybrid metrics

---

## References

**Related Documents:**
- Sprint 4 evaluation log: `evaluation_100proverbs.log`
- Baseline translations: `data/results/baseline_translations/`
- OG-RAG system code: `src/og-rag-system/`

**External Resources:**
- BLEU: https://github.com/mjpost/sacrebleu
- Statistical tests: https://docs.scipy.org/doc/scipy/reference/stats.html
- Visualization: https://seaborn.pydata.org/

---

**Last Updated:** November 7, 2025  
**Next Review:** After metrics calculation completion
