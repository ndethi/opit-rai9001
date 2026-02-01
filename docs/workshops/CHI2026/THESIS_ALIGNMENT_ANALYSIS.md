# CHI2026 Workshop Paper - Thesis Alignment Analysis

**Date:** February 1, 2026  
**Prepared for:** AI Across Cultures @ CHI 2026 Workshop  
**Project:** thiLLMo - Culturally Faithful Kikuyu Proverb Translation

---

## Purpose

This document analyzes the alignment between:
1. The CHI2026 workshop paper submission
2. The final thesis (defended January 14, 2026)
3. The workshop call for participation themes

---

## Workshop Call Alignment

### Workshop Key Questions
The CHI2026 workshop focuses on:

1. **How can AI be adapted to support indigenous languages and cultural contexts?**
   - ✅ **thiLLMo Direct Answer:** OG-RAG system for Kikuyu proverb translation
   - Demonstrates ontology-based approach for low-resource language AI

2. **What sociotechnical frameworks are needed to align AI with diverse cultural values?**
   - ✅ **thiLLMo Contribution:** Formal cultural ontology capturing Kikuyu concepts
   - Knowledge graph integrating cultural themes, values, and practices

3. **How can participatory design reshape AI development?**
   - ⚠️ **Limitation:** No formal community participatory design process
   - Expert translations used but limited community involvement documented

4. **What evaluation practices ensure cultural respect?**
   - ✅ **thiLLMo Innovation:** Culturally-aware evaluation metrics
   - Automated cultural authenticity assessment framework
   - ⚠️ **Gap:** No formal human evaluation with community members (proposed for future)

### Workshop Themes Alignment

| Workshop Theme | thiLLMo Alignment | Evidence |
|----------------|-------------------|----------|
| **Cultural Adaptation of AI** | ✅ Strong | OG-RAG architecture, cultural ontology |
| **Participatory Design** | ⚠️ Limited | Expert-sourced translations, no documented community co-design |
| **Evaluation & Assessment** | ✅ Strong | Custom cultural metrics, automated evaluation framework |
| **Policy & Governance** | ⚠️ Not Addressed | No explicit policy framework discussed |

---

## Proverb Dataset Consistency

### Thesis Evaluation Dataset
- **Total Proverbs:** 100 (MW_001 to MW_100)
- **Focus:** Wealth and prosperity themes
- **Source:** "1000 Kikuyu Proverbs" + Margaret Wambere Ireri's collection
- **Evaluation:** All 100 proverbs across 3 systems (Raw GPT-4, Trad RAG, OG-RAG)

### Key Proverbs for Workshop Paper

For the CHI2026 paper, recommended proverbs that demonstrate cultural translation challenges:

#### 1. **MW_001: Aikaragia mbia ta njuu ngigi**
- **Expert Translation:** "He looks after his money the way storks pursue locusts"
- **Cultural Meaning:** "Whoever has much always wants more"
- **OG-RAG Translation:** "He guards his wealth like a stork chasing locusts"
- **Why Include:** Strong metaphorical imagery, demonstrates cultural context preservation

#### 2. **MW_002: Andu ni indo**
- **Expert Translation:** "People are wealth"
- **Cultural Meaning:** Community over materialism
- **OG-RAG Translation:** "People are the true wealth"
- **Why Include:** Core Kikuyu cultural value, simple but profound

#### 3. **MW_006: Cia thuguri itiyuragia ikumbi**
- **Expert Translation:** "Bought things do not fill the granary"
- **Cultural Meaning:** "One must work hard to achieve wealth"
- **OG-RAG Translation:** "Purchased goods do not fill the barn"
- **Why Include:** Emphasizes self-reliance, agricultural cultural context

#### 4. **MW_014: Gutiri kiega kiumaga heega**
- **Expert Translation:** "There is nothing that is of worth, that is obtained from the comfort corner"
- **Cultural Meaning:** "Nothing of value is given on a silver platter"
- **OG-RAG Translation:** "There is no wisdom in hoarding wealth"
- **Why Include:** Shows translation divergence, cultural adaptation challenge

#### 5. **MW_019: Guthinga kurugite gutonga**
- **Expert Translation:** "Virtue is better than riches"
- **Cultural Meaning:** "Virtue is the only true nobility"
- **OG-RAG Translation:** "To sow is to know wealth"
- **Why Include:** Demonstrates metaphorical interpretation differences

---

## Translation Accuracy Verification

### Methodology
The thesis used **automated evaluation metrics**:

1. **Computational Cultural Metrics (60% weight)**
   - Sentence-BERT embeddings (semantic similarity)
   - ROUGE-L scores (n-gram overlap)
   - Cultural pattern matching (Kikuyu linguistic features)
   - Composite scoring

2. **LLM-as-Judge Assessment (Gemini 2.5 Pro)**
   - Cultural Faithfulness (40%)
   - Translation Accuracy (30%)
   - Business Relevance (20%)
   - Overall Fluency (10%)

### Key Results (from Chapter 5)

| System | Cultural Authenticity | Translation Fidelity | Overall Quality | Grade |
|--------|----------------------|---------------------|-----------------|-------|
| Raw GPT-4 | 0.568 ± 0.080 | 0.308 ± 0.154 | 0.335 ± 0.083 | F |
| Traditional RAG | 0.584 ± 0.088 | 0.334 ± 0.167 | 0.351 ± 0.091 | F |
| **OG-RAG** | **0.627 ± 0.089** | **0.369 ± 0.151** | **0.380 ± 0.085** | **F** |

**Statistical Significance:**
- OG-RAG vs Raw GPT-4: t = 7.468, p < 0.000001 ✅
- OG-RAG vs Trad RAG: t = 5.341, p < 0.000001 ✅

### Important Notes

⚠️ **Evaluation Limitations (from Thesis Chapter 5):**
- ALL metrics are **automated** (no formal human evaluation with multiple annotators)
- Informal qualitative review by researcher (native Kikuyu speaker)
- Should be interpreted as **preliminary** rather than definitive
- Future validation with community members proposed

---

## Recommendations for CHI2026 Paper

### Content Alignment
1. ✅ **Emphasize:** Ontology-grounded approach for cultural preservation
2. ✅ **Highlight:** Low-resource language challenges and solutions
3. ⚠️ **Address:** Limitations of automated evaluation
4. ⚠️ **Acknowledge:** Need for community-based participatory evaluation

### Key Messages for Workshop
1. **Cultural Context Matters:** OG-RAG significantly outperforms baseline approaches
2. **Knowledge Representation:** Formal ontologies capture cultural nuance better than unstructured retrieval
3. **Evaluation Gap:** Standard MT metrics fail for cultural translation - new frameworks needed
4. **Ethical Considerations:** Automated metrics cannot replace community validation

### Data Consistency
- ✅ Use proverbs from the 100-proverb evaluation dataset (MW_001 to MW_100)
- ✅ Cite exact translations from thesis results
- ✅ Use same statistical results (means, standard deviations, p-values)
- ⚠️ Be transparent about evaluation methodology limitations

### Workshop Positioning
Position thiLLMo as:
- **Case Study:** Practical implementation of culturally-grounded AI for indigenous language
- **Methodological Contribution:** Ontology-grounded RAG framework
- **Open Questions:** Need for community-led evaluation and participatory design

---

## Action Items

### For CHI2026 Paper Review
- [ ] Verify all proverb examples match thesis dataset (MW_001 to MW_100)
- [ ] Ensure translation scores match thesis Chapter 5 results exactly
- [ ] Check cultural explanations align with expert translations from thesis
- [ ] Confirm statistical significance values match thesis (t-values, p-values)
- [ ] Add explicit limitations section on automated evaluation

### For LaTeX Conversion
- [ ] Extract proverb examples from thesis dataset
- [ ] Include thesis results tables (Table 5.1, cultural metrics)
- [ ] Reference final thesis properly
- [ ] Align with ACM CHI 2026 workshop paper format

### For Workshop Presentation
- [ ] Prepare demo using actual thesis proverbs
- [ ] Show ontology structure (Neo4j visualization)
- [ ] Demonstrate translation quality differences (side-by-side)
- [ ] Address community validation as future work

---

## Conclusion

The thiLLMo thesis provides strong empirical evidence for ontology-grounded RAG in culturally faithful translation. The CHI2026 workshop paper should:

1. Use **exact proverb dataset** from thesis evaluation (100 proverbs)
2. Report **same statistical results** with full transparency
3. **Acknowledge limitations** of automated evaluation
4. Position as **case study** contributing to workshop themes
5. Propose **community-based validation** as critical next step

This alignment ensures integrity between thesis claims and workshop contribution while positioning thiLLMo as a valuable case for the "AI Across Cultures" discussion.
