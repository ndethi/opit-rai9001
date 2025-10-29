# LLM Selection Decision Log - OG-RAG Implementation

**Date:** October 30, 2025  
**Decision Point:** Day 2 - OG-RAG System Development  
**Status:** ✅ RESOLVED

---

## Context

During OG-RAG implementation planning, we needed to decide which LLM to use for the ontology-grounded translation system, considering:

1. **Proposal recommendation:** Gemini 2.0 (cited from Hakka LRL study - 31% BLEU with RAG)
2. **Existing baseline:** GPT-4, Cohere Aya-23, NLLB-200, Google Translate
3. **Research aim:** Prove OG-RAG improves LLM cultural fidelity

---

## The Dilemma

### **Issue: Confounded Comparison**

If we use different LLMs for baseline vs OG-RAG:
```
❌ OG-RAG (Gemini + Ontology) vs Baseline (GPT-4)
   Problem: Can't separate effects of:
   - LLM difference (Gemini vs GPT-4)
   - Ontology grounding (our innovation)
```

### **Baseline Performance Data**

From gap analysis (100 Kikuyu proverbs):

| System | Failure Rate | Performance | Optimization |
|--------|--------------|-------------|--------------|
| GPT-4 (OpenAI) | 26% | ★★★★☆ | General purpose |
| Aya-23 (Cohere) | 70% | ★★☆☆☆ | LRL-optimized |
| Google Translate | 95% | ★☆☆☆☆ | Commercial MT |
| NLLB-200 | 98% | ☆☆☆☆☆ | Specialized MT |

**Key Finding:** GPT-4 significantly outperformed all systems, including LRL-optimized Aya-23 (44 percentage point gap)

---

## Options Considered

### **Option A: Use GPT-4 (Maintain Baseline Consistency)**

**Pros:**
- ✅ Clean experimental design (isolates ontology effect)
- ✅ Reuses existing baseline (saves 4 hours)
- ✅ Beats state-of-the-art = stronger scientific claim
- ✅ More impressive to examiners
- ✅ Proposal mentions GPT-4 as valid option

**Cons:**
- ⚠️ Doesn't test Gemini recommendation explicitly
- ⚠️ May miss LRL-specific synergies

### **Option B: Re-run Baseline with Gemini**

**Pros:**
- ✅ Honors proposal's Gemini citation
- ✅ Tests LRL optimization claim

**Cons:**
- ❌ 4 extra hours work (re-run 100 proverbs)
- ❌ Discards existing baseline data
- ❌ Near supervisor meeting deadline
- ❌ Additional API costs

### **Option C: Use Cohere Aya-23 (LRL-optimized)**

**Pros:**
- ✅ Matches LRL optimization narrative
- ✅ Baseline already exists

**Cons:**
- ❌ Weaker baseline (70% failure) = less impressive improvements
- ❌ Raises question: "Why not just use GPT-4?"
- ❌ Doesn't address best available system

### **Option D: Test Both GPT-4 and Gemini**

**Pros:**
- ✅ Most comprehensive evaluation
- ✅ Tests generalization across LLMs

**Cons:**
- ❌ Double the work (~10 hours)
- ❌ Double the API costs (~$2.50)
- ❌ Time constraints (supervisor meeting Oct 30)

---

## Decision: Use GPT-4 ✅

### **Rationale**

#### **1. Scientific Rigor**
- **Stronger claim:** "OG-RAG improves even the best-performing system"
- **Harder test:** If we beat GPT-4, we beat everything
- **Cleaner design:** Isolates ontology effect (only RAG type varies)

#### **2. Research Focus**
Our study compares **RAG strategies**, not LLM selection:
```
Comparison:
├─ Raw GPT-4 (no RAG, no ontology)
├─ GPT-4 + Traditional RAG (vector similarity)
└─ GPT-4 + OG-RAG (ontology-grounded) ← Our contribution
```

The Hakka study (proposal citation) compared **different LLMs**. We're comparing **ontology grounding methods**.

#### **3. Practical Impact**
- GPT-4 is what practitioners would use today
- Showing OG-RAG improves GPT-4 has immediate real-world value
- Demonstrates ontology addresses gaps that model improvements alone cannot solve

#### **4. Time Efficiency**
- GPT-4 baseline: ✅ Already complete (0 hours)
- Gemini baseline: 🔹 Would need 4+ hours
- Days until supervisor meeting: 0 (meeting today)

#### **5. Proposal Alignment**
From proposal (page 142):
> "A suitable Large Language Model will be selected, potentially an open-source model or a powerful commercial API **(e.g., Gemini 2.0, GPT-4)**"

Both options explicitly mentioned. GPT-4 is valid choice.

---

## Addressing Potential Concerns

### **Concern 1: "But the proposal cited Gemini?"**

**Response:**
The Hakka study cited in proposal used Gemini to show **RAG improves LLM performance**. We're testing the same principle with GPT-4. The core innovation (ontology-grounding) is independent of specific LLM choice.

**Proposal Write-Up:**
> "While Gemini 2.0 demonstrated superior performance for LRL translation in prior work (Hakka study, 31% BLEU), we selected GPT-4 to maintain consistency with our established baseline and enable clean isolation of the ontology-grounding effect. Future work should evaluate OG-RAG with Gemini to assess potential synergies."

### **Concern 2: "Is it fair to use GPT-4 vs LRL-optimized Aya-23?"**

**Response:**
Yes - we're comparing **ontology grounding methods**, not LLM types:
- Fair: Same LLM, different RAG strategies ✅
- Unfair: Different LLM + different RAG (can't separate effects) ❌

Additionally, Aya-23's 70% failure rate shows LRL optimization alone insufficient for cultural nuance, supporting our thesis that explicit cultural knowledge (ontology) is needed.

### **Concern 3: "Shouldn't we use an LRL-optimized model?"**

**Response:**
Baseline data shows GPT-4 (general) >> Aya-23 (LRL-optimized):
- GPT-4: 26% failure
- Aya-23: 70% failure (44pp worse!)

This suggests general model capability currently exceeds specialized LRL optimization for culturally nuanced tasks. Using GPT-4 represents the **best available alternative** that practitioners would choose today.

---

## Implementation Plan

### **OG-RAG System Architecture**

```
Component           Choice           Rationale
─────────────────────────────────────────────────────────
LLM                 GPT-4 Turbo      Maintain baseline consistency
Retrieval Strategy  Triple-hybrid    Concept + Weight + Semantic
Context Size        Top-5 proverbs   Balance richness/token limits
Test Set            30 → 100         Iterative validation (CRISP-DM)
```

### **Comparison Systems**

1. **Baseline (Raw GPT-4)** - No RAG, no ontology
   - Status: ✅ Complete (26% failure, 0.067 cultural fidelity)
   - Source: `data/results/baseline_translations/baseline_literal_proverb_100proverbs_deduped.csv`

2. **Traditional RAG** - GPT-4 + vector similarity retrieval
   - Status: 🔹 Need to implement
   - Purpose: Show generic RAG provides some improvement

3. **OG-RAG (Ours)** - GPT-4 + ontology-grounded retrieval
   - Status: 🔹 Need to implement
   - Purpose: Show ontology grounding maximizes cultural fidelity

### **Expected Improvements**

Based on OG-RAG literature (55% fact recall, 40% correctness improvement):

| Metric | Raw GPT-4 | Target OG-RAG | Improvement |
|--------|-----------|---------------|-------------|
| Failure Rate | 26% | <15% | -42% |
| Cultural Fidelity | 0.067 | >0.40 | +497% |
| Metaphor Preservation | 0.045 | >0.50 | +1011% |
| Semantic Similarity | 0.115 | >0.60 | +422% |

---

## Future Work

### **Post-Thesis Evaluation with Gemini**

After thesis submission, conduct comprehensive LLM comparison:

```
Track 1: GPT-4 Evaluation (Complete in thesis)
├─ Raw GPT-4
├─ GPT-4 + Traditional RAG
└─ GPT-4 + OG-RAG

Track 2: Gemini Evaluation (Future work)
├─ Raw Gemini 2.0
├─ Gemini + Traditional RAG
└─ Gemini + OG-RAG

Analysis:
- Compare cross-LLM generalization
- Assess LRL-optimized LLM + ontology synergies
- Validate ontology effect independent of LLM choice
```

This would:
1. Test proposal's Gemini hypothesis
2. Provide evidence for ontology generalization
3. Guide LLM selection for production deployment

---

## Sign-off

**Decision:** Use GPT-4 for OG-RAG implementation  
**Approved by:** Research team  
**Date:** October 30, 2025  
**Status:** ✅ FINAL

**Next Steps:**
1. Implement triple-strategy graph retriever
2. Build GPT-4 context formatting
3. Create OG-RAG translation pipeline
4. Run 30-proverb evaluation
5. Compare vs baseline and document improvements

---

## References

- Baseline Gap Analysis: `docs/baseline_gap_analysis.md`
- Proposal: `docs/proposal/OPIT_RAI9001_Research_Proposal_v1.md`
- Day 1 Completion: `docs/development/day_1_completion_summary.md`

---

*This decision log documents our LLM selection rationale for transparency and future reference.*
