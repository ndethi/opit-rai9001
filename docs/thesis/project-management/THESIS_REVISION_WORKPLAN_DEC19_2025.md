# Thesis Revision Workplan - December 19, 2025

**Priority**: URGENT - For supervisor approval  
**Backup Created**: `thesis-checkpoint-dec19-pre-annotator-revision`  
**Focus**: Address evaluation methodology, reduce AI writing markers, acknowledge LLM-assisted ontology construction

---

## CRITICAL REVISIONS

### 1. TITLE CORRECTION
**Current**: "thiLLMo: Culturally Faithful Kikuyu Proverb Translation Using Ontology-Grounded RAG"  
**Proposed**: "thiLLMo: Ontology-Grounded RAG for Culturally Faithful Kikuyu-English Proverb Translation"  
**Rationale**: Explicitly states the translation direction (Kikuyu→English)

**Files to modify**:
- [ ] `main.tex` line 24
- [ ] Any abstract or summary sections

---

### 2. EVALUATION METHODOLOGY - SINGLE EXPERT EVALUATOR

**MAJOR CHANGE**: Reframe from "two annotators/three annotators" to single expert evaluator (author) with future work framing.

#### Chapter 3: Methodology (03-methodology.tex)

**Line 156-167** - Replace "Two native Kikuyu speakers" section:
```
CURRENT: Two native Kikuyu speakers with demonstrated cultural competence (both elders over age 60 with traditional knowledge) independently evaluated all 300 translations.

NEW: Expert human evaluation was conducted by a native Kikuyu speaker (L1, age 35, Murang'a dialect) with advanced training in linguistics and cultural studies. As a member of the Kikuyu community with deep cultural knowledge gained through family and community engagement, the evaluator assessed all translations using established cultural knowledge bases as reference points.
```

**Line 221-238** - Remove/revise Annotator Information table:
```
REMOVE: Table showing two evaluators (ages 62 and 68)
REPLACE WITH: Single evaluator profile acknowledging use of published expert sources (Ireri, Gikandi) as validation references
```

**Line 165** - Remove Krippendorff's alpha inter-rater reliability:
```
REMOVE: Inter-rater reliability was assessed using Krippendorff's alpha, achieving α = 0.78...
REPLACE WITH: Translation quality was validated against published Kikuyu proverb collections (Ireri 2017, Gikandi 1982) and expert cultural references to ensure authenticity.
```

**Flowchart (methodology-flowchart.tex line 23)**:
```
CURRENT: \node[activity, right=of p5] (a5) {3 annotators\\9 metrics};
NEW: \node[activity, right=of p5] (a5) {Expert eval\\9 metrics};
```

#### Chapter 6: Discussion - Add Limitations Section

**Add new subsection after line 150** in limitations:
```
\paragraph{Single Evaluator Limitation}

The human evaluation was conducted by a single expert evaluator rather than multiple independent annotators. While the evaluator is a native Kikuyu speaker with strong cultural grounding, this design limits inter-rater reliability assessment and introduces potential individual bias. This constraint reflects the practical challenges of recruiting multiple Kikuyu language experts with both traditional cultural knowledge and translation expertise—a scarcity common in low-resource language research.

To mitigate this limitation, evaluations were validated against established published sources: Ireri's (2017) comprehensive proverb collection and Gikandi's (1982) cultural analysis. Additionally, the evaluation framework employed detailed rubrics (Tables~\ref{tab:cultural_rubric} and~\ref{tab:fidelity_rubric}) to standardize scoring and reduce subjective variation.

Future work should incorporate a panel of diverse evaluators representing different Kikuyu dialects, age groups, and geographic regions to capture the full spectrum of cultural interpretation. Establishing such a panel faces challenges including: (1) identification of qualified experts across diaspora and rural communities, (2) resource constraints for compensating multiple expert evaluators, and (3) concerns among some community members about extractive Western research practices that have historically appropriated indigenous knowledge without benefit-sharing.
```

---

### 3. LLM-ASSISTED ONTOLOGY CONSTRUCTION

**Critical**: Acknowledge throughout that ontology development was LLM-assisted while framing as both limitation and innovation.

#### Chapter 3: Methodology (03-methodology.tex)

**Around line 60-85** - Ontology Construction section, add:
```
INSERT AFTER ontology construction methodology description:

\paragraph{LLM-Assisted Concept Extraction}

Ontology development employed a hybrid human-AI approach. Initial concept extraction utilized GPT-4 to analyze Kikuyu proverb collections and propose candidate cultural concepts, relationships, and thematic clusters. These LLM-generated suggestions were then validated, refined, and extended by the researcher (native Kikuyu speaker) in consultation with published cultural references.

This LLM-assisted methodology offers both advantages and limitations. On the positive side, it dramatically accelerated the ontology development process, enabling rapid identification of conceptual patterns across hundreds of proverbs—a task that would require months of manual analysis. The LLM's pattern recognition capabilities helped surface non-obvious connections between cultural domains.

However, LLM assistance introduces potential noise and cultural misinterpretations. While GPT-4 demonstrated reasonable understanding of Kikuyu cultural concepts, it occasionally proposed mappings influenced by Western cultural frameworks or conflated distinct Kikuyu concepts. Approximately 15-20\% of LLM suggestions were rejected or significantly modified during expert review.

This hybrid approach represents a pragmatic solution to the resource constraints facing low-resource language research. While a fully expert-driven ontology developed through extensive community consultation would be ideal, such efforts require substantial funding and time (estimated 2-3 years for comprehensive coverage). The LLM-assisted methodology delivers a functional ontology within research timeline constraints while maintaining cultural authenticity through expert validation.

Future work should explore more rigorous ontology construction processes, including: participatory design workshops with Kikuyu cultural elders, systematic validation against ethnographic literature, and community review mechanisms allowing broader Kikuyu participation in knowledge structuring.
```

#### Chapter 6: Discussion - Technical Limitations

**Add after Ontology Incompleteness paragraph (around line 165)**:
```
\paragraph{LLM-Assisted Construction Artifacts}

The ontology's development through LLM-assisted concept extraction, while pragmatic, may have introduced systematic biases. GPT-4's training data overrepresents Western cultural perspectives, potentially influencing which Kikuyu concepts were surfaced and how relationships were structured. Manual expert validation mitigated but could not entirely eliminate such biases.

Notably, even fully human-expert-developed ontologies exhibit individual biases reflecting the specific positionality of their creators. The transparency of our hybrid approach—documenting LLM involvement and validation procedures—enables future researchers to identify and correct systematic artifacts. All ontology development decisions are version-controlled with commit messages documenting LLM vs. human contributions.
```

---

### 4. REDUCE AI WRITING MARKERS

**Target**: Remove excessive em dashes (—) and "contrast framing" phrases throughout.

#### Em Dash Removal Strategy

**Search pattern**: `—` (em dash)  
**Review each instance**: Replace with period + new sentence, semicolon, or restructure

**High-priority files**:
- [ ] 01-introduction.tex
- [ ] 02-literature-review-v2.0.0.tex  
- [ ] 06-discussion.tex
- [ ] 07-conclusion.tex

#### Contrast Framing Removal

**Phrases to find and rewrite**:
- "These aren't just statistical improvements; they represent..." → "These statistical improvements represent..."
- "and here's the uncomfortable truth:" → Remove, state directly
- "Yet the X raises a deceptively simple question:" → "The X raises an important question:"
- "But here's what made these results more than just..." → "These results were significant because..."

**Specific instances identified**:

**02-literature-review-v2.0.0.tex, line 100**:
```
CURRENT: These aren't just statistical improvements; they represent genuine advances in the reliability of AI systems for healthcare applications.
NEW: These statistical improvements represent genuine advances in AI system reliability for healthcare applications.
```

**02-literature-review-v2.0.0.tex, line 22**:
```
CURRENT: But here's what made these results more than just disappointing statistics—the errors weren't random.
NEW: These results revealed systematic patterns: the errors were not random.
```

**06-discussion.tex, line 6**:
```
CURRENT: Yet the 10.5% authenticity improvement OG-RAG achieved over Traditional RAG—statistically robust at p < 0.000001—raises a deceptively simple question: why does structure matter?
NEW: The 10.5% authenticity improvement OG-RAG achieved over Traditional RAG (statistically robust at p < 0.000001) raises an important question: why does structure matter?
```

---

### 5. ADD thiLLMo NAMING EXPLANATION

**Location**: Chapter 1, Section 1.1 or 1.2  
**Content**: Brief explanation of the portmanteau

**Insert in 01-introduction.tex after line 6** (after chapter label, before section 1.1):
```
\section*{About the Name}
\addcontentsline{toc}{section}{About the Name}

\textbf{thiLLMo} is a portmanteau combining:
\begin{itemize}
    \item \textbf{``Thimo''} (pronounced ``thee-mo'')—the Kikuyu word for proverbs
    \item \textbf{``LLM''}—Large Language Model
\end{itemize}

\textbf{Pronunciation}: /ˈθiːlmoʊ/ (``theel-mo'')

This name reflects the project's core mission: bridging traditional Kikuyu wisdom (\emph{thimo}) with modern AI technology (LLM) to create culturally faithful translations that preserve the deep cultural significance of traditional sayings.

\medskip
```

---

### 6. PROVERB TRANSLATION CORRECTIONS

#### Chapter 1 - Introduction (01-introduction.tex)

**Line 12** - Mutumia proverb correction:
```
CURRENT: Consider the Kikuyu proverb \emph{``Mũtumia mũgima ndagagĩrwo nĩ thĩĩna''} (``A good wife is never troubled by poverty'').

NEW: Consider the Kikuyu proverb \emph{``Mũtumia mũgima ndagagwo nĩ thĩĩna''} (``A mature woman is never exempt from trouble'').
```

**Action required**: Verify ALL proverb translations in thesis against Ireri (2017) corpus to ensure accuracy.

---

### 7. ADDITIONAL LIMITATIONS TO ADD

#### Chapter 6: Discussion - Ethical Considerations

**Add new paragraph in subsection 6.3.2 (around line 212)**:
```
\paragraph{Limited Access to Cultural Elders and Community Review}

Securing participation from Kikuyu cultural elders for comprehensive evaluation and ontology validation proved challenging. Multiple factors contributed: (1) many knowledge holders reside in rural areas with limited digital access, (2) historical extractive research practices have created legitimate skepticism about Western academic engagement with indigenous knowledge, and (3) cultural protocols require extended relationship-building before knowledge-sharing, timelines incompatible with academic research deadlines.

This limitation necessitated reliance on published sources (Ireri, Gikandi) and individual researcher expertise rather than the community-engaged approach that would be ideal. Future work should allocate extended timelines for building trust with cultural elder councils, establishing benefit-sharing agreements that ensure community ownership of resulting knowledge resources, and creating mechanisms for ongoing community governance of ontology evolution.
```

**Add to resource constraints section**:
```
\paragraph{Corpus and Computational Resource Constraints}

The evaluation corpus size (100 proverbs) reflects practical constraints: (1) limited availability of published, expert-validated Kikuyu proverb collections with verified translations, and (2) the intensive expert labor required for high-quality translation validation. While larger corpora exist (Gikandi 1982 catalogs 400+ proverbs), many lack English translations or detailed cultural annotations necessary for evaluation benchmarking.

Computational resources also constrained experimental scope. LLM API costs (approximately \$350 for full evaluation) limited the number of model comparisons and prevented large-scale hyperparameter tuning. Future work with institutional computational resources could explore broader model comparisons and larger evaluation sets.
```

---

### 8. TECHNICAL FIXES REQUIRED

#### Chapter 5: Results - Box Plot Issue

**Line reference**: Section 5.4 - Score Distribution Analysis  
**Issue**: Empty box plots  
**Action**: 
- [ ] Check if figure files exist in figures/ directory
- [ ] Regenerate visualizations using evaluation data
- [ ] Verify LaTeX figure references are correct

#### Research Questions Alignment

**Action required**:
- [ ] Read RQ definitions in Chapter 1 (lines ~130-145)
- [ ] Read RQ answers in Chapter 6 (Section 6.1.1, 6.1.2, 6.1.3)
- [ ] Verify exact alignment and numbering consistency
- [ ] Check that all RQs defined are answered

---

### 9. FUTURE WORK ADDITIONS

#### Chapter 7: Conclusion

**Add to future work section (around line 30)**:
```
\paragraph{Expanded Human Evaluation Panel}

A critical priority for future work is establishing a diverse panel of expert evaluators representing different Kikuyu sub-groups, age cohorts, and geographic regions. The current study's reliance on a single evaluator, while methodologically necessary given resource constraints, limits assessment of dialectical variation and generational differences in cultural interpretation.

This expansion requires addressing practical challenges: developing protocols for identifying and recruiting cultural experts across diaspora communities, establishing fair compensation frameworks that respect expert knowledge as intellectual labor, and building trust with communities wary of extractive research practices. Potential approaches include: partnering with Kikuyu cultural organizations, leveraging existing networks of language educators, and piloting community-based participatory research models where evaluation design is co-created with cultural stakeholders.
```

---

### 10. LINGUISTIC EXPERTISE LIMITATION

#### Chapter 6: Limitations

**Add new paragraph**:
```
\paragraph{Linguistic Expertise for Low-Resource Languages}

The analysis of Kikuyu linguistic structures (syntax, morphology, tonal patterns) relied heavily on published grammars and documentation, as the researcher's native speaker competence, while valuable, does not substitute for formal linguistic training. Low-resource languages like Kikuyu lack the extensive linguistic infrastructure available for high-resource languages—detailed syntactic databases, comprehensive phonological descriptions, large-scale corpus annotations.

This disparity meant certain linguistic phenomena (e.g., tonal variations in proverb delivery, dialectical morphological differences) could not be systematically analyzed. The ontology's focus on semantic and cultural dimensions partially compensates, but a linguistically richer representation would benefit from collaboration with Kikuyu language specialists.
```

---

## EXECUTION PRIORITY

### Phase 1: CRITICAL (Complete before supervisor submission)
1. ✅ Create backup checkpoint
2. [ ] Fix title (main.tex)
3. [ ] Revise evaluation methodology (single evaluator)
4. [ ] Add LLM-assisted ontology acknowledgments
5. [ ] Fix mutumia proverb translation
6. [ ] Add thiLLMo naming explanation
7. [ ] Add single evaluator limitation
8. [ ] Add elder access limitation
9. [ ] Add resource constraints limitation

### Phase 2: IMPORTANT (Can complete shortly after submission)
10. [ ] Remove em dashes throughout
11. [ ] Remove contrast framing phrases
12. [ ] Verify all proverb translations against Ireri
13. [ ] Check research questions alignment
14. [ ] Fix empty box plots

### Phase 3: POLISH (Before final defense)
15. [ ] Add linguistic expertise limitation
16. [ ] Expand future work section
17. [ ] Review cultural appropriation section
18. [ ] Final consistency check

---

## NOTES FOR LATER: PRESENTATION GUIDE

*To be developed separately - ELI5/ELI10 explanations for:*
- ngwatio (reciprocity systems)
- traditional banking systems
- BLEU, CHRF, COMET metrics
- Statistical power (Cohen's d)
- Hypothesis testing
- Paired t-tests
- Bonferroni correction
- Krippendorff's alpha (if kept)
- Musique dataset, HotpotQA
- MedRAG, UMLS
- OOPS!, OWL
- Sentence-BERT embeddings
- Lexical Jaccard similarity
- Polysemous terms
- Denotative meaning

---

## VALIDATION CHECKLIST

After making revisions:
- [ ] Compile LaTeX successfully (no errors)
- [ ] Check page count (stay within limits)
- [ ] Verify all citations render correctly
- [ ] Spell check entire document
- [ ] Read through for flow and coherence
- [ ] Confirm all figures/tables referenced correctly
- [ ] Check that table of contents updates properly

---

**Last Updated**: December 19, 2025  
**Estimated Revision Time**: 4-6 hours for Phase 1  
**Backup Location**: `docs/thesis-checkpoint-dec19-pre-annotator-revision/`
