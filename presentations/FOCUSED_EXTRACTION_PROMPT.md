# Thesis Defense Content Extraction - Focused Prompt

## OBJECTIVE
Extract essential thesis content for defense presentation. Create a concise reference document covering: research overview, methodology, results, speaker notes, and key insights.

---

## SECTION 1: RESEARCH OVERVIEW

**Extract from:**
- `README.md`
- `docs/proposal/OPIT_RAI9001_Research_Proposal_v1.md`

**What to extract:**
1. Full thesis title
2. Research problem (2-3 sentences)
3. Primary research question
4. 3-4 main objectives
5. Novel contribution (1-2 sentences)

**Output format:**
```
### 1. RESEARCH OVERVIEW
**Title:** [exact title]
**Problem:** [problem statement]
**Research Question:** [main RQ]
**Objectives:** [numbered list]
**Contribution:** [contribution statement]
```

---

## SECTION 2: METHODOLOGY SUMMARY

**Extract from:**
- `README.md` (system architecture)
- `docs/proposal/OPIT_RAI9001_Research_Proposal_v1.md`

**What to extract:**
1. OG-RAG system components (3-4 points)
2. Corpus description
3. Evaluation metrics (3-4 metrics)
4. Methods compared

**Output format:**
```
### 2. METHODOLOGY
**System:** [3-4 component bullets]
**Data:** [corpus details]
**Metrics:** [metric list]
**Comparisons:** [methods compared]
```

---

## SECTION 3: QUANTITATIVE RESULTS

**Extract from:**
- `data/results/comparative_bleu_summary.json`
- `data/results/cultural_evaluation_summary.json`

**What to extract:**
1. BLEU scores table (3 methods: mean, median, std dev)
2. Cultural fidelity scores (3 methods: cultural authenticity, translation fidelity, overall quality)
3. OG-RAG improvement percentage over Raw GPT-4
4. Statistical significance (p-value, Cohen's d)

**Output format:**
```
### 3. RESULTS

**BLEU Scores (97 proverbs):**
[Table with exact numbers from JSON]

**Cultural Fidelity (100 proverbs):**
[Table with exact numbers from JSON]

**Key Finding:** [improvement statement]
**Significance:** [statistical test results]
```

---

## SECTION 4: SPEAKER NOTES

**Extract from:**
- `docs/thesis/PRESENTATION_GUIDE_ELI5.md`

**What to extract - ELI5 explanations for:**
1. OG-RAG
2. BLEU score
3. Semantic similarity
4. Cultural fidelity
5. Ngwatio (cultural concept)
6. Knowledge graph

**Output format:**
```
### 4. SPEAKER NOTES
**[Term]:**
ELI5: [simple explanation]
Why it matters: [relevance]
[Repeat for each term]
```

---

## SECTION 5: KEY INSIGHTS

**Extract from:**
- `docs/development/COMPARATIVE_BLEU_FINDINGS.md`
- `data/results/EVALUATION_RESULTS_SUMMARY.md`

**What to extract:**
1. Why low BLEU scores are expected (2-3 sentences)
2. Traditional RAG data leakage issue (1-2 sentences)
3. Main thesis argument about metrics (2-3 sentences)
4. 4 key talking points for defense

**Output format:**
```
### 5. CRITICAL INSIGHTS
**Low BLEU Explanation:** [why it's expected]
**Trad RAG Issue:** [data leakage finding]
**Thesis Argument:** [main argument]
**Talking Points:**
1. [Point 1]
2. [Point 2]
3. [Point 3]
4. [Point 4]
```

---

## INSTRUCTIONS

1. Read specified files only
2. Extract exact numbers from JSON files
3. Keep explanations concise (1-3 sentences)
4. Total output: 250-350 lines
5. Save as: `presentations/DEFENSE_CONTENT_REFERENCE.md`

**BEGIN EXTRACTION NOW**
