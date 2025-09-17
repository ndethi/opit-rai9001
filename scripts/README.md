# Scripts Directory

This directory contains automation scripts, data processing tools, and project utilities for the thiLLMo OG-RAG project.

## Core Data Processing Scripts

### `extract_proverbs_from_pdf.py`
Extracts Kikuyu proverbs from PDF documents for the thiLLMo ontology system.

**Purpose**: Initial proverb extraction from research documents  
**Output**: CSV file with extracted proverb data  
**Location**: `data/proverbs/extracted_proverbs.csv`

**Usage**:
```bash
python scripts/extract_proverbs_from_pdf.py
```

### `prepare_expert_review.py` 
Prepares comprehensive expert validation materials from extracted proverbs.

**Purpose**: Generate expert review spreadsheets and documentation  
**Input**: `data/proverbs/extracted_proverbs.csv`  
**Output**: Expert validation materials in `data/processed/`

**Key Features**:
- Filters authentic proverbs from extractions (372 → 96 proverbs)
- Generates multi-sheet Excel validation spreadsheet
- Creates detailed expert instructions with cultural guidelines
- Produces validation preparation reports

**Usage**:
```bash
python scripts/prepare_expert_review.py
```

**Generated Files**:
- `proverb_expert_validation.xlsx` - Main review spreadsheet
- `expert_validation_instructions.md` - Cultural expert guidelines  
- `validation_preparation_report.md` - Process summary

## Directory Structure

### `/automation/`
Contains scripts for automating various project tasks:

**GitHub Issue Management:**
- `add-issue.sh` - Add new GitHub issues
- `create-issues.sh` - Bulk create GitHub issues
- `create-github-labels.sh` - Create GitHub labels
- `debug-create-issue.sh` - Debug issue creation
- `debug-github-issues.py` - Python script for debugging GitHub issues
- `push-crisp-dm-issues.sh` - Push CRISP-DM related issues

**CRISP-DM Automation:**
- `create-crisp-dm-*.sh` - Various CRISP-DM creation scripts
- `update-crisp-dm-*.sh` - CRISP-DM update scripts

**Week-specific Scripts:**
- `create-week1-*.sh` - Week 1 project automation

**Smart Commit System:**
- `ai-smart-commit.sh` - AI-powered commit message generation
- `smart-commit.sh` - Smart commit functionality

**Utilities:**
- `check-deadlines.sh` - Check project deadlines
- `sync-progress.sh` - Sync project progress
- `update-estimates.sh` - Update time estimates
- `generate-report.sh` - Generate project reports
- `compile_literature_review.sh` - Compile literature review
- `test-script.sh` - General testing script
- `parse-issues.py` - Parse and process issues
- `project-fields.js` - Project field configurations

### `/setup/`
Contains installation and configuration scripts:

- `install-and-setup.sh` - Main installation and setup script
- `setup-smart-commit.sh` - Setup smart commit functionality

## Usage

### Proverb Extraction Script

The `extract_proverbs_from_pdf.py` script extracts Kikuyu proverbs from PDF documents for the thiLLMo ontology system.

#### Basic Usage
```bash
# Extract proverbs using default settings
python scripts/extract_proverbs_from_pdf.py

# Extract with custom PDF file
python scripts/extract_proverbs_from_pdf.py --pdf data/sources/my_proverbs.pdf

# Extract with custom output directory
python scripts/extract_proverbs_from_pdf.py --output-dir data/my_proverbs/

# Extract with different confidence threshold
python scripts/extract_proverbs_from_pdf.py --confidence-threshold 0.5
```

#### Advanced Options
```bash
# Specify extraction method
python scripts/extract_proverbs_from_pdf.py --extraction-method pdfplumber

# Output in different formats
python scripts/extract_proverbs_from_pdf.py --format json
python scripts/extract_proverbs_from_pdf.py --format xlsx

# Skip expert review materials generation
python scripts/extract_proverbs_from_pdf.py --no-expert-review

# Verbose logging and dry run
python scripts/extract_proverbs_from_pdf.py --verbose --dry-run
```

#### Directory Flags
- `--pdf, --input-pdf`: Path to input PDF file (default: `data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf`)
- `--output-dir, --output`: Output directory for extracted proverbs (default: `data/proverbs`)
- `--expert-review-dir, --review-dir`: Directory for expert review materials (default: `data/processed`)

#### Output Files
The script generates:
- **Ontology-ready CSV/JSON/Excel**: Main proverb data for system integration
- **Expert review spreadsheet**: Excel file for cultural validation
- **Review instructions**: Markdown guide for cultural experts
- **Extraction summary**: Text report of extraction results

#### Configuration Options
- `--extraction-method`: Choose PDF processing method (`pdfplumber`, `pymupdf`, `pypdf2`, `auto`)
- `--confidence-threshold`: Minimum confidence for proverb candidates (0.0-1.0)
- `--format`: Output format (`csv`, `json`, `xlsx`)
- `--no-expert-review`: Skip expert review materials
- `--verbose`: Enable detailed logging
- `--dry-run`: Preview extraction without saving files

### Other Scripts

To run any script, use:
```bash
# From the project root
./scripts/automation/[script-name]
./scripts/setup/[script-name]

# Or make them executable first
chmod +x scripts/automation/[script-name]
chmod +x scripts/setup/[script-name]
```

## Note

These scripts were moved from the root directory to keep the project structure clean and organized. All functionality remains the same, only the paths have changed.
