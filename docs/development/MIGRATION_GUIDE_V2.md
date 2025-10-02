# Migration Guide: v1.0 → v2.0 Framework Refactoring

**Date**: October 2, 2025  
**Type**: Major refactoring - Generic framework  
**Impact**: Breaking changes for direct script usage

---

## Executive Summary

The expert proverb gold standard pipeline has been refactored from an Ireri-specific implementation (v1.0) to a generic, configuration-driven framework (v2.0) that supports multiple expert sources and low-resource languages.

### What Changed

| Aspect | v1.0 (Ireri-specific) | v2.0 (Generic Framework) |
|--------|----------------------|--------------------------|
| **Scripts** | `extract_ireri_100_proverbs.py` | `extract_expert_proverbs.py` |
| | `convert_ireri_to_gold_standard.py` | `convert_to_gold_standard.py` |
| | `ireri_gold_standard_pipeline.py` | `gold_standard_pipeline.py` |
| **Classes** | `IreriProverb`, `IreriProverbExtractor` | `ExpertProverb`, `ExpertProverbExtractor` |
| | `IreriGoldStandardConverter` | `GoldStandardConverter` |
| **Usage** | Hardcoded paths and settings | `--source parameter` + configuration |
| **Adding Sources** | Duplicate & modify code | Edit YAML config only |

---

## Why Refactor?

**Problem**: Original implementation was hardcoded for Margaret Ireri's collection:
- Class names: `IreriProverb`, `IreriProverbExtractor`, `IreriGoldStandardConverter`
- File names: `extract_ireri_100_proverbs.py`, `convert_ireri_to_gold_standard.py`
- Hardcoded paths: `ireri_100_wealth_prosperity_proverbs.csv`

**Solution**: Generic framework for any expert source:
- Configuration-driven metadata (YAML)
- Source parameter: `--source ireri` (or any configured source)
- Zero code changes to add new expert collections

**Benefits**:
- ✅ Scalable to N expert sources
- ✅ Consistent with research proposal ("dynamic framework for multiple LRLs")
- ✅ No code duplication
- ✅ Easy to maintain
- ✅ Professional quality for thesis

---

## Migration Steps

### For End Users (Running Scripts)

**Old Way**:
```bash
# Run Ireri pipeline
python3 scripts/ireri_gold_standard_pipeline.py

# Extract only
python3 scripts/extract_ireri_100_proverbs.py \
    --pdf data/sources/ireri.pdf \
    --output data/raw/ireri_100_wealth_prosperity_proverbs.csv

# Convert only
python3 scripts/convert_ireri_to_gold_standard.py \
    --input data/raw/ireri_100_wealth_prosperity_proverbs.csv \
    --output data/evaluation/gold_standard_ireri.csv
```

**New Way**:
```bash
# Run any source pipeline
python3 scripts/gold_standard_pipeline.py --source ireri

# Extract only
python3 scripts/extract_expert_proverbs.py --source ireri

# Convert only
python3 scripts/convert_to_gold_standard.py --source ireri

# Paths are auto-generated from configuration!
```

### For Developers (Importing Classes)

**Old Way**:
```python
from extract_ireri_100_proverbs import IreriProverb, IreriProverbExtractor
from convert_ireri_to_gold_standard import IreriGoldStandardConverter

# Use classes
extractor = IreriProverbExtractor(pdf_path)
converter = IreriGoldStandardConverter()
```

**New Way**:
```python
from extract_expert_proverbs import ExpertProverb, ExpertProverbExtractor
from convert_to_gold_standard import GoldStandardConverter

# Use classes with source parameter
extractor = ExpertProverbExtractor(pdf_path, source_name='ireri')
converter = GoldStandardConverter(source_name='ireri')
```

### For Adding New Sources

**Old Way** (required code changes):
1. Duplicate `extract_ireri_100_proverbs.py` → `extract_new_expert_proverbs.py`
2. Find/replace all "ireri"/"Ireri" references
3. Modify class names, file paths, etc.
4. Repeat for converter and pipeline
5. Test everything

**New Way** (configuration only):
1. Edit `scripts/config/expert_sources.yaml`:
```yaml
sources:
  new_expert:
    author: "Dr. Expert Name"
    year: 2025
    title: "Collection Title"
    language: "swahili"
    language_code: "sw"
    # ... more config ...
```

2. Run pipeline:
```bash
python3 scripts/gold_standard_pipeline.py --source new_expert --pdf path/to/pdf
```

3. Done! ✅

---

## File Path Changes

### Script Names

| Old | New | Status |
|-----|-----|--------|
| `extract_ireri_100_proverbs.py` | `extract_expert_proverbs.py` | ✅ Refactored |
| `convert_ireri_to_gold_standard.py` | `convert_to_gold_standard.py` | ✅ Refactored |
| `ireri_gold_standard_pipeline.py` | `gold_standard_pipeline.py` | ✅ Refactored |
| (old scripts) | `scripts/DEPRECATED/` | 📦 Preserved |

### Output Files

| v1.0 | v2.0 | Notes |
|------|------|-------|
| `ireri_100_wealth_prosperity_proverbs.csv` | `ireri_expert_proverbs.csv` | Simpler naming |
| `gold_standard_ireri_100.csv` | `gold_standard_ireri.csv` | **Removed redundant "_100"** (v1.0 files deleted as of Oct 2025) |
| `gold_standard_ireri_100_metadata.json` | `gold_standard_ireri_metadata.json` | **Consistent naming** (v1.0 files deleted as of Oct 2025) |
| `ireri_gold_standard_report.md` | `ireri_gold_standard_report.md` | Unchanged |

**Note**: v2.0 files are now the canonical version. Old v1.0 files (`*_ireri_100.*`) have been removed for cleaner structure.

---

## API Changes

### Class Renames

| Old Class | New Class | Module |
|-----------|-----------|--------|
| `IreriProverb` | `ExpertProverb` | `extract_expert_proverbs` |
| `IreriProverbExtractor` | `ExpertProverbExtractor` | `extract_expert_proverbs` |
| `IreriGoldStandardConverter` | `GoldStandardConverter` | `convert_to_gold_standard` |
| `IreriGoldStandardPipeline` | `GoldStandardPipeline` | `gold_standard_pipeline` |

### Method Signature Changes

**Extractor**:
```python
# Old
extractor = IreriProverbExtractor(pdf_path)

# New
extractor = ExpertProverbExtractor(pdf_path, source_name='ireri')
```

**Converter**:
```python
# Old
converter = IreriGoldStandardConverter()
gold_df = converter.prepare_ireri_gold_standard(
    ireri_csv_path=input_path,
    output_path=output_path
)

# New
converter = GoldStandardConverter(source_name='ireri')
gold_df = converter.prepare_gold_standard(
    source_csv_path=input_path,
    output_path=output_path  # Auto-generated if None
)
```

**Pipeline**:
```python
# Old (DEPRECATED - files removed)
pipeline = IreriGoldStandardPipeline(
    pdf_path=pdf,
    raw_output='data/raw/ireri_100_wealth_prosperity_proverbs.csv',
    gold_standard_output='data/evaluation/gold_standard_ireri.csv'  # Updated path
)

# New (CURRENT)
pipeline = GoldStandardPipeline(
    pdf_path=pdf,
    source_name='ireri',
    # Paths auto-generated from config
)
```

---

## Configuration System

### New File: `scripts/config/expert_sources.yaml`

Central configuration for all expert sources:

```yaml
sources:
  ireri:
    author: "Margaret Wambere Ireri"
    year: 2014
    title: "A Collection of 100 Proverbs..."
    language: "kikuyu"
    language_code: "ki"
    domain: "wealth_prosperity"
    total_proverbs: 100
    
    extraction:
      pattern_type: "numbered"
      start_page: 7
      end_page: 150
    
    quality:
      min_proverbs: 90
      max_empty_texts: 10
      expected_authenticity: 5.0
    
    output:
      raw_csv: "ireri_expert_proverbs.csv"
      gold_standard_csv: "gold_standard_ireri.csv"
      metadata_json: "gold_standard_ireri_metadata.json"
      report_md: "ireri_gold_standard_report.md"
```

### Configuration API

```python
from config import (
    get_source_config,
    get_output_path,
    list_available_sources
)

# List sources
sources = list_available_sources()  # ['ireri', ...]

# Get configuration
config = get_source_config('ireri')
print(config['author'])  # "Margaret Wambere Ireri"

# Get output paths
raw_path = get_output_path('ireri', 'raw_csv')
gold_path = get_output_path('ireri', 'gold_standard_csv')
```

---

## Testing & Validation

### Test Results (Ireri Source)

✅ **Pipeline Execution**: 13.6s total
- Stage 1 (Extract): 13.6s → 197 proverbs
- Stage 2 (Validate): Passed all checks
- Stage 3 (Convert): 0.1s → 197 entries
- Stage 4 (Quality): 100% Kikuyu, 97% English, 5.0/5.0 authenticity
- Stage 5 (Report): Generated

✅ **Output Comparison**:
- Old: `gold_standard_ireri_100.csv` (197 entries, MP_001 - MP_100) - **DELETED Oct 2025**
- Current: `gold_standard_ireri.csv` (197 entries, MW_001 - MW_100)
- Same data quality, updated IDs (Margaret Wambere initials)

✅ **File Management**:
- Old v1.0 scripts preserved in `scripts/DEPRECATED/`
- Old v1.0 data files (`*_ireri_100.*`) have been **removed** for cleaner structure
- Use v2.0 files (`gold_standard_ireri.csv`) as the canonical gold standard

---

## Breaking Changes

### ❌ Direct Imports

```python
# This will fail
from extract_ireri_100_proverbs import IreriProverbExtractor
```

**Fix**: Update imports
```python
from extract_expert_proverbs import ExpertProverbExtractor
```

### ❌ Hardcoded File Paths

```python
# This path is deprecated
df = pd.read_csv('data/raw/ireri_100_wealth_prosperity_proverbs.csv')
```

**Fix**: Use new paths or configuration
```python
from config import get_output_path
path = get_output_path('ireri', 'raw_csv')
df = pd.read_csv(path)

# Or use new naming directly
df = pd.read_csv('data/raw/ireri_expert_proverbs.csv')
```

### ❌ CLI Commands Without --source

```bash
# Old scripts removed from main directory
python3 scripts/ireri_gold_standard_pipeline.py
```

**Fix**: Use new scripts with --source
```bash
python3 scripts/gold_standard_pipeline.py --source ireri

# Or access deprecated version
python3 scripts/DEPRECATED/ireri_gold_standard_pipeline.py
```

---

## Rollback Plan

If you need to temporarily revert:

1. **Use deprecated scripts**:
```bash
python3 scripts/DEPRECATED/ireri_gold_standard_pipeline.py
```

2. **Git revert**:
```bash
git checkout v1.0-ireri-specific
```

3. **Cherry-pick**:
```bash
git log --oneline  # Find commit before refactor
git checkout <commit-hash>
```

**Note**: Deprecated scripts will be removed after 6 months (April 2026) if no issues found.

---

## Support & Documentation

- **Full Analysis**: `docs/development/REFACTORING_IMPACT_ANALYSIS.md`
- **New README**: `scripts/README.md` (updated with generic framework docs)
- **Configuration**: `scripts/config/expert_sources.yaml` (template included)
- **Deprecated Scripts**: `scripts/DEPRECATED/README.md`
- **Examples**: See updated `scripts/README.md` for usage examples

---

## FAQ

**Q: Will my existing gold standard files still work?**  
A: **UPDATE (Oct 2025)**: Old v1.0 files (`gold_standard_ireri_100.csv`, etc.) have been **removed**. Only v2.0 files (`gold_standard_ireri.csv`) remain. Use the comparison report at `data/evaluation/gold_standard_comparison_report.json` to see what changed.

**Q: Do I need to re-extract my data?**  
A: No. The v2.0 gold standard files contain all the same proverbs as v1.0, just with cleaner formatting and updated IDs.

**Q: Can I still use the old scripts?**  
A: Yes, temporarily. They're in `scripts/DEPRECATED/`. But they now output to v2.0 paths. Please migrate to v2.0 pipeline - old scripts will be removed in 6 months.

**Q: What if I have custom code importing old classes?**  
A: Update your imports per the "For Developers" section above. Most changes are simple renames + adding `source_name` parameter.

**Q: How do I add a new expert source?**  
A: Just edit `scripts/config/expert_sources.yaml` - no code changes needed! See "Adding New Sources" section.

**Q: Does this affect my evaluation pipeline?**  
A: No. Gold standard CSV format is unchanged. Your evaluation code will work as-is.

---

**Migration completed**: October 2, 2025  
**Framework version**: 2.0  
**Tested with**: Ireri's Kikuyu proverbs (197 entries, 5.0/5.0 authenticity)  
**Status**: ✅ Production ready

For questions or issues, see `docs/development/REFACTORING_IMPACT_ANALYSIS.md` or contact project maintainers.
