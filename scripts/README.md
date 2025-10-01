# Scripts Directory

This directory contains automation scripts, data processing tools, and comprehensive ontology construction utilities for the thiLLMo OG-RAG project.

## 🌟 Margaret Ireri Gold Standard Pipeline (NEW)

### Complete Pipeline for 100 Expert-Curated Proverbs

A comprehensive, production-ready pipeline for extracting and converting Margaret Wambere Ireri's expertly curated collection of 100 Kikuyu proverbs about money and wealth into evaluation-ready gold standard datasets.

#### `ireri_gold_standard_pipeline.py` 
**Master orchestration script** - Complete end-to-end pipeline from PDF to gold standard

**Features**:
- Automated PDF extraction with quality validation
- Gold standard format conversion
- Metadata generation and documentation
- Comprehensive quality checks and reporting
- Integration-ready output for evaluation frameworks

**Usage**:
```bash
# Run complete pipeline
python3 scripts/ireri_gold_standard_pipeline.py

# Force re-extraction from PDF
python3 scripts/ireri_gold_standard_pipeline.py --force

# Custom PDF path
python3 scripts/ireri_gold_standard_pipeline.py --pdf path/to/pdf
```

**Output Files**:
- `data/raw/ireri_100_wealth_prosperity_proverbs.csv` - Raw extraction (197 entries)
- `data/evaluation/gold_standard_ireri_100.csv` - Gold standard format (197 entries)
- `data/evaluation/gold_standard_ireri_100_metadata.json` - Dataset metadata
- `data/evaluation/ireri_gold_standard_report.md` - Comprehensive report

#### `extract_ireri_100_proverbs.py`
**PDF extraction module** - Specialized extractor for Ireri's numbered proverb collection

**Purpose**: Extract structured proverb data from Margaret Ireri's PDF with high fidelity  
**Method**: Pattern-based extraction using numbered proverb markers (1-100)

**Features**:
- Extracts Kikuyu text, English/Kiswahili translations
- Captures cultural interpretations and teaching messages
- Preserves biblical parallels and source references
- Tracks page numbers and proverb categories
- Validates extraction completeness

**Usage**:
```bash
python3 scripts/extract_ireri_100_proverbs.py \
    --pdf data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf \
    --output data/raw/ireri_100_wealth_prosperity_proverbs.csv
```

**Extraction Summary**:
- Total entries: 197 (includes variations)
- Kikuyu texts: 100% coverage
- English translations: 97% coverage
- Cultural interpretations: ~50% coverage
- Biblical parallels: ~50% coverage

#### `convert_ireri_to_gold_standard.py`
**Gold standard converter** - Transforms raw extractions into evaluation-ready format

**Purpose**: Convert Ireri's proverbs to standardized format for AI translation evaluation  
**Output**: Evaluation-ready dataset with expert translations as baseline

**Features**:
- Standardized field mapping for evaluation frameworks
- Thematic categorization (8 themes: wealth acquisition, business wisdom, etc.)
- Cultural authenticity scoring (5.0/5.0 - expert validated)
- Business relevance context extraction
- Comprehensive metadata generation

**Usage**:
```bash
python3 scripts/convert_ireri_to_gold_standard.py \
    --input data/raw/ireri_100_wealth_prosperity_proverbs.csv \
    --output data/evaluation/gold_standard_ireri_100.csv \
    --metadata data/evaluation/gold_standard_ireri_100_metadata.json
```

**Gold Standard Fields**:
- `proverb_id`: Unique identifier (MP_001 to MP_100)
- `kikuyu_text`: Original Kikuyu proverb
- `expert_translation`: Ireri's English translation (baseline)
- `expert_cultural_meaning`: Cultural interpretation
- `expert_business_relevance`: Wealth/prosperity context
- `thematic_category`: Automated theme classification
- `cultural_authenticity`: Expert validation score (5.0)
- Plus: teaching, biblical context, source references

**Thematic Distribution**:
- Wealth acquisition: 109 entries
- Business wisdom: 34 entries
- Poverty & hardship: 28 entries
- Wealth management: 15 entries
- Other themes: 11 entries

#### Quick Start Example

```python
import pandas as pd

# Load gold standard
gold = pd.read_csv('data/evaluation/gold_standard_ireri_100.csv')

# Use for translation evaluation
for _, proverb in gold.iterrows():
    kikuyu = proverb['kikuyu_text']
    expert_translation = proverb['expert_translation']
    cultural_context = proverb['expert_cultural_meaning']
    
    # Your translation system
    og_rag_translation = your_og_rag_system(kikuyu, cultural_context)
    raw_llm_translation = your_raw_llm(kikuyu)
    
    # Evaluate against expert baseline
    og_rag_score = evaluate(og_rag_translation, expert_translation)
    raw_llm_score = evaluate(raw_llm_translation, expert_translation)
    
    print(f"OG-RAG: {og_rag_score:.2f} | Raw LLM: {raw_llm_score:.2f}")
```

---

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

## 📊 Comprehensive Evaluation Framework

### `create_evaluation_benchmark.py`
Sophisticated evaluation benchmark framework for rigorous AI translation quality assessment.

**Purpose**: Create comprehensive evaluation infrastructure before expert feedback collection  
**Features**: Complete evaluation methodology with quality metrics and expert tools

**Framework Creation**:
```bash
# Generate complete evaluation framework
python scripts/create_evaluation_benchmark.py \
    --proverbs-file data/proverbs/extracted_proverbs.csv \
    --output-dir data/evaluation
```

**Generated Components**:
- **Benchmark Dataset**: 372 evaluation cases with comprehensive field structure
- **Expert Evaluation Templates**: Excel templates with structured scoring sheets
- **Quality Metrics Framework**: Statistical validation and comparative analysis methods
- **Expert Instructions**: Detailed evaluation guidelines and session protocols
- **Validation Framework**: Inter-rater reliability and quality control procedures

**Key Features**:
- 4 weighted quality dimensions (Cultural Faithfulness: 40%, Translation Accuracy: 30%, Business Relevance: 20%, Overall Fluency: 10%)
- Blind evaluation protocol with randomized system presentation
- Expert qualification standards and recruitment guidelines
- Statistical validation framework with significance testing

**Output Structure**:
```
data/evaluation/
├── benchmark/
│   ├── translation_evaluation_benchmark.csv
│   └── benchmark_metadata.json
├── templates/
│   ├── expert_evaluation_template.xlsx
│   ├── expert_evaluation_instructions.md
│   └── evaluation_session_protocol.md
├── metrics/
│   └── evaluation_metrics_framework.json
└── reports/
    └── benchmark_creation_report_YYYYMMDD_HHMMSS.md
```

### Evaluation Framework Employment Scripts

**Expert Feedback Processing**:
```bash
# Process expert evaluations into benchmark
python scripts/process_expert_feedback.py \
    --expert-evaluations data/evaluation/collected/expert_evaluations.xlsx \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --output-file data/evaluation/processed/expert_validated_benchmark.csv
```

**System Translation Generation**:
```bash
# Generate OG-RAG translations
python scripts/generate_og_rag_translations.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --ontology-uri bolt://localhost:7687 \
    --output-file data/evaluation/system_outputs/og_rag_translations.csv

# Generate Raw LLM translations
python scripts/generate_raw_llm_translations.py \
    --benchmark-file data/evaluation/processed/expert_validated_benchmark.csv \
    --model-name gpt-4 \
    --output-file data/evaluation/system_outputs/raw_llm_translations.csv
```

**Comparative Analysis**:
```bash
# Run comprehensive comparative analysis
python scripts/run_comparative_analysis.py \
    --expert-benchmark data/evaluation/processed/expert_validated_benchmark.csv \
    --og-rag-translations data/evaluation/system_outputs/og_rag_translations.csv \
    --raw-llm-translations data/evaluation/system_outputs/raw_llm_translations.csv \
    --output-dir data/evaluation/analysis \
    --generate-report
```

**Evaluation Reporting**:
```bash
# Generate comprehensive evaluation report
python scripts/generate_evaluation_report.py \
    --analysis-results data/evaluation/analysis/comparative_analysis_results.json \
    --output-format html,pdf \
    --include-visualizations \
    --output-file data/evaluation/reports/thiLLMo_evaluation_report.html
```

**Complete Evaluation Workflow**:
```bash
# Run complete evaluation pipeline
./scripts/complete_evaluation_workflow.sh
```

### Evaluation Quality Targets

**Cultural Faithfulness Validation**:
- Target cultural faithfulness score: ≥4.2
- OG-RAG vs Raw LLM cultural advantage: >0.5 points
- Cultural preservation rate: >80% of cases ≥4.0 score

**Statistical Validation**:
- Inter-rater reliability: ≥0.7 (substantial agreement)
- Statistical significance: p<0.05 with effect size >0.5
- Sample size adequacy: Power analysis ≥0.8

**Expected Performance Improvements**:
- 55% increase in factual accuracy through ontology grounding
- 40% improvement in response correctness
- Superior cultural preservation compared to raw LLM translation

## Expert Session Management System
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

## 🔄 Translation Comparison System

### `enhanced_translation_comparison.py`
Comprehensive translation comparison system integrating OG-RAG and Raw LLM translations with LLM as a Judge evaluation.

**Purpose**: End-to-end translation quality comparison combining ontology-grounded and baseline approaches  
**Features**: Integrated LLM judge evaluation, cultural context analysis, statistical validation

**Core Capabilities**:
- **OG-RAG Translation Generation**: Context-aware translations using cultural ontology
- **Raw LLM Baseline**: Direct LLM translations without cultural enhancement
- **LLM Judge Integration**: Automated quality assessment using cultural evaluation framework
- **Comparative Analysis**: Statistical comparison with expert correlation
- **Cultural Context Preparation**: Specialized metadata for LLM judge evaluation

**System Architecture**:
```python
# Initialize comparison system with LLM Judge integration
comparison_system = EnhancedTranslationComparisonSystem(config_file=".env")

# Run complete comparison pipeline
summary = await comparison_system.run_complete_comparison_pipeline(
    benchmark_file="data/evaluation/benchmark/translation_evaluation_benchmark.csv"
)
```

**Usage Examples**:

**Complete Pipeline Execution**:
```bash
# Run full comparison with LLM judge evaluation
python scripts/enhanced_translation_comparison.py
```

**Individual Component Testing**:
```bash
# Test OG-RAG translation generation only
python scripts/enhanced_translation_comparison.py --mode og-rag-only

# Test Raw LLM translation generation only  
python scripts/enhanced_translation_comparison.py --mode raw-llm-only

# Run comparison without LLM judge evaluation
python scripts/enhanced_translation_comparison.py --skip-llm-judge
```

**Configuration Options**:
- Dynamic LLM provider selection via environment variables
- Cultural context depth configuration
- Business relevance analysis level
- Evaluation priority calculation
- Output format customization

**Generated Outputs**:
```
data/evaluation/translations/
├── enhanced_og_rag_translations.csv          # OG-RAG results with metadata
├── raw_llm_translations.csv                  # Baseline LLM translations
├── comprehensive_translation_comparison.csv   # Combined comparison dataset
├── llm_judge_evaluation_results.json         # LLM judge assessment
└── pipeline_summary_YYYYMMDD_HHMMSS.json    # Execution summary
```

**Key Features**:
- **Cultural Metadata**: Rich cultural context for LLM judge evaluation
- **Business Relevance**: Entrepreneurship application analysis
- **Priority Scoring**: Intelligent evaluation prioritization
- **Multi-Provider Support**: Cohere, OpenAI, Anthropic integration
- **Async Processing**: Efficient batch translation generation
- **Quality Tracking**: Confidence scoring and metadata collection

### `run_translation_comparison_demo.py`
Interactive demonstration of the translation comparison system with sample Kikuyu proverbs.

**Purpose**: Quick demonstration and testing of the complete translation comparison pipeline  
**Features**: Sample data generation, full pipeline execution, comprehensive reporting

**Demo Components**:
- **Sample Data Creation**: 10 authentic Kikuyu proverbs with expert translations
- **Pipeline Demonstration**: Complete workflow execution
- **Results Visualization**: Summary reporting and analysis
- **Configuration Testing**: Environment setup validation

**Usage**:
```bash
# Run interactive demo
python scripts/run_translation_comparison_demo.py

# Verbose output for debugging
python scripts/run_translation_comparison_demo.py --verbose
```

**Sample Proverbs Include**:
- Cultural wisdom: "Mũndũ akua na ũkĩa" (A person dies from overeating)
- Business applications: "Mũgũnda ũtarĩmwo ndũciaraga" (An untilled field bears nothing)
- Community values: "Mũndũ akĩrĩra ndagĩaga na marĩa" (When eating, one is not alone with food)

**Demo Output**:
```
🎯 ENHANCED TRANSLATION COMPARISON DEMO RESULTS
📊 Total proverbs processed: 10
🔄 OG-RAG translations: 10
🤖 Raw LLM translations: 10
📋 Comparison pairs created: 10
🎯 High priority evaluations: 3
🤖 LLM Judge Evaluation: ✅ Completed
```

**Next Steps Guidance**:
- API key configuration instructions
- Dataset scaling recommendations
- Neo4j ontology integration steps
- Production deployment guidelines

## 📊 Cultural Translation Evaluation Metrics

### `src/evaluation/cultural_metrics.py`
Comprehensive cultural translation evaluation metrics specifically designed for Kikuyu proverb translation quality assessment.

**Purpose**: Academic-quality evaluation metrics integrating cultural authenticity, linguistic fidelity, and business relevance  
**Features**: Kikuyu-specific cultural pattern analysis, automated quality scoring, expert correlation

**Core Capabilities**:
- **Cultural Authenticity Assessment**: Semantic similarity, cultural context preservation, Kikuyu-specific concept analysis
- **Translation Fidelity Metrics**: ROUGE scores, semantic similarity, structural analysis, word overlap
- **Business Relevance Evaluation**: Entrepreneurship application assessment, modern context integration
- **Expert Alignment Scoring**: Correlation with expert evaluations, weighted quality assessment
- **Kikuyu Cultural Patterns**: Specialized pattern recognition for traditional concepts and values

**Metric Categories**:

**Cultural Authenticity (40% weight)**:
```python
# Cultural concept preservation analysis
cultural_metrics = CulturalTranslationMetrics()
authenticity_score = cultural_metrics.calculate_cultural_authenticity_score(
    translation="Hard work leads to success",
    expert_translation="Diligent effort brings prosperity", 
    cultural_context="Traditional Kikuyu work ethic values",
    og_rag_context="Community-based achievement principles"
)
```

**Translation Fidelity (35% weight)**:
- ROUGE-1, ROUGE-2, ROUGE-L scores for lexical overlap
- Semantic similarity using sentence transformers
- Length ratio analysis and structural similarity
- Word overlap and token-level comparison

**Business Relevance (15% weight)**:
- Entrepreneurship concept matching
- Modern business application scoring
- Resource management principle assessment
- Collaborative business approach evaluation

**Expert Alignment (10% weight)**:
- Correlation with expert cultural faithfulness scores
- Translation accuracy alignment
- Business relevance consistency
- Overall fluency correlation

**Configuration Options**:
```python
config = CulturalMetricsConfig(
    cultural_weight=0.45,              # Emphasize cultural authenticity
    fidelity_weight=0.30,              # Translation accuracy
    business_weight=0.15,              # Business relevance  
    expert_weight=0.10,                # Expert alignment
    min_cultural_threshold=0.65,       # Quality thresholds
    enable_kikuyu_specific=True        # Kikuyu pattern analysis
)
```

**Kikuyu Cultural Pattern Analysis**:
- **Community Values**: Ubuntu, togetherness, cooperation, harambee
- **Traditional Wisdom**: Elder teachings, ancestral knowledge, customs
- **Agricultural Metaphors**: Harvest, cultivation, seasonal wisdom
- **Animal Symbolism**: Traditional animal representations and meanings
- **Social Hierarchy**: Respect, authority, age-based wisdom structures
- **Moral Values**: Honesty, perseverance, humility, generosity

**Usage Examples**:

**Single Translation Evaluation**:
```python
metrics = CulturalTranslationMetrics()
quality_scores = metrics.calculate_overall_quality_score(
    translation="Unity brings strength to the community",
    expert_translation="Together we achieve communal strength",
    cultural_context="Kikuyu harambee principle of collective effort",
    business_application="Teamwork drives business success"
)
```

**Batch Evaluation**:
```python
# Evaluate dataset of translations
results = metrics.evaluate_translation_batch(
    translations_df=comparison_dataset,
    save_results=True,
    output_dir="data/evaluation/cultural_metrics"
)
```

**Output Metrics**:
- Individual quality scores (0.0-1.0 scale)
- Quality grades (A+ to F classification)
- Detailed metric breakdowns
- Improvement recommendations
- Cultural concept analysis
- Statistical summaries

### `scripts/run_integrated_cultural_evaluation.py`
Complete integration pipeline combining translation comparison with cultural metrics evaluation.

**Purpose**: End-to-end cultural evaluation integrating OG-RAG comparison with automated metrics  
**Features**: Full pipeline automation, statistical analysis, comprehensive reporting

**Pipeline Components**:
1. **Translation Generation**: OG-RAG vs Raw LLM comparison
2. **Cultural Metrics Application**: Automated quality assessment
3. **Statistical Analysis**: System performance comparison
4. **Integration Analysis**: LLM judge correlation with cultural metrics
5. **Comprehensive Reporting**: Executive summaries and detailed results

**Usage**:
```bash
# Run complete integrated evaluation
python scripts/run_integrated_cultural_evaluation.py

# With custom benchmark
python scripts/run_integrated_cultural_evaluation.py --benchmark-file data/custom_proverbs.csv
```

**Generated Analysis**:
- **System Performance**: OG-RAG vs Raw LLM statistical comparison
- **Cultural Preservation**: Distribution analysis and preservation rates
- **Business Relevance**: Entrepreneurship application effectiveness
- **Quality Distribution**: Grade distribution and excellence rates
- **Comparative Advantage**: Quantified improvements and effect sizes
- **Recommendations**: System-specific improvement guidance

**Output Structure**:
```
data/evaluation/integrated_analysis/
├── integrated_cultural_analysis_YYYYMMDD_HHMMSS.json
├── executive_summary_YYYYMMDD_HHMMSS.json
└── cultural_metrics/
    ├── cultural_evaluation_results_YYYYMMDD_HHMMSS.json
    └── cultural_evaluation_summary_YYYYMMDD_HHMMSS.csv
```

**Key Features**:
- **Multi-System Evaluation**: Simultaneous assessment of multiple translation approaches
- **Cultural Specialization**: Kikuyu-specific pattern recognition and analysis
- **Academic Rigor**: Comprehensive statistical validation and significance testing
- **Business Integration**: Entrepreneurship application assessment
- **Expert Correlation**: Alignment with expert evaluation standards
- **Automated Reporting**: Executive summaries and detailed technical analysis

## 🤖 LLM as a Judge Evaluation Framework

### `run_llm_evaluation.py`
Comprehensive LLM-based evaluation system for Kikuyu proverb translation quality assessment.

**Purpose**: Automated evaluation of translation quality using culturally-specialized LLM judges  
**Features**: Multi-provider support, ensemble evaluation, statistical analysis, expert correlation

**Core Capabilities**:
- **Dynamic Provider Configuration**: Environment-based LLM setup (Cohere, OpenAI, Anthropic)
- **Cultural Evaluation Specialization**: Prompts designed for Kikuyu cultural context
- **Multi-Model Ensemble**: Robust assessment using multiple LLM judges
- **Comprehensive Scoring**: 4-dimensional quality assessment
- **Statistical Validation**: Significance testing and correlation analysis

**Configuration Setup**:
```bash
# Configure LLM providers in .env file
cp .env.example .env
# Edit with your API keys: COHERE_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY
```

**Usage Examples**:
```bash
# Test configuration
python scripts/run_llm_evaluation.py --mode config --show-summary

# Single translation evaluation
python scripts/run_llm_evaluation.py --mode single \
    --kikuyu "Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ" \
    --translation "A visitor is like a vessel that should be filled with water" \
    --system og_rag

# Comparative evaluation (OG-RAG vs Raw LLM)
python scripts/run_llm_evaluation.py --mode comparative \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --sample-size 50 --enable-ensemble

# Full pipeline evaluation
python scripts/run_llm_evaluation.py --mode pipeline \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --output-dir outputs/evaluation/full_run
```

**Evaluation Modes**:
- `config`: Test and display LLM configuration
- `single`: Evaluate a single translation
- `comparative`: Compare OG-RAG vs Raw LLM systems
- `pipeline`: Full evaluation pipeline with analysis

**Key Features**:
- **Cultural Faithfulness Assessment** (40% weight): Traditional wisdom preservation
- **Translation Accuracy Evaluation** (30% weight): Linguistic correctness
- **Business Relevance Analysis** (20% weight): Modern professional applicability
- **Overall Fluency Assessment** (10% weight): Natural English expression
- **Ensemble Evaluation**: Multi-model consensus for robust assessment
- **Expert Correlation**: Validation against human expert assessments

**Output**:
- Detailed evaluation scores and feedback
- Statistical analysis with significance testing
- Visualization charts and reports
- CSV/JSON exports for further analysis

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
