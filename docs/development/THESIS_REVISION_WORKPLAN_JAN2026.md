# thiLLMo Thesis Revision Workplan
## Supervisor Feedback Implementation - 16-Day Sprint

**Created:** December 18, 2025  
**Target Completion:** January 10, 2026 (16 working days)  
**Current State:** 130 pages, 7 critical issues identified  
**Target State:** 90-100 pages, distinction-level presentation

---

## Executive Summary

### Revision Scope
- **7 supervisor feedback items** requiring systematic implementation
- **3 high-priority blockers** that must be completed first
- **40 pages reduction** through strategic content consolidation
- **New content additions** for methodological rigor and transparency
- **2 architecture diagrams** for technical clarity

### Success Metrics
| Metric | Current | Target | Delta |
|--------|---------|--------|-------|
| Total Pages | 130 | 90-100 | -30 to -40 |
| Chapter 2 (Lit Review) | ~25 | 15 | -10 |
| Chapter 3 (Methodology) | ~30 | 20 | -10 |
| Chapter 7 (Conclusion) | ~15 | 8 | -7 |
| Placeholder References | 8+ | 0 | -8+ |
| Architecture Diagrams | 0 | 2 | +2 |
| Formal Hypotheses | 0 | 1 section | +1 |
| Evaluation Transparency | Incomplete | Complete | +3 sections |

---

## PHASE 1: Critical Blockers (Days 1-5)

### DAY 1: Setup & Placeholder Fixes (8 hours)

**Morning Session (4 hours)**
- [ ] **1.1** Create git branch `supervisor-revisions`
- [ ] **1.2** Backup current thesis state
  - Copy `docs/thesis/` to `docs/thesis-backup-2025-12-18/`
  - Create archive tag in git: `git tag v1.0-supervisor-submission`
- [ ] **1.3** Compile current version, verify page count (130 pages)
- [ ] **1.4** Create tracking document: `REVISION_PROGRESS.md`

**Afternoon Session (4 hours)**
- [ ] **1.5** Search and fix ALL "Chapter ??" placeholders
  - Search pattern: `Chapter \?\?|Section \?\?|Figure \?\?|Table \?\?|Appendix \?\?`
  - Create replacement mapping document
  - Use context keywords to determine correct chapter numbers
- [ ] **1.6** Fix cross-reference issues
  - Verify all `\ref{sec:...}` have corresponding `\label{sec:...}`
  - Check `\ref{fig:...}` and `\ref{tab:...}` references
- [ ] **1.7** Compile LaTeX, verify no errors
- [ ] **1.8** Commit: "Fix all placeholder chapter/section references"

**Deliverables:**
- ✅ Clean backup created
- ✅ Zero "??" placeholders remaining
- ✅ Error-free LaTeX compilation
- ✅ Git commit with fixed references

**Quality Check:**
```bash
# Search for remaining placeholders
grep -r "Chapter ??" docs/thesis/chapters/
grep -r "Section ??" docs/thesis/chapters/
grep -r "Figure ??" docs/thesis/chapters/
# Should return: no results
```

---

### DAY 2-3: Formal Hypotheses Section (12 hours)

**DAY 2 Morning (4 hours)**
- [ ] **2.1** Create new Section 1.4 in `chapters/01-introduction.tex`
  - Insert after Section 1.3 (Problem Statement)
  - Before current Section 1.4 (Research Objectives)
- [ ] **2.2** Write hypothesis introduction paragraph
- [ ] **2.3** Write null hypotheses (H₀¹, H₀², H₀³)
  - Cultural Authenticity
  - Translation Fidelity  
  - Semantic Preservation
- [ ] **2.4** Write alternative hypotheses (H₁, H₂, H₃)
  - Include predicted effect sizes (10%, 15%, 5%, etc.)
  - Add statistical parameters (p < 0.05, d ≥ 0.5)

**DAY 2 Afternoon (4 hours)**
- [ ] **2.5** Write statistical validation approach paragraph
  - Paired t-tests methodology
  - Effect size calculations (Cohen's d)
  - Power analysis justification
- [ ] **2.6** Write expected outcomes paragraph
  - Reference preliminary results (10.5%, 19.8%)
- [ ] **2.7** Add required citations
  - Papineni et al. (2002), Callison-Burch et al. (2006)
  - Cohen (1988), Sawilowsky (2009)
  - Field (2013), Winter (2019)
- [ ] **2.8** Add to `references/references.bib` if missing

**DAY 3 Morning (4 hours)**
- [ ] **2.9** Renumber ALL subsequent sections in Chapter 1
  - Old 1.4 → New 1.5 (Research Objectives)
  - Old 1.5 → New 1.6 (Research Questions)
  - Old 1.6 → New 1.7 (Scope and Limitations)
  - Old 1.7 → New 1.8 (Thesis Structure)
  - Old 1.8 → New 1.9 (Summary)
- [ ] **2.10** Update all internal references to Chapter 1 sections throughout thesis
- [ ] **2.11** Update Table of Contents
- [ ] **2.12** Compile and verify numbering correct

**Deliverables:**
- ✅ New Section 1.4 "Research Hypotheses" complete (~2 pages)
- ✅ All subsequent sections renumbered
- ✅ All cross-references updated
- ✅ Clean LaTeX compilation
- ✅ Git commit: "Add formal hypotheses section (Section 1.4)"

**Quality Check:**
- Hypotheses clearly stated: 3 null + 3 alternative ✓
- Predicted effects quantified (10%, 15%, 5%) ✓
- Statistical methods specified (paired t-test, α=0.05) ✓
- All citations present in bibliography ✓

---

### DAY 4-5: Evaluation Transparency (12 hours)

**DAY 4 Morning (4 hours)**
- [ ] **3.1** Create new Section 3.6.6 in `chapters/03-methodology.tex`
  - Title: "Annotator Information and Inter-Rater Reliability"
  - After Section 3.6.5 (Qualitative Analysis Methods)
- [ ] **3.2** Write Subsection A: Annotator Selection Criteria (1 paragraph)
  - Native/fluent Kikuyu speakers
  - Cultural knowledge requirements
  - Educational background
  - Geographic representation
- [ ] **3.3** Write Subsection B: Annotator Profile (1-2 paragraphs)
  - **ACTION REQUIRED:** Gather actual data on annotators
  - Number (N = ?)
  - Demographics (age, gender, location)
  - Professional background breakdown
  - Experience levels

**DAY 4 Afternoon (4 hours)**
- [ ] **3.4** Write Subsection C: Training Protocol (1-2 paragraphs)
  - Pre-evaluation session duration
  - Calibration exercises performed
  - Rubric familiarization process
  - Consensus building procedures
- [ ] **3.5** Write Subsection D: Inter-Annotator Agreement (2 paragraphs)
  - Cohen's Kappa formula and explanation
  - **ACTION REQUIRED:** Calculate actual κ value from data
  - Interpretation using standard thresholds
  - Disagreement resolution protocol
  - Add citations: Artstein & Poesio (2008), Fleiss (1971), Krippendorff (2004)
- [ ] **3.6** Write Subsection E: Ethical Considerations (1 paragraph)
  - Compensation structure
  - Informed consent
  - Data privacy/anonymization
  - IRB status

**DAY 5 Morning (4 hours)**
- [ ] **3.7** Enhance Section 3.6.2 "Evaluation Metrics"
- [ ] **3.8** Create Table 3.2: Cultural Authenticity Scoring Rubric
  - 5-point scale with criteria, indicators, examples
  - Include Kikuyu-specific example
  - LaTeX tabular format
- [ ] **3.9** Create Table 3.3: Translation Fidelity Scoring Rubric
  - 5-point scale with detailed criteria
- [ ] **3.10** Create Table 3.4: Common Evaluation Scenarios
  - Scenario descriptions
  - Dual scoring examples
  - Rationale explanations

**DAY 5 Afternoon (2 hours)**
- [ ] **3.11** Compile LaTeX, verify tables render correctly
- [ ] **3.12** Check table formatting (fits page width, readable fonts)
- [ ] **3.13** Update cross-references to new tables
- [ ] **3.14** Git commit: "Add evaluation transparency (Section 3.6.6 + Tables)"

**Deliverables:**
- ✅ Section 3.6.6 complete with 5 subsections (~3 pages)
- ✅ Three new tables (3.2, 3.3, 3.4) added
- ✅ Enhanced Section 3.6.2 with detailed rubrics
- ✅ All citations added to bibliography

**Quality Check:**
- Annotator information comprehensive ✓
- Inter-rater reliability calculated and interpreted ✓
- Scoring rubrics detailed with examples ✓
- Ethical considerations addressed ✓
- Tables properly formatted and referenced ✓

**ACTION ITEMS FOR USER:**
- Provide actual annotator count and demographics
- Provide calculated Cohen's Kappa value
- Confirm IRB status and compensation details

---

## PHASE 2: Major Content Reduction (Days 6-10)

### DAY 6-7: Literature Review Reduction (12 hours)

**DAY 6 Morning (4 hours)**
- [ ] **4.1** Create `chapters/appendix-a-literature-details.tex`
- [ ] **4.2** Structure Appendix A:
  ```latex
  \chapter{Extended Literature Review Details}
  \section{RAPTOR Methodology}
  \section{MuSiQue Benchmark}
  \section{Additional Evaluation Frameworks}
  ```
- [ ] **4.3** Identify content to move from Chapter 2:
  - Detailed RAPTOR methodology (recursive processing, tree construction)
  - MuSiQue benchmark composition and examples
  - Extended benchmark descriptions
  - Excessive background not supporting research gap
- [ ] **4.4** Move identified content to Appendix A

**DAY 6 Afternoon (4 hours)**
- [ ] **4.5** Edit Chapter 2 Section 2.5.2 (Specialized Benchmarks)
  - REPLACE long explanations with: "For detailed RAPTOR methodology, see Appendix~\ref{app:raptor}"
  - Keep only essential points supporting research narrative
- [ ] **4.6** Edit Chapter 2 overall:
  - Remove excessive background text
  - Shorten external model summaries
  - Keep only citations establishing research gap
  - Remove tutorial-style explanations
- [ ] **4.7** Add cross-references to Appendix A throughout Chapter 2

**DAY 7 Morning (4 hours)**
- [ ] **4.8** Continue Chapter 2 reduction:
  - Target: Remove ~2,500 words (10 pages)
  - Focus on condensing verbose paragraphs
  - Merge similar points
  - Remove redundant examples
- [ ] **4.9** Verify Chapter 2 narrative flow maintained
- [ ] **4.10** Compile and check page count
  - Target: ~15 pages for Chapter 2

**DAY 7 Afternoon (2 hours)**
- [ ] **4.11** Final Chapter 2 polish:
  - Ensure smooth transitions after cuts
  - Verify all citations remain
  - Check cross-references to Appendix A work
- [ ] **4.12** Git commit: "Reduce Chapter 2 to 15 pages, create Appendix A"

**Deliverables:**
- ✅ Chapter 2 reduced from ~25 to ~15 pages
- ✅ Appendix A created with moved content
- ✅ ~2,500 words removed
- ✅ Narrative flow preserved
- ✅ All cross-references functional

**Quality Check:**
```bash
# Check Chapter 2 page count
pdflatex main.tex
# Extract Chapter 2 page numbers from PDF
# Verify ~15 pages
```

---

### DAY 8-9: Methodology Refinement (12 hours)

**DAY 8 Morning (4 hours)**
- [ ] **5.1** Create `chapters/appendix-b-technical-details.tex`
- [ ] **5.2** Structure Appendix B:
  ```latex
  \chapter{Technical Implementation Details}
  \section{Cypher Query Examples}
  \section{Prompt Templates}
  \section{Statistical Test Formulas}
  \section{Configuration Specifications}
  ```
- [ ] **5.3** Identify content to move from Chapter 3:
  - Detailed Cypher query code
  - Complete prompt templates
  - Statistical formulas and derivations
  - Step-by-step procedures
  - Configuration file specs

**DAY 8 Afternoon (4 hours)**
- [ ] **5.4** Rewrite Section 3.1.1 "Methodological Rationale"
  - REMOVE: Generic CRISP-DM descriptions
  - REMOVE: Textbook explanations of standard phases
  - ADD: Why CRISP-DM suited for cultural translation
  - ADD: Specific adaptations made (3 key modifications)
  - ADD: Novel approach vs. alternatives justification
  - Target transformation: Tutorial → Research-focused
- [ ] **5.5** Apply research-focused pattern to Sections 3.2-3.7
  - Each phase: Remove generic procedures
  - Each phase: Emphasize research-specific decisions
  - Each phase: Show iterative connections
  - Each phase: Include problems/solutions encountered

**DAY 9 Morning (4 hours)**
- [ ] **5.6** Continue Chapter 3 reduction:
  - Move technical details to Appendix B
  - Replace long code examples with: "See Appendix~\ref{app:cypher} for complete Cypher queries"
  - Remove obvious procedural steps
  - Focus on novel contributions
- [ ] **5.7** Target: Remove ~3,000 words (10 pages)
- [ ] **5.8** Verify Chapter 3 page count: ~20 pages

**DAY 9 Afternoon (2 hours)**
- [ ] **5.9** Add cross-references to Appendix B throughout Chapter 3
- [ ] **5.10** Final Chapter 3 polish
- [ ] **5.11** Compile and verify
- [ ] **5.12** Git commit: "Refactor Chapter 3 to research-focus, create Appendix B"

**Deliverables:**
- ✅ Chapter 3 reduced from ~30 to ~20 pages
- ✅ Appendix B created with technical details
- ✅ ~3,000 words removed
- ✅ Tutorial style → Research-focused transformation
- ✅ Novel adaptations emphasized

**Quality Check:**
- Section 3.1.1 research-specific (not generic) ✓
- Each phase description focuses on THIS research ✓
- Technical details moved to appendix ✓
- ~20 pages achieved ✓

---

### DAY 10: Consolidation & Verification (6 hours)

**Morning Session (4 hours)**
- [ ] **6.1** Compile full thesis
- [ ] **6.2** Verify page counts:
  - Total: Should be 100-110 pages (down from 130)
  - Chapter 2: ~15 pages ✓
  - Chapter 3: ~20 pages ✓
- [ ] **6.3** Check Appendix A and B:
  - Properly formatted
  - All cross-references work
  - Content makes sense standalone
- [ ] **6.4** Verify narrative flow across thesis
  - Transitions smooth after cuts
  - No orphaned references
  - Logical progression maintained

**Afternoon Session (2 hours)**
- [ ] **6.5** Update main.tex to include appendices:
  ```latex
  \appendix
  \input{chapters/appendix-a-literature-details}
  \input{chapters/appendix-b-technical-details}
  ```
- [ ] **6.6** Final compilation and PDF generation
- [ ] **6.7** Git commit: "Phase 2 complete: Content reduction achieved"
- [ ] **6.8** Update REVISION_PROGRESS.md

**Deliverables:**
- ✅ Thesis reduced to ~100-110 pages
- ✅ All appendices integrated
- ✅ Narrative flow verified
- ✅ Clean compilation

**Milestone Check:**
- Phase 1 blockers: COMPLETE ✅
- Phase 2 reduction: COMPLETE ✅
- Ready for Phase 3: Visual enhancement ✅

---

## PHASE 3: Visual Enhancement (Days 11-12)

### DAY 11: System Architecture Diagram (8 hours)

**Morning Session (4 hours)**
- [ ] **7.1** Create diagram using draw.io, TikZ, or Python (networkx)
- [ ] **7.2** Design Figure 4.1: OG-RAG System Architecture
  - 5 layers (Data, Retrieval, Context Building, Generation, Evaluation)
  - Components per layer (as specified in directive)
  - Color-code by layer (Blue, Green, Orange, Purple, etc.)
  - Add technology labels
  - Mark novel contributions with star ⭐
  - Show data flow (solid arrows) and feedback loops (dashed)
- [ ] **7.3** Export formats:
  - PDF (for LaTeX inclusion)
  - PNG (300 DPI, for backup)
  - SVG (vector, for editing)
- [ ] **7.4** Save to `docs/thesis/figures/og_rag_architecture.pdf`

**Afternoon Session (4 hours)**
- [ ] **7.5** Write comprehensive caption (as specified)
- [ ] **7.6** Add to Chapter 4 after Section 4.1.2:
  ```latex
  \begin{figure}[htbp]
      \centering
      \includegraphics[width=0.95\textwidth]{figures/og_rag_architecture.pdf}
      \caption[OG-RAG System Architecture]{...}
      \label{fig:og-rag-architecture}
  \end{figure}
  ```
- [ ] **7.7** Add introductory paragraph before figure
- [ ] **7.8** Add referencing paragraph after figure
- [ ] **7.9** Add cross-references throughout Chapter 4:
  - Section 4.3.2: "The GraphRetriever class (see Figure~\ref{fig:og-rag-architecture}, Retrieval Layer)..."
  - Section 4.5: "The prompt construction process (Figure~\ref{fig:og-rag-architecture})..."
  - Section 4.8: "Latency optimization (visualized in Figure~\ref{fig:og-rag-architecture})..."
- [ ] **7.10** Compile, verify figure displays correctly
- [ ] **7.11** Git commit: "Add Figure 4.1: System Architecture Diagram"

**Deliverables:**
- ✅ Figure 4.1 created and integrated
- ✅ Multiple export formats saved
- ✅ Comprehensive caption written
- ✅ Surrounding text added
- ✅ Cross-references throughout Chapter 4

**Quality Check:**
- All 5 layers visible and labeled ✓
- Color-coding clear and colorblind-friendly ✓
- Technology labels readable ✓
- Novel contributions marked ⭐ ✓
- Figure displays at correct size in PDF ✓

---

### DAY 12: Retrieval Pipeline Diagram (8 hours)

**Morning Session (4 hours)**
- [ ] **8.1** Create Figure 4.2: Retrieval and Context Pipeline
- [ ] **8.2** Design 8-stage sequential pipeline (left-to-right):
  1. Input Stage (Kikuyu query)
  2. Embedding Stage (Sentence-BERT)
  3. Semantic Search (Vector index)
  4. Graph Traversal (Cypher)
  5. Context Serialization
  6. Prompt Construction
  7. LLM Generation (GPT-4)
  8. Post-Processing (JSON parsing)
- [ ] **8.3** Add details for each stage:
  - Example data/format
  - Latency annotation
  - Data size/format transformations
- [ ] **8.4** Use color coding for operation types (compute vs. I/O)
- [ ] **8.5** Export formats (PDF, PNG, SVG)
- [ ] **8.6** Save to `docs/thesis/figures/retrieval_pipeline.pdf`

**Afternoon Session (4 hours)**
- [ ] **8.7** Write comprehensive caption with example
- [ ] **8.8** Add to Chapter 4 after Section 4.3.1:
  ```latex
  \begin{figure}[htbp]
      \centering
      \includegraphics[width=\textwidth]{figures/retrieval_pipeline.pdf}
      \caption[Retrieval and Generation Pipeline]{...}
      \label{fig:retrieval-pipeline}
  \end{figure}
  ```
- [ ] **8.9** Add introductory paragraph before figure
- [ ] **8.10** Add referencing paragraph after figure
- [ ] **8.11** Add cross-references throughout Chapter 4 and Chapter 6
- [ ] **8.12** Compile, verify figure displays correctly
- [ ] **8.13** Git commit: "Add Figure 4.2: Retrieval Pipeline Diagram"

**Deliverables:**
- ✅ Figure 4.2 created and integrated
- ✅ 8 stages clearly shown with details
- ✅ Latency annotations added
- ✅ Example data shown
- ✅ Comprehensive caption written

**Quality Check:**
- Sequential flow clear (left-to-right) ✓
- Each stage labeled with component name ✓
- Latency shown for each stage ✓
- Example for "Mũtĩ wa mũtũũri ndũrĩ ũhoro" included ✓
- Total pipeline latency calculated ✓

---

## PHASE 4: Conclusion Refinement (Days 13-14)

### DAY 13: Restructure Chapter 7 (8 hours)

**Morning Session (4 hours)**
- [ ] **9.1** Backup current Chapter 7 to separate file
- [ ] **9.2** Create new Chapter 7 structure:
  ```latex
  \chapter{Conclusion and Future Work}
  \section{Overview}
  \section{Principal Findings}
  \subsection{Cultural Authenticity Improvement}
  \subsection{Translation Fidelity Enhancement}
  \section{Research Contributions}
  \subsection{Theoretical Contribution}
  \subsection{Methodological Contribution}
  \subsection{Practical Contribution}
  \section{Implications}
  \section{Limitations}
  \section{Future Directions}
  ```
- [ ] **9.3** Write Section 7.1 Overview (1 page, 250 words)
  - Problem restatement: 2-3 sentences ONLY
  - Solution summary: 2-3 sentences
  - Key results: Single paragraph with metrics (4.2/5.0, 4.5/5.0, etc.)
  - Chapter roadmap: 1 sentence
- [ ] **9.4** REMOVE from new version:
  - All methodology explanations
  - All result tables/figures
  - Repetition from earlier chapters

**Afternoon Session (4 hours)**
- [ ] **9.5** Write Section 7.2 Principal Findings (2 pages)
- [ ] **9.6** Write 7.2.1: Cultural Authenticity (1 page, 250 words)
  - Achievement statement: "10.5% improvement..."
  - Why it matters
  - Connection to research gap
  - Broader implication
  - NO methodology, NO tables
- [ ] **9.7** Write 7.2.2: Translation Fidelity (1 page, 250 words)
  - Achievement statement: "19.8% improvement..."
  - Why it matters
  - Unexpected finding
  - Implication
  - NO methodology, NO tables
- [ ] **9.8** Verify concise, forward-looking tone

**Deliverables:**
- ✅ New Chapter 7 structure created
- ✅ Sections 7.1-7.2 written (~3 pages)
- ✅ Zero repetition from earlier chapters
- ✅ Focused on achievements, not procedures

**Quality Check:**
- Active voice throughout ✓
- Specific numbers (10.5%, 19.8%, p<0.001) ✓
- No "In conclusion" or "To summarize" phrases ✓
- No methodology repetition ✓

---

### DAY 14: Complete Chapter 7 (8 hours)

**Morning Session (4 hours)**
- [ ] **10.1** Write Section 7.3: Research Contributions (2 pages)
- [ ] **10.2** Write 7.3.1: Theoretical Contribution (2-3 paragraphs)
  - Novel framework
  - Theoretical advance
  - Conceptual contribution
  - Impact on field
- [ ] **10.3** Write 7.3.2: Methodological Contribution (2-3 paragraphs)
  - Evaluation framework
  - Innovation
  - Reusability
  - Validation
- [ ] **10.4** Write 7.3.3: Practical Contribution (2-3 paragraphs)
  - Deliverable 1: OG-RAG implementation
  - Deliverable 2: Corpus of 100 proverbs
  - Deliverable 3: Cultural ontology
  - Impact

**Afternoon Session (4 hours)**
- [ ] **10.5** Write Section 7.4: Implications (1 page, 250 words)
  - For low-resource language NLP
  - For cultural heritage preservation
  - For RAG system design
  - For MT research
  - Each: 2-3 sentences
- [ ] **10.6** Write Section 7.5: Limitations (1 page, 250 words)
  - Sample size
  - Scope
  - Methodology
  - Temporal
  - Generalization
  - Each: 2-3 sentences, honest tone
- [ ] **10.7** Write Section 7.6: Future Directions (1 page, 250 words)
  - Dataset Expansion (with timeline)
  - Cross-Linguistic Generalization
  - Temporal Cultural Dynamics
  - Community-Centered Deployment
  - Each: 2-3 sentences, actionable
- [ ] **10.8** Final polish of entire Chapter 7
- [ ] **10.9** Verify page count: ~8 pages
- [ ] **10.10** Git commit: "Restructure Chapter 7: Non-repetitive, forward-looking"

**Deliverables:**
- ✅ Complete Chapter 7 rewrite (~8 pages)
- ✅ All 6 sections written
- ✅ Zero methodology/results repetition
- ✅ Concrete, actionable future work

**Quality Check:**
- Total pages: 8 ✓
- No generic future work ("more research needed") ✓
- Specific timelines in future directions ✓
- Active, confident tone ✓
- No result tables or figures repeated ✓

---

## PHASE 5: Final Quality & Submission (Days 15-16)

### DAY 15: Comprehensive Validation (8 hours)

**Morning Session (4 hours)**
- [ ] **11.1** Complete LaTeX compilation
  ```bash
  cd /home/ndethi/dev/opit-rai9001/docs/thesis
  pdflatex main.tex
  bibtex main
  pdflatex main.tex
  pdflatex main.tex
  ```
- [ ] **11.2** Check compilation log for:
  - No errors ✓
  - No undefined references ✓
  - No missing citations ✓
  - All figures display ✓
- [ ] **11.3** Verify page counts:
  - Total: 90-100 pages ✓
  - Chapter 2: ~15 pages ✓
  - Chapter 3: ~20 pages ✓
  - Chapter 7: ~8 pages ✓
- [ ] **11.4** Verify all required additions present:
  - Section 1.4 Hypotheses ✓
  - Section 3.6.6 Annotator Information ✓
  - Tables 3.2, 3.3, 3.4 ✓
  - Figures 4.1, 4.2 ✓
  - Appendices A, B ✓

**Afternoon Session (4 hours)**
- [ ] **11.5** Search for remaining issues:
  ```bash
  # Placeholder check
  grep -r "Chapter ??" docs/thesis/chapters/
  grep -r "Section ??" docs/thesis/chapters/
  grep -r "Figure ??" docs/thesis/chapters/
  
  # Terminology consistency
  grep -ri "ontology-grounded" docs/thesis/chapters/
  # Verify consistent capitalization
  
  # Citation format
  grep -r "\\cite{" docs/thesis/chapters/ | head -20
  # Verify proper \citep vs \citet usage
  ```
- [ ] **11.6** Check Table of Contents:
  - All chapters listed ✓
  - Section numbering correct ✓
  - Page numbers accurate ✓
- [ ] **11.7** Check List of Figures:
  - All figures listed ✓
  - Captions match ✓
- [ ] **11.8** Check List of Tables:
  - All tables listed ✓
  - Captions match ✓
- [ ] **11.9** Verify Bibliography:
  - All cited works present ✓
  - No uncited references ✓
  - Consistent formatting ✓

**Deliverables:**
- ✅ Clean PDF compilation (90-100 pages)
- ✅ All validation checks passed
- ✅ Zero placeholders remaining
- ✅ Comprehensive quality verification complete

---

### DAY 16: Final Submission Preparation (6 hours)

**Morning Session (4 hours)**
- [ ] **12.1** Create final PDF: `thiLLMo_Thesis_Revised_2026-01-10.pdf`
- [ ] **12.2** Create submission package directory:
  ```
  submission-package/
  ├── thiLLMo_Thesis_Revised_2026-01-10.pdf
  ├── REVISION_SUMMARY.md
  ├── CHANGES_LOG.md
  └── source/
      └── [LaTeX source files]
  ```
- [ ] **12.3** Write REVISION_SUMMARY.md:
  - Overview of 7 changes implemented
  - Before/After metrics
  - Key improvements summary
- [ ] **12.4** Write CHANGES_LOG.md:
  - Detailed list of all modifications
  - Git commit references
  - Files modified count

**Afternoon Session (2 hours)**
- [ ] **12.5** Final git operations:
  ```bash
  git add .
  git commit -m "Final thesis revision: All supervisor feedback implemented"
  git tag v2.0-supervisor-revised
  git push origin supervisor-revisions
  ```
- [ ] **12.6** Merge to main branch:
  ```bash
  git checkout dev
  git merge supervisor-revisions
  git push origin dev
  ```
- [ ] **12.7** Create GitHub release (if applicable)
- [ ] **12.8** Send to supervisor for review

**Deliverables:**
- ✅ Final PDF generated and verified
- ✅ Submission package complete
- ✅ All source code committed
- ✅ Git tagged with version
- ✅ Ready for supervisor review

**Final Checklist:**
- [ ] Total pages: 90-100 ✓
- [ ] All 7 supervisor items addressed ✓
- [ ] Zero placeholder references ✓
- [ ] 2 architecture diagrams added ✓
- [ ] Formal hypotheses section added ✓
- [ ] Evaluation transparency complete ✓
- [ ] Content reduction achieved ✓
- [ ] Methodology research-focused ✓
- [ ] Conclusion non-repetitive ✓
- [ ] Appendices properly integrated ✓
- [ ] Clean LaTeX compilation ✓
- [ ] Professional presentation ✓

---

## Risk Management

### High-Risk Items

**Risk 1: Missing Annotator Data**
- **Impact:** Cannot complete Section 3.6.6 fully
- **Mitigation:** 
  - Identify missing data on Day 1
  - Request from research team immediately
  - Have placeholder structure ready
- **Contingency:** Use anonymized/aggregated data if specific details unavailable

**Risk 2: LaTeX Compilation Errors**
- **Impact:** Delays in seeing results, broken references
- **Mitigation:**
  - Compile after EVERY major change
  - Keep backup of last working version
  - Use version control extensively
- **Contingency:** Revert to last working commit, re-apply changes incrementally

**Risk 3: Content Reduction Too Aggressive**
- **Impact:** Loss of essential technical details
- **Mitigation:**
  - Review each cut for necessity
  - Move to appendix rather than delete
  - Get second opinion on major cuts
- **Contingency:** Restore from git history if needed

**Risk 4: Diagram Creation Delays**
- **Impact:** Phase 3 bottleneck
- **Mitigation:**
  - Choose familiar diagramming tool
  - Start with hand sketch, refine digitally
  - Allocate full day per diagram
- **Contingency:** Use simplified diagrams if complex versions delayed

### Medium-Risk Items

**Risk 5: Inconsistent Terminology**
- **Impact:** Reduced professional appearance
- **Mitigation:**
  - Create terminology reference document
  - Use search/replace consistently
  - Final terminology audit on Day 15

**Risk 6: Cross-Reference Breakage**
- **Impact:** "??" or incorrect references in PDF
- **Mitigation:**
  - Test compilation frequently
  - Keep list of all labels/refs
  - Use meaningful label names

### Low-Risk Items

**Risk 7: Citation Formatting Issues**
- **Impact:** Bibliography inconsistencies
- **Mitigation:** Use BibTeX consistently, validate before final

**Risk 8: Page Count Overshoot**
- **Impact:** Still too long after reduction
- **Mitigation:** Track page counts daily, adjust cuts accordingly

---

## Daily Progress Tracking Template

Use this template to track daily progress in `REVISION_PROGRESS.md`:

```markdown
## Day [N]: [Date] - [Phase Title]

### Planned Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Completed Tasks
- [x] Task 1 - Notes: ...
- [x] Task 2 - Notes: ...
- [ ] Task 3 - Status: In progress, 60% complete

### Metrics
- Pages today: [Before] → [After]
- Total pages: [Count]
- Commits: [N]

### Issues Encountered
- Issue 1: [Description]
  - Resolution: [How solved]
- Issue 2: [Description]
  - Status: Open, needs attention

### Tomorrow's Priority
1. Complete remaining Task 3
2. Start Day [N+1] tasks
3. Address open issues

### Notes
[Any additional observations, decisions, or learnings]
```

---

## Success Criteria Verification

### Quantitative Targets

| Metric | Target | Verification Method |
|--------|--------|---------------------|
| Total Pages | 90-100 | PDF page count |
| Chapter 2 Pages | 15 | LaTeX aux file |
| Chapter 3 Pages | 20 | LaTeX aux file |
| Chapter 7 Pages | 8 | LaTeX aux file |
| Placeholder Refs | 0 | grep search |
| Architecture Diagrams | 2 | Figure count |
| Formal Hypotheses | 3 | Section 1.4 |
| Evaluation Tables | 3 | Tables 3.2-3.4 |
| Appendices | 2 | Appendix A, B |

### Qualitative Targets

| Aspect | Success Criteria | Verification Method |
|--------|-----------------|---------------------|
| Academic Rigor | Maintained throughout | Supervisor review |
| Narrative Flow | Smooth despite cuts | Read-through |
| Technical Accuracy | No compromise | Technical review |
| Presentation | Distinction-level | Visual inspection |
| Methodology | Research-focused | Section 3.1 review |
| Conclusion | Non-repetitive | Chapter 7 review |

---

## Tools & Resources

### Required Software
- LaTeX distribution (TeXLive/MikTeX) ✓
- BibTeX for bibliography ✓
- PDF viewer (for checking output) ✓
- Git (for version control) ✓
- Diagramming tool (draw.io, TikZ, Python) - Choose one

### Reference Documents
- Supervisor feedback (original email/document)
- Current thesis PDF (for comparison)
- Research proposal (for alignment check)
- Evaluation data (for Section 3.6.6)

### Helpful Commands

**Page count extraction:**
```bash
pdfinfo main.pdf | grep Pages
```

**Search for placeholders:**
```bash
grep -rn "??" docs/thesis/chapters/
```

**Word count (approximate):**
```bash
detex main.tex | wc -w
```

**LaTeX compilation:**
```bash
pdflatex -interaction=nonstopmode main.tex
```

**Clean auxiliary files:**
```bash
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
```

---

## Communication Plan

### Supervisor Updates
- **Day 5:** Send progress update (Phase 1 complete)
- **Day 10:** Send progress update (Phase 2 complete)
- **Day 14:** Send draft Chapter 7 for quick review
- **Day 16:** Send complete revised thesis

### Team Coordination
- Daily standup: Review yesterday's progress, today's plan
- Blocker identification: Escalate immediately if stuck >2 hours
- Decision log: Document all major content decisions

---

## Post-Revision Tasks

**After Supervisor Approval:**
- [ ] Incorporate final supervisor comments (if any)
- [ ] Format for university submission requirements
- [ ] Generate final archival PDF
- [ ] Prepare defense presentation materials
- [ ] Update project README with thesis status
- [ ] Archive all revision materials

**Knowledge Transfer:**
- [ ] Document lessons learned
- [ ] Create template for future thesis revisions
- [ ] Share experience with research group

---

## GETTING STARTED - Day 1 Checklist

**First things first (do these immediately):**

1. [ ] Create backup: `cp -r docs/thesis docs/thesis-backup-2025-12-18`
2. [ ] Create branch: `git checkout -b supervisor-revisions`
3. [ ] Create progress tracker: `touch docs/thesis/REVISION_PROGRESS.md`
4. [ ] Read this entire workplan (30 minutes)
5. [ ] Gather required data:
   - Annotator information (for Day 4)
   - Cohen's Kappa calculation (for Day 5)
   - IRB/ethics documentation (for Day 5)
6. [ ] Choose diagramming tool (for Days 11-12)
7. [ ] Start Day 1 tasks (Section: DAY 1)

**You're ready to begin!** 🚀

---

**End of Workplan - Ready for Implementation**
