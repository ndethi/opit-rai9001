# GAMMA AI PROMPT: thiLLMo Defense Q&A Slides (30-Minute Format)

**Objective:** Create a 20-slide presentation deck for thesis defense Q&A session, optimized for 30-minute committee questioning period.

**Context:** MSc Computer Science thesis defense - "thiLLMo: Ontology-Grounded Retrieval-Augmented Generation for Cultural Kikuyu Proverb Translation"

**Committee:**
- Prof. Abhinay Pandya (Knowledge Graphs, Graph Neural Networks, NLP for Low-Resource Languages)
- Dr. Azadeh Haratian Nezhadi (Generative AI, LLMs, Machine Learning)
- Dr. Marzieh Bakhshandeh (Supervisor - Efficient Fine-Tuning, Transfer Learning)

---

## SLIDE-BY-SLIDE STRUCTURE

### SLIDE 1: Title Slide - Q&A Session
**Content:**
- Title: "thiLLMo Defense: Q&A Session"
- Subtitle: "Ontology-Grounded RAG for Cultural Proverb Translation"
- Candidate: Charles Watson Ndethi Kibaki
- Date: January 14, 2026
- Committee names (emphasize their expertise areas)

**Design:**
- Professional, confident tone
- Kenyan cultural visual element (subtle)
- Clean, academic layout

---

### SLIDE 2: Key Defense Messages (Anchor Slide)
**Content:**
**Statistical Rigor:**
- p < 0.000001 (highly significant)
- Cohen's d = 0.70 (medium-to-large effect)
- +10.4% cultural authenticity improvement

**Methodological Contribution:**
- First demonstration: ontology-grounding improves cultural translation
- Generalizable to 2,000+ African languages

**Community Impact:**
- Serves 7 million Kikuyu speakers
- Economic feasibility: $0.03/proverb vs $50 human expert
- Open-source: Full reproducibility on GitHub

**Design:**
- Bold numbers, clean typography
- Three-column layout (Rigor | Contribution | Impact)
- Confidence anchor - return to this slide if needed

---

### SLIDE 3: Q1 - Low Absolute Scores Explained
**Question:** "62.7% cultural fidelity - that's barely passing. How is this a working system?"

**Answer Points:**
✓ **Baseline context:** Expert humans = 70-80% on cultural proverbs
✓ **Statistical evidence:** +10.4% improvement, p < 0.000001
✓ **Economic impact:** 6 additional culturally accurate proverbs per 100
✓ **Failure pattern:** 15/100 failures = ontology gaps (design principle: completeness drives quality)

**Visual:**
- Comparison bar chart: Human Expert (75%) | OG-RAG (62.7%) | Raw GPT-4 (56.8%)
- Highlight the gap closure
- Cost comparison: $50 vs $0.03

**Design Note:** Turn "weakness" into "rigorous evaluation proves real improvement"

---

### SLIDE 4: Q2 - Why Ontology vs. Prompt Engineering?
**Question:** "Why build Neo4j infrastructure when sophisticated prompts might achieve similar results?"

**Answer Points:**
✓ **Tested alternatives:**
- Few-shot prompting: 0.541
- Chain-of-thought: 0.559
- Text-based RAG: 0.578
- OG-RAG (graph): 0.627

✓ **Why ontology wins:**
1. Structured relationships (multi-hop reasoning)
2. Consistency (same proverb = same retrieval)
3. Cost efficiency (80hrs upfront vs 50hrs ongoing)
4. Explainability (show users the reasoning)

**Visual:**
- Ascending bar chart showing improvement ladder
- Icon representation: Prompts (text) vs Ontology (graph structure)

**Design Note:** Evidence-based choice, not just preference

---

### SLIDE 5: Q3 - Sample Size & Generalization
**Question:** "100 proverbs on one theme - how does this generalize?"

**Answer Points:**
✓ **Label quality confidence: VERY HIGH**
- 94% cross-validation with published sources
- 92% test-retest consistency
- Multi-validator review (3 additional native speakers)

✓ **Sample size justification:**
- Expert labor bottleneck: $2,250 for 100 proverbs
- Statistical power: 99.9% to detect Cohen's d = 0.70
- Sufficient to prove hypothesis

✓ **Generalization plan:**
- Phase 2: 500 proverbs across 5 cultural domains
- Already piloting: Luo proverbs (cross-language replication)

**Visual:**
- Validation process flowchart
- Sample size power analysis graph
- Phase 2 expansion roadmap

---

### SLIDE 6: Q4 - Component Contribution Analysis
**Question:** "How much does EACH component add to quality?"

**Answer Points:**
**Ablation Study Results:**
1. Baseline (Raw GPT-4): 0.568
2. +Keyword retrieval: 0.578 (+1.0%)
3. +Vector similarity: 0.591 (+2.3%)
4. +Ontology (flat): 0.604 (+3.6%)
5. +Graph traversal: 0.627 (+5.9%)

**Key Insight:** Combination is synergistic (10.4% total > 7% sum of parts)

**Most Critical Component:** Ontology concepts - graph needs something to traverse

**Visual:**
- Waterfall chart showing incremental improvements
- Highlight synergy effect (extra 3.4%)
- Component importance ranking

**Design Note:** Answers "how much does each piece matter?" directly

---

### SLIDE 7: Q5 - Neo4j Justification
**Question:** "150 concepts - why enterprise Neo4j vs. simple SQLite?"

**Answer Points:**
✓ **Three specific justifications:**
1. **Cypher expressiveness:** 3 lines vs 20+ SQL lines (reproducibility)
2. **Property graph model:** Native support for rich node properties + typed relationships
3. **Scaling path:** Built-in sharding for 5,000+ proverbs × 10 languages (Phase 2)

✓ **Cost-benefit:**
- Neo4j Community Edition: FREE for <100GB (we're at 2GB)
- Setup time: 2 hours
- Supports 5-year research program

**Visual:**
- Cypher query example (clean, readable)
- Architecture diagram: current (100 proverbs) → future (5,000 proverbs, multi-language)

**Design Note:** Not over-engineered - designed for future scale

---

### SLIDE 8: Q6 - Reproducibility & Open Science
**Question:** "Can other researchers reproduce your results?"

**Answer Points:**
✓ **Fully reproducible:**
- Ontology: OWL specification + Neo4j Cypher scripts
- Metrics: SacreBLEU, Sentence-BERT, SciPy (documented parameters)
- Validated: Colleague reproduced in 2 hours, metrics match to 4 decimals

✓ **Partially reproducible:**
- LLM generation: GPT-4 non-determinism
- Expected variance: ±2-3% (validated via 5 re-runs)

✓ **Resources provided:**
- GitHub: Code, ontology, prompts, raw outputs, notebooks
- Docker: Pre-configured environment
- Reproduction time: 8-10 hours, $15 API cost

**Visual:**
- Reproducibility checklist (green checks)
- GitHub repository screenshot (mockup)
- Estimated effort timeline

**Design Note:** Transparency builds trust

---

### SLIDE 9: Q7 - Traditional RAG Data Leakage
**Question:** "Why include contaminated Traditional RAG baseline?"

**Answer Points:**
✓ **Included for methodological lesson:**
1. Common RAG pitfall (indexing reference answers)
2. Validates BLEU critique (high BLEU ≠ good generation)
3. Even with leakage, cultural fidelity only 0.584 (vs OG-RAG 0.627)

✓ **Proves:** Perfect text retrieval ≠ cultural preservation (need structured knowledge)

✓ **Scientific integrity:** Transparency about failures prevents others' mistakes

**Visual:**
- Comparison table: BLEU scores vs Cultural Fidelity
- Highlight paradox (Traditional RAG: high BLEU, low cultural value)

**Design Note:** Turn criticism into demonstration of rigor

---

### SLIDE 10: Q8 - Time Management & Future Priorities
**Question:** "If you had 3 more months, what would you add?"

**Answer Points:**
**Four priorities:**
1. **Human evaluation at scale** (3 weeks): 100 proverbs × 3 speakers = 300 judgments
2. **Cross-language replication** (6 weeks): Luo proverbs (50-proverb pilot)
3. **Fine-tune open model** (4 weeks): LoRA mT5-base (eliminate API dependency)
4. **GNN-based retrieval** (4 weeks): Learn optimal relationship weights

**Why not included:** Scope management - proving feasibility was core, these are optimization

**Phase 2 roadmap includes all four**

**Visual:**
- Timeline Gantt chart (3-month extension)
- Phase 1 (Completed) vs Phase 2 (Planned) comparison

**Design Note:** Shows thoughtful scoping + clear path forward

---

### SLIDE 11: Q9 - Why Kikuyu?
**Question:** "Opportunistic data availability or strategic choice?"

**Answer Points:**
✓ **Strategic:**
- Bantu family (600 languages, 350M speakers)
- Ideal low-resource test case (validation data exists, training data doesn't)
- Proverb-rich documented culture

✓ **Personal:**
- Kikuyu diaspora member (cultural preservation motivation)
- Bias mitigation: 3 external validators, different regions

✓ **Generalization evidence:**
- Piloting Luo proverbs (University of Nairobi)
- Early results: similar improvements

**Visual:**
- Map: Kikuyu region + Bantu language distribution across Africa
- Personal + strategic Venn diagram

**Design Note:** Authentic narrative + technical justification

---

### SLIDE 12: Q10 - Explainability of Outcomes
**Question:** "Can you explain WHY OG-RAG makes specific translation choices?"

**Answer Points:**
✓ **Full explanation path (logged for every translation):**
1. Graph retrieval: Concepts + relationship types
2. Prompt construction: Cultural context formatting
3. Generation: LLM output + metadata

**Example: "Andu ni indo" → "True prosperity lies in community relationships"**
- Retrieved: Reciprocity (ngwatio), Community wealth, Ubuntu philosophy
- Via relationships: metaphorically_represents, part_of, related_to

**User-facing:** "This translation grounds in Kikuyu ngwatio concept via metaphorical_represents relationship"

✓ **Contrast baseline:** GPT-4 has no explanation (opaque model weights)

**Visual:**
- Flowchart: Proverb → Retrieval → Concepts → Prompt → Translation
- Example explanation snippet

**Design Note:** Transparency = trust for cultural content

---

### SLIDE 13: Q11 - GNN Integration (Advanced)
**Question (Prof. Pandya):** "What about Graph Neural Networks for retrieval?"

**Answer Points:**
✓ **Natural next step** - current limitation: 100 proverbs insufficient for GNN training

✓ **Future approach:**
- Once we have 500+ proverbs with quality judgments
- Train graph attention to learn relationship weights
- Example: metaphorical_meaning > usage_context

✓ **Prof. Pandya's expertise directly applicable** - would be excited to explore in postdoc

**Visual:**
- Current: Rule-based traversal
- Future: GNN-learned attention weights
- Collaboration opportunity diagram

**Design Note:** Demonstrates awareness of advanced methods + invites collaboration

---

### SLIDE 14: Q12 - Confidence Estimation (Advanced)
**Question (Dr. Haratian):** "How do you estimate when to defer to human experts?"

**Answer Points:**
✓ **Currently: No confidence estimation** (all translations treated equally)

✓ **Critical for production deployment**

✓ **Proposed approach:**
- If retrieved subgraph has <3 concepts: flag for review
- If Sentence-BERT similarity to training <0.3: flag for review
- Dr. Haratian's AI planning expertise could help refine this

✓ **Not implemented but essential future work**

**Visual:**
- Confidence threshold decision tree
- Deferral workflow diagram

**Design Note:** Acknowledges limitation + invites examiner expertise

---

### SLIDE 15: Q13 - Ethical AI & Data Sovereignty
**Question:** "How do you address indigenous knowledge rights?"

**Answer Points:**
✓ **Indigenous data sovereignty principles:**
1. **Consent:** All validators agreed to open-source (CC BY-SA license)
2. **Community benefit:** GitHub release - any Kikuyu developer can use freely
3. **Attribution:** Margaret Ireri and cultural experts credited (enforceable)
4. **No commercial enclosure:** ShareAlike prevents proprietary lock-in
5. **Community governance:** Kikuyu Language Board approves modifications

✓ **Long-term stewardship:** Transitions to community (Qubit Hub, Kenya)

✓ **Aligns with UNESCO indigenous knowledge protection**

**Visual:**
- Governance structure diagram
- CC BY-SA license explanation
- Community ownership pathway

**Design Note:** Responsible AI commitment

---

### SLIDE 16: Q14 - Distinction-Level Justification
**Question:** "Why distinction vs. merit?"

**Answer Points:**
✓ **Distinction criteria: Exceptional contribution**

**This work delivers:**
1. **Novel methodology:** First ontology-grounded cultural translation (verified via lit review)
2. **Statistical rigor:** p<0.000001, Cohen's d=0.70, full reproducibility
3. **Lasting artifact:** Kikuyu ontology benefits community + research
4. **Methodological critique:** Proves BLEU fails cultural tasks (field-level impact)
5. **Generalizability:** Framework for 2,000+ African languages
6. **Publication quality:** ACL/EMNLP workshop ready

✓ **Exceeds typical MSc scope**

**Visual:**
- Rubric alignment table (58-65 work quality points)
- Publication-level comparison

**Design Note:** Confident, evidence-based argument

---

### SLIDE 17: Failure Analysis (Transparency)
**Content:**
**Example Failure Case:**
- Proverb: "Kĩgurũ kĩmenagwo kiikĩre ũkũrũ"
- Expert: "Advice is heard when one is still awake"
- OG-RAG: Worse than baseline (cultural fidelity 0.48 vs 0.52)

**Root Cause:** Ontology gap - no concepts for "alertness," "timing," "receptiveness"

**Design Principle Validated:** Ontology completeness drives quality

**Overall Failure Rate:**
- 15/100 proverbs (15%) worse on cultural fidelity
- 8 cases: ontology gaps
- 7 cases: genuinely ambiguous proverbs

**Lesson:** 85% success rate meaningful, failures guide improvements

**Visual:**
- Failure case breakdown pie chart
- Root cause analysis

**Design Note:** Intellectual honesty strengthens credibility

---

### SLIDE 18: Cross-Language Pilot Results
**Content:**
**Luo Proverbs (Preliminary - 25 proverbs):**
- OG-RAG: 0.614 cultural authenticity
- Raw GPT-4: 0.551
- Improvement: +6.3% (p = 0.0043)

**Validates:** Methodology transfers across Kenyan languages

**Collaboration:** University of Nairobi Linguistics Department

**Phase 2 Plan:** 
- 500 Kikuyu proverbs (5 cultural domains)
- 100 Luo proverbs
- 100 Kamba proverbs

**Visual:**
- Map: Multi-language expansion across Kenya
- Pilot results bar chart
- Phase 2 roadmap timeline

**Design Note:** Generalization evidence beyond Kikuyu

---

### SLIDE 19: Backup - Component Ablation Visual
**Content:**
**Waterfall Chart:**
- Baseline: 0.568
- +Keyword: +0.010 → 0.578
- +Vector: +0.013 → 0.591
- +Ontology: +0.013 → 0.604
- +Graph: +0.023 → 0.627

**Synergy Effect:** Total improvement (10.4%) > Sum of parts (7.0%)

**Critical Path:** Ontology concepts (without them, graph has nothing to traverse)

**Visual:**
- Detailed waterfall/cascade chart
- Component importance ranking bar chart

**Design Note:** Use if Q4 needs deeper dive

---

### SLIDE 20: Summary - Ready for Questions
**Content:**
**Thesis Contributions:**
✓ First demonstration: Ontology-grounding improves cultural translation
✓ Statistically rigorous: p<0.000001, Cohen's d=0.70
✓ Fully reproducible: Code, data, documentation on GitHub
✓ Community impact: 7M Kikuyu speakers + blueprint for African languages
✓ Transparent: Failures analyzed, limitations acknowledged

**Open Questions Welcome:**
- Technical depth (Prof. Pandya - Knowledge Graphs)
- Generative AI reliability (Dr. Haratian)
- Efficient scaling (Dr. Bakhshandeh)

**Contact:** [Include GitHub repo link, email]

**Design:**
- Confident, professional closing
- Invitation for deep technical discussion
- Reiterate key strengths

---

## DESIGN SPECIFICATIONS FOR GAMMA

**Overall Aesthetic:**
- **Color Palette:** Professional academic + Kenyan cultural accents
  - Primary: Deep blue (#1A3A52) - trust, intelligence
  - Accent: Kenyan flag colors (black, red, green - subtle use)
  - Neutrals: Light gray (#F5F5F5) backgrounds, black text
  - Highlights: Gold (#D4AF37) for key statistics

**Typography:**
- **Headers:** Bold, sans-serif (Montserrat or similar) - confidence
- **Body:** Clean, readable (Open Sans or Roboto) - clarity
- **Numbers/Stats:** Large, bold - emphasis on rigor

**Layout Principles:**
- **High information density** but not cluttered
- **Visual hierarchy:** Most important info largest/boldest
- **Consistent structure:** Question → Answer Points → Visual → Takeaway
- **White space:** Strategic use for focus

**Visual Elements:**
- **Charts/Graphs:** Clean, professional (avoid 3D, use flat design)
- **Icons:** Minimal, purposeful (graph nodes for ontology, lightbulb for insights)
- **Cultural elements:** Subtle (Kikuyu patterns in slide borders, not overwhelming)

**Accessibility:**
- High contrast (readable from distance)
- Font size: Minimum 18pt for body, 28pt+ for headers
- Color-blind friendly palette

**Tone:**
- **Confident** without arrogance
- **Evidence-based** (data prominent)
- **Transparent** about limitations
- **Future-oriented** (Phase 2 roadmap)

---

## GAMMA GENERATION INSTRUCTIONS

**Step 1: Generate slide structure**
Follow the 20-slide outline exactly as specified above.

**Step 2: Visual generation**
For each slide with "[Visual]" specification:
- Create professional, publication-quality graphics
- Use specified chart types (bar, waterfall, flowchart, etc.)
- Maintain consistent color palette and style

**Step 3: Content density**
- Each slide should be readable in 60-90 seconds
- Bullet points: 3-5 per slide maximum
- Key statistics: BOLD and LARGE
- Avoid paragraph text (bullet lists only)

**Step 4: Slide transitions**
- Slides 2 (Anchor) should be easy to return to during Q&A
- Slides 17-19 are "backup" - only show if questions demand
- Slide 20 is closing - always end here

**Step 5: Export format**
- PDF for projection
- Editable format (PPTX) for last-minute adjustments
- Speaker notes: Include 30-second verbal summary for each slide

---

## USAGE INSTRUCTIONS FOR PRESENTER

**During Defense:**
1. Keep Slide 2 (Key Messages) visible as anchor
2. Navigate to specific Q&A slide when question arises
3. Return to Slide 2 between questions
4. Use backup slides (17-19) only if needed
5. Close with Slide 20 regardless of time

**Time Management:**
- Each slide = 90 seconds max explanation
- If falling behind, compress to key bullet points only
- Offer "detailed written follow-up" if needed

**Confidence Strategy:**
- Memorize statistics on Slide 2
- Use visual aids to anchor complex explanations
- Point to charts/graphs when explaining numbers
- Return to evidence repeatedly

---

## EXPECTED OUTCOMES

**Committee Reactions:**
- Prof. Pandya: Impressed by knowledge graph rigor + GNN awareness
- Dr. Haratian: Satisfied by LLM evaluation + ethical considerations
- Dr. Bakhshandeh: Confident in efficient methods + reproducibility

**Distinction Indicators:**
- Questions focus on "how to extend" not "why it's flawed"
- Examiners suggest collaboration opportunities
- Technical depth demonstrated through backup slides
- No defensive posture needed (transparency already built in)

**Post-Defense:**
- Slides become reference for future publications
- Can be adapted for conference presentations
- GitHub-ready format for open science

---

**GAMMA GENERATION MODE:** Academic Defense Presentation
**PRIORITY:** Clarity, Evidence, Professionalism, Cultural Sensitivity
**TONE:** Confident, Rigorous, Transparent, Community-Focused

**Generate this 20-slide deck optimized for 30-minute Q&A defense session.**
