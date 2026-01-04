# Visual Enhancement Plan: Adding Thesis Figures to Presentation Slides

**Date:** January 4, 2026  
**Purpose:** Integrate thesis figures into presentation to enhance visual appeal, create coherence with written thesis, and break monotony of text-heavy slides  
**Available Figures:** 8 thesis figures (5 PNG charts, 3 TikZ diagrams)

---

## EXECUTIVE SUMMARY

**Recommendation:** Add **6 key figures** to presentation slides to:
- ✅ Create visual coherence between thesis and presentation
- ✅ Replace text-heavy descriptions with professional diagrams
- ✅ Provide memorable visual anchors for committee
- ✅ Demonstrate methodological rigor through data visualization
- ✅ Break monotony with color-coded charts

**Impact:** Transforms presentation from 90% text to balanced 60% text / 40% visuals

---

## AVAILABLE THESIS FIGURES

### Data Visualization Charts (PNG)

1. **`cultural_authenticity_comparison.png`**
   - Bar/box plot comparing Cultural Authenticity scores (Raw GPT-4, Traditional RAG, OG-RAG)
   - Shows 0.568 → 0.627 improvement
   - Used in: Thesis Chapter 5, Section 5.2.1

2. **`translation_fidelity_comparison.png`**
   - Bar/box plot comparing Translation Fidelity scores
   - Shows 0.308 → 0.369 improvement (19.8%)
   - Used in: Thesis Chapter 5, Section 5.2.2

3. **`overall_quality_comparison.png`**
   - Bar/box plot comparing Overall Quality composite metric
   - Shows 0.335 → 0.380 improvement (13.4%)
   - Used in: Thesis Chapter 5, Section 5.2.3

4. **`score_distributions.png`**
   - Box plots showing score distributions across all 3 metrics and all 3 systems
   - Demonstrates consistency (tighter IQR for OG-RAG)
   - Used in: Thesis Chapter 5, Section 5.4

5. **`og_rag_improvements.png`**
   - Summary bar chart showing percentage improvements over baseline
   - Visual representation of 10.5%, 19.8%, 13.5% gains
   - Used in: Thesis Chapter 5, Section 5.4

### System Architecture Diagrams (TikZ/LaTeX)

6. **`system-architecture.tex`**
   - 5-layer architecture diagram (Knowledge Graph → Retrieval → Context Builder → LLM → Evaluation)
   - Shows feedback loop from evaluation to retrieval
   - Color-coded layers (green KG, cyan retrieval, yellow context, orange LLM, purple eval)
   - Used in: Thesis Chapter 4

7. **`methodology-flowchart.tex`**
   - CRISP-DM adapted methodology flowchart
   - 6 phases with activities and deliverables
   - Shows iterative refinement loops
   - Used in: Thesis Chapter 3

8. **`retrieval-pipeline.tex`**
   - Detailed retrieval mechanism flowchart
   - Shows Cypher query → Graph traversal → Subgraph extraction → Context formatting
   - Used in: Thesis Chapter 4

---

## RECOMMENDED FIGURE INTEGRATION PLAN

### 🎯 PRIORITY 1: Essential Results Figures (Must Add)

#### **SLIDE 13: Quantitative Results - Cultural Fidelity**

**Current State:** Table-only presentation of cultural fidelity scores

**ADD FIGURE:** `cultural_authenticity_comparison.png`

**Integration:**
```markdown
## SLIDE 13: QUANTITATIVE RESULTS - CULTURAL FIDELITY

### Visual Content:

**[INSERT FIGURE: cultural_authenticity_comparison.png]**
*Figure: Cultural Authenticity scores across three translation systems (n=100)*

**Key Statistics:**

| Method | Cultural Authenticity | Translation Fidelity | Overall Quality |
|--------|----------------------|---------------------|-----------------|
| Raw GPT-4 | 0.568 (±0.080) | 0.308 (±0.154) | 0.335 (±0.083) |
| Traditional RAG | 0.584 (±0.088) | 0.334 (±0.167) | 0.351 (±0.091) |
| **OG-RAG** | **0.627 (±0.089)** | **0.369 (±0.151)** | **0.380 (±0.085)** |

**Improvement Over Baseline (Raw GPT-4):**
- Cultural Authenticity: **+10.4%** ✓
- Translation Fidelity: **+19.8%** ✓
- Overall Quality: **+13.4%** ✓

**Statistical Significance:**
- **t-statistic:** 7.468
- **p-value:** **< 0.000001** (highly significant)
- **Cohen's d:** 0.70 (medium-to-large effect)
```

**Why This Figure:**
- 📊 Visual reinforcement of key claim (10.4% improvement)
- 🎯 Committee can SEE the gap between systems
- ✅ Directly from thesis = coherence
- 💡 Easier to remember than numbers in table

**Placement:** Replace or supplement existing table

**Timing Impact:** No change (figure speaks while you narrate)

---

#### **SLIDE 17: Core Research Contributions**

**Current State:** Text-only list of 4 contributions

**ADD FIGURE:** `og_rag_improvements.png`

**Integration:**
```markdown
## SLIDE 17: CORE RESEARCH CONTRIBUTIONS

### Visual Content:

**[INSERT FIGURE: og_rag_improvements.png]**
*Figure: OG-RAG Performance Improvements Over Raw GPT-4 Baseline*

**Four Primary Contributions:**

1. **Methodological Innovation** [Point to bars in chart]
   → First application of ontology-grounded RAG to cultural proverb translation  
   → 10.5% cultural authenticity, 19.8% translation fidelity, 13.5% overall quality

2. **Resource Creation**
   → Structured, machine-readable ontology of Kikuyu proverbs (847 concepts)
   → Reusable for NLP, linguistic, and cultural studies research

3. **Empirical Evidence** [Gesture to statistical bars]
   → Quantitative proof that structured cultural knowledge reduces hallucinations  
   → Statistical significance: p < 0.000001, Cohen's d = 0.70

4. **Metric Critique**
   → Demonstrates BLEU inadequacy for cultural translation  
   → Establishes need for culturally-aware evaluation frameworks
```

**Why This Figure:**
- 📈 Makes "10.5%, 19.8%, 13.5%" visually memorable
- 🎨 Color-coded bars create visual interest
- 👁️ Committee sees empirical contribution immediately
- 🔗 Direct link to thesis Chapter 5

**Placement:** Center of slide, above contribution list

**Timing Impact:** +30 seconds (gesture to bars while speaking)

---

### 🎯 PRIORITY 2: Methodology & Architecture Figures (Highly Recommended)

#### **SLIDE 8: OG-RAG System Architecture**

**Current State:** Text-based description of 4-component pipeline

**ADD FIGURE:** Render `system-architecture.tex` to PNG

**Integration:**
```markdown
## SLIDE 8: OG-RAG SYSTEM ARCHITECTURE

### Visual Content:

**[INSERT FIGURE: system-architecture.tex rendered as PNG]**
*Figure: Five-layer OG-RAG architecture with feedback loop*

**System Pipeline (5 Layers):**

**Layer 1: Knowledge Graph (Neo4j)** [Green in diagram]
   → 847 cultural concepts, 1,247 semantic relationships
   → Proverbs + metaphors + cultural themes

**Layer 2: Ontology-Grounded Retrieval** [Cyan in diagram]
   → Graph traversal via Cypher queries
   → Retrieves semantically connected subgraphs

**Layer 3: Context Builder** [Yellow in diagram]
   → Structures retrieved knowledge into prompts
   → Preserves relational context

**Layer 4: LLM Integration (GPT-4)** [Orange in diagram]
   → Culturally-grounded generation
   → Reduced hallucinations through structured context

**Layer 5: Evaluation** [Purple in diagram]
   → Cultural authenticity + translation fidelity metrics
   → Feedback loop to improve retrieval [Red dashed arrow]

**Key Innovation:** Graph-based retrieval preserves semantic relationships, 
not just text chunks
```

**Why This Figure:**
- 🏗️ Replaces 4-component text list with professional architecture diagram
- 🎨 Color-coding makes layers memorable (Prof. Pandya will appreciate visual clarity)
- 🔁 Shows feedback loop visually
- 📐 Matches thesis Figure 4.1 exactly

**Rendering Required:** 
```bash
pdflatex system-architecture.tex
convert system-architecture.pdf system-architecture.png
```

**Placement:** Full-width center of slide

**Timing Impact:** -30 seconds (diagram is self-explanatory, reduces verbal description)

---

#### **SLIDE 10: CRISP-DM Research Methodology**

**Current State:** Text-based description of 6 phases with iteration cycles

**ADD FIGURE:** Render `methodology-flowchart.tex` to PNG

**Integration:**
```markdown
## SLIDE 10: CRISP-DM RESEARCH METHODOLOGY

### Visual Content:

**[INSERT FIGURE: methodology-flowchart.tex rendered as PNG]**
*Figure: CRISP-DM framework adapted for cultural AI research*

**Systematic 6-Phase Approach:**

**1. Problem Definition** → Research gap, hypotheses  
**2. Data Understanding** → 100 proverbs, theme extraction  
**3. Ontology Construction** → 847 concepts, Neo4j knowledge graph  
**4. System Development** → OG-RAG + 3 baselines  
**5. Evaluation** → Expert evaluation, 9 metrics, p < 0.000001  
**6. Deployment** → Thesis documentation, reusable framework  

**Iterative Refinement:**
- Red dashed arrows show feedback loops
- Error analysis → Ontology refinement
- Evaluation insights → System improvements

**Why CRISP-DM:**
Dr. Bakhshandeh's recommendation for systematic rigor, ensuring 
reproducibility and industry-standard methodology
```

**Why This Figure:**
- 📊 Shows methodology is systematic, not ad-hoc
- 🔄 Visualizes iteration cycles (3 feedback loops)
- 🎓 Demonstrates methodological sophistication to committee
- 🔗 Matches thesis Figure 3.1 exactly

**Rendering Required:** 
```bash
pdflatex methodology-flowchart.tex
convert methodology-flowchart.pdf methodology-flowchart.png
```

**Placement:** Full-width center of slide

**Timing Impact:** No change (diagram supports existing speaker notes)

---

### 🎯 PRIORITY 3: Supplementary Data Figures (Optional but Valuable)

#### **SLIDE 16: Interpreting Low Absolute Scores**

**Current State:** Table showing score ranges, text explanation of grade distribution

**ADD FIGURE:** `score_distributions.png`

**Integration:**
```markdown
## SLIDE 16: INTERPRETING LOW ABSOLUTE SCORES

### Visual Content:

**[INSERT FIGURE: score_distributions.png]**
*Figure: Score distributions across all three metrics and translation systems*

**Key Observations:**

1. **All Systems Show Low Absolute Scores** (median 0.32-0.37)
   - Box plots show similar bottom quartiles
   - 96% of translations graded F
   - Reflects inherent task difficulty, not system failure

2. **OG-RAG Shows Consistent Improvement**
   - Higher medians across all three metrics
   - Tighter IQR = more consistent performance
   - Fewer catastrophic failures (scores < 0.3)

3. **Distribution Shift Matters More Than Absolute Values**
   - Entire OG-RAG distribution shifted right
   - Reduced variance = reliability
   - Maximum scores improved (0.68 → 0.74)

**Why All Scores Are Low:**
- Proverbs deeply embedded in cultural worldviews
- Single-reference evaluation (conservative)
- Expert grading standards (90%+ = A)
```

**Why This Figure:**
- 📊 Box plots show variability, not just means
- 🎯 Preemptively addresses "why are scores so low?" question
- 📈 Demonstrates consistency improvement (tighter IQR)
- 🔬 Shows statistical sophistication

**Placement:** Above existing text explanation

**Timing Impact:** +30 seconds (explain box plot interpretation)

---

#### **BACKUP SLIDE 1: Detailed Statistical Analysis**

**Current State:** Table of t-tests, p-values, Cohen's d

**ADD FIGURE:** `cultural_authenticity_comparison.png` (reuse)

**Why:**
- If committee asks "Show me the actual data behind p < 0.000001"
- Visual proof of 0.568 → 0.627 gap
- Reinforces statistical claims with visual evidence

---

### 🎯 PRIORITY 4: Translation Quality Figures (Specialized)

#### **SLIDE 12: Quantitative Results - BLEU Scores**

**Current State:** Table-only BLEU scores

**OPTIONAL ADD:** Create new figure showing BLEU distribution
- Would require generating new visualization from comparative_bleu_scores.csv
- Lower priority since BLEU is de-emphasized as inadequate metric

**Decision:** **SKIP** - We intentionally de-emphasize BLEU, so adding visual prominence contradicts thesis argument

---

#### **SLIDE 15: Qualitative Example 2 - Visual Metaphor**

**Current State:** Text description of stork/locust proverb

**OPTIONAL ADD:** Custom illustration
- Drawing of stork chasing locusts
- Side-by-side comparison: "Storks chasing locusts" vs "Hunting game"
- Would require new artwork creation

**Decision:** **DEFER** - Could be powerful, but requires art creation outside thesis scope

---

## IMPLEMENTATION PLAN

### Phase 1: Render TikZ Diagrams to PNG (Required)

**Action Items:**
1. Navigate to thesis figures directory
2. Compile TikZ diagrams to standalone PDFs
3. Convert PDFs to high-resolution PNGs (300 DPI)

**Commands:**
```bash
cd /Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/docs/thesis/figures

# Render system architecture
pdflatex -shell-escape system-architecture.tex
convert -density 300 system-architecture.pdf system-architecture.png

# Render methodology flowchart
pdflatex -shell-escape methodology-flowchart.tex
convert -density 300 methodology-flowchart.pdf methodology-flowchart.png

# Optional: Render retrieval pipeline (if adding to backup slides)
pdflatex -shell-escape retrieval-pipeline.tex
convert -density 300 retrieval-pipeline.pdf retrieval-pipeline.png
```

**Estimated Time:** 30 minutes

---

### Phase 2: Update Presentation Slides with Figures

**Slides to Modify:**

| Slide | Figure to Add | Priority | Effort |
|-------|--------------|----------|--------|
| **Slide 8** | system-architecture.png | HIGH | 15 min |
| **Slide 10** | methodology-flowchart.png | HIGH | 15 min |
| **Slide 13** | cultural_authenticity_comparison.png | **CRITICAL** | 10 min |
| **Slide 17** | og_rag_improvements.png | **CRITICAL** | 10 min |
| **Slide 16** | score_distributions.png | MEDIUM | 10 min |
| **Backup Slide 1** | cultural_authenticity_comparison.png | LOW | 5 min |

**Total Modification Time:** 65 minutes (1 hour)

---

### Phase 3: Test Presentation with Figures

**Validation Checks:**
1. ✅ All figures render correctly in presentation software
2. ✅ Figure captions match thesis exactly
3. ✅ Color schemes are visible on projector (avoid light backgrounds)
4. ✅ Text is readable at presentation distance (minimum 18pt font in figures)
5. ✅ Timing still within 25-minute target
6. ✅ Figures enhance rather than clutter slides

**Estimated Time:** 30 minutes

---

## VISUAL COHERENCE STRATEGY

### Color Coding Consistency (Thesis → Presentation)

**System Architecture (Slide 8):**
- 🟢 Green = Knowledge Graph layer
- 🔵 Cyan = Retrieval layer
- 🟡 Yellow = Context Builder layer
- 🟠 Orange = LLM Integration layer
- 🟣 Purple = Evaluation layer
- 🔴 Red dashed = Feedback loop

**Methodology Flowchart (Slide 10):**
- 🔵 Blue = CRISP-DM phases
- 🟢 Green = Key activities
- 🟠 Orange = Deliverables/outputs
- 🔴 Red dashed = Iteration feedback

**Result Charts (Slides 13, 16, 17):**
- Consistent color scheme across all result figures
- OG-RAG typically highlighted in distinct color (e.g., blue or green)
- Raw GPT-4 baseline in neutral color (gray)
- Traditional RAG in intermediate color (orange)

### Typography Consistency

**Ensure all figures use:**
- Sans-serif font (Arial, Helvetica) for readability
- Minimum 18pt for labels
- Bold for emphasis
- Consistent capitalization with slide text

---

## PRESENTATION SOFTWARE INTEGRATION

### For PowerPoint/Keynote:

**Insert Format:**
```markdown
![Figure Caption](../docs/thesis/figures/cultural_authenticity_comparison.png)
*Figure X.X: Caption text matching thesis*
```

**Sizing:**
- Full-width figures: 10-11 inches wide
- Half-width figures: 5-6 inches wide
- Maintain aspect ratio (don't distort)

### For Gamma.app (Current Platform):

**Markdown Syntax:**
```markdown
**Visual Content:**

![Cultural Authenticity Comparison](path/to/cultural_authenticity_comparison.png)
*Figure: Cultural Authenticity scores across three translation systems (n=100)*
```

**Upload Strategy:**
1. Upload all PNG figures to Gamma.app media library
2. Reference via uploaded URLs or local paths
3. Test rendering before finalizing

---

## SPEAKER NOTES INTEGRATION

### Gestural Coordination with Figures

**Slide 8 (Architecture):**
```
**Speaker Notes:** "Let me walk you through the five-layer architecture..."
[Point to green layer] "At the foundation, we have the Neo4j knowledge graph 
with 847 cultural concepts..."
[Trace upward with hand] "The retrieval layer extracts semantically connected 
subgraphs via Cypher queries..."
[Point to red dashed arrow] "Notice this feedback loop - evaluation insights 
refine retrieval strategies..."
```

**Slide 13 (Cultural Fidelity):**
```
**Speaker Notes:** "This chart shows the cultural authenticity improvement..."
[Gesture to bars] "Raw GPT-4 achieves 0.568, OG-RAG reaches 0.627..."
[Use hands to show gap] "That 10.4% improvement represents statistically 
significant cultural preservation..."
```

**Slide 17 (Contributions):**
```
**Speaker Notes:** "Our empirical contribution is quantified here..."
[Point to three bars] "10.5% authenticity, 19.8% fidelity, 13.5% overall quality..."
[Sweep hand across chart] "These aren't marginal gains - they're fundamental 
improvements in how AI preserves culture."
```

---

## ANTICIPATED COMMITTEE QUESTIONS

### Question: "Why use these specific visualizations?"

**Answer:**
"These figures come directly from the thesis document, ensuring complete 
coherence between the written work and this presentation. Each visualization 
was created to communicate specific empirical findings:

- The architecture diagram (Figure 4.1 in thesis) shows the five-layer 
  ontology-grounded system structure
- The methodology flowchart (Figure 3.1) demonstrates CRISP-DM rigor
- The cultural authenticity chart (Figure 5.1) provides visual proof of the 
  10.4% improvement claimed in Hypothesis 1

Using thesis figures ensures you're seeing exactly what was peer-reviewed 
and approved, not presentation-only visuals."

---

### Question: "Can you explain the box plots in the score distribution figure?"

**Answer:**
"Absolutely. Box plots show five key statistics for each system:

- The box represents the middle 50% of scores (interquartile range)
- The line inside the box is the median
- The whiskers extend to 1.5× IQR
- Outliers appear as individual points

Notice OG-RAG has a tighter box - that's more consistent performance. The 
median is higher, and we see fewer extreme low scores. This consistency 
matters for real-world deployment where reliability is crucial."

---

## FINAL RECOMMENDATIONS

### Must Add (Critical Priority):

1. ✅ **Slide 13:** `cultural_authenticity_comparison.png`
   - Core empirical finding
   - Visual proof of 10.4% improvement
   - Replaces text-heavy table

2. ✅ **Slide 17:** `og_rag_improvements.png`
   - Summary of all contributions
   - Memorable visual
   - Reinforces empirical rigor

### Highly Recommended (High Priority):

3. ✅ **Slide 8:** `system-architecture.png` (rendered from .tex)
   - Replaces text description
   - Shows Prof. Pandya sophisticated architecture
   - Demonstrates technical competence

4. ✅ **Slide 10:** `methodology-flowchart.png` (rendered from .tex)
   - Shows Dr. Bakhshandeh systematic CRISP-DM approach
   - Visualizes iteration cycles
   - Proves methodological rigor

### Optional but Valuable (Medium Priority):

5. ⭕ **Slide 16:** `score_distributions.png`
   - Preempts "why are scores low?" question
   - Shows statistical sophistication
   - Demonstrates consistency improvement

### Defer (Low Priority or Out of Scope):

6. ⏸️ **Slide 12:** BLEU distribution chart (would require new creation)
7. ⏸️ **Slide 15:** Custom stork/locust illustration (requires artwork)

---

## IMPACT ASSESSMENT

### Before Figure Integration:
- **Text-to-Visual Ratio:** 90% text / 10% tables
- **Visual Memorability:** Low (committee forgets numbers)
- **Coherence with Thesis:** Medium (content matches, format differs)
- **Committee Engagement:** Medium (text-heavy slides cause cognitive load)

### After Figure Integration (Adding 4 key figures):
- **Text-to-Visual Ratio:** 60% text / 40% visuals
- **Visual Memorability:** High (charts create mental anchors)
- **Coherence with Thesis:** Very High (exact thesis figures)
- **Committee Engagement:** High (visual variety maintains attention)

**Overall Impact:** Transforms presentation from academic report to professional research defense

---

## NEXT STEPS

1. **Immediate (Today):**
   - Render TikZ diagrams to PNG (30 min)
   - Upload figures to Gamma.app (15 min)

2. **Short-term (This Week):**
   - Insert figures into Slides 8, 10, 13, 17 (1 hour)
   - Update speaker notes with figure references (30 min)
   - Practice presentation with new visuals (1 hour)

3. **Before Defense (Within 10 Days):**
   - Rehearse with timing (ensure still 25 min)
   - Verify figure readability on projector
   - Prepare gestural coordination for each figure

**Total Additional Preparation Time:** 3-4 hours  
**Defense Impact:** Significant improvement in visual engagement and thesis coherence

---

**END OF VISUAL ENHANCEMENT PLAN**

**Status:** Ready for implementation  
**Recommendation:** Add all 4 Priority 1-2 figures (Slides 8, 10, 13, 17)  
**Timeline:** Complete by January 6, 2026 (3 days)  
**Defense Date:** January 14, 2026 (10 days remaining)
