# GitHub Copilot Prompt: Thesis Defense Content Extraction (Focused)

## OBJECTIVE
Extract key thesis content for defense presentation slides. Focus on essential elements: research question, methodology, results, and contributions. Prioritize clarity and conciseness.

## SCOPE
Extract from this thiLLMo (Kikuyu proverb translation) thesis repository:
1. Core findings and statistics from `data/results/`
2. Research objectives from `docs/proposal/` and `README.md`
3. Simplified explanations from `docs/thesis/PRESENTATION_GUIDE_ELI5.md`
4. System architecture overview from implementation files

## OUTPUT FORMAT
Create a concise reference document with 5 main sections (not the full presentation).

## OUTPUT FORMAT
Create a concise reference document with 5 main sections (not the full presentation).

---

## SECTION 1: RESEARCH OVERVIEW (Extract from README.md and proposal)

**What to extract:**
- Full thesis title
- Research problem in 2-3 sentences
- Primary research question
- 3-4 key objectives
- Novel contribution statement

**Sources:**
- `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/README.md`
- `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/docs/proposal/OPIT_RAI9001_Research_Proposal_v1.md`

**Format:**
```markdown
### 1. RESEARCH OVERVIEW
**Title:** [Extract exact title]
**Problem:** [Extract problem statement - 2-3 sentences]
**Research Question:** [Extract main RQ]
**Objectives:** 
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]
**Contribution:** [Extract novel contribution in 1-2 sentences]
```

---

## SECTION 2: METHODOLOGY SUMMARY (Extract from proposal and system architecture)

**What to extract:**
- OG-RAG system components (3-4 bullet points)
- Data: Corpus size and description
- Evaluation metrics used
- Comparison methods (Raw GPT-4, Traditional RAG, OG-RAG)

**Sources:**
- README.md (system architecture section)
- `docs/proposal/OPIT_RAI9001_Research_Proposal_v1.md` (methodology section)

**Format:**
```markdown
### 2. METHODOLOGY
**System Architecture:**
- [Component 1]
- [Component 2]
- [Component 3]

**Data:**
- Corpus: [X] Kikuyu proverbs on [topic]
- Expert translations: [description]

**Evaluation:**
- Metrics: [list 3-4 metrics]
- Methods compared: [list methods]
```

---

## SECTION 3: KEY RESULTS (Extract from data/results/)

**What to extract:**
- BLEU scores table (3 methods)
- Cultural fidelity scores (3 methods)
- Statistical significance findings
- Key improvement percentages

**Sources:**
- `data/results/comparative_bleu_summary.json`
- `data/results/cultural_evaluation_summary.json`
- `data/results/EVALUATION_RESULTS_SUMMARY.md`

**Format:**
```markdown
### 3. QUANTITATIVE RESULTS

**BLEU Scores (97 proverbs):**
| Method | Mean | Median | Std Dev |
|--------|------|--------|---------|
| Raw GPT-4 | [X.XX] | [X.XX] | [X.XX] |
| Traditional RAG | [X.XX] | [X.XX] | [X.XX] |
| OG-RAG | [X.XX] | [X.XX] | [X.XX] |

**Key Finding:** OG-RAG shows [X]% improvement over Raw GPT-4

**Cultural Fidelity (100 proverbs):**
| Method | Cultural Authenticity | Translation Fidelity | Overall Quality |
|--------|----------------------|---------------------|-----------------|
| Raw GPT-4 | [X.XX] | [X.XX] | [X.XX] |
| Traditional RAG | [X.XX] | [X.XX] | [X.XX] |
| OG-RAG | [X.XX] | [X.XX] | [X.XX] |

**Statistical Significance:** [Extract p-value and Cohen's d for OG-RAG vs Raw]
```

---

## SECTION 4: SPEAKER NOTES (Extract from PRESENTATION_GUIDE_ELI5.md)

**What to extract:**
- ELI5 explanations for 5-6 key technical terms
- ELI5 explanations for 2-3 cultural concepts
- Focus on terms likely to need explanation during defense

**Sources:**
- `docs/thesis/PRESENTATION_GUIDE_ELI5.md`

**Priority terms:**
1. OG-RAG (Ontology-Grounded RAG)
2. BLEU score
3. Semantic similarity
4. Cultural fidelity
5. Ngwatio (cultural concept example)
6. Knowledge graph

**Format:**
```markdown
### 4. SPEAKER NOTES (Simple Explanations)

**OG-RAG:**
ELI5: [Extract simplified explanation]
Why it matters: [Extract relevance]

**BLEU Score:**
ELI5: [Extract simplified explanation]
Limitation: [Extract why it's limited for cultural translation]

[Repeat for other terms...]
```

---

## SECTION 5: CRITICAL FINDINGS & TALKING POINTS

**What to extract:**
- Why BLEU scores are low (and why that's okay)
- Traditional RAG data leakage issue
- Main thesis argument about metrics
- 3-4 key talking points for defense

**Sources:**
- `docs/development/COMPARATIVE_BLEU_FINDINGS.md`
- `docs/development/TRADITIONAL_RAG_DATA_LEAKAGE_DECISION.md`
- `data/results/EVALUATION_RESULTS_SUMMARY.md`

**Format:**
```markdown
### 5. CRITICAL INSIGHTS & TALKING POINTS

**Why Low BLEU is Expected:**
[Extract 2-3 sentence explanation]

**Traditional RAG Issue:**
[Extract data leakage finding in 1-2 sentences]

**Main Thesis Argument:**
[Extract argument about inadequacy of standard MT metrics for cultural translation]

**Key Talking Points:**
1. [Point 1 - about OG-RAG improvement]
2. [Point 2 - about cultural preservation]
3. [Point 3 - about methodology contribution]
4. [Point 4 - about future applications]
```

---

## EXECUTION INSTRUCTIONS

1. **Read files in this order:**
   - README.md (overview)
   - data/results/comparative_bleu_summary.json (BLEU data)
   - data/results/cultural_evaluation_summary.json (cultural metrics)
   - docs/thesis/PRESENTATION_GUIDE_ELI5.md (speaker notes)
   - docs/development/COMPARATIVE_BLEU_FINDINGS.md (insights)

2. **Extract only what's specified** - don't add extra interpretation

3. **Use exact numbers** from JSON files

4. **Keep explanations concise** - 1-3 sentences per item

5. **Output as markdown** with clear section headers

6. **Total length target:** 300-400 lines (not thousands)

---

## OUTPUT FILE
Save as: `presentations/DEFENSE_CONTENT_REFERENCE.md`

---

## BEGIN EXTRACTION
Execute the focused extraction for these 5 sections only. Prioritize accuracy and conciseness over comprehensiveness.
**INSTRUCTION:** Conduct a comprehensive scan of the thesis repository and create a hierarchical content map.

**Execute the following Tree of Thoughts exploration:**

#### Branch 1: Core Thesis Documents
- [ ] Locate and analyze `docs/thesis/main.pdf` or `thiLLMo_Thesis_Revised_Dec2025.pdf`
- [ ] Extract chapter structure and section headings
- [ ] Identify research questions, hypotheses, and objectives
- [ ] Map theoretical framework and conceptual models
- [ ] Extract methodology description and justification
- [ ] Identify key findings from each results section
- [ ] Capture discussion points and theoretical implications
- [ ] Extract contribution to field statements
- [ ] Note limitations and future research directions

#### Branch 2: LaTeX Source Analysis (if available)
- [ ] Scan `docs/thesis/chapters/` for individual chapter files
- [ ] Extract all `\section{}`, `\subsection{}`, and `\subsubsection{}` titles
- [ ] Identify all `\begin{figure}` and `\begin{table}` environments
- [ ] Extract caption text for all figures and tables
- [ ] Locate all mathematical equations and their significance
- [ ] Identify key definitions (`\textbf{}` or definition environments)
- [ ] Extract all bullet points and enumerated lists
- [ ] Note all citations to key theoretical works

#### Branch 3: Supplementary Documentation
- [ ] Review `docs/proposal/` for original research design
- [ ] Analyze `docs/development/` for methodology evolution
- [ ] Examine `docs/ethics/` for ethical considerations
- [ ] Review `docs/workshops/` for presentation iterations
- [ ] Check `REVISION_SUMMARY.md` for key improvements made
- [ ] Review `PHASE1_COMPLETION_SUMMARY.md` for milestone achievements
- [ ] **EXTRACT `docs/thesis/PRESENTATION_GUIDE_ELI5.md`** for speaker notes and simplified explanations

---

### Phase 2: Visual Asset Extraction
**INSTRUCTION:** Identify, catalog, and extract ALL visual elements with contextual metadata.

**Apply Chain of Thought reasoning for each visual type:**

#### A. Figures and Diagrams
```
FOR EACH figure in docs/thesis/figures/:
  1. Capture file name and location
  2. Extract associated caption from LaTeX source
  3. Identify which chapter/section it appears in
  4. Determine the research question it addresses
  5. Note the key message the figure conveys
  6. Assess presentation suitability (complexity, clarity)
  7. Suggest presentation adaptation if needed
```

**Expected figure types:**
- [ ] System architecture diagrams (OG-RAG system design)
- [ ] Process flow diagrams (translation pipeline, evaluation workflow)
- [ ] Conceptual frameworks (ontology structure, cultural context model)
- [ ] Data flow diagrams (Neo4j graph relationships)
- [ ] Comparison diagrams (traditional RAG vs OG-RAG)

#### B. Data Visualizations
```
FOR EACH visualization in data/results/visualizations/:
  1. Identify chart type (bar, line, scatter, heatmap, etc.)
  2. Extract data source file
  3. Determine statistical measure displayed
  4. Identify comparison being made
  5. Note significance level if applicable
  6. Extract key insights visible in the chart
  7. Assess whether it supports a major claim
```

**Expected visualization categories:**
- [ ] BLEU score comparisons (Raw GPT-4 vs Trad RAG vs OG-RAG)
- [ ] Semantic similarity distributions
- [ ] Cultural fidelity metrics (metaphor preservation, context alignment)
- [ ] Statistical test results (p-values, effect sizes)
- [ ] Performance benchmarks
- [ ] Ontology coverage metrics

#### C. Tables and Data Summaries
```
FOR EACH table in:
  - Thesis chapters
  - data/results/*.csv
  - Evaluation reports
DO:
  1. Extract table title/description
  2. Identify column headers and row labels
  3. Determine if quantitative or qualitative
  4. Extract key numerical findings
  5. Identify highest/lowest/significant values
  6. Note comparison patterns
  7. Suggest condensed presentation version
```

**Priority tables to extract:**
- [ ] Comparative BLEU summary (comparative_bleu_summary.json)
- [ ] OG-RAG metrics summary (ograg_metrics_summary.csv)
- [ ] Cultural evaluation results (cultural_evaluation_summary.json)
- [ ] Statistical significance tests
- [ ] Ontology concept statistics
- [ ] Expert evaluation agreement scores

---

### Phase 3: Insight Crystallization
**INSTRUCTION:** Apply Chain of Thought reasoning to identify presentation-worthy insights.

#### A. Research Problem and Motivation
**Extract and synthesize:**
```
1. WHY does this research matter?
   - What gap in knowledge does it address?
   - What real-world problem does it solve?
   - Who benefits from this work?

2. WHAT is the research question?
   - Primary research question
   - Sub-questions or hypotheses
   - Scope and boundaries

3. HOW is this research novel?
   - What hasn't been done before?
   - What makes OG-RAG different?
   - What is the theoretical contribution?
```

**Source locations:**
- `docs/thesis/chapters/chapter1_introduction.tex`
- `docs/proposal/research_proposal.md`
- Thesis abstract and introduction sections

#### B. Methodological Contributions
**Extract innovation points:**
```
FOR EACH methodological component:
  1. Identify the traditional approach
  2. Explain the OG-RAG innovation
  3. Justify why the innovation matters
  4. Quantify the improvement (if applicable)

COMPONENTS TO ANALYZE:
- Ontology-grounded retrieval mechanism
- Cultural context integration
- Kikuyu proverb domain modeling
- Neo4j graph database design
- Translation evaluation framework
- Multi-dimensional metrics (BLEU + semantic + cultural)
```

**Source locations:**
- `docs/thesis/chapters/chapter3_methodology.tex`
- `src/og-rag-system/` architecture
- `scripts/ontology_builder.py` implementation
- `docs/ontology/` design documents

#### C. Key Empirical Findings
**Extract with statistical rigor:**
```
FOR EACH major finding:
  1. STATE the finding in one sentence
  2. QUANTIFY with specific numbers
  3. PROVIDE statistical significance (p-value, CI)
  4. CONTEXTUALIZE against baseline/literature
  5. EXPLAIN the practical implication

PRIORITY FINDINGS:
- OG-RAG vs Raw GPT-4 improvement (BLEU, semantic similarity)
- OG-RAG vs Traditional RAG comparison
- Cultural fidelity scores
- Ontology coverage and concept linkage
- Expert evaluation agreement
- Statistical significance of improvements
```

**Source locations:**
- `data/results/EVALUATION_RESULTS_SUMMARY.md`
- `data/results/comparative_bleu_summary.json`
- `data/results/cultural_evaluation_summary.json`
- `data/results/ograg_metrics_summary.json`
- `docs/thesis/chapters/chapter4_results.tex`

#### D. Theoretical and Practical Implications
**Synthesize contribution statements:**
```
THEORETICAL CONTRIBUTIONS:
- How does OG-RAG advance RAG research?
- What does it reveal about cultural translation?
- How does it bridge NLP and cultural preservation?

PRACTICAL APPLICATIONS:
- Who can use this system? (linguists, cultural researchers)
- What scenarios benefit? (low-resource languages, cultural heritage)
- How can it be extended? (other languages, other cultural artifacts)

LIMITATIONS AND FUTURE WORK:
- What are the constraints? (data size, language coverage)
- What questions remain unanswered?
- What are the next research directions?
```

**Source locations:**
- `docs/thesis/chapters/chapter5_discussion.tex`
- `docs/thesis/chapters/chapter6_conclusion.tex`
- Thesis limitations section

---

### Phase 4: Narrative Thread Development
**INSTRUCTION:** Synthesize extracted elements into coherent presentation storylines.

**Apply Self-Consistency validation by generating THREE narrative approaches:**

#### Narrative Approach 1: Problem-Solution Arc
```
OPENING: The Challenge of Cultural Translation
- Kikuyu proverbs are culturally rich but underserved
- Standard machine translation fails to preserve cultural meaning
- Existing RAG systems lack cultural grounding

SOLUTION: Ontology-Grounded RAG
- Novel approach integrating cultural ontology
- Neo4j graph database for semantic relationships
- Multi-dimensional evaluation framework

EVIDENCE: Measurable Improvements
- 17.4% BLEU improvement over baseline
- Higher semantic similarity scores
- Better cultural fidelity metrics

IMPACT: Advancing Cultural Preservation
- Framework for low-resource languages
- Bridge between AI and cultural heritage
- Foundation for future research
```

#### Narrative Approach 2: Methodological Innovation Arc
```
FOUNDATION: Literature and Gaps
- Traditional RAG limitations
- Cultural translation challenges
- Need for domain-specific grounding

INNOVATION: OG-RAG Architecture
- Ontology design and construction
- Graph-based retrieval mechanism
- Cultural context integration

VALIDATION: Empirical Evaluation
- Comparative benchmark (3 methods)
- Statistical significance tests
- Expert validation study

CONTRIBUTION: Novel Framework
- Reusable methodology
- Open-source implementation
- Extensible to other domains
```

#### Narrative Approach 3: Data-Driven Discovery Arc
```
OBSERVATION: Initial Hypothesis
- Can ontological grounding improve translation quality?
- Do cultural concepts enhance RAG retrieval?

EXPERIMENT: System Implementation
- 100 Kikuyu proverbs corpus
- Cultural ontology with X concepts
- Comparative translation pipeline

RESULTS: Empirical Evidence
- [BLEU scores table]
- [Semantic similarity comparison]
- [Cultural fidelity metrics]

INSIGHT: Validated Hypothesis
- Ontology improves retrieval precision
- Cultural context enhances translation quality
- Multi-metric evaluation reveals nuanced improvements
```

**INSTRUCTION:** Select the narrative approach that best fits committee expectations and time constraints.

---

## EXTRACTION DELIVERABLES SPECIFICATION

### Master Reference Document Structure

```markdown
# Thesis Defense Presentation - Master Reference Document

## 1. RESEARCH OVERVIEW
### 1.1 Title and Author
- [Full thesis title]
- [Author name, program, date]

### 1.2 Research Question
- [Primary research question]
- [Sub-questions]

### 1.3 Objectives
- [Enumerated list of research objectives]

### 1.4 Scope and Boundaries
- [What is included]
- [What is excluded]

---

## 2. PROBLEM STATEMENT
### 2.1 Contextual Background
- [Kikuyu language and proverb significance]
- [Cultural preservation challenges]
- [Machine translation limitations]

### 2.2 Research Gap
- [What existing research has done]
- [What is missing]
- [Why this gap matters]

### 2.3 Motivation
- [Real-world application]
- [Beneficiaries]
- [Broader impact]

**SLIDE RECOMMENDATION:** 2-3 slides
**VISUAL ASSETS:**
- [List relevant figures/diagrams]

---

## 3. LITERATURE REVIEW SYNTHESIS
### 3.1 Key Theoretical Foundations
- [RAG systems overview]
- [Cultural translation theory]
- [Low-resource NLP]

### 3.2 Related Work
- [Existing translation systems]
- [Ontology-based NLP]
- [Cultural computing]

### 3.3 Positioning This Research
- [How OG-RAG differs]
- [Novel contributions]

**SLIDE RECOMMENDATION:** 2-3 slides
**VISUAL ASSETS:**
- [Comparison table: Traditional RAG vs OG-RAG]
- [Research landscape diagram]

---

## 4. METHODOLOGY
### 4.1 System Architecture
**Description:** [Overview of OG-RAG system design]

**Components:**
1. Ontology Construction
   - [Number of concepts extracted]
   - [Ontology structure diagram]
   - [Neo4j graph database design]

2. Retrieval Mechanism
   - [Graph-based retrieval algorithm]
   - [Context ranking approach]

3. Translation Pipeline
   - [LLM integration (GPT-4, Cohere)]
   - [Prompt engineering strategy]

**VISUAL ASSETS:**
- FIGURE: System architecture diagram [docs/thesis/figures/...]
- FIGURE: Ontology structure [docs/thesis/figures/...]
- FIGURE: Translation pipeline flowchart

**SLIDE RECOMMENDATION:** 4-5 slides

### 4.2 Data Collection
- [Corpus description: 100 Kikuyu proverbs]
- [Expert translation process]
- [Data sources and validation]

**VISUAL ASSETS:**
- TABLE: Corpus statistics
- FIGURE: Data collection workflow

### 4.3 Evaluation Framework
**Metrics:**
1. BLEU Score (lexical similarity)
2. Semantic Similarity (sentence embeddings)
3. Cultural Fidelity (metaphor preservation, context alignment)

**Comparison Methods:**
- Raw GPT-4 (baseline)
- Traditional RAG
- OG-RAG (proposed method)

**VISUAL ASSETS:**
- TABLE: Evaluation metrics definitions
- FIGURE: Evaluation pipeline

**SLIDE RECOMMENDATION:** 2-3 slides

---

## 5. RESULTS
### 5.1 Quantitative Findings

#### 5.1.1 BLEU Score Comparison
**DATA SOURCE:** `data/results/comparative_bleu_summary.json`

| Method | Average BLEU | Median | Min | Max | Improvement |
|--------|--------------|--------|-----|-----|-------------|
| Raw GPT-4 | [X.XX] | [X.XX] | [X.XX] | [X.XX] | baseline |
| Traditional RAG | [X.XX] | [X.XX] | [X.XX] | [X.XX] | [+X%] |
| OG-RAG | [X.XX] | [X.XX] | [X.XX] | [X.XX] | [+X%] |

**KEY INSIGHT:** [One-sentence interpretation]

**STATISTICAL SIGNIFICANCE:** [p-value, confidence interval]

**VISUAL ASSETS:**
- CHART: Bar chart comparing average BLEU scores
- CHART: Box plot showing score distributions

#### 5.1.2 Semantic Similarity Results
**DATA SOURCE:** `data/results/semantic_similarity_summary.json`

[Extract similar table structure]

#### 5.1.3 Cultural Fidelity Metrics
**DATA SOURCE:** `data/results/cultural_evaluation_summary.json`

**Metaphor Preservation:** [Score and interpretation]
**Context Alignment:** [Score and interpretation]
**Overall Cultural Fidelity:** [Score and interpretation]

**VISUAL ASSETS:**
- CHART: Radar chart of cultural metrics
- CHART: Heatmap of per-proverb cultural scores

**SLIDE RECOMMENDATION:** 5-7 slides (results core)

### 5.2 Qualitative Findings
**INSTRUCTION:** Extract 2-3 exemplary proverb translations that demonstrate:
1. High cultural fidelity + low BLEU (shows metric limitation)
2. OG-RAG success case (clear improvement over baseline)
3. Challenging case (where all methods struggled)

**FORMAT FOR EACH EXAMPLE:**
```
PROVERB: [Kikuyu text]
EXPERT: [Expert translation]
RAW GPT-4: [Translation + BLEU score]
OG-RAG: [Translation + BLEU score + cultural fidelity score]
INSIGHT: [Why OG-RAG performed better/differently]
```

**SLIDE RECOMMENDATION:** 2-3 slides (qualitative examples)

---

## 6. DISCUSSION
### 6.1 Interpretation of Findings
- [Why did OG-RAG improve performance?]
- [What does this reveal about cultural translation?]
- [How do results align with hypothesis?]

### 6.2 Theoretical Contributions
1. [Contribution to RAG research]
2. [Contribution to cultural NLP]
3. [Contribution to low-resource language processing]

### 6.3 Practical Implications
- [Who can use this?]
- [What problems does it solve?]
- [How can it be deployed?]

### 6.4 Limitations
- [Data limitations (sample size, language coverage)]
- [Technical limitations (computation, model constraints)]
- [Methodological limitations (evaluation metrics)]

### 6.5 Future Research Directions
- [Extension to other languages]
- [Additional cultural artifact types]
- [Improved evaluation frameworks]

**SLIDE RECOMMENDATION:** 3-4 slides

---

## 7. CONCLUSION
### 7.1 Research Summary
- [Problem addressed]
- [Methodology employed]
- [Key findings]

### 7.2 Contributions to Field
- [Novel framework]
- [Empirical evidence]
- [Open-source implementation]

### 7.3 Final Takeaway
[One powerful concluding statement]

**SLIDE RECOMMENDATION:** 1-2 slides

---

## 8. APPENDICES FOR Q&A PREPARATION

### 8.1 Technical Deep-Dives
- [Neo4j schema details]
- [Ontology construction algorithm]
- [Prompt engineering examples]

### 8.2 Additional Statistical Tests
- [Full ANOVA results]
- [Post-hoc test results]
- [Effect size calculations]

### 8.3 Extended Examples
- [Full translation comparisons]
- [Error analysis]

### 8.4 Implementation Details
- [Code repository structure]
- [Deployment considerations]
- [Reproducibility notes]

**SLIDE RECOMMENDATION:** Backup slides (not in main presentation)

---

## 9. VISUAL ASSET CATALOG

### 9.1 Architecture Diagrams
- [ ] **File:** [path to system architecture diagram]
  - **Caption:** [full caption]
  - **Slide location:** Methodology Section
  - **Key message:** [what it demonstrates]

- [ ] **File:** [path to ontology structure diagram]
  - **Caption:** [full caption]
  - **Slide location:** Methodology Section
  - **Key message:** [what it demonstrates]

[Continue for all diagrams...]

### 9.2 Data Visualizations
- [ ] **File:** [path to BLEU comparison chart]
  - **Data source:** comparative_bleu_summary.json
  - **Chart type:** Bar chart
  - **Slide location:** Results Section
  - **Key insight:** [OG-RAG shows X% improvement]

[Continue for all visualizations...]

### 9.3 Tables
- [ ] **Table:** Comparative BLEU Summary
  - **Data source:** comparative_bleu_summary.json
  - **Format:** 3 columns × 5 rows
  - **Slide location:** Results Section
  - **Presentation adaptation:** [Highlight OG-RAG row]

[Continue for all tables...]

---

## 10. PRESENTATION NARRATIVE FLOW

### Recommended Structure (45-minute defense)

**OPENING (3 minutes)**
- Title slide
- Research question and motivation
- Preview of presentation structure

**BACKGROUND (7 minutes)**
- Problem statement
- Literature review synthesis
- Research gap and contribution

**METHODOLOGY (12 minutes)**
- OG-RAG architecture
- Ontology construction
- Evaluation framework
- Data collection

**RESULTS (15 minutes)**
- Quantitative findings (BLEU, semantic, cultural)
- Statistical significance
- Qualitative examples
- Key insights

**DISCUSSION (5 minutes)**
- Interpretation
- Limitations
- Future work

**CONCLUSION (3 minutes)**
- Summary of contributions
- Final takeaway
- Acknowledgments

**Q&A PREPARATION (backup content)**
- Technical deep-dives
- Additional analyses
- Implementation details

---

## 11. KEY TALKING POINTS AND SPEAKER NOTES

### 11.1 ELI5/ELI10 Concept Explanations
**DATA SOURCE:** `docs/thesis/PRESENTATION_GUIDE_ELI5.md`

**INSTRUCTION:** For each technical term and cultural concept, extract simplified explanations suitable for:
- Committee members from non-technical backgrounds
- Audience members unfamiliar with Kikuyu culture
- Quick verbal explanations during presentation
- Speaker notes to prepare before defense

**FORMAT:**
```
TERM: [Technical or cultural term]
ELI5: [Ultra-simple explanation]
ELI10: [Slightly more detailed explanation]
WHY IT MATTERS: [Relevance to research]
SPEAKER NOTE: [How to explain verbally in 30 seconds]
```

**PRIORITY CONCEPTS TO EXTRACT:**

#### Cultural Concepts:
- [ ] Ngwatio (reciprocity systems)
- [ ] Traditional banking systems
- [ ] Kikuyu proverb structures
- [ ] Cultural metaphors

#### Technical Concepts:
- [ ] BLEU score (and why it's limited)
- [ ] CHRF score
- [ ] Semantic similarity
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] OG-RAG (Ontology-Grounded RAG)
- [ ] Neo4j graph database
- [ ] Ontology
- [ ] Vector embeddings
- [ ] Cosine similarity

#### Methodological Concepts:
- [ ] Cultural fidelity metrics
- [ ] Metaphor preservation
- [ ] Context alignment
- [ ] Statistical significance (p-values, confidence intervals)
- [ ] Effect size (Cohen's d)

### 11.2 Slide-Specific Talking Points
### 11.2 Slide-Specific Talking Points
**INSTRUCTION:** Extract or generate concise talking points (2-3 bullet points per slide)

**EXAMPLE:**
**SLIDE: OG-RAG System Architecture**
- "Our system consists of three main components..."
- "The key innovation is the ontology-grounded retrieval mechanism..."
- "This architecture enables cultural context to guide translation..."

**SPEAKER NOTE (from ELI5):** "Think of it like Google search, but instead of searching the whole internet, we search a carefully organized knowledge graph of Kikuyu cultural concepts. This helps the AI understand the cultural context before translating."

[Generate talking points for all major content slides]

---

## 12. ANTICIPATED QUESTIONS AND ANSWERS

### Technical Questions:
1. **Q:** Why did you choose Neo4j over other graph databases?
   **A:** [Extract justification from methodology]

2. **Q:** How did you ensure ontology quality?
   **A:** [Extract validation approach]

3. **Q:** What is the computational cost of your system?
   **A:** [Extract performance metrics]

### Methodological Questions:
1. **Q:** Why only 100 proverbs? Is this sufficient?
   **A:** [Extract sample size justification]

2. **Q:** How do you address potential bias in expert translations?
   **A:** [Extract validation approach]

### Results Questions:
1. **Q:** Why is the BLEU improvement modest?
   **A:** [Extract BLEU limitation discussion]

2. **Q:** How do you know the improvement is statistically significant?
   **A:** [Extract statistical test results]

### Contribution Questions:
1. **Q:** How is this different from existing RAG systems?
   **A:** [Extract novelty statement]

2. **Q:** Can this be applied to other languages?
   **A:** [Extract generalizability discussion]

---

## QUALITY ASSURANCE CHECKLIST

### Content Completeness:
- [ ] All research questions addressed
- [ ] All hypotheses tested and reported
- [ ] All objectives achieved or justified if not
- [ ] All major findings quantified with statistics
- [ ] All key figures and tables included
- [ ] All contributions clearly stated
- [ ] All limitations acknowledged

### Academic Rigor:
- [ ] Statistical significance reported for all comparisons
- [ ] Effect sizes calculated where appropriate
- [ ] Methodology justified with literature support
- [ ] Results interpreted in context of prior work
- [ ] Limitations discussed honestly
- [ ] Future work is logical extension

### Presentation Readiness:
- [ ] Narrative flow is logical and coherent
- [ ] Visuals are clear and properly labeled
- [ ] Technical jargon is defined for diverse committee
- [ ] Time allocation matches presentation guidelines
- [ ] Backup content prepared for deep-dive questions
- [ ] Talking points are concise and memorable

---

## EXECUTION INSTRUCTIONS FOR GITHUB COPILOT

**STEP 1:** Scan the following directories in order of priority:
1. `docs/thesis/` - Primary thesis document and chapters
2. `docs/thesis/PRESENTATION_GUIDE_ELI5.md` - Speaker notes and simplified explanations
3. `data/results/` - All evaluation results and summaries
4. `docs/` - Supporting documentation
5. `src/` - System implementation for technical details
6. `scripts/` - Analysis scripts for methodology

**STEP 2:** For each section of the master reference document:
1. Extract relevant content from identified sources
2. Organize content hierarchically
3. Include specific numbers, statistics, and citations
4. Link to visual assets with file paths
5. Generate slide recommendations
6. Create talking points

**STEP 3:** Validate completeness:
1. Cross-reference thesis document with extracted content
2. Ensure all major claims are backed by data
3. Verify all figures are cataloged
4. Confirm narrative coherence

**STEP 4:** Format output as markdown document with:
- Clear section headers
- Bullet points for scannability
- Tables for quantitative data
- File path references for all assets
- Presentation time estimates

**OUTPUT FILE:** `presentations/THESIS_DEFENSE_MASTER_REFERENCE.md`

---

## SUCCESS CRITERIA

The extracted master reference document should enable:

✅ **Rapid slide generation** - All content pre-organized by section
✅ **Visual asset integration** - All figures/charts cataloged with context
✅ **Narrative coherence** - Multiple storyline options provided
✅ **Statistical rigor** - All claims backed by quantified evidence
✅ **Q&A readiness** - Anticipated questions with prepared answers
✅ **Time management** - Slide recommendations with time allocations
✅ **Academic credibility** - Proper positioning of contributions and limitations
✅ **Accessibility** - Complex concepts explained for multidisciplinary committee

The final presentation should demonstrate clear research narrative flow, effectively communicate complex findings to diverse audiences, and position the candidate as a competent researcher ready for independent academic work.

---

## BEGIN EXTRACTION
Execute the multi-phase extraction methodology outlined above, applying Tree of Thoughts reasoning, Chain of Thought analysis, and Self-Consistency validation to produce a comprehensive master reference document.
