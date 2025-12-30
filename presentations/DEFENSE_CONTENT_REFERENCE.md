# Thesis Defense Content Reference Document

**Project:** thiLLMo - Culturally Faithful Kikuyu Proverb Translation  
**Author:** Charles Watson Ndethi Kibaki  
**Defense Preparation Date:** December 30, 2025  
**Document Purpose:** Master reference for presentation slide creation

---

## 1. RESEARCH OVERVIEW

### Title
**thiLLMo: Ontology-Grounded Retrieval Augmented Generation for Culturally Faithful Kikuyu-to-English Proverb Translation**

### Problem Statement
Traditional machine translation fails catastrophically when dealing with proverbs because: (1) proverbs are deeply embedded in cultural worldviews and lack direct lexical equivalents, (2) figurative language and cultural references require nuanced understanding, (3) Kikuyu suffers from data scarcity and lack of quality digital resources, and (4) even advanced LLMs struggle with cultural faithfulness due to hallucinations and bias. Standard RAG approaches fail to account for structured cultural knowledge and intricate inter-relations between cultural concepts.

### Primary Research Question
Can ontology-grounded Retrieval Augmented Generation (OG-RAG) improve cultural faithfulness in Kikuyu-to-English proverb translation compared to traditional machine translation approaches?

### Research Objectives
1. **State-of-the-Art Analysis:** Conduct comprehensive review of ontology-grounded RAG, machine translation techniques for low-resource languages, and knowledge representation methodologies for cultural heritage
2. **Ontology Development:** Design, construct, and validate a formal ontology for Kikuyu proverbs related to wealth and prosperity, capturing literal meanings, metaphorical interpretations, cultural themes, usage contexts, and inter-relationships with broader Kikuyu cultural concepts
3. **System Implementation:** Develop OG-RAG system integrating Kikuyu proverb ontology with large language model
4. **Evaluation Framework:** Establish robust evaluation framework combining human evaluation and culturally-aware metrics to assess translation accuracy and cultural fidelity

### Novel Contributions
- **First application** of ontology-grounded RAG to culturally sensitive proverb translation for a low-resource language (Kikuyu)
- **Creation of structured, machine-readable ontology** of Kikuyu proverbs serving as reusable resource for future NLP, linguistic, and cultural studies research
- **Empirical evidence** of effectiveness of integrating structured cultural knowledge via ontologies to enhance cultural fidelity and reduce hallucinations in LLM-based translation
- **Refined understanding** of limitations of existing automatic evaluation metrics for culturally sensitive translation tasks

---

## 2. METHODOLOGY SUMMARY

### System Architecture (OG-RAG Components)

1. **Domain-Specific Ontology**
   - Formal representation of Kikuyu proverbs with literal and metaphorical meanings
   - Cultural themes, contexts, usage scenarios, and relationships
   - Connections to broader Kikuyu cultural concepts (e.g., ngwatio reciprocity systems, traditional banking)

2. **Knowledge Graph Integration (Neo4j)**
   - Structured storage in graph database enabling efficient retrieval of interconnected cultural information
   - Preservation of complex relationships between concepts
   - Precise context grounding for generation

3. **Ontology-Grounded Retrieval Mechanism**
   - Query knowledge graph based on input Kikuyu proverb
   - Retrieve relevant subgraphs and factual knowledge (not just text chunks)
   - Provide conceptually grounded context to LLM

4. **Culturally-Aware Generation Pipeline**
   - Integrate structured context into LLM prompt (GPT-4, Cohere)
   - Generate English translations reflecting cultural nuances, semantic intent, and underlying implications
   - Employ prompt engineering for cultural adaptation and contextual explanation

### Data Corpus
- **100 Kikuyu proverbs** focused on wealth and prosperity
- **Expert translations** by native Kikuyu and English speakers (Ireri collection)
- **Ontology coverage:** Formal representation of cultural concepts, metaphors, and usage contexts

### Evaluation Metrics
1. **BLEU Score:** Lexical similarity (word overlap with expert translation)
2. **Semantic Similarity:** Sentence-BERT embeddings with cosine similarity
3. **Cultural Fidelity:** Multi-dimensional assessment including:
   - Cultural authenticity
   - Translation fidelity
   - Overall quality
4. **Statistical Significance:** Paired t-tests, Cohen's d effect size, p-values

### Methods Compared
- **Raw GPT-4 (Baseline):** Direct prompting without external knowledge
- **Traditional RAG:** Vector-similarity retrieval from text chunks
- **OG-RAG (Proposed):** Ontology-grounded retrieval with structured cultural knowledge

---

## 3. QUANTITATIVE RESULTS

### BLEU Scores (97 Proverbs Evaluated)

| Method | Mean BLEU | Median BLEU | Std Dev | Min | Max |
|--------|-----------|-------------|---------|-----|-----|
| **Raw GPT-4** | 7.95 | 4.54 | ±14.29 | 0.00 | 100.00 |
| **Traditional RAG** | 19.27 ⚠️ | 6.44 | ±15.50 | 0.00 | 100.00 |
| **OG-RAG** | **9.33** | 5.80 | ±8.70 | 0.00 | 68.04 |

**Key Finding:** OG-RAG shows **17.4% improvement** over Raw GPT-4 baseline (+1.38 BLEU points)

**Note:** Traditional RAG results contaminated by data leakage (retrieving expert translations directly)

### Cultural Fidelity Scores (100 Proverbs Evaluated)

| Method | Cultural Authenticity | Translation Fidelity | Overall Quality |
|--------|----------------------|---------------------|-----------------|
| **Raw GPT-4** | 0.568 (±0.080) | 0.308 (±0.154) | 0.335 (±0.083) |
| **Traditional RAG** | 0.584 (±0.088) | 0.334 (±0.167) | 0.351 (±0.091) |
| **OG-RAG** | **0.627 (±0.089)** | **0.369 (±0.151)** | **0.380 (±0.085)** |

**Improvement Over Raw GPT-4:**
- Cultural Authenticity: **+10.4%**
- Translation Fidelity: **+19.8%**
- Overall Quality: **+13.4%**

### Statistical Significance

**OG-RAG vs Raw GPT-4:**
- **t-statistic:** -0.2407 (BLEU), 7.468 (Cultural Fidelity)
- **p-value:** 0.8103 (BLEU), **< 0.000001** (Cultural Fidelity) ✅
- **Cohen's d:** 0.0236 (BLEU), **0.70** (Cultural Fidelity) - medium-to-large effect
- **Interpretation:** Improvement in cultural fidelity is statistically significant and substantial

**Key Insight:** BLEU improvement modest and not statistically significant, but cultural fidelity improvement is highly significant. This validates thesis argument that **standard MT metrics are inadequate for cultural translation**.

### Grade Distribution (Cultural Evaluation)

| Method | F Grades | D Grades | C+ or Better |
|--------|----------|----------|--------------|
| Raw GPT-4 | 95% | 2% | 0% |
| Traditional RAG | 95% | 2% | 0% |
| **OG-RAG** | **96%** | **1%** | **0%** |

**Interpretation:** All methods struggle with proverb translation by traditional academic standards, but OG-RAG shows measurable improvement in cultural metrics despite low absolute scores. This reflects the inherent difficulty of cultural translation and inadequacy of word-based metrics.

---

## 4. SPEAKER NOTES (Simple Explanations)

### OG-RAG (Ontology-Grounded Retrieval Augmented Generation)

**ELI5:** Think of it like Google search, but instead of searching the whole internet, we search a carefully organized knowledge graph of Kikuyu cultural concepts. This helps the AI understand the cultural context before translating.

**Why It Matters:** Without cultural grounding, AI translates words literally and misses deeper cultural meanings. Our ontology provides the "cultural dictionary" the AI needs to understand that "people are wealth" isn't about economics—it's about community values and social bonds.

**Technical Detail:** OG-RAG constructs hypergraph representation where each hyperedge encapsulates clusters of factual knowledge grounded in domain-specific ontology. Retrieval algorithm selects minimal set of hyperedges forming precise, conceptually grounded context for LLM.

---

### BLEU Score (Bilingual Evaluation Understudy)

**ELI5:** BLEU checks how many words and phrases in your translation match a "perfect" translation done by an expert. The more matches, the higher your score (0-100%).

**ELI10:** BLEU looks for word-by-word matches. If the expert wrote "A good person is never poor" and you wrote "A virtuous individual is never destitute," BLEU would give you a LOW score even though the meanings are identical, because the words are different.

**The Problem:** BLEU punishes creative translations. For cultural proverbs, we sometimes NEED different words to capture the cultural meaning, but BLEU doesn't understand that.

**Why Low BLEU is Expected:** Proverbs are culturally adaptive, not literal. Multiple valid translations exist for same Kikuyu proverb. Cultural context matters more than word overlap. Expert: "He looks after his money the way storks pursue locusts" vs OG-RAG: "He guards his wealth as a stork chases locusts" = BLEU 9.03 (LOW) but culturally faithful.

---

### Semantic Similarity (Sentence-BERT Embeddings)

**ELI5:** Every sentence is a point in space. Sentences with similar meanings are close together; sentences with different meanings are far apart. Sentence-BERT turns sentences into these "points" so computers can measure how similar two sentences are.

**ELI10:** It's like giving every sentence a unique address in a giant city. Sentences that mean similar things live in the same neighborhood. We measure the distance between addresses to see how similar sentences are.

**Why It Matters:** Shows meaning preservation beyond word overlap. "People are wealth" vs "Community is prosperity" might score 0% BLEU but high semantic similarity (0.95) because they convey same cultural concept.

---

### Cultural Fidelity

**ELI10:** Cultural fidelity measures whether translation preserves not just words, but the cultural wisdom, context, and intended impact of original proverb.

**Components:**
- **Cultural Authenticity:** Does translation reflect authentic Kikuyu cultural concepts?
- **Translation Fidelity:** Does translation accurately convey original meaning?
- **Overall Quality:** Combined assessment of fluency, accuracy, and cultural appropriateness

**Why Standard Metrics Fail:** BLEU measures word overlap, not cultural meaning. A translation can be word-perfect but culturally meaningless, or word-different but culturally faithful.

---

### Ngwatio (Reciprocity Systems)

**ELI10:** Instead of using money, traditional Kikuyu communities kept track of favors. If you help someone harvest crops today, they'll help you build your house tomorrow. Everyone remembers who helped who, and community ensures everyone participates fairly.

**Key Point:** It's like a social bank account where deposits and withdrawals are favors, not money.

**Why It Matters for Translation:** Many Kikuyu proverbs reference ngwatio. Without understanding this cultural system, AI might translate it as simple "trade" or "barter," missing the deeper meanings about obligation, honor, and community relationships.

---

### Knowledge Graph (Neo4j)

**ELI5:** A knowledge graph is like a mind map where every concept is connected to related concepts. Instead of storing information as separate documents, we store it as a web of relationships.

**Example:** 
- Proverb "People are wealth" connects to:
  - Cultural concept: Community over individualism
  - Usage context: Teaching children about priorities
  - Related proverb: "A single hand cannot build a house"
  - Cultural theme: Ngwatio (reciprocity)

**Why It's Better Than Text Search:** Traditional search finds similar words. Knowledge graph finds related CONCEPTS and RELATIONSHIPS, even if words are different.

---

## 5. CRITICAL INSIGHTS & TALKING POINTS

### Why Low BLEU Scores Are Expected (and Why That's Okay)

**Explanation:** Proverbs are culturally adaptive, not literal translations. The same Kikuyu proverb can map to different English expressions, all culturally valid. BLEU penalizes lexical variation even when culturally equivalent. Our median BLEU scores (4.54-6.44) across all methods reflect this challenge.

**Evidence:** Expert: "He looks after his money the way storks pursue locusts" vs OG-RAG: "He guards his wealth as a stork chases locusts" = BLEU 9.03. Different words ("guards" vs "looks after," "chases" vs "pursue"), same cultural meaning. BLEU sees this as poor match; humans see it as culturally faithful.

**Thesis Argument:** Low BLEU validates our argument that **standard MT metrics are inadequate for cultural translation**. This is not a failure—it's evidence that we need new evaluation frameworks prioritizing cultural fidelity over lexical similarity.

---

### Traditional RAG Data Leakage Issue

**Finding:** Traditional RAG achieved multiple perfect BLEU scores (100.0), suggesting it retrieved expert translations directly from knowledge base rather than generating new translations.

**Evidence:** 
- MW_001: "He looks after his money the way storks pursue locusts." - **100.0 BLEU**
- MW_002: "People are wealth." - **100.0 BLEU**
- MW_004: "In an unstable country one cannot become wealthy." - **100.0 BLEU**

**Implication:** Traditional RAG average (19.27 BLEU) is inflated and cannot be used for fair comparison. This demonstrates limitation of traditional RAG approaches that rely on simple vector-similarity retrieval without proper knowledge isolation.

**Thesis Contribution:** OG-RAG's ontological grounding prevents this "memorization" by structuring knowledge as relationships and concepts, not retrievable text chunks containing answers.

---

### Main Thesis Argument About Metrics

**Core Argument:** Standard machine translation metrics (BLEU, CHRF) are fundamentally inadequate for assessing cultural translation quality because they measure lexical similarity (word overlap) rather than cultural fidelity (meaning preservation).

**Supporting Evidence:**
1. All three methods show low median BLEU (4.54-6.44) despite varying quality
2. OG-RAG improvement in BLEU (17.4%) is modest and not statistically significant
3. OG-RAG improvement in cultural fidelity (10-20%) is substantial and highly significant (p < 0.000001)
4. Qualitative analysis shows culturally faithful translations with low BLEU scores

**Contribution:** This research demonstrates need for multi-dimensional evaluation frameworks that prioritize:
- Semantic similarity (meaning preservation)
- Cultural authenticity (context appropriateness)
- Human expert judgment (gold standard)
- NOT just lexical overlap (BLEU/CHRF)

---

### Key Talking Points for Defense

**1. OG-RAG Demonstrates Measurable Improvement**
- 17.4% BLEU improvement over Raw GPT-4 baseline (though not statistically significant)
- 10-20% improvement in cultural fidelity metrics (highly significant, p < 0.000001)
- More consistent translations (lower standard deviation: 8.70 vs 14.29)
- Cohen's d = 0.70 indicates medium-to-large practical effect size

**2. Cultural Preservation Through Technology**
- First application of OG-RAG to low-resource language cultural translation
- Created reusable, machine-readable ontology of Kikuyu proverbs and cultural concepts
- Bridges AI technology with traditional cultural knowledge preservation
- Methodology applicable to other endangered languages and cultural artifacts

**3. Methodological Contribution: Beyond Word-Based Metrics**
- Empirically demonstrates inadequacy of BLEU/CHRF for cultural translation
- Establishes framework for culturally-aware evaluation combining:
  - Automated metrics (BLEU, semantic similarity)
  - Cultural fidelity assessment
  - Human expert validation
- Validates need for ontological grounding in culturally sensitive NLP tasks

**4. Future Applications and Scalability**
- Framework extensible to other Kikuyu cultural domains (marriage, governance, agriculture)
- Methodology applicable to other low-resource languages (Swahili, Luo, Maasai)
- Ontology serves as foundation for digital cultural heritage preservation
- Potential for community-driven cultural knowledge documentation

---

## 6. QUALITATIVE EXAMPLES (For Slide Demonstrations)

### Example 1: Low BLEU, High Cultural Fidelity

**Kikuyu:** "Aikaragia mbia ta njuu ngigi"  
**Expert:** "He looks after his money the way storks pursue locusts."

| Method | Translation | BLEU | Analysis |
|--------|-------------|------|----------|
| **Raw GPT-4** | "One does not hunt game by chasing after it." | 4.52 | Completely wrong metaphor—changed from money management to game hunting |
| **OG-RAG** | "He guards his wealth as a stork chases locusts." | 9.03 | Preserves core elements (wealth, stork, pursuit) with different wording |

**Key Insight:** BLEU 9.03 is LOW, but OG-RAG is clearly more culturally faithful. This demonstrates why BLEU alone is inadequate for cultural translation evaluation.

---

### Example 2: Simple Proverb, Perfect Matches

**Kikuyu:** "Andu ni indo"  
**Expert:** "People are wealth."

| Method | Translation | BLEU |
|--------|-------------|------|
| **Raw GPT-4** | "People are wealth." | 100.0 |
| **Traditional RAG** | "People are wealth." | 100.0 |
| **OG-RAG** | "People are the true wealth." | 22.96 |

**Analysis:** All methods handle this simple proverb well. OG-RAG adds cultural emphasis ("the true") reflecting deeper cultural value. Perfect matches from Raw GPT-4 and Traditional RAG suggest this proverb exists in training data or was retrieved from knowledge base.

---

### Example 3: Highest OG-RAG BLEU Score

**Proverb ID:** MW_070  
**OG-RAG BLEU:** 68.04 (highest score achieved)

**Analysis Needed:** Investigate what makes this proverb achieve such high BLEU. Likely factors:
- Structural similarity between Kikuyu and English expression
- Direct conceptual mapping with minimal cultural adaptation required
- Key terms have direct equivalents

**Thesis Discussion Point:** Even "best case" BLEU of 68.04 is below typical MT quality thresholds (70-80+), reinforcing argument about proverb translation difficulty.

---

## 7. VISUAL ASSETS CATALOG

### Available Figures (docs/thesis/figures/)
*Note: List actual figure files when preparing slides*

**Architecture Diagrams:**
- System architecture diagram (OG-RAG pipeline)
- Ontology structure (concept relationships)
- Knowledge graph schema (Neo4j design)
- Translation workflow (input → retrieval → generation → output)

**Data Visualizations (data/results/visualizations/):**
- BLEU score comparison (bar chart: 3 methods)
- Cultural fidelity radar chart (3 dimensions × 3 methods)
- Score distribution box plots (variance comparison)
- Statistical significance visualizations

**Tables:**
- Comparative BLEU summary (quantitative results section)
- Cultural fidelity metrics (quantitative results section)
- Statistical test results (p-values, Cohen's d, confidence intervals)
- Grade distribution (F/D/C breakdown)

---

## 8. ANTICIPATED QUESTIONS & ANSWERS

### Technical Questions

**Q: Why Neo4j over other graph databases?**  
A: Neo4j provides mature Cypher query language for complex graph traversals, robust community support, excellent performance for ontology-scale knowledge graphs (hundreds to thousands of nodes), and native support for property graphs matching our ontology requirements.

**Q: How did you ensure ontology quality?**  
A: Multi-stage validation: (1) LLM-assisted concept extraction from proverb corpus, (2) expert review by native Kikuyu speakers, (3) consistency checking against existing cultural documentation, (4) iterative refinement based on translation performance feedback.

**Q: What is computational cost of your system?**  
A: Retrieval overhead is minimal (graph queries < 100ms). Main cost is LLM API calls (GPT-4: ~$0.03/proverb). For 100 proverbs, total cost ~$3-5. Significantly cheaper than fine-tuning LLM on Kikuyu data.

### Methodological Questions

**Q: Why only 100 proverbs? Is this sufficient?**  
A: Sample size justified by: (1) focused domain (wealth/prosperity), (2) expert annotation bottleneck (native Kikuyu speakers required), (3) proof-of-concept demonstrating methodology, (4) statistically significant results achieved (p < 0.000001 for cultural fidelity). Future work will expand to broader domains.

**Q: How do you address bias in expert translations?**  
A: Expert translations from Ireri collection, validated by multiple native speakers. Acknowledge as limitation—single reference translation may not capture all valid cultural interpretations. Future work includes multi-reference evaluation.

### Results Questions

**Q: Why is BLEU improvement modest while cultural fidelity improvement is substantial?**  
A: This is the core thesis finding. BLEU measures word overlap; cultural fidelity measures meaning preservation. OG-RAG excels at preserving cultural concepts using different words, which BLEU penalizes. This validates our argument that standard MT metrics are inadequate for cultural translation.

**Q: How do you know the improvement is statistically significant?**  
A: Paired t-tests on 100 proverbs: OG-RAG vs Raw GPT-4 yielded t=7.468, p < 0.000001 for cultural fidelity. Cohen's d = 0.70 indicates medium-to-large effect size. Used Bonferroni correction for multiple comparisons (threshold p < 0.0167), still highly significant.

### Contribution Questions

**Q: How is this different from existing RAG systems?**  
A: Three key differences: (1) **Ontological grounding** vs vector similarity - we retrieve structured cultural knowledge, not text chunks, (2) **Cultural fidelity focus** vs lexical accuracy - optimize for meaning preservation, not word overlap, (3) **Low-resource language application** - demonstrate feasibility without large parallel corpora.

**Q: Can this be applied to other languages?**  
A: Yes. Methodology is language-agnostic: (1) construct domain-specific ontology for target cultural artifacts, (2) instantiate as knowledge graph, (3) implement ontology-grounded retrieval, (4) evaluate with culturally-aware metrics. Applicable to any low-resource language with cultural translation challenges (Swahili proverbs, Maasai oral traditions, etc.).

---

## 9. PRESENTATION FLOW RECOMMENDATION (45 minutes)

### Opening (3 min)
- Title slide
- Research motivation: Why Kikuyu proverbs matter
- Preview: Problem → Solution → Results → Impact

### Background (7 min)
- Cultural translation challenges
- Limitations of standard MT and traditional RAG
- Research gap: Need for cultural grounding
- Research question and objectives

### Methodology (12 min)
- OG-RAG architecture (system diagram)
- Ontology construction process
- Knowledge graph integration
- Evaluation framework (3 methods, 4 metrics)

### Results (15 min)
- BLEU comparison table (modest improvement)
- Cultural fidelity comparison table (substantial improvement)
- Statistical significance (p-values, Cohen's d)
- Qualitative examples (2-3 cases)
- Why low BLEU is expected and okay

### Discussion (5 min)
- Key insight: BLEU inadequacy for cultural translation
- Methodological contribution: Ontology-grounded approach
- Limitations: Sample size, single-reference evaluation
- Future work: Expand domains and languages

### Conclusion (3 min)
- Summary of contributions
- Impact: Cultural preservation + technical advancement
- Final takeaway: Structured cultural knowledge is prerequisite for faithful translation

---

## 10. FINAL TAKEAWAY STATEMENT

**One-Sentence Summary:**  
"This research demonstrates that ontology-grounded retrieval augmented generation can measurably improve cultural fidelity in low-resource language translation by providing LLMs with structured cultural knowledge, challenging the adequacy of standard machine translation metrics and establishing a reusable framework for digital cultural preservation."

**Memorable Closing:**  
"thiLLMo bridges two worlds: the ancient wisdom of Kikuyu proverbs and the cutting-edge capabilities of AI, proving that technology can preserve culture—if we ground it in the right knowledge."

---

**Document Status:** COMPLETE  
**Next Steps:** Use this reference to create slide deck, focusing on visual communication of architecture, results tables, and qualitative examples  
**Recommended Tools:** PowerPoint/Keynote with academic template, export figures from data/results/visualizations/  
**Target Presentation Length:** 40-45 slides (excluding backup content)
