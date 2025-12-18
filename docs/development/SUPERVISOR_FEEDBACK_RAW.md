# Supervisor Feedback - Raw Comments
**Date Received:** December 2024  
**Context:** Master's Thesis Review - thiLLMo OG-RAG System

---

## 1. The thesis is too long and too dense

**Issue:** The document is ~130 pages, and many chapters (especially Literature Review & Methodology) contain over-explaining and repetition. This affects readability and grading.

**What to reduce:**
- Remove excessive background text in Chapter 2 that does not directly support the research
- Shorten detailed summaries of external models
- Move long explanations (e.g., RAPTOR, MuSiQue benchmark discussions) to an appendix

---

## 2. The evaluation needs more clarity on: methodology, sample size, and scoring

**Issue:** In Chapter 5, the evaluation is described well, but missing critical details.

**Missing details:**
- Who were the annotators? How many? What cultural expertise? Were they trained?
- Inter-annotator agreement (Cohen's kappa or Krippendorff's alpha) - especially important because evaluation is subjective
- Definition of each metric (Cultural Authenticity, Translation Fidelity) - needs precise scoring rubrics

**Comment:** Right now the evaluation sounds strong but lacks transparency on how scoring was done.

---

## 3. A formal hypothesis statement is missing early in the thesis

**Issue:** The contribution claims improvements of 10.5% and 19.8% but nowhere in Chapter 1 is a formal hypothesis written.

**Required addition:**
Add something like:
- H1: Ontology-grounded RAG produces higher cultural authenticity scores than Traditional RAG and Raw LLMs
- H2: OG-RAG yields statistically significant improvements in translation fidelity

---

## 4. The Research Questions section references "Chapter ??"

**Issue:** This appears multiple times (RQ text and later references).

**Example:** "quantitative results demonstrated in Chapter ??"

**Action:** These placeholders must be fixed.

---

## 5. The Methodology section sometimes reads like a tutorial rather than a thesis

**Issue:** For instance, the explanation of CRISP-DM is too long and not focused on its adaptation.

**Reduce:**
- General textbook descriptions
- Step-by-step explanations that are not directly tied to research execution

**Increase:**
- Why CRISP-DM is an appropriate framework for this specific study
- What adaptations were necessary
- What parts were iterative

---

## 6. System Architecture (Chapter 4) needs diagrams

**Issue:** Given the technical complexity, at least two diagrams are necessary.

**Required diagrams:**
1. Overall OG-RAG architecture
2. Knowledge graph → retrieval → context → LLM flow

**Comment:** Currently chapter 4 is text-only, which reduces clarity.

---

## 7. The Conclusion should be more concise and less repetitive

**Issue:** Currently Chapter 7 re-explains multiple things from earlier chapters.

**The conclusion should focus on:**
- What was achieved
- What was learned
- What future work is essential

---

## Summary of Required Actions

| # | Issue | Severity | Action Required |
|---|-------|----------|-----------------|
| 1 | Length/density (130 pages) | High | Reduce to 90-100 pages, move content to appendix |
| 2 | Evaluation transparency | Critical | Add annotator details, IAA scores, scoring rubrics |
| 3 | Missing hypotheses | Critical | Add formal H1, H2 statements in Chapter 1 |
| 4 | Chapter placeholders | High | Fix all "Chapter ??" references |
| 5 | Methodology tutorial style | Medium | Condense CRISP-DM, focus on adaptation |
| 6 | Missing architecture diagrams | High | Add minimum 2 diagrams to Chapter 4 |
| 7 | Conclusion repetitive | Medium | Condense, remove redundancy |
