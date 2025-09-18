# Scripts Directory

This directory contains automation scripts, data processing tools, and comprehensive ontology construction utilities for the thiLLMo OG-RAG project.

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
Prepares expert evaluation materials for creating AI translation quality benchmarks.

**Purpose**: Generate expert evaluation spreadsheets for creating gold standard AI translation benchmarks  
**Input**: `data/proverbs/extracted_proverbs.csv`  
**Output**: Expert evaluation materials in `data/processed/`

**Key Features**:
- Filters authentic proverbs from extractions (372 → 96 proverbs)
- Generates multi-sheet Excel evaluation benchmark spreadsheet
- Creates detailed expert instructions for AI evaluation standard creation
- Produces evaluation benchmark preparation reports

**Usage**:
```bash
python scripts/prepare_expert_review.py
```

**Generated Files**:
- `expert_evaluation_benchmark.xlsx` - Main evaluation benchmark spreadsheet
- `expert_validation_instructions.md` - AI evaluation benchmark creation guidelines  
- `validation_preparation_report.md` - Process summary

## 🏗️ Comprehensive Ontology Construction System

### `ontology_builder.py`
Sophisticated ontology construction framework for creating culturally-aware knowledge graphs from expert validation data.

**Purpose**: Transform expert validation data into rich Neo4j knowledge graphs for OG-RAG systems  
**Features**: 434 lines of advanced cultural semantic analysis and relationship modeling

**Core Capabilities**:
- **Cultural Concept Extraction**: Advanced Kikuyu semantic pattern recognition
- **Business Domain Mapping**: Modern business application relevance assessment
- **Relationship Modeling**: Multi-layered semantic connections and cultural authenticity preservation
- **Quality Assurance**: Expert validation integration and cultural authenticity scoring

**Usage**:
```bash
# Basic ontology construction
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --neo4j-uri bolt://localhost:7687 \
    --username neo4j \
    --password kikuyu_proverbs_2024

# Advanced construction with comprehensive analysis
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --cultural-analysis-depth advanced \
    --business-mapping comprehensive \
    --relationship-strength-threshold 0.6 \
    --min-expert-score 3.0
```

**Advanced Options**:
- `--cultural-analysis-depth`: `basic|intermediate|advanced` (default: intermediate)
- `--business-mapping`: `minimal|standard|comprehensive` (default: standard)
- `--relationship-strength-threshold`: Minimum relationship strength (0.0-1.0)
- `--min-expert-score`: Minimum expert validation score (1.0-5.0)
- `--cultural-authenticity-threshold`: Minimum cultural authenticity score

**Output**:
- Rich Neo4j knowledge graph with 6 node types and 6 relationship types
- Cultural concept network with semantic relationships
- Business application mapping with relevance scoring
- Expert validation integration and quality metrics

### `ontology_querier.py`
Advanced query interface for OG-RAG retrieval with cultural context awareness.

**Purpose**: Sophisticated querying system for culturally-grounded retrieval augmented generation  
**Features**: 600+ lines of advanced query strategies and cultural context integration

**Query Types**:

**Cultural Similarity Search**:
```bash
python scripts/ontology_querier.py \
    --query-type cultural_similarity \
    --input "Mwanake mutari gitonga ni kirume" \
    --limit 5 \
    --cultural-weight 0.8
```

**Business Application Search**:
```bash
python scripts/ontology_querier.py \
    --query-type business_application \
    --domain leadership \
    --context modern_workplace \
    --limit 10 \
    --min-relevance 0.7
```

**Advanced Semantic Search**:
```bash
python scripts/ontology_querier.py \
    --query-type semantic_search \
    --concepts "work_ethics,responsibility,community" \
    --cultural-weight 0.8 \
    --business-weight 0.6 \
    --relationship-depth 2
```

**Expert Validation Search**:
```bash
python scripts/ontology_querier.py \
    --query-type expert_validated \
    --min-expert-score 4.0 \
    --min-cultural-authenticity 4.0 \
    --domains "leadership,entrepreneurship"
```

**Contextual Retrieval for OG-RAG**:
```bash
python scripts/ontology_querier.py \
    --query-type contextual_subgraph \
    --input-proverb "Gutiri utuku utakira" \
    --context-radius 2 \
    --include-business-applications \
    --include-cultural-contexts
```

**Advanced Features**:
- Multi-modal semantic similarity algorithms
- Cultural context-aware retrieval strategies
- Business application ranking and filtering
- Expert validation score integration
- Relationship strength-based traversal
- Subgraph extraction for OG-RAG context

### `ontology_validator.py`
Comprehensive validation and quality assurance framework for ontology construction.

**Purpose**: Extensive validation suite ensuring ontology quality for OG-RAG deployment  
**Features**: Complete quality assessment across structural, semantic, and cultural dimensions

**Validation Suite**:
```bash
# Complete validation with detailed reporting
python scripts/ontology_validator.py \
    --save-results \
    --output-dir reports/validation

# Performance and quality assessment
python scripts/ontology_validator.py \
    --uri bolt://localhost:7687 \
    --username neo4j \
    --password kikuyu_proverbs_2024 \
    --database neo4j
```

**Validation Dimensions**:
- **Structural Validation**: Node counts, relationship integrity, constraint validation
- **Data Quality**: Completeness analysis, consistency checks, field validation
- **Semantic Consistency**: Relationship validation, concept clustering, network analysis
- **Cultural Authenticity**: Expert validation analysis, cultural coverage assessment
- **Performance Metrics**: Query performance, index utilization, OG-RAG optimization
- **Coverage Analysis**: Concept coverage, business application mapping, domain distribution

**Quality Scoring**:
- Individual dimension scores (0.0-1.0)
- Overall quality grade (A+ to F)
- Criteria assessment against predefined thresholds
- Detailed recommendations for improvement

**Output Reports**:
- `ontology_validation_comprehensive_YYYYMMDD_HHMMSS.json` - Complete validation results
- `ontology_validation_summary_YYYYMMDD_HHMMSS.json` - Executive summary
- Console logging with quality scores and recommendations

## Expert Session Management System

### `create_expert_tracking_template.py`
Generates comprehensive Excel tracking template for expert session management.

**Purpose**: Create structured tracking system for expert recruitment and progress  
**Output**: Multi-sheet Excel workbook with expert tracking capabilities  
**Location**: `data/processed/expert_review/expert_tracking_template.xlsx`

**Usage**:
```bash
python scripts/create_expert_tracking_template.py
```

**Generated Sheets**:
- Expert_Tracking - Main expert information and recruitment status
- Communication_Log - Complete interaction history with experts
- Review_Progress - Session-by-session progress tracking
- Instructions - Status codes and workflow guidelines
- Summary - Real-time project statistics

### `track_expert_progress.py`
Command-line interface for managing expert review sessions and progress tracking.

**Purpose**: Comprehensive expert session management and progress monitoring  
**Features**:
- Add and manage expert contacts
- Track recruitment status with workflow validation
- Monitor review progress and session details
- Generate status reports and overdue notifications
- Log all communications and interactions

## Command-Line Interface

### Adding New Experts
```bash
# Basic expert addition
python scripts/track_expert_progress.py --action add \
  --name "Dr. Jane Wanjiku" \
  --email "j.wanjiku@uonbi.ac.ke" \
  --expertise "Kikuyu Cultural Studies"

# Add expert with full details
python scripts/track_expert_progress.py --action add \
  --name "Prof. John Kariuki" \
  --email "j.kariuki@university.edu" \
  --expertise "Traditional Business Wisdom" \
  --title "Professor of African Studies" \
  --institution "University of Nairobi" \
  --phone "+254-XXX-XXXXXX"
```

### Updating Expert Status
```bash
# Update status with notes
python scripts/track_expert_progress.py --action update \
  --name "Dr. Jane Wanjiku" \
  --status "Contacted" \
  --notes "Initial recruitment email sent via university portal"

# Valid status transitions
python scripts/track_expert_progress.py --action update \
  --name "Dr. Jane Wanjiku" \
  --status "Interested" \
  --notes "Responded positively, scheduled introductory call"

python scripts/track_expert_progress.py --action update \
  --name "Dr. Jane Wanjiku" \
  --status "Confirmed" \
  --notes "Agreed to participate, materials package sent"

python scripts/track_expert_progress.py --action update \
  --name "Dr. Jane Wanjiku" \
  --status "In Progress" \
  --notes "Started reviewing proverbs, first session completed"

python scripts/track_expert_progress.py --action update \
  --name "Dr. Jane Wanjiku" \
  --status "Completed" \
  --notes "All 96 proverbs reviewed with excellent quality"
```

### Recording Review Progress
```bash
# Record session progress
python scripts/track_expert_progress.py --action progress \
  --name "Dr. Jane Wanjiku" \
  --proverbs 25 \
  --duration "2.5 hours" \
  --notes "Completed cultural meaning section, excellent insights"

# Update progress without session details
python scripts/track_expert_progress.py --action progress \
  --name "Dr. Jane Wanjiku" \
  --proverbs 50

# Record progress with issues encountered
python scripts/track_expert_progress.py --action progress \
  --name "Dr. Jane Wanjiku" \
  --proverbs 75 \
  --duration "3 hours" \
  --notes "Expert requested clarification on business relevance ratings"
```

### Generating Reports and Monitoring
```bash
# Generate comprehensive status report
python scripts/track_expert_progress.py --action report

# Check for overdue experts
python scripts/track_expert_progress.py --action overdue

# Use custom tracking file
python scripts/track_expert_progress.py --action report \
  --tracking-file "data/processed/expert_review/custom_tracking.xlsx"
```

### Command-Line Options

#### Required Parameters
- `--action`: Action to perform (`add`, `update`, `progress`, `report`, `overdue`)

#### Expert Management Options
- `--name`: Expert full name (required for add, update, progress actions)
- `--email`: Expert email address (required for add action)
- `--expertise`: Expert expertise area (required for add action)
- `--title`: Expert professional title (optional for add action)
- `--institution`: Expert institution or community affiliation (optional)
- `--phone`: Expert phone number (optional)

#### Status Update Options
- `--status`: New recruitment status (required for update action)
- `--notes`: Additional notes or comments (optional)

#### Progress Tracking Options
- `--proverbs`: Number of proverbs completed (required for progress action)
- `--duration`: Session duration (e.g., "2.5 hours", "3h 30m") (optional)

#### System Options
- `--tracking-file`: Path to Excel tracking file (default: auto-detected)

**Expert Status Workflow**:
```
Identified → Contacted → Interested → Confirmed → In Progress → Completed
                ↓           ↓           ↓           ↓
            No Response  Declined    Declined    Declined
```

### Complete Workflow Example
```bash
# 1. Add new expert
python scripts/track_expert_progress.py --action add \
  --name "Dr. Mary Muthoni" \
  --email "m.muthoni@ics.ac.ke" \
  --expertise "Cultural Anthropology & Proverb Studies"

# 2. Contact expert
python scripts/track_expert_progress.py --action update \
  --name "Dr. Mary Muthoni" \
  --status "Contacted" \
  --notes "Sent recruitment email using professional template"

# 3. Expert responds positively
python scripts/track_expert_progress.py --action update \
  --name "Dr. Mary Muthoni" \
  --status "Interested" \
  --notes "Responded within 24 hours, very enthusiastic about project"

# 4. Confirm participation
python scripts/track_expert_progress.py --action update \
  --name "Dr. Mary Muthoni" \
  --status "Confirmed" \
  --notes "Signed agreement, sent validation materials package"

# 5. Track review sessions
python scripts/track_expert_progress.py --action progress \
  --name "Dr. Mary Muthoni" \
  --proverbs 30 \
  --duration "3 hours" \
  --notes "First session: excellent cultural insights on traditional themes"

python scripts/track_expert_progress.py --action progress \
  --name "Dr. Mary Muthoni" \
  --proverbs 65 \
  --duration "2.5 hours" \
  --notes "Second session: focused on business relevance assessments"

python scripts/track_expert_progress.py --action progress \
  --name "Dr. Mary Muthoni" \
  --proverbs 96 \
  --duration "2 hours" \
  --notes "Final session: completed all reviews with high quality"

# 6. Mark as completed
python scripts/track_expert_progress.py --action update \
  --name "Dr. Mary Muthoni" \
  --status "Completed" \
  --notes "Excellent work, provided comprehensive cultural validation"

# 7. Generate final report
python scripts/track_expert_progress.py --action report
```

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
