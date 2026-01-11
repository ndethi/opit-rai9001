# Gamma AI Prompt for Thesis Defense Presentation

## Context for Gamma AI

Create a professional, academically rigorous thesis defense presentation for a PhD dissertation titled:

**"Ontology-Grounded Retrieval-Augmented Generation for Culturally Faithful Translation of Kikuyu Proverbs"**

**Presenter**: PhD Candidate in Computer Science  
**System Name**: thiLLMo (pronounced "theel-mo") - combining "thimo" (Kikuyu word for proverbs) + LLM  
**Defense Date**: January 2026  
**Audience**: Mixed - Computer Science faculty, linguists, cultural studies experts, and general academic audience

---

## Presentation Requirements

**Duration**: 25-30 minutes  
**Slide Count**: 20-25 slides  
**Tone**: Professional, confident, accessible to non-specialists  
**Visual Style**: Modern academic, clean design with cultural elements  
**Color Scheme**: Use warm earth tones reflecting Kikuyu culture (terracotta, sage green, deep brown, gold accents)

---

## Content Structure & Slide Breakdown

### Opening Slides (3-4 slides)

**Slide 1: Title Slide**
- Full dissertation title
- Candidate name
- Institution
- Defense date
- Simple visual: Kenyan landscape or traditional Kikuyu patterns

**Slide 2: The Problem in One Example**
- Show the proverb: "Andu ni indo" (Kikuyu)
- Literal translation: "People are things/wealth"
- Generic AI translation: "People are important" ❌
- Culturally faithful translation: "Community relationships constitute true prosperity through reciprocal obligation systems" ✅
- Tagline: "Why getting the words right isn't enough"

**Slide 3: The Cultural Translation Gap**
- Visual comparison:
  - LEFT: Word-by-word translation (mechanical, loses meaning)
  - RIGHT: Cultural translation (preserves worldview, values, context)
- Key stat: Traditional MT systems fail 60% of the time on cultural accuracy
- The challenge: How do we teach AI to understand culture, not just language?

**Slide 4: Research Question**
- PRIMARY: Can structured cultural knowledge improve AI translation of culturally nuanced text?
- Test case: Kikuyu proverbs
- Why proverbs? They're dense with cultural meaning, resist literal translation, and are measurable

---

### Background & Motivation (4-5 slides)

**Slide 5: Why Kikuyu Proverbs Matter**
- ~7 million speakers globally
- Rich oral tradition spanning 500+ years
- Proverbs encode: Economics (ngwatio reciprocity), Governance (council wisdom), Ethics (moral philosophy), Social structure (age-sets, kinship)
- Problem: Disappearing with language shift and urbanization
- Digital preservation requires MORE than transcription - needs cultural context

**Slide 6: The Double-Bind Problem**
Two challenges that make each other worse:
1. **Cultural Opacity**: AI doesn't understand metaphors, context, cultural values
2. **Data Scarcity**: Low-resource languages lack millions of training examples

Traditional solution: Get more data  
Our insight: Add structured cultural knowledge to compensate for missing data

**Slide 7: What Current Systems Get Wrong**
Show 3 examples of failed translations:
1. "Cia thuguri itiyuragia ikumbi" → Generic AI: "Bought things don't fill storage" ❌  
   Cultural meaning: Self-sufficiency beats consumption (economic philosophy)

2. "Mũtĩ ndũũagaga mũtĩ" → Generic AI: "A tree doesn't grow another tree" ❌  
   Cultural meaning: Family lineage and ancestral continuity through children

3. Real scores: Raw GPT-4 achieves only 0.68 cultural authenticity (scale 0-1)

**Slide 8: Why RAG? Why Ontologies?**
- **RAG (Retrieval-Augmented Generation)**: Give AI relevant knowledge BEFORE it translates
  - Like open-book exam vs. closed-book
  - AI retrieves cultural context, THEN generates translation
  
- **Ontology (Knowledge Graph)**: Structured encyclopedia of Kikuyu culture
  - 847 cultural concepts (Reciprocity, Wisdom, Community, Elderhood...)
  - 1,247 relationships between concepts
  - Maps proverbs to their cultural themes and usage contexts

Simple analogy: "We built a cultural GPS so the AI doesn't get lost"

---

### Solution: The thiLLMo System (5-6 slides)

**Slide 9: System Architecture Overview**
Visual diagram showing:
1. INPUT: Kikuyu proverb → "Andu ni indo"
2. RETRIEVAL MODULE: Query knowledge graph for related concepts
   - Finds: Reciprocity (ngwatio), Community wealth, Traditional economics
3. CONTEXT FORMATTING: Package cultural knowledge into prompt
4. LLM GENERATION: GPT-4 translates WITH cultural context
5. OUTPUT: Culturally faithful English translation

**Slide 10: The Cultural Ontology**
Visual: Neo4j knowledge graph screenshot showing nodes and relationships
- 100 proverbs (core dataset)
- 847 cultural concepts organized into 15 thematic domains:
  - Wisdom & Knowledge
  - Community & Kinship
  - Economic Philosophy (ngwatio)
  - Governance & Leadership
  - Gender & Age-Sets
  - Agriculture & Land
  - Ethics & Morality
- 1,247 edges connecting proverbs to themes, themes to domains

**Slide 11: Ontology Development - The Hybrid Approach**
Challenge: Building cultural ontologies takes YEARS of community consultation
Our solution: LLM-assisted + Expert validation
- GPT-4 analyzed 100 proverbs → proposed 1,200 concepts
- Native speaker expert reviewed EVERY suggestion
- Rejected/modified 15-20% (e.g., "ngwatio" ≠ "barter")
- Cross-validated against published sources (Ireri 2017, Gikandi 1982)
Result: 40% faster than manual, culturally accurate

Key innovation: All LLM suggestions are version-controlled (Git commits) - full transparency

**Slide 12: How Retrieval Works - Hybrid Strategy**
We combine TWO retrieval methods:
1. **Graph Traversal**: Follow relationships in the ontology
   - Proverb → expresses → Reciprocity → part_of → Economic Philosophy
   - Gets structural cultural knowledge
   
2. **Semantic Search**: Vector similarity (Sentence-BERT)
   - Finds similar proverbs by meaning, not just structure
   - Gets contextual usage examples

Final prompt includes:
- Cultural themes (from graph)
- Usage contexts (when/why this proverb is said)
- Related proverbs (from semantic search)
- Moral lessons and metaphorical interpretations

**Slide 13: Baseline Comparisons**
We tested 3 systems on the same 100 proverbs:
1. **Raw GPT-4**: Just translate, no context
2. **Traditional RAG**: Give similar proverb examples (unstructured text)
3. **OG-RAG (thiLLMo)**: Full ontology-grounded approach

Why compare? Need to prove ontology structure MATTERS, not just retrieval

---

### Evaluation & Results (5-6 slides)

**Slide 14: Evaluation Framework**
Two-dimensional scoring (0-1 scale):
1. **Cultural Authenticity** (60% weight)
   - Preserves Kikuyu worldview?
   - Metaphors culturally appropriate?
   - Contextually suitable?
   - Values aligned?

2. **Translation Fidelity** (40% weight)
   - Semantically accurate?
   - Fluent English?
   - Complete (nothing lost)?

**Overall Quality** = 0.6 × Authenticity + 0.4 × Fidelity

Why 60/40? Consultation with cultural experts: "For proverbs, cultural preservation matters MORE than word-for-word accuracy"

**Slide 15: Human Evaluation Methodology**
- Single native Kikuyu speaker evaluator (author)
- Nyeri dialect, deep cultural knowledge
- All 300 translations (3 systems × 100 proverbs)
- Blind evaluation (systems anonymized)
- Detailed rubrics to reduce subjectivity
- Cross-validated against published sources
- Test-retest reliability: 92% consistency

Note: Single evaluator design acknowledged as limitation, but common in low-resource language research due to scarcity of qualified evaluators

**Slide 16: Results - Cultural Authenticity**
Bar chart comparing systems:
- **OG-RAG (thiLLMo)**: 0.79 (excellent) 🟢
- **Traditional RAG**: 0.74 (good) 🟡
- **Raw GPT-4**: 0.68 (adequate) 🟠

Statistical significance:
- OG-RAG vs Raw GPT-4: p < 0.000001, Cohen's d = 0.73 (LARGE effect)
- OG-RAG vs Trad RAG: p < 0.000001, Cohen's d = 0.51 (MEDIUM effect)

Interpretation: Ontology structure provides **5.3% absolute improvement** - statistically and practically significant

**Slide 17: Results - Translation Fidelity**
Bar chart:
- **OG-RAG**: 0.82 (fluent + accurate)
- **Traditional RAG**: 0.80 (fluent + mostly accurate)
- **Raw GPT-4**: 0.76 (fluent but sometimes inaccurate)

Key finding: Ontology helps with accuracy too, not just cultural depth
Why? Structured context disambiguates polysemous terms (mũtĩ = tree vs. medicine vs. lineage)

**Slide 18: Qualitative Analysis - Success Example**
Proverb: "Andu ni indo"

**Raw GPT-4**: "People are important"
- Problem: Generic, loses economic philosophy
- Cultural authenticity: 0.65

**Traditional RAG**: "People are wealth, not possessions"
- Better: Contrasts people vs. material goods
- Cultural authenticity: 0.72

**OG-RAG (thiLLMo)**: "True prosperity lies in community relationships and reciprocal obligations (ngwatio), not material accumulation"
- Excellent: Captures economic philosophy, references ngwatio system, preserves worldview
- Cultural authenticity: 0.87

**Slide 19: Why It Works - Mechanism Analysis**
Compared translations with retrieved ontology contexts:
- High-scoring translations used retrieved cultural themes DIRECTLY in output
- Ontology provided: Usage contexts → "Said during wealth distribution ceremonies"
- This context prevented generic translations like "people matter"
- Graph relationships connected proverb → ngwatio → collective prosperity
- LLM integrated this structure into coherent English explanation

Key insight: **Structure matters** - organized knowledge beats unstructured examples

---

### Contributions & Future Work (3-4 slides)

**Slide 20: Research Contributions**

**Technical:**
- thiLLMo architecture: Hybrid graph+vector retrieval for cultural RAG
- Open-source ontology: 847 Kikuyu cultural concepts (reusable template)
- Demonstrates ontologies work for cultural domains (like MedRAG for medicine)

**Methodological:**
- Two-dimensional evaluation framework (authenticity vs. fidelity)
- LLM-assisted ontology development with expert validation (40% faster)
- Single-evaluator design with published source cross-validation

**Theoretical:**
- **Structure Hypothesis**: Structured cultural knowledge outperforms unstructured retrieval when concepts have hierarchical/relational organization
- Cultural AI design principles: Community partnership, epistemic humility, benefit sharing, graceful degradation

**Slide 21: Limitations (Be Honest)**
1. **Single evaluator**: One native speaker, potential individual bias
   - Mitigation: Cross-validation with published sources, test-retest reliability
   - Future: Multi-evaluator panel (Nyeri, Kiambu, Embu dialects)

2. **LLM-assisted ontology**: 15-20% of GPT-4 suggestions were culturally inaccurate
   - Mitigation: Expert review of EVERY suggestion, version control for transparency
   - Future: Community-driven ontology refinement

3. **Ontology coverage**: 847 concepts can't capture ALL Kikuyu culture
   - Future: Expand to folktales, songs, ceremonial discourse

4. **Scalability**: Manual ontology building doesn't scale to thousands of languages
   - Future: Semi-automated ontology bootstrapping methods

**Slide 22: Future Directions**

**Near-term:**
- Expand to other Kikuyu text genres (folktales, oral histories)
- Multi-dialect support (Nyeri, Kiambu, Embu variants)
- Community evaluation: Involve cultural elders, diaspora speakers

**Long-term:**
- Apply framework to other low-resource languages (Swahili proverbs, Zulu oral literature)
- Cultural ontology governance: Who owns cultural knowledge in AI systems?
- Benefit-sharing models: Ensure communities profit from their cultural data
- Multilingual cultural ontology federation (connect Kikuyu → Swahili → other Bantu cultures)

**Moonshot:**
- Cultural preservation AI: Interactive system for youth to learn proverbs with cultural context
- Reverse translation: Generate new culturally appropriate Kikuyu proverbs from English concepts

---

### Closing (2 slides)

**Slide 23: Key Takeaways**
1. **Cultural translation ≠ word translation** - requires deep cultural knowledge
2. **Ontologies can compensate for data scarcity** - structure beats volume for cultural domains
3. **AI + Indigenous knowledge** - when done ethically, AI can help preserve endangered cultural heritage
4. **Methodology matters** - hybrid human-AI approaches balance efficiency with accuracy
5. **This works** - 5.3% improvement, p < 0.000001, medium-large effect size

**Slide 24: Thank You**
- "Nĩ tũkahoreria" (We shall meet again) - Kikuyu closing
- Contact info
- GitHub repo: github.com/ndethi/opit-rai9001
- Open-source: Code + Ontology available for research use
- Cultural note: Ontology under restricted license - requires community permission for commercial use

---

## Design Notes for Gamma

**Visual Elements to Include:**
- Kenyan/Kikuyu cultural imagery (traditional patterns, earth tones)
- Knowledge graph visualizations (Neo4j screenshots)
- Bar charts for quantitative results (use color-blind friendly palette)
- Architecture diagrams (clean, professional)
- Before/After translation comparisons (side-by-side)
- Proverb examples in both Kikuyu and English (use contrasting fonts)

**Typography:**
- Kikuyu text: Use serif font for authenticity
- Technical terms: Sans-serif for clarity
- Emphasis: Bold for key numbers (0.79, p < 0.000001, 5.3%)

**Accessibility:**
- All charts have text labels, not just color
- High contrast text
- Font size minimum 18pt for body text
- Alternative text for all images

**Storytelling Arc:**
1. Hook with real example (Slide 2)
2. Build tension (the problem is HARD)
3. Present solution (we built a cultural GPS)
4. Prove it works (rigorous evaluation)
5. Acknowledge limits (we're honest)
6. Inspire future (this is just the beginning)

---

## Technical Terms Glossary (Use ELI10 Versions When Explaining)

**For Non-Technical Audience:**
- **Ontology** → "Like a cultural encyclopedia that shows how concepts connect"
- **RAG** → "Giving the AI relevant knowledge before it translates (open-book exam)"
- **BLEU** → "Translation metric that counts word matches (too strict for culture)"
- **COMET** → "Smart metric that understands meaning, not just words"
- **p < 0.000001** → "Results are statistically rock-solid, not random luck"
- **Cohen's d = 0.73** → "Improvement is large enough to see clearly, not tiny"

**For Technical Audience:**
- **Neo4j** → "Graph database for ontology storage and traversal-based retrieval"
- **Sentence-BERT** → "768-dimensional embeddings, cosine similarity for semantic search"
- **Hybrid retrieval** → "Graph traversal + vector similarity for context assembly"
- **Paired t-tests** → "Within-subjects design, Bonferroni-corrected significance threshold"
- **Knowledge graph** → "Property graph: nodes (concepts/proverbs), edges (relationships/themes)"

---

## Delivery Tips for Presenter

**Timing:**
- Opening (Slides 1-4): 4 minutes - Hook them with the problem
- Background (Slides 5-8): 5 minutes - Build credibility and context
- Solution (Slides 9-13): 7 minutes - Core technical contribution
- Evaluation (Slides 14-19): 8 minutes - Prove it works with data
- Contributions (Slides 20-22): 4 minutes - Broader impact
- Closing (Slides 23-24): 2 minutes - Strong finish

**Engagement Strategies:**
- Start with "Imagine you need to translate..." (make it relatable)
- Use Slide 2 example throughout (callback to "Andu ni indo")
- Acknowledge elephant in room: "You might wonder why we used LLMs to build a cultural ontology..." (address on Slide 11)
- Be confident about limitations (Slide 21) - shows intellectual honesty
- End with cultural proverb in Kikuyu (Slide 24) - brings it full circle

**Anticipated Questions:**
- Q: "Why not just hire more translators?"
  - A: "Scalability + preservation - we need systems that can help translators, not replace them, and ontologies can be reused"
  
- Q: "How do you prevent cultural appropriation?"
  - A: "Restricted license, community permission for commercial use, benefit-sharing model (Slide 24 note)"
  
- Q: "Single evaluator - isn't that a problem?"
  - A: "Yes, acknowledged limitation (Slide 21). Mitigated by cross-validation with published sources. Common in low-resource language research due to expert scarcity"
  
- Q: "Can this work for other languages?"
  - A: "Yes - principle is domain-agnostic. Already shown for medicine (MedRAG). Cultural domains have similar hierarchical structure"

---

**Final Note to Gamma AI:**  
Generate slides that are **visually compelling**, **intellectually rigorous**, and **accessible to mixed audiences**. Balance technical precision with storytelling. Use the ELI5/ELI10 glossary to make complex concepts digestible without dumbing them down. Show confidence in the work while acknowledging limitations honestly. This is a PhD defense - the committee wants to see you OWN the research while showing humility about what remains unknown.
