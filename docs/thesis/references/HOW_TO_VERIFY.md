# How to Use the Verification Checklist

This guide explains how to use `COMPREHENSIVE_VERIFICATION_CHECKLIST.csv` for manual bibliography verification.

## Opening the File

**Recommended**: Open in Excel, Google Sheets, or LibreOffice Calc for best viewing.

```bash
# Open in default application
open docs/thesis/references/COMPREHENSIVE_VERIFICATION_CHECKLIST.csv
```

## Column Descriptions

| Column | Purpose | What to Check |
|--------|---------|---------------|
| **Citation_Key** | BibTeX citation key | Matches key in references.bib and \cite{} commands |
| **Authors** | Author list | Names are correct, "et al." used appropriately |
| **Year** | Publication year | Matches actual publication date, not arXiv submission |
| **Title** | Paper/book title | Exact title from authoritative source |
| **Venue** | Conference/journal | Correct venue name and year |
| **Entry_Type** | BibTeX type | article, inproceedings, book, misc |
| **Priority** | Importance level | CRITICAL/HIGH/MEDIUM/LOW based on thesis impact |
| **Google_Scholar_Search_Query** | Search string | Copy-paste into Google Scholar for verification |
| **Where_Found_Option** | Source URL | Authoritative link to paper/resource |
| **Notes** | Additional info | Phase 3 updates, corrections made, special notes |
| **Verification_Status** | Current status | VERIFIED/PENDING/NEEDS_CORRECTION/VERIFY_DUPLICATE |
| **Action_Required** | Next step | What needs to be done for PENDING/NEEDS_CORRECTION entries |

## Verification Workflow

### For VERIFIED Entries ✅
1. Spot-check high-priority entries by clicking the URL
2. Confirm authors/title match the source
3. If everything looks good, no action needed

### For PENDING Entries ⏳
1. Copy the `Google_Scholar_Search_Query` text
2. Paste into [Google Scholar](https://scholar.google.com)
3. Find the correct paper
4. Update the `Where_Found_Option` with the URL
5. Verify authors, year, title, venue
6. Change `Verification_Status` to VERIFIED
7. Update `references.bib` with correct information

### For NEEDS_CORRECTION Entries 🔧
1. Note the issue in the `Notes` column (usually year mismatch)
2. Follow the action in `Action_Required` column
3. Update the citation key in `references.bib`
4. Search all `.tex` files for the old key
5. Replace with the new key
6. Mark as VERIFIED once complete

### For VERIFY_DUPLICATE Entries 🔍
1. Open `references.bib` in your editor
2. Search for both citation keys listed in `Notes`
3. Compare the entries side-by-side
4. Determine which entry is more complete/accurate
5. Search `.tex` files for both keys
6. Replace all citations with the retained key
7. Delete the duplicate entry from `references.bib`
8. Mark as VERIFIED

## Priority-Based Review Strategy

### Start with CRITICAL entries (6 total)
These are foundational to your thesis. Verify these first:
- Core methodology papers (OG-RAG, RAG)
- Cultural sources (Kenyatta, Gikandi, Ireri)
- Indigenous data governance (CARE Principles)

### Then HIGH priority (43 entries)
Your main literature review papers:
- GraphRAG variants (HyperGraphRAG, GNN-RAG, G-Retriever)
- RAG architectures (RAPTOR, HippoRAG, MedRAG)
- Knowledge graph papers
- Low-resource NLP papers

### Finally MEDIUM and LOW (48 entries)
Supporting literature and peripheral references.

## Quick Actions

### Find Entries Needing Attention
```bash
# In terminal, filter CSV for pending/correction items
grep "PENDING\|NEEDS_CORRECTION\|VERIFY_DUPLICATE" \
  docs/thesis/references/COMPREHENSIVE_VERIFICATION_CHECKLIST.csv
```

### Count by Status
```bash
# Count verified entries
grep -c "VERIFIED" docs/thesis/references/COMPREHENSIVE_VERIFICATION_CHECKLIST.csv

# Count pending entries  
grep -c "PENDING" docs/thesis/references/COMPREHENSIVE_VERIFICATION_CHECKLIST.csv

# Count corrections needed
grep -c "NEEDS_CORRECTION" docs/thesis/references/COMPREHENSIVE_VERIFICATION_CHECKLIST.csv
```

## Updating references.bib

After verifying an entry in the CSV:

1. **Open references.bib** in your editor
2. **Find the entry** using the citation key
3. **Update metadata** based on CSV verification
4. **Save the file**
5. **Recompile thesis** to check for broken citations

### Example: Fixing a Year Mismatch

**CSV shows**: `agarwal2024llm` should be `agarwal2022llm` (actual year 2022)

```bibtex
# BEFORE (incorrect)
@article{agarwal2024llm,
  author = {Agarwal, Oshin and ...},
  year = {2022},  # <-- Key says 2024 but year is 2022!
  ...
}

# AFTER (correct)
@article{agarwal2022llm,
  author = {Agarwal, Oshin and ...},
  year = {2022},
  ...
}
```

Then update all `.tex` files:
```latex
# BEFORE
\cite{agarwal2024llm}

# AFTER  
\cite{agarwal2022llm}
```

## Verification Checklist

Use this checklist for each entry you manually verify:

- [ ] Google Scholar search confirms paper exists
- [ ] Authors are complete and correctly spelled
- [ ] Year matches actual publication (not arXiv submission)
- [ ] Title is exact (including capitalization)
- [ ] Venue is correct (conference name, journal, publisher)
- [ ] URL/DOI is accessible and points to correct paper
- [ ] Citation key matches year (e.g., smith2023paper for 2023)
- [ ] Entry type is appropriate (@article, @inproceedings, @book)
- [ ] No duplicate entries exist for this paper

## Common Issues to Watch For

### ❌ Year Mismatches
**Problem**: Citation key says 2024, but paper published in 2023  
**Fix**: Update key to match publication year

### ❌ arXiv vs. Conference
**Problem**: Using arXiv entry when paper was published at a conference  
**Fix**: Update venue to conference name, keep arXiv as note/URL

### ❌ Incomplete Author Lists
**Problem**: "Wang et al." when there are only 2-3 authors  
**Fix**: List all authors explicitly

### ❌ Wrong Venue Year
**Problem**: Paper says "EMNLP 2022" but it's actually EMNLP 2023  
**Fix**: Verify venue year from authoritative source

### ❌ Duplicate Entries
**Problem**: Same paper appears twice with different keys  
**Fix**: Keep one, update all citations, delete duplicate

## Tips for Efficient Verification

1. **Batch by Source**: Verify all arXiv papers together, then ACL papers, etc.
2. **Use Publisher Tools**: ACL Anthology, NeurIPS proceedings have export BibTeX
3. **Trust Verified Entries**: Focus on PENDING/NEEDS_CORRECTION items
4. **Document Changes**: Update the Notes column with any corrections made
5. **Test Compilation**: After major changes, compile thesis to catch broken citations

## After Verification is Complete

1. ✅ All entries marked as VERIFIED
2. ✅ No PENDING or NEEDS_CORRECTION items remain
3. ✅ Duplicates resolved
4. ✅ Thesis compiles without citation errors
5. ✅ Spot-check 10-20 random citations in compiled PDF

**Then**: Bibliography is publication-ready! 🎉

---

## Need Help?

- **CSV won't open properly**: Try UTF-8 encoding in your spreadsheet app
- **Can't find a paper**: Check alternative spellings, look for updated versions
- **Broken URL**: Search by title+authors on Google Scholar for alternative link
- **Duplicate confusion**: Compare DOIs/arXiv IDs - if same, it's a duplicate

---

**Created**: January 18, 2026  
**For**: Comprehensive bibliography verification (97 entries)  
**Related Files**: 
- `COMPREHENSIVE_VERIFICATION_CHECKLIST.csv`
- `VERIFICATION_SUMMARY.md`
- `docs/thesis/references/references.bib`
