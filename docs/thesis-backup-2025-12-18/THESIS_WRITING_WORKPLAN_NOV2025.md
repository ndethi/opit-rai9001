# Thesis Writing Workplan - November 2025

**Author**: Charles Watson Ndethi Kibaki  
**Created**: November 17, 2025  
**Thesis**: thiLLMo - Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation  
**Deadline**: November 30, 2025

---

## Executive Summary

**Strategy**: **Results-First Approach**  
**Rationale**: All evaluation data, statistical tests, and visualizations are ready. Starting with Chapter 5 (Results) provides immediate reviewable content to supervisor while enabling parallel writing of methodology chapters informed by actual results.

**Key Milestones**:
- Nov 19 (Day 3): Submit Chapters 1, 5, 6, 7 for supervisor review (~25-30 pages)
- Nov 24 (Day 8): Complete Chapters 3, 4, and appendices
- Nov 30 (Day 14): Final thesis submission

---

## Current Status Assessment

### ✅ **Completed Work**

**Chapter 2: Literature Review**
- Status: **COMPLETE** (v2.0.0)
- Word Count: ~7,500 words
- Quality: PhD-level comprehensive SotA analysis
- References: 35+ citations (80% from 2024-2025)
- File: `docs/thesis/chapters/02-literature-review-v2.0.0.tex`

**Evaluation Results**
- Cultural metrics evaluation: ✅ Complete (100 proverbs, 3 systems)
- Statistical tests: ✅ Complete (paired t-tests, all significant p<0.05)
- Visualizations: ✅ Complete (5 publication-quality figures)
- LaTeX tables: ✅ Generated and ready
- Interpretation sections: ✅ Generated and ready

### ❌ **Pending Chapters**

- Chapter 1: Introduction (NOT STARTED)
- Chapter 3: Methodology (NOT STARTED)
- Chapter 4: System Design and Implementation (NOT STARTED)
- Chapter 5: Results (DATA READY - needs writing)
- Chapter 6: Discussion (NOT STARTED)
- Chapter 7: Conclusion (NOT STARTED)

---

## Strategic Approach: Results-First Method

### Why Start with Chapter 5?

1. **✅ Data Readiness** - All results, statistics, and visualizations generated
2. **🎯 Critical for Validation** - Results prove research contribution
3. **⏱️ Fastest Path to Draft** - Can produce complete chapter in 1-2 days
4. **🔄 Enables Informed Writing** - Methodology/design written to match actual results
5. **📊 Concrete Foundation** - Results inform introduction and discussion framing

### Advantages Over Sequential Approach

| Traditional (Ch 1→7) | Results-First (Ch 5→1,3,4,6,7→2) |
|----------------------|-----------------------------------|
| Week to write Ch 1-4 | Ch 5 draft in 1-2 days |
| Rewrites after seeing results | Methodology matches results |
| Nothing reviewable quickly | Substantial draft in 3 days |
| Sequential dependencies | Parallel writing possible |

---

## Phase 1: Immediate Priority (Nov 17-19)
**Goal**: Reviewable draft to supervisor by Nov 19 evening

### Day 1: November 17 (TODAY)
**Target**: Chapter 5.1-5.3 (8-10 pages)

**Morning Session (4 hours)**:
- ✅ Create `05-evaluation.tex` file
- ✅ Run `generate_thesis_chapter5.py` and save output
- ✍️ Write Section 5.1: Evaluation Overview (2 pages)
  - Research questions recap
  - Evaluation methodology overview
  - 100-proverb dataset description
  - Three systems compared
  - Metrics overview

**Afternoon Session (4 hours)**:
- ✍️ Write Section 5.2: Cultural Metrics Results (4-5 pages)
  - 5.2.1: Cultural Authenticity Results (use generated content)
  - 5.2.2: Translation Fidelity Results (use generated content)
  - 5.2.3: Overall Quality Assessment (use generated content)
  - 5.2.4: Statistical Significance Analysis
- 📊 Insert Table 5.1 (Cultural Metrics Summary)
- 📊 Insert Table 5.2 (Statistical Tests)
- 🖼️ Insert Figures 1-3 (bar charts)

**Evening Session (2 hours)**:
- ✍️ Write Section 5.3: Score Distributions (2-3 pages)
- 🖼️ Insert Figure 4 (box plots)
- 🖼️ Insert Figure 5 (improvements chart)
- 📝 Initial draft review and editing

**Deliverable**: 8-10 pages of Chapter 5 drafted

---

### Day 2: November 18
**Target**: Complete Chapter 5 + Draft Chapter 6 (12-15 pages total)

**Morning Session (4 hours)**:
- ✍️ Write Section 5.4: Qualitative Analysis (2-3 pages)
  - Example translations showcasing improvements
  - Error analysis (where OG-RAG still fails)
  - Edge cases and interesting findings
  - Translation strategy patterns
- ✍️ Write Section 5.5: Summary of Key Findings (2 pages)
  - Recap of main results
  - Answer to each RQ briefly
  - Transition to Discussion

**Afternoon Session (4 hours)**:
- ✍️ Write Chapter 6.1: Answering RQ1 (3-4 pages)
  - Use generated interpretation content
  - How ontologies enhanced contextual understanding
  - Three mechanisms: semantic grounding, context enrichment, cultural coherence
  - Significance of 10.5% improvement
- ✍️ Write Chapter 6.2: Answering RQ2 (2-3 pages)
  - Business corpus development process
  - Quality validation approach
  - Coverage and limitations

**Evening Session (2 hours)**:
- ✍️ Start Chapter 6.3: Answering RQ3 (2-3 pages)
  - OG-RAG vs Traditional RAG comparison
  - 5.3% improvement significance (t=5.341, p<0.000001)
  - Why ontology structure matters
  - Trade-offs and considerations

**Deliverable**: Chapter 5 complete (12-15 pages), Chapter 6 partial draft (6-8 pages)

---

### Day 3: November 19
**Target**: Chapter 1 + Chapter 7 (10-13 pages)

**Morning Session (4 hours)**:
- ✍️ Write Chapter 1: Introduction (6-8 pages)
  - 1.1: Background and Motivation (2 pages)
    - Importance of cultural preservation
    - Challenges in proverb translation
    - Low-resource language context
  - 1.2: Problem Statement (1-2 pages)
    - Limitations of existing MT approaches
    - Need for cultural fidelity
    - Gap in current research
  - 1.3: Research Questions (1 page)
    - RQ1: Cultural ontologies enhancement
    - RQ2: Business corpus development
    - RQ3: OG-RAG vs Traditional RAG
  - 1.4: Research Contributions (1-2 pages)
    - Novel OG-RAG application for Kikuyu
    - Structured cultural knowledge resource
    - Empirical validation framework
  - 1.5: Thesis Structure (1 page)
    - Overview of chapters

**Afternoon Session (3 hours)**:
- ✍️ Write Chapter 7: Conclusion (4-5 pages)
  - 7.1: Summary of Work (1-2 pages)
    - Recap of problem and approach
    - Overview of contributions
  - 7.2: Key Findings (1 page)
    - Highlight main results (reference Ch 5)
  - 7.3: Limitations (1 page)
    - Dataset size constraints
    - Single language pair
    - Evaluation scope
  - 7.4: Future Work (1-2 pages)
    - Scaling to full proverb corpus
    - Extension to other LRLs
    - LLM-as-a-Judge integration
    - Community deployment

**Evening Session (2 hours)**:
- 📝 Complete Chapter 6 (finish 6.3, add 6.4: Limitations)
- 🔍 Review and polish Chapters 1, 5, 6, 7
- 📧 Prepare submission package for supervisor
- ✉️ Draft email to supervisor with review request

**Deliverable**: Chapters 1, 5, 6, 7 complete (~25-30 pages)

**📧 SUBMISSION TO SUPERVISOR**: November 19, 8:00 PM
- **Subject**: "Thesis Draft - Results Chapters for Review (thiLLMo Project)"
- **Attached**: PDF of Chapters 1, 2, 5, 6, 7
- **Request**: Priority review of Chapter 5 (Results)
- **Timeline**: Chapters 3-4 to be completed by Nov 24

---

## Phase 2: Technical Chapters (Nov 20-25)
**Goal**: Complete methodology and implementation chapters

### Day 4-5: November 20-21
**Target**: Chapter 3: Methodology (10-12 pages)

**Day 4 Morning (4 hours)**:
- ✍️ Write Section 3.1: Research Design (2-3 pages)
  - CRISP-DM framework overview
  - Justification for methodology choice
  - Iterative nature of approach
  - Ethical considerations
- ✍️ Write Section 3.2: Data Understanding Phase (2 pages)
  - Kikuyu proverb corpus analysis
  - Cultural context exploration
  - Data scarcity challenges

**Day 4 Afternoon (4 hours)**:
- ✍️ Write Section 3.3: Ontology Construction (3-4 pages)
  - 7-step methodology (from proposal)
  - Scope determination
  - Term enumeration and class definition
  - Property specification
  - Instance creation
  - Validation approach (OOPS!, expert review)

**Day 5 Morning (4 hours)**:
- ✍️ Write Section 3.4: System Development (2-3 pages)
  - LLM selection criteria and choice
  - Knowledge graph integration
  - Retrieval mechanism design
  - Generation module architecture
- ✍️ Write Section 3.5: Evaluation Framework (2-3 pages)
  - Cultural metrics design
  - Statistical testing approach
  - Human evaluation protocol
  - Qualitative analysis methods

**Day 5 Afternoon (2 hours)**:
- 📝 Polish and cross-reference Chapter 3
- 🔗 Ensure alignment with actual results (Ch 5)
- 📊 Add methodology diagrams if needed

**Deliverable**: Chapter 3 complete (10-12 pages)

---

### Day 6-7: November 22-23
**Target**: Chapter 4: System Design and Implementation (12-15 pages)

**Day 6 Morning (4 hours)**:
- ✍️ Write Section 4.1: System Architecture (2-3 pages)
  - Overall architecture diagram
  - Component overview
  - Data flow description
  - Technology stack
- ✍️ Write Section 4.2: Ontology Implementation (3-4 pages)
  - OWL representation
  - Class hierarchy
  - Properties and relationships
  - Sample instances
  - Validation results

**Day 6 Afternoon (4 hours)**:
- ✍️ Write Section 4.3: Knowledge Graph Implementation (2-3 pages)
  - Neo4j database setup
  - Graph schema
  - Data ingestion pipeline
  - Query optimization
- ✍️ Write Section 4.4: RAG Pipeline (2-3 pages)
  - Retrieval mechanism implementation
  - Context construction
  - Prompt engineering strategy

**Day 7 Morning (3 hours)**:
- ✍️ Write Section 4.5: Translation Module (2 pages)
  - LLM integration details
  - Generation parameters
  - Post-processing pipeline
- ✍️ Write Section 4.6: Technical Challenges (2 pages)
  - Key implementation challenges
  - Solutions adopted
  - Lessons learned

**Day 7 Afternoon (3 hours)**:
- 📝 Polish Chapter 4
- 📊 Add architecture diagrams and code snippets
- 🔗 Cross-reference with Chapters 3 and 5

**Deliverable**: Chapter 4 complete (12-15 pages)

---

### Day 8: November 24
**Target**: Finalize appendices and remaining content

**Morning Session (3 hours)**:
- ✍️ Write Appendices
  - Appendix A: Ontology Schema (OWL/Turtle excerpt)
  - Appendix B: Sample Proverbs and Translations
  - Appendix C: Evaluation Instruments
  - Appendix D: Statistical Test Details
  - Appendix E: Code Repositories and Resources

**Afternoon Session (3 hours)**:
- 📝 Review entire thesis flow
- 🔗 Fix cross-references and citations
- 📊 Verify all figures and tables numbered correctly
- 📚 Complete bibliography entries

**Deliverable**: Complete first draft (all chapters)

---

## Phase 3: Finalization (Nov 25-30)

### Day 9-10: November 25-26
**Target**: Incorporate supervisor feedback and revise

**Day 9 (4-6 hours)**:
- 📧 Review supervisor feedback
- 📝 Create revision checklist
- ✏️ Revise Chapter 5 based on comments
- ✏️ Revise Chapter 1 based on comments

**Day 10 (4-6 hours)**:
- ✏️ Revise Chapters 6 and 7
- ✏️ Update Chapters 3 and 4 if needed
- 🔍 Second read-through for consistency

---

### Day 11-12: November 27-28
**Target**: Polish and finalize

**Day 11 Morning (3 hours)**:
- 📖 Complete reference formatting
  - Ensure all citations in text have entries
  - Format according to BibLaTeX standards
  - Alphabetize and check for duplicates
- 📝 Write Abstract (250-300 words)
  - Background (2 sentences)
  - Problem (1 sentence)
  - Approach (2-3 sentences)
  - Results (2-3 sentences)
  - Significance (1-2 sentences)

**Day 11 Afternoon (3 hours)**:
- 📋 Write Executive Summary (if required, 1-2 pages)
- 📄 Write Acknowledgments
- 📝 Polish Introduction and Conclusion

**Day 12 (6 hours)**:
- 🔍 Comprehensive proofread
  - Grammar and spelling check
  - Consistency in terminology
  - Formatting uniformity
  - Figure/table caption quality
- 📊 Final formatting adjustments
  - Page breaks
  - Widow/orphan control
  - Header/footer consistency

---

### Day 13: November 29
**Target**: Final compilation and quality assurance

**Morning Session (4 hours)**:
- 📄 Generate final PDF
- ✅ Quality checks:
  - [ ] Table of Contents complete and accurate
  - [ ] List of Figures complete
  - [ ] List of Tables complete
  - [ ] All cross-references working
  - [ ] All citations formatted correctly
  - [ ] All figures displaying correctly
  - [ ] All tables formatted properly
  - [ ] Page numbers correct
  - [ ] Headers/footers consistent

**Afternoon Session (3 hours)**:
- 📊 Generate statistics:
  - Total word count
  - Page count by chapter
  - Figure and table counts
  - Reference count
- 📝 Create submission checklist
- 📦 Prepare submission package
  - Main PDF
  - Supplementary materials (if required)
  - Source files (if required)
  - Copyright forms (if required)

---

### Day 14: November 30
**Target**: SUBMISSION DAY

**Morning (2-3 hours)**:
- 🔍 Final review of PDF
- ✅ Verify submission requirements
- 📧 Prepare submission email/portal upload
- 🚀 **SUBMIT FINAL THESIS**

**Afternoon**:
- 📦 Archive all materials
  - Source files
  - Data files
  - Code repositories
  - Figures (original formats)
  - Notes and drafts
- 📧 Confirmation to supervisor
- 🎉 Celebrate completion!

---

## Daily Time Estimates

| Phase | Days | Hours/Day | Total Hours |
|-------|------|-----------|-------------|
| Phase 1: Immediate (Ch 1,5,6,7) | 3 | 8-10 | 24-30 |
| Phase 2: Technical (Ch 3,4) | 5 | 6-8 | 30-40 |
| Phase 3: Finalization | 6 | 4-6 | 24-36 |
| **TOTAL** | **14** | **Avg 6-7** | **78-106** |

**Realistic Assessment**: ~80-90 hours of focused writing over 14 days = **6-7 hours/day**

---

## Key Success Factors

### 1. **Discipline**
- Dedicated writing blocks (no distractions)
- Pomodoro technique (50 min work, 10 min break)
- Daily targets must be met

### 2. **Leverage Generated Content**
- Use `generate_thesis_chapter5.py` output directly
- Copy LaTeX tables and text sections
- Don't reinvent - adapt and polish

### 3. **Early Supervisor Engagement**
- Nov 19 submission critical
- Enables feedback while writing continues
- Reduces risk of major revisions

### 4. **Parallel Activities**
- While waiting for supervisor feedback (Nov 20-24)
- Write technical chapters informed by results
- Keep momentum going

### 5. **Buffer Management**
- Nov 25-28 = 4-day buffer for revisions
- Nov 29 = safety day for compilation issues
- Nov 30 = submission day (don't use for writing!)

---

## Risk Mitigation

### Risk 1: Supervisor unavailable or slow feedback
**Mitigation**: Proceed with Chapters 3-4 anyway; results chapter stands alone

### Risk 2: Writing slower than estimated
**Mitigation**: Chapters 3-4 can be compressed; Results + Discussion are priority

### Risk 3: Technical issues with LaTeX compilation
**Mitigation**: Test compilation after each chapter; keep backups; have Plan B (Word)

### Risk 4: Additional data analysis requested
**Mitigation**: All core analyses done; mark additional requests as "Future Work"

### Risk 5: Personal interruptions/emergencies
**Mitigation**: 4-day buffer in finalization phase; can compress if needed

---

## Quality Targets

### Content Quality
- **Chapter 5 (Results)**: Publication-ready - most polished chapter
- **Chapters 1, 6, 7**: High quality - well-argued and clear
- **Chapters 3, 4**: Good quality - technically sound, may be terser
- **Chapter 2**: Already excellent (v2.0.0)

### Quantitative Targets
- **Total Word Count**: 20,000-25,000 words
- **Page Count**: 80-100 pages (double-spaced)
- **Figures**: 8-12 (5 already created)
- **Tables**: 4-8 (2 already created)
- **References**: 40-50 (35 already in Ch 2)

---

## Tools and Resources

### Writing Tools
- **LaTeX Editor**: VS Code with LaTeX Workshop extension
- **Bibliography**: BibTeX/BibLaTeX with `references.bib`
- **Figures**: Already in `docs/thesis/figures/`
- **Content Generator**: `scripts/generate_thesis_chapter5.py`

### Reference Materials
- Research Proposal: `docs/proposal/OPIT_RAI9001_Research_Proposal_v1.md`
- Evaluation Results: `data/results/cultural_evaluation_summary.json`
- Generated Content: Output from thesis scripts
- Literature Review: `docs/thesis/chapters/02-literature-review-v2.0.0.tex`

### Support Resources
- Supervisor: Weekly check-ins (request extra for Nov 20, 25)
- Writing guides: Institution thesis guidelines
- Proofreading: Grammarly/AI assistance for grammar only
- Peer review: Consider asking colleague for quick read

---

## Motivation and Mental Health

### Daily Routine
- **Morning**: Fresh mind for new content
- **Afternoon**: Editing and polishing
- **Evening**: Light work (formatting, references)

### Self-Care
- 7-8 hours sleep daily (non-negotiable)
- Regular meals
- Short walks between sessions
- Exercise if possible
- Limit caffeine after 2 PM

### Milestone Celebrations
- ✅ Nov 17 end: Chapter 5 draft → Treat yourself
- ✅ Nov 19 end: Supervisor submission → Nice dinner
- ✅ Nov 24 end: All chapters drafted → Evening off
- ✅ Nov 30: Final submission → Major celebration!

---

## Commitment Statement

**I commit to this workplan with the following understanding:**

1. **Results-First approach** is the optimal strategy given available data
2. **November 19 supervisor submission** is non-negotiable milestone
3. **Daily targets** must be met to stay on schedule
4. **Quality over quantity** - but meet word count minimums
5. **Buffer time** is for revisions, not new writing

**Signature**: _________________________  
**Date**: November 17, 2025

---

## Appendix: Chapter Outlines

### Chapter 1: Introduction (6-8 pages)
1.1 Background and Motivation (2 pages)
1.2 Problem Statement (1-2 pages)
1.3 Research Questions (1 page)
1.4 Research Contributions (1-2 pages)
1.5 Thesis Structure (1 page)

### Chapter 3: Methodology (10-12 pages)
3.1 Research Design (2-3 pages)
3.2 Data Understanding (2 pages)
3.3 Ontology Construction (3-4 pages)
3.4 System Development (2-3 pages)
3.5 Evaluation Framework (2-3 pages)

### Chapter 4: System Design (12-15 pages)
4.1 System Architecture (2-3 pages)
4.2 Ontology Implementation (3-4 pages)
4.3 Knowledge Graph (2-3 pages)
4.4 RAG Pipeline (2-3 pages)
4.5 Translation Module (2 pages)
4.6 Technical Challenges (2 pages)

### Chapter 5: Results (12-15 pages)
5.1 Evaluation Overview (2 pages)
5.2 Cultural Metrics (4-5 pages)
5.3 Statistical Analysis (2-3 pages)
5.4 Qualitative Analysis (2-3 pages)
5.5 Summary of Findings (2 pages)

### Chapter 6: Discussion (10-12 pages)
6.1 Answering RQ1 (3-4 pages)
6.2 Answering RQ2 (2-3 pages)
6.3 Answering RQ3 (2-3 pages)
6.4 Implications (2 pages)
6.5 Limitations (1-2 pages)

### Chapter 7: Conclusion (4-5 pages)
7.1 Summary (1-2 pages)
7.2 Key Findings (1 page)
7.3 Limitations (1 page)
7.4 Future Work (1-2 pages)

---

**END OF WORKPLAN**

*This is a living document. Update daily with actual progress and adjust timeline as needed while maintaining Nov 30 deadline.*
