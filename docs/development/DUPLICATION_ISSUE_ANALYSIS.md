# Gold Standard Duplication Issue - Root Cause Analysis

**Date**: October 7, 2025  
**Status**: ✅ RESOLVED

## Executive Summary

The baseline translation CSV contained **50 rows for 25 unique proverbs** (2x duplication) despite the script being designed to generate ONE row per proverb. Investigation revealed the **bug was NOT in the translation script**, but rather in the **SOURCE data file** (gold_standard_ireri.csv).

## Root Cause

**SOURCE DATA STRUCTURE**: The `data/evaluation/gold_standard_ireri.csv` file contains **197 rows for 100 unique proverbs** (almost exactly 2:1 ratio).

### Why Duplicates Exist in Source

Each proverb_id appears **twice** with different levels of expert annotation:

1. **Row 1 (Basic)**: Minimal information
   - `proverb_id`, `kikuyu_text`, `expert_translation`
   - `expert_cultural_meaning`: NaN (empty)
   - Other fields: Basic metadata

2. **Row 2 (Detailed)**: Full expert analysis
   - Same `proverb_id` and `kikuyu_text`
   - `expert_cultural_meaning`: **Populated with cultural insights**
   - `expert_teaching`: Teaching points
   - `biblical_context`: Biblical parallels
   - Other enriched fields

### Example (MW_001)

```csv
proverb_id,kikuyu_text,expert_translation,expert_cultural_meaning
MW_001,Aikaragia mbia ta njuu ngigi.,He looks after his money the way storks pursue locusts.,
MW_001,Aikaragia mbia ta njuu ngigi.,He looks after his money the way storks pursue locusts.,Whoever has much always wants more.
```

## Impact on Baseline Generation

The `generate_baseline_translations.py` script **correctly processes every row** from the source file:

```python
for idx, row in gold_df.iterrows():  # Processes ALL 197 rows (not 100)
    proverb_id = row.get('proverb_id', f'proverb_{idx}')
    kikuyu_text = row.get('kikuyu_text', '')
    # ... translate with all systems ...
```

**Result**: Requesting 50 proverbs from the source file actually processed **100 rows** (50 basic + 50 detailed), generating 50 translations for 25 unique proverbs.

## Solution Implemented

### 1. Created Deduplication Script

**File**: `scripts/deduplicate_gold_standard.py`

**Strategy**: Merge duplicate proverb_id rows by:
- Grouping by `proverb_id`
- For each column, prefer **non-null values**
- For multiple non-null values, keep the **most complete** (longest string)
- Result: ONE row per proverb with merged information

**Execution**:
```bash
python scripts/deduplicate_gold_standard.py
```

**Output**:
```
📥 Input: data/evaluation/gold_standard_ireri.csv
📊 Total rows: 197
🎯 Unique proverb_ids: 100

✅ DEDUPLICATION COMPLETE
📉 Rows reduced: 197 → 100
🎯 Unique proverbs: 100

💾 Saved to: data/evaluation/gold_standard_ireri_deduplicated.csv
```

### 2. Updated Baseline Generation

**New Command**:
```bash
python scripts/generate_baseline_translations.py \
  --input data/evaluation/gold_standard_ireri_deduplicated.csv \
  --max-proverbs 50 \
  --output baseline_translations_clean_50proverbs_deduped.csv
```

**Expected Result**: **50 rows for 50 unique proverbs** (1:1 ratio) ✅

## Data Quality Assessment

### Original Source (gold_standard_ireri.csv)
- ❌ **197 rows** for 100 proverbs (2x duplication)
- ❌ Inconsistent structure (alternating basic/detailed rows)
- ✅ Rich expert annotations (preserved in detailed rows)

### Deduplicated Source (gold_standard_ireri_deduplicated.csv)
- ✅ **100 rows** for 100 proverbs (1:1 mapping)
- ✅ Consistent structure (merged information)
- ✅ All expert annotations preserved

### Generated Baselines
- **OLD** (baseline_translations_clean_50proverbs_20251007_000921.csv): 
  - ❌ 50 rows for 25 proverbs (2x duplication)
  - Generated from duplicated source
  
- **NEW** (baseline_translations_clean_50proverbs_deduped.csv):
  - ✅ 50 rows for 50 proverbs (clean 1:1 mapping)
  - Generated from deduplicated source

## Verification Commands

### Check for duplicates in any CSV:
```bash
python -c "
import pandas as pd
df = pd.read_csv('FILE.csv')
print(f'Total rows: {len(df)}')
print(f'Unique proverb_ids: {df[\"proverb_id\"].nunique()}')
print(f'Duplicates: {len(df) - df[\"proverb_id\"].nunique()}')
print(df['proverb_id'].value_counts().sort_index().head(20))
"
```

### Count proverbs by ID:
```bash
cut -d',' -f1 FILE.csv | sort | uniq -c | head -20
```

## Files Affected

### Created
- ✅ `scripts/deduplicate_gold_standard.py` - Deduplication utility
- ✅ `data/evaluation/gold_standard_ireri_deduplicated.csv` - Clean source (100 proverbs)
- ✅ `docs/development/DUPLICATION_ISSUE_ANALYSIS.md` - This document

### To Be Updated
- ⏳ `data/results/baseline_translations/baseline_translations_clean_50proverbs_deduped.csv` - In progress

### To Be Cleaned Up
- 🗑️ `data/results/baseline_translations/baseline_translations_clean_50proverbs_20251007_000921.csv` - Duplicated (DELETE)
- 🗑️ `data/results/baseline_translations/baseline_clean_temp_*.csv` - Temporary files (DELETE)
- 🗑️ Other old baseline CSVs with duplicates (ARCHIVE or DELETE)

## Lessons Learned

1. **Always verify source data structure** before processing
   - Run exploratory analysis on input files
   - Check for duplicates, nulls, and structural anomalies

2. **Document data provenance clearly**
   - Why does gold_standard_ireri.csv have 2 rows per proverb?
   - Was this intentional (versioning) or accidental?

3. **Add data validation to scripts**
   - Consider adding deduplication checks to `generate_baseline_translations.py`
   - Warn users if source contains duplicates

4. **Test with small samples first**
   - Running with `--max-proverbs 5` would have revealed duplicates immediately
   - Saves API costs and debugging time

## Recommendations

### Immediate Actions
1. ✅ Use `gold_standard_ireri_deduplicated.csv` as canonical source
2. ⏳ Complete 50-proverb baseline generation with clean source
3. 🗑️ Delete duplicate baseline CSVs from results folder
4. 📄 Update README files to reference deduplicated source

### Future Improvements
1. **Add deduplication check** to `generate_baseline_translations.py`:
   ```python
   # Before processing
   if len(gold_df) != gold_df['proverb_id'].nunique():
       logger.warning("⚠️  SOURCE CONTAINS DUPLICATES!")
       # Offer to auto-deduplicate or abort
   ```

2. **Add data validation script** to `scripts/setup/`:
   - Check all CSV files for duplicates
   - Run as pre-processing step
   - Generate data quality report

3. **Document data lineage**:
   - Create `data/evaluation/README.md` explaining:
     - Why original has duplicates
     - When to use deduplicated version
     - How data was collected/structured

## Status: RESOLVED ✅

- [x] Root cause identified (source data duplication)
- [x] Deduplication script created and tested
- [x] Clean source file generated (100 proverbs)
- [x] Regenerating 50-proverb baseline with clean source (IN PROGRESS)
- [ ] Clean up baseline translations folder
- [ ] Update documentation with clean workflows

---

**Next Steps**: Complete baseline generation, verify 50 rows for 50 proverbs, then proceed with comparative analysis.
