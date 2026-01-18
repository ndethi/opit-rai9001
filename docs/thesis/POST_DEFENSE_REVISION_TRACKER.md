# POST-DEFENSE REVISION TRACKER

**Date Started**: January 16, 2026  
**Branch**: `post-defense`  
**Purpose**: Incorporate defense feedback and align thesis with dissertation presentation

---

## REVISION EXECUTION PLAN

### Priority Order (As Per Prompt)

1. **✅ DIRECTIVE 3**: Bibliography Audit (CRITICAL - Academic Integrity)
2. **⏳ DIRECTIVE 1**: Evaluation Methodology Transparency
3. **⏳ DIRECTIVE 4**: Deformalize Hypothesis Statements
4. **⏳ DIRECTIVE 5**: Update Ontology Description
5. **⏳ DIRECTIVE 2**: Add Chat Interface Future Work
6. **⏳ DIRECTIVE 6**: General Quality Improvements

---

## CRITICAL CONTEXT (From Addendum)

**Key Understanding:**
- Dissertation (defense doc) DID disclose automated evaluation honestly
- Thesis needs to ALIGN with what was presented during defense
- This is STANDARD thesis revision (not damage control)
- Frame as: "Incorporating clarifications from defense discussion"

**Framing to Use:**
- ✅ "Incorporating clarifications from defense discussion"
- ✅ "Aligning final thesis with defense presentation"
- ✅ "As discussed during defense"
- ❌ "Correcting errors in original thesis"
- ❌ "Admitting evaluation was informal"

---

## DIRECTIVE 1: EVALUATION METHODOLOGY TRANSPARENCY

### Files to Update:
- [ ] `chapters/03-methodology.tex` - Section 3.6 (complete rewrite)
- [ ] `chapters/05-evaluation.tex` - Chapter 4 introduction
- [ ] `chapters/06-discussion.tex` - Section 5.1 Limitations
- [ ] `chapters/07-conclusion.tex` - Section 5.3 Future Work

### Implementation Verification Checklist:
- [ ] Checked `/src/evaluation/cultural_metrics.py` - confirm automated framework
- [ ] Checked `/src/evaluation/llm_judge.py` - confirm Gemini 2.5
- [ ] Checked `/outputs/evaluation/` - verify no human evaluation files
- [ ] Checked `/data/results/cultural_evaluation_100proverbs.csv` - confirm columns

### Key Changes:
- [ ] Section 3.6.1: Add dual-automated approach description
- [ ] Section 3.6.2: Detail cultural metrics (sentence transformers, ROUGE)
- [ ] Section 3.6.3: Detail LLM-as-judge (Gemini 2.5)
- [ ] Section 3.6.4: NEW - Informal researcher review (non-systematic)
- [ ] Section 3.6.5: NEW - Evaluation validity discussion
- [ ] Section 3.6.6: NEW - Future human validation study
- [ ] Chapter 4 intro: Clarify all results from automated metrics
- [ ] Section 5.1.4: NEW - Add limitation on lack of human evaluation

---

## DIRECTIVE 2: FUTURE WORK - CHAT INTERFACE

### Files to Update:
- [ ] `chapters/07-conclusion.tex` - Add Section 5.3.X

### Key Changes:
- [ ] Add new subsection: "Interactive Chatbot Interface"
- [ ] Preserve all existing future work sections
- [ ] Update abstract if it mentions future work
- [ ] Update Section 1.4 contributions

---

## DIRECTIVE 3: BIBLIOGRAPHY AUDIT (HIGHEST PRIORITY)

### Files to Check:
- [ ] `references/references.bib` - Main bibliography file
- [ ] All chapter `.tex` files - In-text citations

### Verification Process:
- [ ] Export all citations to spreadsheet
- [ ] Google Scholar verify EVERY citation
- [ ] Check publication years (2025-2026 citations suspicious)
- [ ] Verify authors exist
- [ ] Verify venues are real
- [ ] Match claims to actual paper content

### High-Risk Sections (Check First):
- [ ] Chapter 2: Section 2.4 (Cultural Translation)
- [ ] Chapter 2: Section 2.3 (Knowledge Graphs)
- [ ] Chapter 2: Any Kikuyu/African NLP citations

### Replacement Strategy:
- [ ] Create list of FAKE citations
- [ ] Find real alternatives or remove claims
- [ ] Use verified foundational papers list (from prompt)

---

## DIRECTIVE 4: DEFORMALIZE HYPOTHESES

### Files to Update:
- [ ] `chapters/01-introduction.tex` - Section 1.3 Research Questions
- [ ] `chapters/03-methodology.tex` - Section 3.1 Research Design
- [ ] `chapters/05-evaluation.tex` - Results language

### Find-and-Replace Patterns:
- [ ] H1/H2/H3 → RQ1/RQ2/RQ3
- [ ] "We hypothesize" → "We investigate"
- [ ] "hypothesis-driven" → "research question-guided"
- [ ] "H1 was confirmed" → "RQ1 findings indicate"
- [ ] "supporting our hypothesis" → "supporting the exploratory finding"

### Key Additions:
- [ ] Section 1.3: Rewrite as exploratory research questions
- [ ] Section 3.1: Add exploratory design justification
- [ ] Results: Change framing from confirmatory to exploratory

---

## DIRECTIVE 5: UPDATE ONTOLOGY DESCRIPTION

### Repository Verification:
- [ ] Count actual nodes in Neo4j database
- [ ] Count actual relationships
- [ ] List all relationship types
- [ ] Verify cultural concept categories
- [ ] Check if OWL files exist

### Files to Update:
- [ ] `chapters/03-methodology.tex` - Section 3.3

### Key Updates:
- [ ] Use EXACT node counts from repository
- [ ] Use EXACT relationship counts
- [ ] List ALL relationship types with descriptions
- [ ] Match cultural concept categories to implementation
- [ ] Verify OWL claims (or remove if not implemented)

---

## DIRECTIVE 6: GENERAL QUALITY IMPROVEMENTS

### Consistency Checks:
- [ ] Terminology standardization (OG-RAG, Kikuyu, GPT-4, Neo4j)
- [ ] Verb tense by section (past for methods/results, present for intro/discussion)
- [ ] Citation style consistency (ACL or APA)

### Figure/Table Quality:
- [ ] All figures have descriptive captions
- [ ] All tables referenced in text before appearing
- [ ] Readable fonts and high resolution
- [ ] Accessible colors

### Content Optimization:
- [ ] Abstract structure (context, gap, approach, results, significance)
- [ ] Strong introduction hook
- [ ] Clear contribution statement (Section 1.4)
- [ ] Complete limitations section
- [ ] Formatting polish (page numbers, headings, spacing)

---

## VERIFICATION CHECKLIST (From Addendum)

**After completing revision, verify:**

- [ ] Section 3.6 describes dual-automated framework as PRIMARY
- [ ] Section 3.6.4 clearly marks informal review as non-systematic
- [ ] Chapter 4 intro states results from automated metrics
- [ ] Section 5.1 includes limitation on lack of independent validation
- [ ] Optional: Note on defense discussion added to Section 3.6 intro
- [ ] No language suggesting "correcting errors" or "fixing mistakes"
- [ ] Framing emphasizes standard thesis revision process

---

## SUCCESS CRITERIA

**Revision complete when:**

1. [ ] Supervisor's five feedback points all addressed
2. [ ] No hallucinated citations remain (100% bibliography verified)
3. [ ] Evaluation methodology accurately reflects implementation
4. [ ] Research appropriately framed as exploratory
5. [ ] Ontology description matches repository
6. [ ] Document meets OPIT formatting requirements
7. [ ] Ready for AI4AL 2025 submission

---

## CHANGE LOG

### Session 1: January 16, 2026

**Started**: Bibliography Audit (Directive 3)
- Status: IN PROGRESS
- Next: Continue systematic verification

---

## NOTES

- Working on `post-defense` branch (defense version preserved in `supervisor-revisions`)
- All changes track what was discussed during January 14, 2026 defense
- Maintain academic rigor while enhancing transparency
- Frame all updates as standard thesis revision incorporating defense feedback

