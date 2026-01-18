# BIBLIOGRAPHY AUDIT - STEP-BY-STEP PROCEDURE

**Directive**: 3 (Highest Priority - Academic Integrity)  
**Date**: January 16, 2026  
**Estimated Duration**: 2-3 hours  
**Status**: Ready to Execute

---

## 🎯 OBJECTIVE

Systematically verify every citation in the thesis bibliography, identify hallucinated references, and replace them with verified sources or remove unsupported claims.

---

## 📋 STEP-BY-STEP PROCEDURE

### **PHASE 1: INVENTORY AND RISK ASSESSMENT** (15 minutes)

#### Step 1.1: Count Total Citations
```bash
# Count all citations in references.bib
grep -c "^@" /Users/ndethi/dev/opit/opit-rai9001/docs/thesis/references/references.bib
```
**Expected**: ~100-150 citations

#### Step 1.2: Identify High-Risk Citations
```bash
# Extract all 2024+ citations (high risk for hallucination)
grep -E "@(article|inproceedings|misc|book).*\{.*202[456]" \
  /Users/ndethi/dev/opit/opit-rai9001/docs/thesis/references/references.bib > high_risk_citations.txt

# Count them
wc -l high_risk_citations.txt
```
**Current Count**: 25 citations from 2024+

#### Step 1.3: Extract Citation Keys
```bash
# Get list of all citation keys for tracking
grep "^@" references.bib | sed 's/@[^{]*{\([^,]*\).*/\1/' > all_citation_keys.txt
```

#### Step 1.4: Create Audit Spreadsheet Template
**File**: `BIBLIOGRAPHY_AUDIT_SHEET.csv`

**Columns**:
- Citation_Key (e.g., chen2024og)
- Authors (e.g., "Chen et al.")
- Year (e.g., 2024)
- Title
- Venue (Journal/Conference)
- Google_Scholar_Found (YES/NO)
- Status (VERIFIED/FAKE/SUSPICIOUS)
- Notes
- Action (KEEP/REPLACE/DELETE)
- Replacement_Citation (if needed)

---

### **PHASE 2: SYSTEMATIC VERIFICATION** (90-120 minutes)

#### Step 2.1: Verify All 2024+ Citations (HIGH PRIORITY)

**For EACH of the 25 citations from 2024+:**

**Verification Protocol**:
1. Copy exact title from .bib file
2. Search Google Scholar: https://scholar.google.com
3. Check:
   - ✅ Paper exists with exact title?
   - ✅ Authors match exactly?
   - ✅ Year matches?
   - ✅ Venue is real (conference/journal has official website)?
   - ✅ DOI/arXiv link works?
   - ✅ Paper content matches what thesis claims?

**Red Flags** (Mark as FAKE):
- ❌ No Google Scholar results for exact title
- ❌ Authors don't exist (no Google Scholar profiles, no university affiliations)
- ❌ Conference doesn't exist (no official website)
- ❌ arXiv number doesn't work
- ❌ Publication date impossible (cited before paper existed)
- ❌ Title sounds AI-generated ("Comprehensive Survey of...")

**Examples from Current Bibliography to Check**:

1. **chen2024og** - "Ontology-Grounded Retrieval-Augmented Generation"
   - Search: Full title in Google Scholar
   - Check: NeurIPS 2024 proceedings
   - Verify: Authors "Chen, Xiaoxuan" exist

2. **wang2024hypergraphrag** - "HyperGraphRAG: Enhancing..."
   - Search: Full title + authors
   - Check: ACL 2024 proceedings
   - Verify: DOI works

3. **edge2024graphrag** - "From Local to Global: A Graph RAG Approach"
   - Search: arXiv:2404.16130
   - Check: Authors at Microsoft Research
   - **LIKELY REAL** - this is Microsoft's GraphRAG paper

#### Step 2.2: Verify Foundational/Core Citations (30 minutes)

**Check these MUST-BE-REAL citations**:
- lewis2020retrieval (RAG paper - VERIFY: NeurIPS 2020)
- karpukhin2020dense (DPR - VERIFY: EMNLP 2020)
- reimers2019sentence (Sentence-BERT - VERIFY: EMNLP 2019)
- papineni2002bleu (BLEU - VERIFY: ACL 2002)
- lin2004rouge (ROUGE - VERIFY: ACL 2004 Workshop)

**Why check these?**
Even foundational papers can have typos in author names or venues.

#### Step 2.3: Verify Cultural/Kikuyu Citations (30 minutes)

**HIGH RISK AREA** - African NLP citations are often hallucinated.

**Check every citation about**:
- Kikuyu language
- Kikuyu culture
- African NLP
- Low-resource languages
- Bantu languages

**Search Strategy**:
1. Google Scholar exact title
2. If not found, search author + "Kikuyu" + year
3. Check if author has publications (university page, ResearchGate)
4. Verify Ireri (2017) citation - this is YOUR gold standard corpus

**Critical Citation to Verify**:
- Ireri (2017) - What's the exact publication?
  - Book? Thesis? Journal article?
  - Publisher? Pages?
  - **ACTION**: Find exact bibliographic details

#### Step 2.4: Check In-Text Citation Accuracy (30 minutes)

**For 5-10 VERIFIED papers, cross-check claims**:

1. Find where cited in thesis (grep citation key in .tex files)
2. Read what thesis claims the paper says
3. Read the paper's abstract
4. **Verify**: Does the claim match the paper?

**Example**:
```
Thesis says: "Chen et al. (2024) showed ontology-grounding improves 
              cultural translation by 15%."

Check: Does chen2024og paper actually report 15%? Actually discuss 
       cultural translation? Or is this a hallucination?
```

---

### **PHASE 3: REPLACEMENT STRATEGY** (30-45 minutes)

#### Step 3.1: Categorize Fake Citations

**For each FAKE citation identified:**

**Category A: Specific fake claim that's actually true**
- **Example**: Fake paper about "RAG improves factuality"
- **Action**: Find REAL paper making this claim
- **Replacement**: Lewis et al. (2020) - original RAG paper

**Category B: Vague claim without specific evidence**
- **Example**: "Recent work has shown..." + 3 fake citations
- **Action**: Remove "Recent work" phrase, make claim general
- **Replacement**: Either cite foundational work OR delete citation

**Category C: Completely unsupported claim**
- **Example**: "Ontology-grounded systems improve cultural translation by 20%"
- **Action**: DELETE claim entirely (no evidence exists)
- **Replacement**: None - rewrite section without this claim

#### Step 3.2: Use Verified Replacement List

**SAFE REPLACEMENTS** (from prompt - all verified):

**LLMs**:
- Brown et al. (2020) - "Language Models are Few-Shot Learners" (GPT-3)
- OpenAI (2023) - "GPT-4 Technical Report" arXiv:2303.08774

**RAG**:
- Lewis et al. (2020) - "Retrieval-Augmented Generation..." NeurIPS
- Guu et al. (2020) - "REALM: Retrieval-Augmented LM Pre-Training" ICML

**Knowledge Graphs**:
- Speer & Havasi (2012) - "ConceptNet 5" LREC
- Bollacker et al. (2008) - "Freebase" SIGMOD

**Sentence Embeddings**:
- Reimers & Gurevych (2019) - "Sentence-BERT" EMNLP

**MT Evaluation**:
- Papineni et al. (2002) - "BLEU" ACL
- Lin (2004) - "ROUGE" ACL Workshop
- Banerjee & Lavie (2005) - "METEOR" ACL Workshop

**Low-Resource NLP**:
- Joshi et al. (2020) - "State and Fate of Linguistic Diversity" ACL
- Nekoto et al. (2020) - "Participatory Research for Low-resourced MT" EMNLP

**African NLP**:
- Orife et al. (2020) - "Masakhane - MT For Africa" AfricaNLP Workshop

#### Step 3.3: Create Replacement Map

**File**: `CITATION_REPLACEMENT_MAP.txt`

**Format**:
```
OLD: chen2024og (FAKE - doesn't exist)
NEW: lewis2020retrieval (REAL - original RAG paper)
FILES TO UPDATE: chapters/02-literature-review-v2.0.0.tex (line 145)
CLAIM CHANGE: "Chen et al. showed..." → "Lewis et al. demonstrated..."
```

---

### **PHASE 4: EXECUTE REPLACEMENTS** (30-45 minutes)

#### Step 4.1: Update references.bib

**For each FAKE citation**:
1. Comment out with % (don't delete yet - may need reference)
2. Add REAL replacement citation
3. Add comment explaining replacement

**Example**:
```bibtex
% REMOVED: Fake citation - paper doesn't exist
% @inproceedings{chen2024og,
%   title = {Ontology-Grounded RAG...},
%   author = {Chen et al.},
%   year = {2024}
% }

% REPLACEMENT: Original RAG paper (verified NeurIPS 2020)
@inproceedings{lewis2020retrieval,
  author = {Lewis, Patrick and Perez, Ethan and ...},
  title = {Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks},
  booktitle = {Advances in Neural Information Processing Systems 33},
  year = {2020},
  pages = {9459--9474}
}
```

#### Step 4.2: Update In-Text Citations

**For each chapter .tex file**:
1. Search for old citation key (e.g., `\citep{chen2024og}`)
2. Replace with new key (e.g., `\citep{lewis2020retrieval}`)
3. Update surrounding text if claim changes

**Use multi_replace_string_in_file for efficiency**

#### Step 4.3: Remove Orphaned Claims

**If claim has NO valid replacement**:
1. Find paragraph containing claim
2. Delete claim sentence
3. Verify paragraph still flows logically
4. If paragraph now empty, delete entire paragraph

#### Step 4.4: Test LaTeX Compilation

```bash
cd /Users/ndethi/dev/opit/opit-rai9001/docs/thesis
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Check for errors**:
- ❌ "Citation undefined" → missed a replacement
- ❌ "Empty thebibliography environment" → .bib file broken
- ✅ "Output written to main.pdf" → SUCCESS

---

### **PHASE 5: VERIFICATION AND DOCUMENTATION** (15 minutes)

#### Step 5.1: Generate Final Audit Report

**File**: `BIBLIOGRAPHY_AUDIT_REPORT.md`

**Contents**:
```markdown
# Bibliography Audit Report

**Date**: January 16, 2026
**Auditor**: GitHub Copilot + User Verification
**Thesis**: thiLLMo OG-RAG System

## Summary

- Total Citations Reviewed: XXX
- Verified as Real: XXX
- Identified as Fake: XXX
- Replaced: XXX
- Deleted (no replacement): XXX

## Fake Citations Removed

1. chen2024og - "Ontology-Grounded RAG..." (NeurIPS 2024)
   - Issue: Paper doesn't exist, authors not found
   - Replacement: lewis2020retrieval
   - Chapters Updated: 02-literature-review-v2.0.0.tex

[... list all fakes ...]

## Verification Notes

- All foundational citations (RAG, BLEU, ROUGE) verified ✅
- Kikuyu/African NLP citations checked ✅
- In-text claims matched to paper content ✅

## Next Steps

- Directive 1: Evaluation Methodology Rewrite
- Directive 4: Deformalize Hypotheses
```

#### Step 5.2: Update Revision Tracker

Mark Directive 3 as ✅ COMPLETE in `POST_DEFENSE_REVISION_TRACKER.md`

#### Step 5.3: Git Commit

```bash
git add docs/thesis/references/references.bib
git add docs/thesis/chapters/*.tex
git add docs/thesis/BIBLIOGRAPHY_AUDIT_REPORT.md
git commit -m "Bibliography audit: Remove hallucinated citations, verify all sources

- Verified all 2024+ citations (25 total)
- Removed X fake citations
- Replaced with verified foundational papers
- Updated in-text claims to match real sources
- All citations now Google Scholar verified"
git push origin post-defense
```

---

## 🔍 QUALITY CHECKS

**Before marking complete, verify**:

- [ ] Every citation in references.bib found in Google Scholar
- [ ] Every author has verifiable academic profile
- [ ] Every venue (journal/conference) has official website
- [ ] Every DOI/arXiv link works
- [ ] Every in-text citation has corresponding .bib entry
- [ ] Every .bib entry is cited in thesis (no orphans)
- [ ] LaTeX compiles without "Citation undefined" errors
- [ ] Generated PDF has complete bibliography section
- [ ] All claims match cited paper content (spot-checked)

---

## 📊 EXPECTED OUTCOMES

**Pessimistic Scenario** (Many fakes found):
- 25 citations from 2024+ checked
- 15 are fake (60% hallucination rate)
- 10 replacements found
- 5 claims deleted (no valid replacement)
- 3 hours total time

**Optimistic Scenario** (Few fakes):
- 25 citations from 2024+ checked
- 5 are fake (20% hallucination rate)
- 5 replacements found
- 0 claims deleted
- 2 hours total time

**Realistic Scenario**:
- 25 citations from 2024+ checked
- 10 are fake (40% hallucination rate)
- 8 replacements found
- 2 claims deleted
- 2.5 hours total time

---

## ⚠️ CRITICAL REMINDERS

**During Execution**:
- ✅ Verify EVERY citation - don't assume it's real
- ✅ Check author names match exactly (not just similar)
- ✅ Verify publication year (not cited before paper existed)
- ✅ Read abstracts to confirm claims match
- ✅ Save work frequently (git commit after each phase)

**Don't**:
- ❌ Trust that "it sounds real" = it is real
- ❌ Skip verification because author is famous
- ❌ Delete citations without checking if they're used
- ❌ Rush - accuracy matters more than speed

---

## 🚀 READY TO EXECUTE?

**This procedure is now documented.**

**Next step**: Begin Phase 1 (Inventory and Risk Assessment)

**Confirm to start**: "Begin bibliography audit - Phase 1"

