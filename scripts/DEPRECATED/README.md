# Deprecated Scripts

This folder contains legacy scripts that have been superseded by the refactored generic framework (v2.0).

## Deprecated Files (2025-10-02)

### From v1.0 (Ireri-specific implementation):

1. **`extract_ireri_100_proverbs.py`** → Replaced by `extract_expert_proverbs.py`
   - Old: Hardcoded for Margaret Ireri's collection
   - New: Generic framework supporting multiple expert sources via configuration

2. **`convert_ireri_to_gold_standard.py`** → Replaced by `convert_to_gold_standard.py`
   - Old: Ireri-specific class names and methods
   - New: Generic converter with source_name parameter

3. **`ireri_gold_standard_pipeline.py`** → Replaced by `gold_standard_pipeline.py`
   - Old: Hardcoded imports and file paths for Ireri
   - New: Configuration-driven pipeline for any expert source

## Migration Notes

**Do NOT use these scripts for new work!**

Use the new generic framework scripts in `scripts/`:
- `extract_expert_proverbs.py` - Extract proverbs from any expert PDF
- `convert_to_gold_standard.py` - Convert to standardized format
- `gold_standard_pipeline.py` - Complete orchestrated pipeline

### Key Changes in v2.0:
- **Configuration-driven**: All source metadata in `scripts/config/expert_sources.yaml`
- **Generic naming**: `ExpertProverb`, `ExpertProverbExtractor`, `GoldStandardConverter`
- **Source parameter**: `--source ireri` (or any configured source)
- **Auto-generated paths**: File paths derived from configuration
- **Multi-LRL ready**: Easy to add new languages and expert sources

### Example Migration:

**Old way (v1.0):**
```bash
python3 scripts/ireri_gold_standard_pipeline.py
```

**New way (v2.0):**
```bash
python3 scripts/gold_standard_pipeline.py --source ireri
```

### For New Expert Sources:

1. Add source configuration to `scripts/config/expert_sources.yaml`
2. Run pipeline with `--source new_source_name`
3. No code changes required!

## Preservation Rationale

These files are preserved for:
- Historical reference
- Comparison with refactored version
- Recovery if needed during transition period

**Planned removal**: After 6 months (April 2026) if no issues found

---

*See `docs/development/REFACTORING_IMPACT_ANALYSIS.md` for detailed refactoring documentation*
