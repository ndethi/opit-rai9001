# Citation Verification Completion Workplan

**Date**: January 21, 2026  
**Branch**: `post-defense`  
**File**: `Author_Verification_97-Citations_2026-01-21_COMPLETE.csv`  
**Goal**: Achieve 100% verified bibliography with zero hallucinations

---

## CURRENT STATUS

**Total Citations**: 97  
**Verified**: 86 (88.7%)  
**Pending Work**: 11 entries requiring action

### Breakdown by Action Required:
- 🔍 **PENDING** (3 entries) - Need URL/venue verification
- ✏️ **NEEDS_CORRECTION** (5 entries) - Year mismatches in citation keys
- 🔗 **VERIFY_DUPLICATE** (4 entries) - Potential duplicate entries
- ❌ **Special Cases** (1 entry) - "fail" but marked VERIFIED (needs review)

---

## VERIFICATION RULES (Ground Truth)

### Rule 1: Dual Verified = PASS
```
IF ok_alt = "ok" OR "https://..." AND Verification_Status = "VERIFIED"
THEN → No action needed, citation passes
```

### Rule 2: ok_alt Contains Link = RE-VERIFY
```
IF ok_alt = "https://..."
THEN → Visit link, parse fresh metadata (authors, title, year, venue)
     → Update all columns with authoritative data
     → Mark as VERIFIED
```

### Rule 3: ok_alt = "fail" OR "Fail" = FIND ALTERNATIVE
```
IF ok_alt = "fail" OR "Fail"  
THEN → Search thesis chapters for usage context
     → Find verifiable alternative reference
     → Use arXiv verification script OR Google Scholar
     → Replace or DELETE if no alternative found
```

### Rule 4: Duplicates = CONSOLIDATE
```
IF multiple entries reference same paper
THEN → Keep highest-quality metadata version
     → Update all in-text \cite{} commands to unified key
     → DELETE duplicate BibTeX entries
```

---

## PHASE 1: PENDING ENTRIES (3 items)

### Entry 1: guo2024lazygraphrag
- **ok_alt**: `https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/`
- **Action**: Visit Microsoft Research blog link
- **Tasks**:
  1. Extract full author list
  2. Verify title: "LazyGraphRAG: Setting a New Standard for Quality and Cost"
  3. Determine if published on arXiv (search arXiv.org)
  4. Update venue (blog vs. arXiv vs. conference)
  5. Mark VERIFIED if found, DELETE if blog-only gray literature

### Entry 2: zhang2024triplex
- **ok_alt**: `Fail`
- **Venue**: Unknown
- **Action**: Determine if legitimate reference
- **Tasks**:
  1. Search Google Scholar: "Triplex Zhang 2024 graph knowledge"
  2. Search arXiv: "Triplex" + "Zhang" + "2024"
  3. Check thesis chapters for citation usage context
  4. If found: Update with verified metadata
  5. If NOT found: **DELETE** and remove from thesis chapters

### Entry 3: guo2024lightrag
- **ok_alt**: `https://arxiv.org/abs/2410.05779`
- **Action**: Visit arXiv link and extract metadata
- **Tasks**:
  1. Parse arXiv page for authors, title, date
  2. Extract: Full author list (likely multiple)
  3. Verify title: "LightRAG: Simple and Fast Retrieval-Augmented Generation"
  4. Confirm publication date (Oct 2024)
  5. Update venue to arXiv:2410.05779
  6. Mark VERIFIED

---

## PHASE 2: YEAR MISMATCHES (5 items)

### Entry 1: agarwal2024llm → agarwal2022llm
- **Current Key**: agarwal2024llm
- **Correct Year**: 2022 (arXiv:2211.10511)
- **Action**: Update citation key throughout thesis

### Entry 2: you2021graph → you2018graph
- **Current Key**: you2021graph
- **Correct Year**: 2018 (ICML 2018)
- **Action**: Update citation key throughout thesis

### Entry 3: wang2024pandalm → wang2023pandalm
- **Current Key**: wang2024pandalm
- **Correct Year**: 2023 (arXiv:2306.05087)
- **Action**: Update citation key throughout thesis

### Entry 4: BuildingDataFramework
- **Current**: Year = "Unknown"
- **Action**: Visit `https://www.llamaindex.ai/blog/building-the-data-framework-for-llms-bca068e89e0e`
- **Tasks**:
  1. Extract publication date from blog post
  2. Update year field
  3. Confirm as @misc (blog post)

### Entry 5: khattab2021baleen → khattab2022baleen
- **Current Key**: khattab2021baleen
- **Correct Year**: 2022 (arXiv:2212.14024)
- **Action**: Update citation key throughout thesis

**PHASE 2 WORKFLOW**:
1. For each entry: `grep -r "cite{OLD_KEY}" chapters/*.tex`
2. Replace: `sed -i 's/\\cite{OLD_KEY}/\\cite{NEW_KEY}/g' chapters/*.tex`
3. Update BibTeX: Rename `@article{OLD_KEY,` → `@article{NEW_KEY,`
4. Ensure year field matches key year
5. Verify compilation with `pdflatex main.tex`

---

## PHASE 3: VERIFY DUPLICATES (4 items)

### Duplicate 1: bai2024hipporag vs jimenezgutierrezHipporagNeurobiologicallyInspired2024
- **Paper**: HippoRAG - Neurobiologically Inspired Long-Term Memory
- **arXiv**: 2405.14831
- **Venue**: NeurIPS 2024
- **Action**:
  1. Compare author lists (Bai vs. Jimenez Gutierrez - first author difference?)
  2. Visit arXiv:2405.14831 to confirm actual first author
  3. **Keep**: Entry with correct first author from arXiv
  4. **Delete**: Duplicate entry
  5. Update all \cite{} commands to unified key

### Duplicate 2: edge2024graphrag vs edge2024local
- **Paper**: From Local to Global: A Graph RAG Approach
- **arXiv**: 2404.16130
- **Authors**: Edge, D. et al. (Microsoft Research)
- **Action**:
  1. Both reference same paper (same arXiv ID)
  2. **Keep**: edge2024graphrag (better key name)
  3. **Delete**: edge2024local
  4. Replace all \cite{edge2024local} → \cite{edge2024graphrag}

### Duplicate 3: ireri2019 vs ireri2019proverbs
- **Paper**: 100 Kikuyu Proverbs and Wise Sayings
- **Author**: Ireri, M. W.
- **Year**: 2019 (Self-published Nairobi)
- **Action**:
  1. Verify both keys reference same book
  2. **Keep**: ireri2019proverbs (more descriptive key)
  3. **Delete**: ireri2019
  4. Replace all \cite{ireri2019} → \cite{ireri2019proverbs}

### Duplicate 4: yasunaga2021qa vs yasunaga2021qagnn
- **Paper**: QA-GNN: Reasoning with LMs and KGs for QA
- **Venue**: NAACL 2021
- **Action**:
  1. Verify both reference same NAACL 2021 paper
  2. **Keep**: yasunaga2021qagnn (matches standard naming)
  3. **Delete**: yasunaga2021qa
  4. Replace all \cite{yasunaga2021qa} → \cite{yasunaga2021qagnn}

**PHASE 3 WORKFLOW**:
1. Visit arXiv/ACL Anthology links to confirm same paper
2. Choose canonical key (more descriptive or standard convention)
3. `grep -r "cite{DUPLICATE_KEY}" chapters/*.tex` to find usages
4. Replace: `sed -i 's/\\cite{DUPLICATE_KEY}/\\cite{CANONICAL_KEY}/g' chapters/*.tex`
5. Delete duplicate from references.bib
6. Verify no orphaned citations remain

---

## PHASE 4: SPECIAL CASES (1 item)

### Entry: he2024gretriever
- **ok_alt**: `fail`
- **Verification_Status**: VERIFIED
- **Issue**: Contradictory (fail but verified?)
- **Action**:
  1. Review notes: "Confirmed 8 authors including LeCun"
  2. Check Where_Found: https://openreview.net/forum?id=M4diZmkPp8
  3. Visit OpenReview link to verify
  4. If verified: Change ok_alt from "fail" → "ok" or add URL
  5. If not verified: Investigate why marked VERIFIED

### Entry: chase2022langchain
- **ok_alt**: `fail`
- **Verification_Status**: VERIFIED
- **Notes**: "GitHub repository"
- **Action**:
  1. GitHub repos are gray literature but acceptable for tools
  2. Change ok_alt to: https://github.com/langchain-ai/langchain
  3. Confirm as @misc entry type
  4. Mark fully VERIFIED

---

## PHASE 5: BULK RE-VERIFICATION FROM LINKS

**Entries with ok_alt = URL (need fresh metadata extraction)**:

1. wang2024hypergraphrag → https://arxiv.org/abs/2503.21322
2. zhang2024graphvis → https://proceedings.neurips.cc/...
3. bai2024hipporag → https://proceedings.neurips.cc/...
4. neo4j2024graphrag → https://neo4j.com/books/...
5. he2022ontology → https://aclanthology.org/K19-1015/
6. fernandez2019ontology → https://aaai.org/papers/...
7. you2021graph → https://arxiv.org/abs/1802.08773
8. jimenezgutierrezHipporagNeurobiologicallyInspired2024 → https://arxiv.org/abs/2405.14831

**For each**:
1. Visit URL
2. Extract: Full author list, exact title, publication year, venue
3. Update CSV with authoritative metadata
4. Cross-check BibTeX entry matches
5. Update if discrepancies found

---

## PHASE 6: FINAL CONSOLIDATION

### Step 1: Create Verified Citations Master List
```bash
# Export cleaned CSV to Excel
python scripts/csv_to_excel_verified.py \
  --input citation-verification/author-verification/Author_Verification_97-Citations_2026-01-21_COMPLETE.csv \
  --output citation-verification/author-verification/Author_Verification_FINAL_2026-01-21.xlsx
```

### Step 2: Update references.bib
```bash
# Backup current bibliography
cp references/references.bib references/references.bib.backup_2026-01-21

# Apply all changes:
# - Delete 3 PENDING entries if not found
# - Rename 5 citation keys (year corrections)
# - Delete 4 duplicate entries
# - Update metadata from fresh URL parsing
```

### Step 3: Update Thesis Chapters
```bash
# Find all citation usages
grep -r "\\cite{" chapters/*.tex | cut -d: -f2 | sort -u > /tmp/all_citations.txt

# For each changed/deleted key:
# - Update \cite{OLD} → \cite{NEW}
# - Remove \cite{DELETED} and rephrase sentence
```

### Step 4: Validate No Broken Citations
```bash
# Extract all \cite{} commands from chapters
grep -oh "\\cite{[^}]*}" chapters/*.tex | sed 's/\\cite{//; s/}//' | sort -u > /tmp/thesis_citations.txt

# Extract all BibTeX keys from references.bib
grep "^@" references/references.bib | sed 's/@[^{]*{//; s/,$//' | sort > /tmp/bib_keys.txt

# Find orphaned citations (in thesis but not in .bib)
comm -23 /tmp/thesis_citations.txt /tmp/bib_keys.txt

# Should return EMPTY (no orphans)
```

### Step 5: Compile and Verify
```bash
cd docs/thesis
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Check for citation warnings
grep -i "citation.*undefined" main.log
# Should be EMPTY

# Check bibliography compiles
grep -i "bibliography" main.log | grep -i error
# Should be EMPTY
```

---

## PHASE 7: FINAL DOCUMENTATION

### Create Final Report
```markdown
# Citation Verification - Final Report
**Date**: January 21, 2026
**Status**: ✅ 100% VERIFIED

## Summary
- Total Citations: 94 (down from 97)
- Deleted: 3 entries (2 PENDING not found, 1 duplicate)
- Corrected: 5 year mismatches
- Consolidated: 4 duplicate pairs → 4 canonical entries
- Fresh Metadata: 8 entries re-verified from authoritative URLs
- Verified: 94/94 (100%)

## Changes Made
[List all deletions, renames, consolidations]

## Validation Results
- ✅ No broken citations in thesis
- ✅ All BibTeX entries have corresponding .tex citations
- ✅ No hallucinated citations remain
- ✅ All years match actual publication dates
- ✅ No duplicate entries remain

## Bibliography Health
- Verification Rate: 100%
- Hallucination Rate: 0%
- Duplicate Rate: 0%
- Gray Literature: X% (acceptable for tools/datasets)
```

### Update Compliance Tracker
```bash
# Update post-defense-revisions/DIRECTIVE_COMPLIANCE_CHECK.md
# Change: ⚠️ 88.7% COMPLETE → ✅ 100% COMPLETE
# Update: Bibliography Health: 88.7% → 100%
# Mark: Directive 3 as FULLY COMPLETE
```

---

## EXECUTION TIMELINE

### Session 1: PENDING + Year Corrections (1.5 hours)
1. Phase 1: Resolve 3 PENDING entries (45 min)
2. Phase 2: Fix 5 year mismatches (45 min)
3. Commit progress

### Session 2: Duplicates + Special Cases (1 hour)
1. Phase 3: Consolidate 4 duplicates (30 min)
2. Phase 4: Resolve 2 special cases (15 min)
3. Phase 5: Re-verify 8 URL entries (15 min)
4. Commit progress

### Session 3: Final Consolidation (1 hour)
1. Phase 6: Update references.bib (20 min)
2. Phase 6: Update thesis chapters (20 min)
3. Phase 6: Validate compilation (10 min)
4. Phase 7: Create final report (10 min)
5. Final commit and push

**Total Time**: 3.5 hours  
**Expected Completion**: January 21, 2026 (end of day)

---

## SUCCESS CRITERIA

✅ **Zero PENDING entries** - All URLs verified or deleted  
✅ **Zero NEEDS_CORRECTION entries** - All keys match actual years  
✅ **Zero VERIFY_DUPLICATE entries** - All duplicates consolidated  
✅ **100% Verification Rate** - All citations verified from authoritative sources  
✅ **Zero Broken Citations** - All \cite{} commands have BibTeX entries  
✅ **Clean LaTeX Compilation** - No citation warnings or errors  
✅ **Final Excel Export** - Author_Verification_FINAL_2026-01-21.xlsx created  
✅ **Updated references.bib** - Matches final verified list exactly  
✅ **Updated Thesis** - All chapters use correct citation keys  
✅ **Documentation Complete** - Final report and compliance check updated  

---

## AUTOMATED SCRIPTS NEEDED

### Script 1: arXiv Metadata Extractor
```python
# scripts/extract_arxiv_metadata.py
# Input: arXiv URL or ID
# Output: JSON with {authors, title, year, abstract, doi}
```

### Script 2: BibTeX Key Renamer
```python
# scripts/rename_bibtex_key.py
# Input: references.bib, old_key, new_key
# Output: Updated .bib + report of changes
```

### Script 3: Citation Usage Finder
```python
# scripts/find_citation_usage.py
# Input: Citation key
# Output: List of files and line numbers using that key
```

### Script 4: Duplicate Detector
```python
# scripts/detect_duplicate_citations.py
# Input: references.bib
# Output: Groups of potential duplicates (same arXiv ID, same DOI, similar titles)
```

---

## RISK MITIGATION

### Backup Strategy
1. **Before any changes**: `git commit -m "Pre-verification checkpoint"`
2. **After each phase**: Commit with descriptive message
3. **Backup references.bib**: Keep timestamped copies
4. **Backup chapters/**: Keep timestamped copies

### Rollback Plan
```bash
# If something goes wrong:
git log --oneline  # Find last good commit
git reset --hard COMMIT_SHA  # Rollback
```

### Validation Checkpoints
- After Phase 1: Run LaTeX compilation
- After Phase 2: Verify no undefined citations
- After Phase 3: Check for orphaned entries
- After Phase 6: Full document compilation
- After Phase 7: Final QA check

---

## NEXT IMMEDIATE ACTION

**START HERE**: Phase 1, Entry 1 - guo2024lazygraphrag  
**Command**: Open browser → Visit Microsoft Research blog link  
**Extract**: Authors, title, publication date, arXiv ID if exists  
**Update**: CSV with verified metadata  
**Mark**: VERIFIED or DELETE if blog-only gray literature  

**Ready to begin? Confirm to start Phase 1.**
