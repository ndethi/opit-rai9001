# DoCEIS 2026 Conference Paper Guide

## Content Allocation & Page Budget

### Target: 12-16 pages (aim for 14-15 pages to stay comfortably within range)

| Section | Target Pages | Word Count | Status |
|---------|-------------|------------|--------|
| Abstract | 0.5 | 200-250 | ✅ DRAFTED |
| 1. Introduction | 2.0 | 1,200-1,400 | ✅ DRAFTED |
| 2. Related Work | 1.75 | 900-1,200 | ✅ DRAFTED |
| 3. Methodology | 3.5 | 2,000-2,500 | ✅ DRAFTED |
| 4. Results | 3.5 | 2,000-2,500 | ✅ DRAFTED |
| 5. Discussion | 2.0 | 1,200-1,400 | ✅ DRAFTED |
| 6. Conclusion | 1.0 | 600-800 | ✅ DRAFTED |
| References | 0.75 | N/A | ✅ DRAFTED |
| **TOTAL** | **14-15** | **~8,500-10,000** | **DRAFT COMPLETE** |

---

## Writing Progress Checklist

### Phase 1: Core Technical Content ✅ COMPLETE
- [x] Section 3: Methodology (architecture, ontology, evaluation)
- [x] Section 4: Results (quantitative + qualitative)
- [x] Bibliography with all required citations

### Phase 2: Framing & Context ✅ COMPLETE
- [x] Section 1: Introduction (societal challenge focus)
- [x] Section 2: Related Work (condensed, 3-4 areas)
- [x] Abstract (200-250 words, impact-focused)

### Phase 3: Discussion & Wrap-up ✅ COMPLETE
- [x] Section 5: Discussion (generalizability, ethics, limitations)
- [x] Section 6: Conclusion (future work, impact)

### Phase 4: Polish & Figures (TODO)
- [ ] Extract figures from thesis (system architecture, score distributions)
- [ ] Anonymize for double-blind review
- [ ] Proofread for Springer LNCS compliance
- [ ] Generate example translation table (Table 2)
- [ ] Check all cross-references

### Phase 5: Submission Prep (TODO)
- [ ] Remove author names/affiliations
- [ ] Strip PDF metadata
- [ ] Anonymize acknowledgments
- [ ] Change "we" → "this work" where needed
- [ ] Final compile and PDF generation

---

## Key Figures Needed (Extract from Thesis)

### Figure 1: System Architecture
**Source**: `docs/thesis/figures/system-architecture.tex`
**Caption**: thiLLMo system architecture showing ontology-grounded retrieval pipeline with hybrid fallback mechanisms.
**Location**: Section 3.1

### Figure 2: Score Distribution Box Plots
**Source**: Need to generate from evaluation data
**Caption**: Distribution of cultural authenticity, translation fidelity, and overall quality scores across three systems.
**Location**: Section 4.3

### Table 1: Overall Performance Summary
**Status**: ✅ Already in Section 4.1
**Location**: Section 4.1

### Table 2: Example Translations
**Status**: ✅ Already in Section 4.5
**Location**: Section 4.5

### Table 3: Ablation Study
**Status**: ✅ Already in Section 4.6
**Location**: Section 4.6

---

## Double-Blind Anonymization Checklist

Before final submission, MUST remove/anonymize:

- [ ] Author names on title page
- [ ] Institutional affiliations
- [ ] Acknowledgments mentioning supervisor/institution
- [ ] First-person pronouns ("we" → "this work", "our" → "the")
- [ ] References to "our previous work" (rephrase generically)
- [ ] GitHub repository URLs (add "anonymized for review" note)
- [ ] Funding statements naming specific grants
- [ ] PDF metadata (author, institution, creation date)
- [ ] Figure captions with possessive language

---

## Springer LNCS Requirements

### Format
- [x] Use `llncs` document class
- [x] Include running heads
- [x] Use `splncs04` bibliography style
- [ ] Ensure 12-16 pages total

### Structure
- [x] Abstract with keywords
- [x] Numbered sections
- [x] Proper figure/table captions with labels
- [x] Bibliography at end

### Style
- [x] British/American English (consistent)
- [x] Proper citation format
- [x] No headers/footers except page numbers
- [x] Figures referenced in text before appearing

---

## Compilation Instructions

```bash
cd docs/conferences/doceis2026

# Compile LaTeX
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Or use latexmk for automatic compilation
latexmk -pdf main.tex

# Clean auxiliary files
latexmk -c
```

---

## Timeline Suggestion

### Week 1 (Current): Draft Complete ✅
- [x] All sections drafted
- [x] Bibliography complete
- [x] Basic structure in place

### Week 2: Figures & Polish
- [ ] Extract/adapt thesis figures
- [ ] Proofread all sections
- [ ] Check citation accuracy
- [ ] Verify page count (aim for 14-15 pages)

### Week 3: Anonymization & Review
- [ ] Apply double-blind anonymization
- [ ] Internal review by supervisor
- [ ] Address feedback
- [ ] Final polishing

### Week 4: Submission
- [ ] Generate final PDF
- [ ] Strip metadata
- [ ] Submit through conference system
- [ ] Confirm submission receipt

---

## Key Messages for Reviewers

### Societal Impact Focus (DoCEIS requirement)
> "This work addresses cultural knowledge extinction in endangered languages—a critical societal challenge where 50% of languages will disappear by 2100. By developing ontology-grounded RAG for Kikuyu proverb translation, we provide a replicable methodology for preserving indigenous knowledge across Africa's 2000+ languages."

### Technical Contribution
> "First work to combine ontology-grounded retrieval with RAG for low-resource cultural translation, achieving 10.5% improvement in cultural authenticity through structured knowledge augmentation."

### Evaluation Rigor
> "Paired t-tests on 100 proverbs with strict significance testing (p<0.001), effect size reporting (Cohen's d), and dual-metric framework separating cultural authenticity from translation fidelity."

### Open Science
> "All artifacts (code, ontology, corpus) open-source to enable replication and extension across indigenous languages worldwide."

---

## Next Steps

1. **Extract Figures**: Copy system architecture diagram from thesis
2. **Compile & Check**: Generate PDF to verify page count and formatting
3. **Proofread**: Read through all sections for clarity and consistency
4. **Supervisor Review**: Share draft for feedback
5. **Iterate**: Address comments and refine
6. **Anonymize**: Apply double-blind requirements
7. **Submit**: Upload through DoCEIS conference system

---

## Contact Information (For Internal Use Only)

- **Conference**: DoCEIS 2026
- **Contact**: Luis M. Camarinha-Matos
- **Submission Deadline**: [Check conference website]
- **Review Type**: Double-blind
- **Page Limit**: 12-16 pages
- **Format**: Springer LNCS

---

## Notes

- All section files use relative paths and can be compiled independently
- Bibliography uses BibTeX with `splncs04` style
- Keywords selected for discoverability: ontology, RAG, low-resource languages, cultural AI
- Abstract emphasizes societal challenge per DoCEIS feedback
- Structure follows standard conference paper format (Intro → Related → Method → Results → Discussion → Conclusion)
