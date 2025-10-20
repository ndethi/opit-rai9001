# Day 0 - Corpus Preparation (URGENT - Do This First)
**Date:** October 21, 2025 (TODAY)  
**Duration:** 2-3 hours  
**Critical:** Must complete before Day 1 activities

---

## 🚨 IMMEDIATE PRIORITY: Extract 1000-Proverb Corpus

### Background
We have two separate corpora:
1. **Ireri Collection** (100 proverbs) - ✅ Already extracted and processed
   - Location: `data/evaluation/gold_standard_ireri_deduplicated.csv`
   - Domain: Wealth/Prosperity
   - Status: Ready for Tier 1

2. **Barra G. / Gikandi Collection** (1000 proverbs) - ⏳ PDF not yet extracted
   - Source: "1000 Kikuyu Proverbs" (1939)
   - Domain: Mixed (all aspects of life)
   - Status: PDF available but not uploaded/extracted
   - **NEEDED FOR:** Tier 2 generalization testing

---

## 📋 STEP-BY-STEP EXTRACTION PROCESS

### Step 1: Upload PDF (5 minutes)
1. Locate your "1000 Kikuyu Proverbs" PDF
2. Upload to project:
   ```bash
   # Create sources directory if needed
   mkdir -p /Users/ndethi/dev/opit/opit-rai9001/data/sources
   
   # Upload PDF to this location:
   # /Users/ndethi/dev/opit/opit-rai9001/data/sources/1000_kikuyu_proverbs.pdf
   ```

3. Verify upload:
   ```bash
   ls -lh /Users/ndethi/dev/opit/opit-rai9001/data/sources/1000_kikuyu_proverbs.pdf
   ```

### Step 2: Extract Proverbs from PDF (30-60 minutes)

We have an existing extraction script that worked well for Ireri's PDF. We'll adapt it:

```bash
# Navigate to scripts
cd /Users/ndethi/dev/opit/opit-rai9001/scripts

# Run extraction script
python extract_proverbs_from_pdf.py \
  --input ../data/sources/1000_kikuyu_proverbs.pdf \
  --output ../data/raw/barra_1000_proverbs_raw.csv \
  --format standard
```

**Expected Output:**
- Raw CSV with Kikuyu text + English translations
- Approximately 1000 rows (may have duplicates/formatting issues)

### Step 3: Quick Quality Check (15 minutes)

```bash
# Check extraction results
cd /Users/ndethi/dev/opit/opit-rai9001

# Count extracted proverbs
wc -l data/raw/barra_1000_proverbs_raw.csv

# View first 10 proverbs
head -20 data/raw/barra_1000_proverbs_raw.csv

# Check for any obvious issues
python scripts/validate_proverb_extraction.py \
  --input data/raw/barra_1000_proverbs_raw.csv \
  --report data/raw/barra_extraction_report.txt
```

**Quality Checks:**
- [ ] Kikuyu text present (not just English)
- [ ] English translations present
- [ ] Reasonable proverb count (800-1200 range)
- [ ] No major formatting errors
- [ ] Column structure consistent

### Step 4: Clean and Deduplicate (30 minutes)

```bash
# Run cleaning pipeline
python scripts/cleanup_proverb_corpus.py \
  --input data/raw/barra_1000_proverbs_raw.csv \
  --output data/processed/barra_1000_proverbs_cleaned.csv \
  --remove-duplicates \
  --standardize-format
```

**Cleaning Tasks:**
- Remove exact duplicates
- Standardize column names
- Fix encoding issues
- Remove empty rows
- Validate Kikuyu characters

### Step 5: Thematic Sampling for Tier 2 (30 minutes)

Create the 75-proverb diverse sample we need:

```bash
# Sample diverse proverbs
python scripts/sample_diverse_proverbs.py \
  --input data/processed/barra_1000_proverbs_cleaned.csv \
  --output data/evaluation/tier2_diverse_sample.csv \
  --sample-size 75 \
  --strategy stratified \
  --exclude-theme wealth \
  --themes social,nature,wisdom,family,conflict
```

**Stratified Sampling:**
- Social relationships: 15 proverbs
- Agriculture/Nature: 15 proverbs
- Wisdom/Education: 15 proverbs
- Family/Marriage: 15 proverbs
- Conflict/Resolution: 15 proverbs

**Critical:** Ensure NO overlap with Ireri's 100 wealth proverbs

### Step 6: Verification and Documentation (15 minutes)

```bash
# Generate corpus summary
python scripts/generate_corpus_summary.py \
  --ireri data/evaluation/gold_standard_ireri_deduplicated.csv \
  --barra data/processed/barra_1000_proverbs_cleaned.csv \
  --tier2-sample data/evaluation/tier2_diverse_sample.csv \
  --output docs/data/corpus_summary.md
```

**Verify:**
- [ ] Tier 1 corpus: 100 wealth proverbs ✅
- [ ] Tier 2 corpus: 75 diverse proverbs ✅
- [ ] No overlap between Tier 1 and Tier 2 ✅
- [ ] Thematic distribution documented ✅
- [ ] Quality metrics acceptable ✅

---

## 🎯 SUCCESS CRITERIA

At the end of Day 0, you should have:

✅ PDF uploaded to `data/sources/1000_kikuyu_proverbs.pdf`  
✅ Raw extraction: `data/raw/barra_1000_proverbs_raw.csv` (~1000 proverbs)  
✅ Cleaned corpus: `data/processed/barra_1000_proverbs_cleaned.csv` (800-1000 proverbs)  
✅ Tier 2 sample: `data/evaluation/tier2_diverse_sample.csv` (75 proverbs)  
✅ Quality validation report generated  
✅ No overlap with Tier 1 verified  
✅ Thematic distribution documented  

---

## 🚨 IF EXTRACTION FAILS

### Fallback Plan A: Manual Extraction (2-3 hours)
If automated extraction has issues:
1. Use existing `extracted_proverbs.csv` (373 proverbs) as source
2. Manually verify it's from Barra collection (not Ireri)
3. Filter out wealth-related proverbs
4. Sample 75 diverse proverbs manually
5. Document methodology

### Fallback Plan B: Use Existing Corpus (30 minutes)
If `extracted_proverbs.csv` is already the Barra collection:
1. Verify source and provenance
2. Check for overlap with Ireri's 100
3. Remove any wealth-domain proverbs
4. Sample 75 proverbs for Tier 2
5. Proceed to Day 1

### Fallback Plan C: Reduced Tier 2 (If necessary)
If extraction problematic and time critical:
1. Use smaller Tier 2 sample (40-50 proverbs)
2. Still validates generalization
3. Document limitation
4. Adjust statistical power expectations

---

## 📝 EXTRACTION SCRIPT TEMPLATE

If you need to create a custom extraction script, here's a template:

```python
# scripts/extract_1000_proverbs.py
import pdfplumber
import pandas as pd
import re
from pathlib import Path

def extract_proverbs_from_pdf(pdf_path, output_path):
    """Extract proverbs from Barra G.'s 1000 Kikuyu Proverbs PDF"""
    
    proverbs = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            
            # Pattern to match: Number. Kikuyu text - English translation
            # Adjust pattern based on actual PDF format
            pattern = r'(\d+)\.\s*([^-]+)\s*-\s*(.+?)(?=\d+\.|$)'
            matches = re.finditer(pattern, text, re.MULTILINE)
            
            for match in matches:
                proverb_num = match.group(1)
                kikuyu_text = match.group(2).strip()
                english_translation = match.group(3).strip()
                
                proverbs.append({
                    'proverb_id': f"BARRA_{proverb_num}",
                    'kikuyu_text': kikuyu_text,
                    'english_translation': english_translation,
                    'source': 'Barra G. 1939',
                    'page_number': page_num
                })
    
    # Create DataFrame
    df = pd.DataFrame(proverbs)
    
    # Save to CSV
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Extracted {len(proverbs)} proverbs")
    print(f"Saved to {output_path}")
    
    return df

if __name__ == "__main__":
    pdf_path = "../data/sources/1000_kikuyu_proverbs.pdf"
    output_path = "../data/raw/barra_1000_proverbs_raw.csv"
    
    df = extract_proverbs_from_pdf(pdf_path, output_path)
    
    # Quick statistics
    print("\nQuick Stats:")
    print(f"Total proverbs: {len(df)}")
    print(f"Avg Kikuyu length: {df['kikuyu_text'].str.len().mean():.0f} chars")
    print(f"Avg English length: {df['english_translation'].str.len().mean():.0f} chars")
```

---

## ⏰ TIME ESTIMATE

**If PDF extraction goes smoothly:** 2-3 hours  
**If manual intervention needed:** 3-4 hours  
**If major issues:** 4-6 hours + may need to adjust plan

---

## 🎬 IMMEDIATE ACTION

**Right now, please:**

1. **Locate the PDF file** on your computer
2. **Upload it** to `data/sources/` directory
3. **Tell me:**
   - PDF filename
   - Approximate page count
   - Any visible structure (numbered proverbs? sections? format?)

**Then I'll create/adapt the extraction script specifically for your PDF format.**

---

## 📅 REVISED TIMELINE

**Day 0 (TODAY):** Corpus extraction ← **WE ARE HERE**  
**Day 1 (Oct 22):** Ontology population begins  
**Day 2-3:** OG-RAG implementation  
**Day 4-5:** Tier 1 evaluation  
**Day 6-7:** Tier 2 evaluation  
**Day 8 (Oct 29):** Final analysis + presentation prep  
**Day 9 (Oct 30):** Supervisor meeting ✨

---

**Status:** Waiting for PDF upload to proceed  
**Next Step:** Upload PDF and share format details  
**Priority:** HIGH - Need this completed today to stay on schedule
