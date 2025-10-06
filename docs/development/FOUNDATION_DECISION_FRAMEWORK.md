# Foundation Decision Framework for OG-RAG Development

## Executive Summary

**Decision Point**: Which system should we build the cultural ontology enhancement on top of?

**Options**:
1. **NLLB-200** (Meta's specialized MT with native Kikuyu support)
2. **Raw LLM** (GPT-4/Cohere Aya - general multilingual AI)
3. **Google Translate** (commercial baseline)

---

## Decision Criteria Matrix

| Criterion | NLLB-200 | Raw LLM | Google Translate | Weight |
|-----------|----------|---------|------------------|--------|
| **Native Kikuyu Support** | ✅ Trained on Kikuyu data | ⚠️ Some Kikuyu knowledge | ❌ Not supported | 🔴🔴🔴 Critical |
| **Availability** | ⚠️ Needs API key (free) | ✅ Available now | ⚠️ Limited Kikuyu | 🟡🟡 Important |
| **Cost** | ✅ Free API | 💰 $0.01-0.05/proverb | ✅ Free (limited) | 🟢 Nice to have |
| **Speed** | ✅ ~1s/proverb | ⚠️ 3-5s/proverb | ✅ ~1-2s/proverb | 🟢 Nice to have |
| **Research Validity** | ✅✅✅ Best baseline | ✅✅ Good baseline | ⚠️ Weak baseline | 🔴🔴🔴 Critical |
| **Reproducibility** | ✅ Deterministic | ⚠️ Model updates | ✅ Stable | 🟡🟡 Important |

---

## Detailed Analysis

### Option 1: NLLB-200 (Specialized MT) ⭐ RECOMMENDED

#### Strengths
- **✅ NATIVE KIKUYU SUPPORT**: Only MT model actually trained on Kikuyu↔English parallel data
- **✅ Research Rigor**: Strongest possible baseline for scientific comparison
- **✅ Specialized Design**: Built specifically for low-resource languages like Kikuyu
- **✅ Clear Value Proposition**: "Even compared to specialized Kikuyu MT, our ontology adds value"
- **✅ Separation of Concerns**: MT handles translation, ontology handles culture
- **✅ Fast & Free**: ~1s per proverb via HF API (free tier with key)

#### Weaknesses
- **⚠️ Setup Required**: Needs HF API key (5 minutes to get free token)
- **⚠️ Less Explored**: Newer technology, less community support than OpenAI

#### Architecture
```
Input (Kikuyu) 
    ↓
NLLB-200 (Specialized MT Baseline)
    ↓
Base Translation (technical accuracy)
    ↓
Cultural Ontology Layer
    ↓
OG-RAG Enhanced Translation
    ↓
Output (Culturally-faithful English)
```

#### Research Value
- **Publication Impact**: "Compared against Meta's NLLB-200, specifically trained on Kikuyu..."
- **Gap Identification**: NLLB shows what specialized MT can do, ontology fills cultural gaps
- **Scientific Baseline**: Industry standard for low-resource MT evaluation

#### When to Choose NLLB
✅ Your research focuses on cultural enhancement **on top of** strong MT  
✅ You want the strongest possible baseline for comparison  
✅ You're willing to spend 5 minutes getting HF API key  
✅ You want to demonstrate ontology value clearly  
✅ Publication in MT/NLP conferences where NLLB is known  

---

### Option 2: Raw LLM (General AI)

#### Strengths
- **✅ Already Available**: Working now with OpenAI/Cohere credentials
- **✅ Cultural Awareness**: LLMs have broader world knowledge
- **✅ Flexible**: Can provide cultural reasoning, not just translation
- **✅ Proven**: Well-understood technology with community support
- **✅ Fallback**: Good alternative if NLLB unavailable

#### Weaknesses
- **⚠️ Not Specialized**: General purpose, not optimized for Kikuyu
- **⚠️ Weaker Baseline**: Less impressive to compare against
- **⚠️ Cost**: API costs for production use (~$0.01-0.05/proverb)
- **⚠️ Slower**: 3-5s per proverb vs NLLB's 1s
- **⚠️ Research Story**: "Better than general AI" is less compelling than "Better than specialized MT"

#### Architecture
```
Input (Kikuyu)
    ↓
Raw LLM (General AI Baseline)
    ↓
Base Translation (with some cultural awareness)
    ↓
Cultural Ontology Layer
    ↓
OG-RAG Enhanced Translation
    ↓
Output (Culturally-faithful English)
```

#### Research Value
- **Publication Impact**: Moderate - comparing against general AI
- **Gap Identification**: Harder to separate MT vs cultural enhancement
- **Scientific Baseline**: Less impressive but still valid

#### When to Choose Raw LLM
✅ NLLB setup is blocked/delayed  
✅ Need immediate development progress  
✅ Cost is not a concern  
✅ Prefer well-known, proven technology  
✅ Want LLM's broader reasoning capabilities  

---

### Option 3: Google Translate ❌ NOT RECOMMENDED

#### Issues
- **❌ No Kikuyu Support**: Doesn't officially support Kikuyu language
- **❌ Weak Baseline**: Inappropriate comparison for research
- **❌ Limited Value**: Can't demonstrate meaningful improvement

**Verdict**: Use only as reference, not as foundation.

---

## Strategic Recommendation

### 🎯 PRIMARY RECOMMENDATION: Build on NLLB-200

**Rationale:**

1. **Strongest Research Position**
   - "Even Meta's specialized Kikuyu MT model struggles with cultural nuances"
   - Clear demonstration of ontology's unique value
   - Publication-ready baseline comparison

2. **Best Separation of Concerns**
   ```
   NLLB handles:          Ontology handles:
   - Grammar              - Cultural meaning
   - Vocabulary           - Traditional wisdom
   - Syntax               - Business relevance
   - Literal meaning      - Community values
   ```

3. **Clear Value Proposition**
   - NLLB baseline: Technically accurate Kikuyu translation
   - OG-RAG adds: Cultural depth, traditional context, business wisdom
   - Gap is obvious and measurable

4. **Future-Proof**
   - NLLB is state-of-the-art for low-resource MT
   - Comparing against best-in-class is always defensible
   - If you beat NLLB, your contribution is clear

5. **Practical Benefits**
   - Fast (1s per proverb)
   - Free (with API key)
   - Reproducible
   - Native Kikuyu support

### 🔄 FALLBACK: Raw LLM if NLLB Blocked

If HF API key is blocked or you need immediate progress, Raw LLM is acceptable:
- Still provides valid baseline
- Already working in your system
- Can switch to NLLB later for final evaluation

---

## Implementation Roadmap

### Phase 1: Foundation Setup (This Week)

**If choosing NLLB (5 minutes):**
```bash
# 1. Get free HF API key
Visit: https://huggingface.co/settings/tokens
Click: "New token" → Read access → Create

# 2. Set environment variable
export HF_API_KEY='your_token_here'

# 3. Test integration
python scripts/test_nllb_integration.py

# 4. Generate 50-proverb baseline
python scripts/generate_50proverb_baseline.py
```

**If choosing Raw LLM (Already done):**
```bash
# Just run baseline
python scripts/generate_50proverb_baseline.py
```

### Phase 2: Gap Analysis (Next Week)

1. **Run Full Baseline** (200 proverbs)
   ```bash
   python src/evaluation/baseline_translation_system.py
   ```

2. **Analyze Failures**
   - Where does chosen foundation fail?
   - What cultural elements are missing?
   - What patterns emerge?

3. **Document Gaps**
   - Create gap analysis report
   - Prioritize ontology requirements
   - Design ontology structure

### Phase 3: Ontology Development (Weeks 3-4)

1. **Design Ontology Schema**
   - Based on identified gaps
   - Focus on cultural concepts missing from baseline
   - Include business wisdom connections

2. **Populate Ontology**
   - Use expert translations as ground truth
   - Encode cultural meanings
   - Link traditional wisdom to business concepts

3. **Integration Testing**
   - Build OG-RAG on chosen foundation
   - Test ontology enhancement
   - Measure improvement over baseline

### Phase 4: Evaluation (Week 5)

1. **Quantitative Metrics**
   - BLEU, METEOR, BERTScore
   - Cultural fidelity scores
   - Business relevance ratings

2. **Qualitative Analysis**
   - Expert review
   - LLM-as-a-Judge evaluation
   - Cultural authenticity assessment

3. **Comparative Analysis**
   - OG-RAG vs Foundation baseline
   - Statistical significance testing
   - Publication-ready results

---

## Decision Tree

```
START: Choose OG-RAG Foundation
│
├─ Can you get HF API key? (5 mins)
│  │
│  ├─ YES → Choose NLLB-200 ✅ BEST OPTION
│  │       Benefits: Strongest baseline, native Kikuyu, research rigor
│  │
│  └─ NO → Why not?
│      │
│      ├─ Organizational policy → Use Raw LLM (fallback)
│      │
│      └─ Just haven't done it → Get key! It's free and takes 5 mins
│
└─ Need immediate progress?
   │
   ├─ YES → Start with Raw LLM, switch to NLLB later
   │
   └─ NO → Get HF key, use NLLB for best results
```

---

## Conclusion

### 🏆 FINAL RECOMMENDATION

**Use NLLB-200 as OG-RAG foundation** because:

1. ✅ It's the **only MT model with native Kikuyu training**
2. ✅ Provides **strongest possible baseline** for research
3. ✅ **Clear separation**: MT handles translation, ontology handles culture
4. ✅ **Best publication story**: "Better than specialized Kikuyu MT"
5. ✅ **Fast and free** with simple API key setup

### Next Action

```bash
# Option A: Get HF key (5 minutes) → Use NLLB
Visit: https://huggingface.co/settings/tokens
export HF_API_KEY='your_token'
python scripts/generate_50proverb_baseline.py

# Option B: Immediate progress → Use Raw LLM
python scripts/generate_50proverb_baseline.py
# (System will use Raw LLM if NLLB unavailable)
```

---

**Decision Made**: _______________ (NLLB-200 / Raw LLM)

**Date**: October 6, 2025

**Rationale**: _______________________________________________

**Next Steps**: _______________________________________________
