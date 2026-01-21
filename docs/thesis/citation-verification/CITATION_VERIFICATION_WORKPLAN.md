# Citation Verification Completion Workplan

**Date**: January 21, 2026  
**Branch**: `post-defense`  
**File**: `Author_Verification_97-Citations_2026-01-21_COMPLETE.csv`  
**Goal**: Achieve 100% verified bibliography with zero hallucinations

---

## CURRENT STATUS

**Total Citations**: 91 (down from 97)  
**Verified in CSV**: 91/91 (100%)  
**Actually Verified from URLs**: ~68/91 (75%)  
**Remaining Work**: Phase 5 URL re-verification (23 entries)

### Phase Completion Status:
- ✅ **Phase 1 COMPLETE**: 3 PENDING entries resolved (1 verified, 2 deleted)
- ✅ **Phase 2 COMPLETE**: 5 year mismatches corrected
- ✅ **Phase 3 COMPLETE**: 4 duplicate pairs consolidated
- ⏸️ **Phase 4 PENDING**: 2 special cases (deferred until after Phase 5)
- � **Phase 5 CRITICAL**: 23 entries with URLs in ok_alt need FRESH metadata extraction
- ⏸️ **Phase 6 PENDING**: Final consolidation
- ⏸️ **Phase 7 PENDING**: Final documentation

### Critical Discovery (January 21, 2026 - Post Phase 3):
**User identified verification gap**: Many entries marked VERIFIED in CSV have URLs in ok_alt column but metadata was NOT freshly extracted from those authoritative sources per Rule 2. This violates "ok_alt is ground truth" principle. Phase 5 scope expanded from 8→23 entries.

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

## PHASE 1: PENDING ENTRIES ✅ COMPLETE

**Completion Date**: January 21, 2026  
**Commit**: d035b22  
**Results**: 1 verified, 2 deleted → 97→95 citations

### Entry 1: guo2024lazygraphrag ❌ DELETED
- **ok_alt**: `https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/`
- **Resolution**: Blog post only - gray literature, NOT cited in thesis
- **Action Taken**: Marked GRAY_LITERATURE_DELETE in CSV
- **BibTeX**: Removed from references.bib

### Entry 2: zhang2024triplex ❌ DELETED
- **ok_alt**: `Fail`
- **Resolution**: Could not verify existence, NOT cited in thesis
- **Action Taken**: Marked NOT_FOUND_DELETE in CSV
- **BibTeX**: Removed from references.bib

### Entry 3: guo2024lightrag ✅ VERIFIED
- **ok_alt**: `https://arxiv.org/abs/2410.05779`
- **Resolution**: Verified 5 authors from arXiv (submitted Oct 8, 2024)
- **Metadata Extracted**:
  - Authors: Guo, Z., Xia, L., Yu, Y., Ao, T., & Huang, C.
  - Title: LightRAG: Simple and Fast Retrieval-Augmented Generation
  - Venue: arXiv:2410.05779
  - Year: 2024
- **Action Taken**: Updated CSV with verified metadata, marked VERIFIED
- **BibTeX**: No changes needed

**Impact**: 97→95 citations, 88.7%→91.6% verification rate

---

## PHASE 2: YEAR MISMATCHES ✅ COMPLETE

**Completion Date**: January 21, 2026  
**Commit**: [hash]  
**Results**: 5 citation keys corrected → 95 citations maintained

### Entry 1: agarwal2024llm → agarwal2022llm ✅ CORRECTED
- **Issue**: Key said 2024, actual year 2022 (arXiv:2211.10511)
- **Action Taken**: Renamed BibTeX key, updated references.bib
- **Impact**: No thesis citations to update (not cited)

### Entry 2: you2021graph → you2018graph ✅ CORRECTED
- **Issue**: Key said 2021, actual year 2018 (ICML 2018)
- **Action Taken**: Renamed BibTeX key, updated references.bib
- **Impact**: No thesis citations to update (not cited)

### Entry 3: wang2024pandalm → wang2023pandalm ✅ CORRECTED
- **Issue**: Key said 2024, actual year 2023 (arXiv:2306.05087)
- **Action Taken**: 
  - Renamed BibTeX key in references.bib
  - Updated chapters/03-methodology.tex: \cite{wang2024pandalm} → \cite{wang2023pandalm}
- **Impact**: 1 citation updated in thesis

### Entry 4: BuildingDataFramework ✅ CORRECTED
- **Issue**: Year field was missing
- **Resolution**: Blog post dated June 6, 2023
- **Action Taken**: Added year=2023, month=jun, author="Liu, Jerry" to BibTeX
- **Impact**: No thesis citations to update (not cited)

### Entry 5: khattab2021baleen → khattab2022baleen ✅ CORRECTED
- **Issue**: Key said 2021, actual year 2022 (arXiv:2212.14024)
- **Action Taken**: Renamed BibTeX key, updated references.bib
- **Impact**: No thesis citations to update (not cited)

**Impact**: 95 citations, 91.6%→96.8% verification rate

---

## PHASE 3: VERIFY DUPLICATES ✅ COMPLETE

**Completion Date**: January 21, 2026  
**Commit**: 83f0983  
**Results**: 4 duplicates removed → 95→91 citations

### Duplicate 1: bai2024hipporag ❌ DELETED
- **Issue**: Wrong first author (Bai vs. Jimenez Gutierrez)
- **Paper**: HippoRAG - Neurobiologically Inspired Long-Term Memory
- **arXiv**: 2405.14831 (visited to confirm first author)
- **Resolution**: Kept jimenezgutierrezHipporagNeurobiologicallyInspired2024 (correct first author)
- **Action Taken**: 
  - Deleted bai2024hipporag from references.bib
  - Marked DUPLICATE_DELETE in CSV
- **Impact**: No thesis citations affected (not cited)

### Duplicate 2: edge2024graphrag ❌ DELETED
- **Issue**: Identical to edge2024local (same arXiv:2404.16130)
- **Paper**: From Local to Global: A Graph RAG Approach
- **Resolution**: Kept edge2024local (CITED in chapters/01-introduction.tex)
- **Action Taken**:
  - Deleted edge2024graphrag from references.bib
  - Marked DUPLICATE_DELETE in CSV
- **Impact**: No thesis updates needed (duplicate not cited)

### Duplicate 3: ireri2019 ❌ DELETED
- **Issue**: Identical to ireri2019proverbs (same book)
- **Paper**: 100 Kikuyu Proverbs and Wise Sayings
- **Resolution**: Kept ireri2019proverbs (more descriptive key, CITED 4× in thesis)
- **Action Taken**:
  - Deleted ireri2019 from references.bib
  - Marked DUPLICATE_DELETE in CSV
- **Impact**: No thesis updates needed (duplicate not cited)

### Duplicate 4: yasunaga2021qa ❌ DELETED
- **Issue**: Identical to yasunaga2021qagnn (same NAACL 2021 paper)
- **Paper**: QA-GNN: Reasoning with LMs and KGs for QA
- **Resolution**: Kept yasunaga2021qagnn (standard naming convention)
- **Action Taken**:
  - Deleted yasunaga2021qa from references.bib
  - Marked DUPLICATE_DELETE in CSV
- **Impact**: No thesis citations affected (not cited)

**Impact**: 95→91 citations, 96.8%→100% marked VERIFIED in CSV

---

## PHASE 4: SPECIAL CASES ⏸️ DEFERRED

**Status**: Deferred until after Phase 5 completion  
**Reason**: Need to complete bulk URL re-verification first per Rule 2

### Entry 1: he2024gretriever
- **ok_alt**: `fail`
- **Verification_Status**: VERIFIED
- **Issue**: Contradictory (fail but verified?)
- **Deferred Action**:
  1. Review notes: "Confirmed 8 authors including LeCun"
  2. Check Where_Found: https://openreview.net/forum?id=M4diZmkPp8
  3. Visit OpenReview link to verify
  4. If verified: Change ok_alt from "fail" → "ok" or add URL
  5. If not verified: Investigate why marked VERIFIED

### Entry 2: chase2022langchain
- **ok_alt**: `fail`
- **Verification_Status**: VERIFIED
- **Notes**: "GitHub repository"
- **Deferred Action**:
  1. GitHub repos are gray literature but acceptable for tools
  2. Change ok_alt to: https://github.com/langchain-ai/langchain
  3. Confirm as @misc entry type
  4. Mark fully VERIFIED

**Will execute after Phase 5 completion**

---

## PHASE 5: BULK RE-VERIFICATION FROM LINKS 🔴 CRITICAL - IN PROGRESS

**Status**: EXPANDED SCOPE - 23 entries require fresh metadata extraction  
**Discovery Date**: January 21, 2026 (post Phase 3)  
**Critical Issue**: Many entries marked VERIFIED have URLs in ok_alt but metadata NOT extracted per Rule 2

**Rule 2 Violation**: "IF ok_alt = URL THEN visit link, parse fresh metadata, update all columns"  
**Impact**: ~25% of bibliography may have unverified or incorrect metadata

---

### CATEGORY A: ALREADY VERIFIED (Notes confirm fresh metadata extraction)

These entries have URLs in ok_alt AND notes showing metadata was extracted:

1. ✅ **wang2024hypergraphrag** → https://arxiv.org/abs/2503.21322
   - Notes: "Updated with 20 authors from authoritative source" ✓
   
2. ✅ **zhang2024graphvis** → https://proceedings.neurips.cc/paper_files/paper/2024/hash/7cb04f510593c9ba30da398f5e0a7e7b-Abstract-Conference.html
   - Notes: "Verified 6 authors from arXiv" ✓
   
3. ✅ **guo2024lightrag** → https://arxiv.org/abs/2410.05779
   - Notes: "Verified with 5 authors from arXiv (submitted Oct 8 2024)" ✓

**Status**: NO ACTION NEEDED (already properly verified)

---

### CATEGORY B: NEEDS FRESH VERIFICATION (URLs present but no extraction evidence)

These entries have URLs in ok_alt but notes DON'T indicate fresh metadata extraction:

#### 🔴 HIGH PRIORITY - Year Discrepancies Detected

1. **he2022ontology** → https://aclanthology.org/K19-1015/
   - **CRITICAL**: Citation key says 2022, ACL Anthology URL says K19 (2019)
   - Current: Authors: "He, S. et al.", Year: 2022, Title: "Learning to Represent Bilingual Dictionaries"
   - Action: Visit K19-1015, extract actual metadata, likely rename to he2019ontology
   - Notes: "Bilingual learning" (no verification evidence)

2. **brown2023figurative** → https://aclanthology.org/2022.emnlp-main.481.pdf
   - **CRITICAL**: Citation key says 2023, ACL Anthology URL says 2022.emnlp
   - Current: Authors: "Brown, T. C. et al.", Year: 2023, Title: "Figurative Language Understanding: A Survey"
   - Action: Visit URL, extract metadata, likely rename to brown2022figurative
   - Notes: "Figurative language survey" (no verification evidence)

3. **chen2024multilingual** → https://aclanthology.org/2020.findings-emnlp.290/
   - **CRITICAL**: Citation key says 2024, ACL Anthology URL says 2020.findings-emnlp
   - Current: Authors: "Chen, Z. et al.", Year: 2024, Title: "MultiLingual Knowledge Graph Completion via Ensemble Knowledge Distillation"
   - Action: Visit URL, extract metadata, likely rename to chen2020multilingual
   - Notes: "Multilingual KG completion" (no verification evidence)

#### 🟡 MEDIUM PRIORITY - arXiv URLs (Need Author/Title Verification)

4. **sarthi2024raptor** → https://arxiv.org/abs/2401.18059
   - Current: Authors: "Sarthi, P. et al.", Year: 2024
   - Notes: "Added OpenReview URL" (URL added but metadata not extracted)
   - Action: Visit arXiv, extract full author list, verify title exactly

5. **lewis2020retrieval** → https://arxiv.org/abs/2005.11401
   - Current: Authors: "Lewis, P. et al.", Year: 2020
   - Notes: "Foundational RAG paper" (no verification evidence)
   - Action: Visit arXiv, extract full author list (likely Facebook AI authors)

6. **you2018graph** → https://arxiv.org/abs/1802.08773
   - Current: Authors: "You, J. et al.", Year: 2018
   - Notes: "Year corrected: key updated from you2021graph to you2018graph"
   - Action: Visit arXiv, verify authors and title (year already corrected)

7. **zhou2024collaborative** → https://arxiv.org/html/2411.04920v1
   - Current: Authors: "Zhou, X. et al.", Year: 2024
   - Notes: "LLM knowledge construction" (no verification evidence)
   - Action: Visit arXiv, extract full author list, verify title

8. **chenOmniRAGComprehensiveRetrievalAugmented2025** → https://arxiv.org/abs/2501.02460
   - Current: Authors: "Chen, Z. et al.", Year: 2025
   - Notes: "Medical RAG comprehensive" (no verification evidence)
   - Action: Visit arXiv, extract authors, verify title

9. **zhao2025medrag** → https://arxiv.org/abs/2502.04413
   - Current: Authors: "Zhao, X. et al.", Year: 2025
   - Notes: "Replacement for jin2024medrag" (no verification evidence)
   - Action: Visit arXiv, extract authors, verify title

10. **costa2022no** → https://arxiv.org/abs/2207.04672
    - Current: Authors: "Costa-jussà, M. R. et al.", Year: 2022
    - Notes: "Multilingual MT foundation" (no verification evidence)
    - Action: Visit arXiv, extract full author list (NLLB paper, many authors)

11. **zhao2020knowledge** → https://arxiv.org/abs/2106.07935
    - Current: Authors: "Zhao, W. et al.", Year: 2020
    - Notes: "Readability with KG" (no verification evidence)
    - Action: Visit arXiv, verify year matches (arXiv ID is 2106 = June 2021, not 2020!)

12. **sun2020knowledge** → https://arxiv.org/abs/1809.00782
    - Current: Authors: "Sun, H. et al.", Year: 2020
    - Notes: "KB-text fusion" (no verification evidence)
    - Action: Visit arXiv, verify year (arXiv ID is 1809 = Sept 2018, not 2020!)

#### 🟢 LOW PRIORITY - Book/Misc URLs (Need Title/Metadata Verification)

13. **neo4j2024graphrag** → https://neo4j.com/books/definitive-guide-graph-databases-rdbms-developer/
    - Current: Authors: "Neo4j Inc.", Year: 2024
    - Notes: "Changed to @book with exact title" (title extracted but needs verification)
    - Action: Visit URL, verify title exactly, check publication date

14. **liu2022llamaindex** → https://www.ibm.com/think/topics/llamaindex
    - Current: Authors: "Liu, J.", Year: 2022
    - Notes: "GitHub repository" (contradicts ok_alt which is IBM blog)
    - Action: Visit IBM blog, extract metadata, determine if @misc or @online

15. **christie2019indigenous** → https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/journals-and-magazines/social-policy-journal/spj17/decolonizing-methodologies-research-and-indigenous-peoples.html
    - Current: Authors: "Christie, M.", Year: 2019
    - Notes: "Indigenous research ethics" (no verification evidence)
    - Action: Visit URL, extract authors, title, journal details

16. **fernandez2019ontology** → https://aaai.org/papers/0005-ss97-06-005-methontology-from-ontological-art-towards-ontological-engineering/
    - Current: Authors: "Fernández-López, M. et al.", Year: 2000
    - Notes: "Ontology methodology" (no verification evidence)
    - Action: Visit AAAI URL (says ss97 = 1997, not 2000!), extract metadata

17. **poveda2014oops** → https://www.semantic-web-journal.net/system/files/swj989.pdf
    - Current: Authors: "Poveda-Villalón, M. et al.", Year: 2014
    - Notes: "Ontology validation tool" (no verification evidence)
    - Action: Visit PDF, extract authors, verify title and year

18. **kenyatta1938facing** → https://sahistory.org.za/sites/default/files/archive-files3/jomo_kenyatta_facing_mount_kenya_the_tribal_lifbook4me.org_.pdf
    - Current: Authors: "Kenyatta, J.", Year: 1938
    - Notes: "Kikuyu ethnography" (no verification evidence)
    - Action: Visit PDF, verify title page matches 1938 Secker and Warburg edition

19. **noy2001ontology** → https://protege.stanford.edu/publications/ontology_development/ontology101.pdf
    - Current: Authors: "Noy, N. F. & McGuinness, D. L.", Year: 2001
    - Notes: "Ontology development guide" (no verification evidence)
    - Action: Visit Stanford PDF, extract metadata from document

20. **suarez2012ontology** → https://link.springer.com/chapter/10.1007/978-3-642-24794-1_1
    - Current: Authors: "Suárez-Figueroa, M. C. et al.", Year: 2012
    - Notes: "Ontology engineering" (no verification evidence)
    - Action: Visit Springer link, extract authors, verify title

21. **ma2023hybrid** → https://medium.com/@zhengbuqian/enhancing-information-retrieval-with-learned-sparse-embeddings-16e701db4003
    - Current: Authors: "Ma, X. et al.", Year: 2023
    - Notes: "Hybrid retrieval" (no verification evidence)
    - Action: Visit Medium blog, determine if blog post or links to paper

22. **almeida2019challenges** → https://chnt.at/wp-content/uploads/Bordoni_2014.pdf
    - Current: Authors: "Almeida, J. P. et al.", Year: 2019
    - Notes: "Domain ontology" (no verification evidence)
    - Action: Visit PDF (URL says Bordoni 2014, not Almeida 2019!), extract metadata

23. **keegan2017maori** → https://researchcommons.waikato.ac.nz/entities/publication/46ddab82-fb00-4911-8e70-d1ac59879fc8
    - Current: Authors: "Keegan, T. T. et al.", Year: 2017
    - Notes: "Indigenous language tech" (no verification evidence)
    - Action: Visit Waikato repository, extract full metadata

---

### PHASE 5 WORKFLOW

**For each entry in Category B (23 entries)**:

1. **Visit ok_alt URL** using fetch_webpage tool
2. **Extract authoritative metadata**:
   - Full author list (all authors, not "et al.")
   - Exact title (word-for-word from source)
   - Publication year (from source, not arXiv submission date)
   - Venue (journal, conference, book publisher)
3. **Compare extracted vs. CSV data**:
   - Authors match? (check first author especially)
   - Year matches? (RED FLAG if discrepancy)
   - Title matches? (check for errors)
   - Venue correct?
4. **Update CSV if discrepancies found**:
   - Authors column: Update with full list
   - Year column: Correct to authoritative source
   - Title column: Fix any errors
   - Venue column: Update with official venue
   - Notes column: Add "Verified from [URL] - [metadata extracted]"
5. **Update references.bib if needed**:
   - If year changed: Rename citation key
   - If authors changed: Update author field
   - If title changed: Update title field
   - If venue changed: Update journal/booktitle/etc.
6. **Update thesis chapters if citation key changed**:
   - Search for \cite{OLD_KEY}
   - Replace with \cite{NEW_KEY}
7. **Mark entry as truly VERIFIED**:
   - Update Verification_Status if needed
   - Update ok_alt to "ok" after URL verification complete

---

### EXPECTED ISSUES TO FIX

Based on URL analysis, likely corrections needed:

**Year Mismatches** (6+ entries):
- he2022ontology → he2019ontology (K19 = 2019)
- brown2023figurative → brown2022figurative (2022.emnlp)
- chen2024multilingual → chen2020multilingual (2020.findings-emnlp)
- zhao2020knowledge → zhao2021knowledge (arXiv 2106 = June 2021)
- sun2020knowledge → sun2018knowledge (arXiv 1809 = Sept 2018)
- fernandez2019ontology → fernandez1997ontology (ss97 = 1997)
- almeida2019challenges → bordoni2014... (URL says 2014)

**Author Mismatches** (unknown until verification):
- liu2022llamaindex: May need corporate author or different author
- ma2023hybrid: Verify first author from actual paper
- Others TBD

**Title Errors** (unknown until verification):
- Multiple entries may have slight title variations

---

### PHASE 5 TIMELINE

**Estimated Time**: 4-5 hours total
- High Priority (3 year discrepancies): 45 min
- Medium Priority (12 arXiv URLs): 2 hours
- Low Priority (8 misc URLs): 1.5 hours
- CSV + BibTeX updates: 1 hour

**Completion Target**: January 21, 2026 (end of day)

---

**NEXT ACTION**: Start with HIGH PRIORITY entries (year discrepancies) first

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
