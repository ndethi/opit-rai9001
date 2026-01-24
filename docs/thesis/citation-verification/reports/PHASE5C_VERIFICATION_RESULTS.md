# Phase 5C URL Verification Results
## LOW PRIORITY URLs (Books, PDFs, Miscellaneous Sources)

**Date:** January 21, 2026  
**Verifier:** AI Agent  
**Total Entries:** 11  
**Successfully Fetched:** 6  
**Failed (PDF direct links):** 5  
**Errors Discovered:** 5 critical metadata errors

---

## CRITICAL ERRORS REQUIRING CORRECTION

### 1. liu2022llamaindex → WRONG AUTHORS, WRONG SOURCE TYPE
**Current CSV:**
- Key: `liu2022llamaindex`
- Authors: "Liu, J."
- Year: 2022
- Venue: "GitHub repository"
- URL: https://www.ibm.com/think/topics/llamaindex

**Actual from URL:**
- Authors: "Winland, V. & Russi, E."
- Title: "What is LlamaIndex?"
- Publisher: IBM Think (educational article/blog)
- Year: Not explicitly stated, references 2024 developments
- Type: @misc or @online, NOT GitHub repository

**Correction needed:**
- Authors: Liu → "Winland, V. & Russi, E." (IBM)
- Venue: Remove "GitHub repository"
- Entry type: @misc
- Note: Jerry Liu created LlamaIndex framework, but THIS URL is IBM educational content

---

### 2. christie2019indigenous → COMPLETELY WRONG ENTRY
**Current CSV:**
- Key: `christie2019indigenous`
- Authors: "Christie, M."
- Year: 2019
- Title: "Decolonizing Methodologies: Research and Indigenous Peoples"
- URL: https://www.msd.govt.nz/.../decolonizing-methodologies-research-and-indigenous-peoples.html

**Actual from URL:**
- This is a BOOK REVIEW by "Wilson, C." published December 2001
- Journal: Social Policy Journal of New Zealand, Issue 17
- Book being reviewed: "Decolonizing Methodologies" by Linda Tuhiwai Smith (1999), Zed Books
- Reviewer affiliation: Knowledge Management Group, Ministry of Social Development

**Correction Options:**
1. **Option A - Use book review:** wilson2001decolonizing, authors "Wilson, C.", 2001, @article
2. **Option B - Use original book:** smith1999decolonizing, authors "Tuhiwai Smith, L.", 1999, @book
3. **Option C - Delete entry** if this was mistaken citation

**Decision needed:** Which source was actually intended for citation?

---

### 3. fernandez2019ontology → WRONG YEAR (22-year error from key, 3-year from notes)
**Current CSV:**
- Key: `fernandez2019ontology`
- Authors: "Fernández-López, M. et al." (notes show Year: 2000)
- Venue: "AAAI Spring Symposium"
- URL: https://aaai.org/papers/0005-ss97-06-005-methontology...

**Actual from URL:**
- Authors: "Fernández, M., Gómez-Pérez, A., & Juristo, N." (3 authors, not "et al.")
- Title: "Methontology: From Ontological Art Towards Ontological Engineering"
- Proceedings: Papers from the 1997 AAAI Spring Symposium
- Code: SS-97-06
- Year: **1997** (not 2000, definitely not 2019)

**Correction needed:**
- Key: fernandez2019ontology → fernandez1997methontology
- Authors: List all 3 authors explicitly
- Year: 1997
- Name: Fernández (not Fernández-López)

---

### 4. ma2023hybrid → WRONG AUTHOR, WRONG YEAR
**Current CSV:**
- Key: `ma2023hybrid`
- Authors: "Ma, X. et al."
- Year: 2023
- Title: "Hybrid Retrieval with Learned Sparse Embeddings"
- Venue: "arXiv:2302.13971"
- URL: https://medium.com/@zhengbuqian/enhancing-information-retrieval-with-learned-sparse-embeddings-16e701db4003

**Actual from URL:**
- Author: "Buqian Zheng" (zhengbuqian) - NOT "Ma, X."
- Published: April 26, 2024 (NOT 2023)
- Platform: Medium blog post
- Affiliation: Engineer at Zilliz
- Title: "Enhancing Information Retrieval with Learned Sparse Embeddings — Part 1"

**Issue:** CSV lists arXiv:2302.13971 as venue but URL is Medium blog. Need to verify if:
- This should cite actual arXiv paper (different authors)
- OR this Medium blog post (Zheng 2024)

**Correction needed:**
- Check arXiv:2302.13971 for actual authors
- If blog post intended: Key → zheng2024learned, Author → "Zheng, B.", Year → 2024, Type → @misc

---

### 5. keegan2017maori → WRONG URL (points to 2007 PhD thesis, not 2017 journal article)
**Current CSV:**
- Key: `keegan2017maori`
- Authors: "Keegan, T. T. et al."
- Year: 2017
- Title: "Using Indigenous Language in Digital Technologies"
- Venue: "AlterNative"
- URL: https://researchcommons.waikato.ac.nz/entities/publication/46ddab82-fb00-4911-8e70-d1ac59879fc8
- DOI: https://doi.org/10.1177/1177180117701779

**Actual from URL:**
- Title: "Indigenous Language Usage in a Digital Library: He Hautoa Kia Ora Tonu Ai."
- Type: PhD Thesis (not journal article)
- Author: "Keegan, Te Taka Adrian Gregory" (T. T. A. G.)
- Date: **2007** (not 2017)
- Degree: Doctor of Philosophy (PhD)
- University: The University of Waikato
- Supervisors: Apperley, M., Benton, R., Cunningham, S. J.

**Issue:** DOI https://doi.org/10.1177/1177180117701779 likely points to correct 2017 AlterNative journal article, but ok_alt URL points to wrong 2007 thesis.

**Correction needed:**
- Update ok_alt to journal article landing page, not thesis repository
- Verify title and authors match 2017 journal article, not 2007 thesis

---

## VERIFIED CORRECT (No changes needed)

### 6. neo4j2024graphrag
- Title confirmed: "The Definitive Guide to Graph Databases for the RDBMS Developer"
- Publisher: Neo4j, Inc.
- Year: CSV says 2024, website copyright 2026 (likely website year, not book year)
- **Action:** Assume 2024 correct unless evidence otherwise

---

## FAILED TO FETCH (Direct PDF URLs)

### 7. poveda2014oops
- URL: www.semantic-web-journal.net/system/files/swj989.pdf
- Error: "Invalid URL" (direct PDF link)
- **Action needed:** Find journal article landing page URL

### 8. kenyatta1938facing
- URL: sahistory.org.za/.../jomo_kenyatta_facing_mount_kenya...pdf
- Error: "Invalid URL" (direct PDF link)
- **Action needed:** Verify 1938 year from alternative source

### 9. noy2001ontology
- URL: https://protege.stanford.edu/publications/ontology_development/ontology101.pdf
- Error: "Invalid URL" (direct PDF link)
- Authors: "Noy, N. F. & McGuinness, D. L.", Year: 2001
- **Action needed:** Verify from Stanford KSL technical reports or citations

### 10. almeida2019challenges
- URL: https://chnt.at/wp-content/uploads/Bordoni_2014.pdf
- Error: "Invalid URL" (direct PDF link)
- **NOTE:** URL filename says "Bordoni_2014" but CSV says "Almeida...2019" - 5-year discrepancy
- **Action needed:** Verify actual authors/year, likely 2014 Bordoni not 2019 Almeida

### 11. suarez2012ontology
- URL: https://link.springer.com/chapter/10.1007/978-3-642-24794-1_1
- Error: Paywall/cookie consent, no metadata accessible
- **Action needed:** Use DOI https://doi.org/10.1007/978-3-642-24794-1 to verify

---

## SUMMARY STATISTICS

**Total Phase 5 (Categories A+B+C):**
- Total entries verified: 23
- Errors found in Phase 5A (HIGH): 3
- Errors found in Phase 5B (MEDIUM): 3
- Errors found in Phase 5C (LOW): 5
- **Total corrections needed: 11 entries**

**Error types discovered:**
- Wrong year: 9 entries (ranging from 1-22 years off)
- Wrong first author: 5 entries
- Wrong paper entirely: 3 entries
- Wrong source type: 2 entries

**Verification success rate:**
- Successfully fetched: 17/23 (74%)
- Failed (PDF direct links): 6/23 (26%)

---

## NEXT STEPS

1. **Immediate corrections (5 entries):**
   - liu2022llamaindex → Update authors to IBM writers
   - christie2019indigenous → Determine correct source (Wilson 2001 or Tuhiwai Smith 1999 or delete)
   - fernandez2019ontology → fernandez1997methontology
   - ma2023hybrid → Verify if arXiv paper or Medium blog intended
   - keegan2017maori → Find correct journal article URL

2. **Retry failed PDFs (5 entries):**
   - Find alternative URLs for poveda2014, kenyatta1938, noy2001, almeida2019, suarez2012
   - Use DOIs, landing pages, or bibliographic databases

3. **Update CSV and BibTeX files**

4. **Commit Phase 5C corrections**

5. **Proceed to Phase 4** (special cases)
