# Thesis Quality Assurance Workflow Guide

**Created**: November 26, 2025  
**Thesis**: thiLLMo - Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation  
**Target Completion**: November 30, 2025

---

## Overview

This directory contains all materials for running comprehensive quality assurance on the thesis chapters through:
1. **Citations Verification** - Expert academic integrity review
2. **Editorial Refinement** - Enhancing writing clarity and scholarly voice while preserving academic rigor

---

## Directory Structure

```
quality-assurance/
├── QA-WORKFLOW-GUIDE.md          # This file
├── ISSUES-LOG.md                  # Track all issues found and fixes applied
├── input-packages/                # Prepared inputs for prompts
│   └── all-chapters-for-citation-verification.tex
├── chapter-extracts/              # Individual chapters for humanization
│   ├── 01-introduction.tex        (~2,394 words)
│   ├── 02-literature-review.tex   (~2,172 words)
│   ├── 03-methodology.tex         (~3,888 words)
│   ├── 04-design-implementation.tex (~3,313 words)
│   ├── 05-evaluation.tex          (~3,436 words)
│   ├── 06-discussion.tex          (~3,577 words)
│   └── 07-conclusion.tex          (~2,205 words)
└── outputs/                       # Store prompt analysis outputs here
    ├── citation-verification-report.md
    ├── humanization-reports/
    └── revision-tracking/
```

---

## Workflow

### Phase 1: Citations Verification (Do First)

**Why First**: Citation fixes may affect content across all chapters; do before humanization to avoid re-humanizing changed sections.

#### Step 1: Run Citation Verification Prompt

**Input File**: `input-packages/all-chapters-for-citation-verification.tex`

**Contains**:
- All 7 chapters (concatenated)
- Full bibliography file (`references.bib`)
- ~3,512 lines total

**Prompt to Use**: The citations/referencing expert prompt you have ready

**Action**:
1. Open your prompt tool (ChatGPT/Claude/etc.)
2. Paste the citation verification prompt
3. Upload or paste contents of `all-chapters-for-citation-verification.tex`
4. Run the analysis

#### Step 2: Save the Analysis Report

**Output Location**: `outputs/citation-verification-report.md`

**Expected Report Sections**:
- Executive Summary
- Citation Style Assessment
- Detailed Citation Audit
- Alternative Reference Recommendations
- Best Practice Recommendations
- Compliance Checklist

#### Step 3: Log Issues in ISSUES-LOG.md

As you review the report, log each issue with:
- Issue ID (e.g., CIT-001)
- Type (broken reference, formatting error, missing DOI, etc.)
- Location (chapter, citation key)
- Severity (critical, high, medium, low)
- Recommended fix
- Status (identified, fixed, verified)

#### Step 4: Implement Citation Fixes

GitHub Copilot can help with bulk citation fixes:
- Missing DOIs
- Format corrections
- Bibliography updates
- Cross-reference verification

**Ask me** when ready to implement fixes and I'll help apply them efficiently.

---

### Phase 2: Editorial Refinement (Do After Citations Fixed)

**Why After**: Avoid re-humanizing sections that changed due to citation fixes.

#### Priority Order (Recommended)

1. **Chapter 1** (Introduction) - First impression, most critical
2. **Chapter 3** (Methodology) - High AI-marker risk in methodology descriptions
3. **Chapter 5** (Evaluation) - Results need clear, direct presentation
4. **Chapter 6** (Discussion) - Needs intellectual wrestling, critical depth
5. **Chapter 2** (Literature Review) - May already be well-written
6. **Chapter 4** (Design/Implementation) - Technical content, lower AI-detection risk
7. **Chapter 7** (Conclusion) - Shortest, do last

#### For Each Chapter:

**Step 1: Run Humanization Prompt**

**Input File**: `chapter-extracts/0X-chapter-name.tex`

**Prompt to Use**: The humanization & AI detection prompt you have ready

**Action**:
1. Copy contents of the specific chapter file
2. Paste the humanization prompt
3. Paste the chapter content
4. Specify priority patterns based on chapter (see prompt guidance)
5. Run the analysis

**Step 2: Save Chapter Analysis**

**Output Location**: `outputs/humanization-reports/chapter-0X-analysis.md`

**Expected Analysis**:
- AI markers identified
- Humanization strategies applied
- Verification checklist
- Improvements achieved

**Step 3: Log Issues in ISSUES-LOG.md**

For each chapter, log:
- Issue ID (e.g., HUM-CH1-001)
- Pattern type (formulaic opener, generic vocabulary, etc.)
- Location (section, paragraph)
- Original text excerpt
- Suggested revision
- Status

**Step 4: Review and Apply Changes**

Review the humanized version:
- Verify technical accuracy preserved
- Check all citations intact
- Confirm academic tone maintained
- Validate improvements address AI markers

**Ask me** to help apply the changes to the actual chapter files.

---

## Key Success Metrics

### Citations Verification
- [ ] Zero broken/missing references
- [ ] All citations match bibliography
- [ ] Consistent formatting (BibTeX/BibLaTeX)
- [ ] DOIs added where available
- [ ] Alternative sources identified for problematic refs

### Humanization
- [ ] Zero "In this section/chapter" openers
- [ ] <2 unnecessary hedges per section
- [ ] Em dashes: <2 per page
- [ ] "Delve/dive deep/shed light/tapestry": 0 instances
- [ ] Paragraph length variation (60-250 word range)
- [ ] Sentence structure variation
- [ ] Researcher voice added (1-2 narratives per major section)
- [ ] All citations preserved exactly
- [ ] All technical accuracy maintained

### Overall Quality Targets
- **Citation Integrity**: 95%+ (currently 91.3%)
- **Authenticity**: 90-95% (from baseline 72-78%)
- **Academic Rigor**: Enhanced through deeper analysis
- **Publication Readiness**: Achieved

---

## Tips for Efficient Execution

### For Citations:
1. Start with Executive Summary to identify high-priority issues
2. Fix critical issues first (broken refs, major format violations)
3. Batch similar fixes together (all missing DOIs, all format corrections)
4. Use GitHub Copilot for repetitive fixes

### For Humanization:
1. Process one chapter completely before moving to next
2. Focus on highest-impact patterns first (openers, paragraph variation)
3. Save original chapter as backup before applying changes
4. Compile LaTeX after each chapter to catch errors early
5. Don't force changes that compromise technical accuracy

### Time Estimates:
- **Citations Verification**: 2-3 hours (analysis + fixes)
- **Per Chapter Humanization**: 1-2 hours each
- **Total Humanization**: 7-14 hours across all chapters
- **Final Verification**: 2-3 hours
- **Total**: 11-20 hours

---

## Quality Checkpoints

After each major phase, verify:

### Post-Citation Fixes:
```bash
# Check LaTeX compiles
cd /Users/ndethi/dev/opit/opit-rai9001/docs/thesis
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Check for undefined references
grep "Warning.*undefined" main.log
grep "Warning.*Citation" main.log
```

### Post-Humanization (Each Chapter):
```bash
# Word count check
wc -w chapters/0X-chapter-name.tex

# Citation preservation check
grep -c "\\cite{" chapters/0X-chapter-name.tex

# AI marker check (should be 0 or near 0)
grep -i "in this section\|in this chapter\|it is worth noting" chapters/0X-chapter-name.tex
grep -i "delve\|dive deep\|shed light\|tapestry" chapters/0X-chapter-name.tex
```

---

## Emergency Rollback

If changes break something:

```bash
# Restore from Git
cd /Users/ndethi/dev/opit/opit-rai9001
git checkout chapters/0X-chapter-name.tex

# Or restore from quality-assurance backup
cp quality-assurance/chapter-extracts/0X-chapter-name.tex chapters/
```

---

## Final Deliverables

When QA is complete:

1. **Updated Chapter Files** (7 files)
2. **Updated Bibliography** (`references/references.bib`)
3. **Issues Log** with all fixes documented
4. **QA Report Summary** (generated from ISSUES-LOG.md)
5. **Compiled PDF** of final thesis
6. **Git Commit** with comprehensive QA message

---

## Contact for Help

If you need assistance implementing fixes or encounter issues:
- Ask GitHub Copilot in this workspace
- Refer to this guide's workflow steps
- Check ISSUES-LOG.md for similar resolved issues

---

**Status Tracking**: See `ISSUES-LOG.md` for real-time progress on all QA items.

**Last Updated**: November 26, 2025
