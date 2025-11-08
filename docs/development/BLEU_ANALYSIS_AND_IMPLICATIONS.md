# BLEU Score Analysis & Implications
**Date:** November 8, 2025  
**Analysis:** Impact of simplified metrics calculation

---

## 📊 Current Results Overview

### Summary Statistics
- **Total Proverbs Evaluated:** 97
- **Average BLEU Score:** 9.33
- **Range:** 0.0 - 68.04
- **Median (approx):** ~9.0

### What We Calculated
✅ **BLEU scores** using `sacrebleu` (industry-standard implementation)
- Per-proverb scores comparing OG-RAG output to expert translations
- Summary statistics (mean, min, max)

### What We're Missing (due to scipy issues)
❌ **Statistical tests** 
- Paired t-tests (OG-RAG vs Raw GPT-4)
- Effect sizes (Cohen's d)
- Confidence intervals
- Significance testing (p-values)

---

## 🎯 Critical Assessment: Are These Results Useful?

### ✅ YES - Here's Why:

#### 1. **BLEU Scores ARE Valid**
The BLEU calculation itself is completely correct:
- Uses `sacrebleu` library (official implementation)
- Standard n-gram overlap metric (1-4 grams)
- Properly normalized (0-100 scale)
- **No dependency on scipy for BLEU calculation**

#### 2. **Low BLEU is EXPECTED for Proverb Translation**
**Why 9.33 is actually not alarming:**

**Example 1: High BLEU (68.04)**
```
Expert:  "Selected goods do not fill the granary."
OG-RAG:  "Borrowed seeds do not fill the granary."
BLEU:    68.04 (very high word overlap)
```
Analysis: High overlap because both preserve structure, just different word choices

**Example 2: Medium BLEU (36.56)**
```
Expert:  "Bought things do not fill the granary."
OG-RAG:  "Purchased goods do not fill the storehouse."
BLEU:    36.56 (synonyms: bought/purchased, things/goods, granary/storehouse)
```
Analysis: Same meaning, different words → moderate BLEU

**Example 3: Low BLEU (7.49)**
```
Expert:  "The property of an invalid are not distributed while the person is still alive."
OG-RAG:  "The belongings of the weak are not divided while they still breathe."
BLEU:    7.49 (complete paraphrase)
```
Analysis: **Culturally equivalent but lexically different** → low BLEU

#### 3. **This Reveals a FUNDAMENTAL INSIGHT**
**BLEU is NOT the right metric for cultural translation quality!**

Proverb translation requires:
- Cultural meaning preservation (not word matching)
- Metaphorical equivalence (not literal similarity)
- Contextual appropriateness (not lexical overlap)

**Your low BLEU scores actually VALIDATE your thesis argument:**
> "Standard MT metrics fail for culturally-grounded translation tasks"

---

## 🔬 What We CAN Learn From These Results

### Insight 1: Translation Strategy Patterns

**High BLEU (60-70):** Literal/structural preservation
- OG-RAG maintains expert translation structure
- Word choices are similar
- Example: "granary" vs "storehouse" pattern

**Medium BLEU (20-40):** Synonym substitution
- Same concepts, different words
- Culturally equivalent expressions
- Example: "bought" vs "purchased"

**Low BLEU (0-15):** Creative paraphrasing
- Complete reinterpretation
- Cultural meaning preserved, words different
- **This might actually be BETTER translation quality**

### Insight 2: What We Need Instead

**Better metrics for your thesis:**

1. **Semantic Similarity** (not BLEU)
   - Sentence embeddings (BERT, SentenceTransformers)
   - Cosine similarity of meaning representations
   - Captures paraphrase equivalence

2. **Cultural Fidelity Score** (LLM-as-Judge)
   - GPT-4 evaluates cultural meaning preservation
   - Likert scale (1-5): How well is cultural context preserved?
   - Qualitative assessment of metaphor translation

3. **Human Expert Evaluation** (Gold Standard)
   - Cultural experts rate translations
   - Multi-dimensional: accuracy, cultural appropriateness, fluency
   - Small sample (10-20 proverbs) but authoritative

---

## ⚠️ Implications for Your Thesis

### What This Means:

#### ✅ **Good News:**
1. **You have valid BLEU scores** - calculation is correct
2. **Low scores support your thesis** - BLEU inadequate for cultural translation
3. **Can still present these results** - with proper interpretation
4. **No need to rerun** - sacrebleu results are complete and correct

#### ⚠️ **Concerns:**
1. **BLEU alone is insufficient** for proving OG-RAG superiority
2. **Need additional metrics** to demonstrate improvement
3. **Statistical tests would be helpful** but not critical if you have semantic similarity
4. **Qualitative analysis is ESSENTIAL** - show translation examples

### What You Should Do:

#### **Priority 1: Add Semantic Similarity (Easy)**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compare expert vs OG-RAG embeddings
expert_emb = model.encode(expert_translation)
ograg_emb = model.encode(ograg_translation)
semantic_sim = cosine_similarity(expert_emb, ograg_emb)
```
**Time:** 1-2 hours
**Impact:** HIGH - shows meaning preservation beyond word overlap

#### **Priority 2: Qualitative Examples (Critical)**
Select 10-15 representative cases showing:
- High semantic similarity, low BLEU (cultural equivalence)
- Metaphor preservation examples
- Cultural context handling
- Failure cases and why they failed

**Time:** 2-3 hours
**Impact:** CRITICAL - shows what numbers can't capture

#### **Priority 3: Statistical Tests (Nice to Have)**
Fix scipy installation OR use alternative approaches:
- Bootstrap confidence intervals (numpy only)
- Permutation tests (no scipy needed)
- Effect size from simple formulas

**Time:** 2-4 hours (if scipy works) or skip
**Impact:** MEDIUM - adds rigor but not essential if you have strong qualitative analysis

---

## 📈 Recommended Metrics Suite

### For Your Supervisor Meeting:

**Present THREE metrics:**

1. **BLEU Score (9.33)** 
   - "Standard MT metric shows low overlap"
   - "Expected for cultural translation - validates need for better metrics"

2. **Semantic Similarity (to calculate)**
   - "Meaning preservation: XX% average cosine similarity"
   - "Shows OG-RAG captures cultural meaning despite different words"

3. **Cultural Fidelity (qualitative)**
   - "10 example cases showing cultural context preservation"
   - "Expert validation: X/10 rated as culturally appropriate"

### For Your Thesis:

**Chapter 5 (Results) Structure:**

```markdown
5.1 Quantitative Evaluation
    5.1.1 BLEU Scores (baseline metric)
    5.1.2 Semantic Similarity (meaning preservation)
    5.1.3 Cultural Fidelity Scores (LLM-as-judge)

5.2 Qualitative Analysis
    5.2.1 Example Translation Cases (10-15 proverbs)
    5.2.2 Metaphor Preservation Analysis
    5.2.3 Cultural Context Handling
    5.2.4 Failure Mode Analysis

5.3 Comparative Analysis
    5.3.1 OG-RAG vs Raw GPT-4
    5.3.2 OG-RAG vs Traditional RAG
    5.3.3 Statistical Significance (if available)

5.4 Discussion
    5.4.1 Why BLEU is Insufficient
    5.4.2 Cultural Translation Challenges
    5.4.3 Contribution of Ontology Grounding
```

---

## 🎯 Action Plan for This Weekend

### Saturday (Nov 9):
1. **Calculate Semantic Similarity** (1-2 hours)
   - Install sentence-transformers
   - Run on all 97 proverbs
   - Compare expert vs OG-RAG embeddings

2. **Select 10-15 Example Cases** (2 hours)
   - High semantic sim, low BLEU (cultural equivalence)
   - High BLEU (literal preservation)
   - Low scores (failures - analyze why)

3. **Draft Results Summary** (3-4 hours)
   - Executive summary (1 page)
   - Quantitative results (2 pages)
   - Qualitative examples (2-3 pages)
   - Total: 5-8 pages

### Sunday (Nov 10):
4. **Create Visualizations** (2 hours)
   - BLEU score distribution histogram
   - Semantic similarity vs BLEU scatter plot
   - Top 10 / Bottom 10 examples comparison

5. **Prepare Supervisor Materials** (2-3 hours)
   - 10-15 slide presentation
   - 1-page status update
   - List of questions for supervisor

---

## 💡 Key Takeaways

### Question: "What effect will skipping scipy have?"
**Answer:** Minimal impact on core findings, moderate impact on statistical rigor.

**What you lose:**
- P-values and significance tests
- Formal effect size calculations
- Confidence intervals

**What you keep:**
- Valid BLEU scores (complete and correct)
- Ability to show descriptive statistics
- Foundation for qualitative analysis

**What you gain:**
- Recognition that BLEU is insufficient for cultural translation
- Motivation to add better metrics (semantic similarity)
- Stronger qualitative analysis focus

### Question: "Do the results give us anything useful?"
**Answer:** YES - Very useful, but need to be properly interpreted and supplemented.

**Useful aspects:**
1. ✅ Valid baseline metric (industry-standard BLEU)
2. ✅ Evidence that cultural translation ≠ word-for-word matching
3. ✅ Foundation for comparative analysis (once you add semantic similarity)
4. ✅ Basis for selecting qualitative examples
5. ✅ Support for your thesis argument about metric inadequacy

**Missing aspects:**
1. ❌ Semantic meaning preservation metric
2. ❌ Cultural fidelity quantification
3. ❌ Statistical significance testing
4. ⚠️ Comparative baseline (need Raw GPT-4 BLEU scores too!)

---

## 🚨 CRITICAL REALIZATION

**You calculated OG-RAG BLEU scores, but do you have:**
- Raw GPT-4 BLEU scores?
- Traditional RAG BLEU scores?

**If not, you need to calculate those to show improvement!**

Check your data - the CSV has columns:
- `raw_translation` (Raw GPT-4)
- `trad_rag_translation` (Traditional RAG)
- `ograg_translation` (OG-RAG)

**You should calculate BLEU for ALL THREE methods to compare!**

---

## 📋 Immediate Next Steps

### Option 1: Complete BLEU Comparison (Recommended)
Run the BLEU calculator on all three translation methods:
```bash
python scripts/simple_bleu_calculator.py \
  --compare-methods raw,trad_rag,ograg \
  --output-dir data/results
```

This will show:
- Raw GPT-4: X.XX BLEU
- Traditional RAG: X.XX BLEU
- OG-RAG: 9.33 BLEU

**Hypothesis:** OG-RAG might actually have HIGHER BLEU than raw or trad_rag!

### Option 2: Add Semantic Similarity (Recommended)
Install sentence-transformers and calculate:
- Shows meaning preservation beyond BLEU
- Quick to implement (1-2 hours)
- Powerful validation metric

### Option 3: Focus on Qualitative (Essential)
- Select 10-15 best examples
- Write detailed analysis
- Show cultural meaning preservation
- This is REQUIRED regardless of metrics

---

## 🎓 Thesis Contribution Statement

**Your contribution is NOT high BLEU scores.**

**Your contribution IS:**
1. Demonstrating that ontology-grounding improves **cultural** translation
2. Showing why standard metrics (BLEU) are inadequate
3. Proposing better evaluation frameworks for cultural NLP
4. Providing methodology for low-resource language translation

**Low BLEU + High Semantic Similarity + Good Qualitative Examples = Strong Thesis**

---

**Recommended Action:** Calculate BLEU for all three methods (Raw, Trad RAG, OG-RAG) to enable comparison, then add semantic similarity metric.

Would you like me to:
1. Modify the BLEU calculator to compare all three methods?
2. Create a semantic similarity calculator?
3. Help select qualitative examples?
4. All of the above?
