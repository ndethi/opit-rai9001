# Scripts Directory

This directory contains organized automation and setup scripts for the OG-RAG project.

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

## Python Scripts

### thiLLMo System Scripts

**`thiLLMo_setup.py`** - Complete thiLLMo System Orchestration
- Comprehensive setup and deployment script for the thiLLMo OG-RAG system
- Features:
  - Environment validation and configuration
  - Neo4j database connection testing
  - Cultural ontology creation and validation
  - Kikuyu proverb data loading with cultural sensitivity
  - System verification and health checks
- Usage: `python scripts/thiLLMo_setup.py`
- Dependencies: Requires `.env` file configuration and Docker services running

**`test_thiLLMo_system.py`** - System Verification and Testing
- Comprehensive testing suite for thiLLMo system validation
- Features:
  - Cultural data integrity testing
  - Search functionality validation
  - Sample query execution and response verification
  - Performance benchmarking
  - Cultural sensitivity compliance checking
- Usage: `python scripts/test_thiLLMo_system.py`
- Dependencies: Requires completed thiLLMo setup via `thiLLMo_setup.py`

**`extract_proverbs_from_pdf.py`** - PDF Proverb Extraction Pipeline
- Extracts Kikuyu proverbs from PDF documents for thiLLMo OG-RAG integration
- Features:
  - Multi-method PDF text extraction with Unicode preservation
  - Kikuyu-specific linguistic pattern recognition
  - Wealth/entrepreneurship domain classification
  - Cultural authenticity assessment and morphological analysis
  - Expert review material preparation
  - Direct integration with thiLLMo ontology system
- Usage: `python scripts/extract_proverbs_from_pdf.py`
- Dependencies: PyPDF2, pdfplumber, PyMuPDF, pandas, openpyxl
- Install dependencies: `./scripts/install_thiLLMo_pdf_tools.sh`

**`test_thiLLMo_og_rag.py`** - Comprehensive OG-RAG System Testing
- Advanced testing suite for thiLLMo OG-RAG system validation
- Features:
  - Kikuyu proverb full-text search testing
  - Cultural ontology retrieval validation
  - Hypergraph traversal for wealth/entrepreneurship domain
  - Translation pattern verification
  - Cultural sensitivity compliance checking
  - Performance benchmarking with detailed reporting
- Usage: `python scripts/test_thiLLMo_og_rag.py`
- Dependencies: neo4j, python-decouple, JSON logging

### Complete thiLLMo Workflow

```bash
# 1. Extract proverbs from PDF sources (if needed)
python scripts/extract_proverbs_from_pdf.py

# 2. Ensure Docker services are running
docker-compose up -d

# 3. Run complete system setup
python scripts/thiLLMo_setup.py

# 4. Verify system functionality
python scripts/test_thiLLMo_system.py

# 5. Run comprehensive OG-RAG testing
python scripts/test_thiLLMo_og_rag.py
```

### Quick Start for thiLLMo

```bash
# 1. Ensure Docker services are running
docker-compose up -d

# 2. Run complete system setup
python scripts/thiLLMo_setup.py

# 3. Verify system functionality
python scripts/test_thiLLMo_system.py
```

### Data Preparation Scripts

**PDF Processing Pipeline:**
```bash
# Install PDF processing dependencies
./scripts/install_thiLLMo_pdf_tools.sh

# Extract proverbs from PDF documents
python scripts/extract_proverbs_from_pdf.py

# Review extracted proverbs (expert validation required)
# Check: data/processed/expert_review/
```

### Legacy Scripts (Root Directory Scripts)

The following scripts are also available in the project root and automation folder:

**GitHub Issue Management:**
- `add-issue.sh` - Add new GitHub issues
- `create-issues.sh` - Bulk create GitHub issues  
- `create-github-labels.sh` - Create GitHub labels
- `debug-github-issues.py` - Python script for debugging GitHub issues
- `parse-issues.py` - Parse and process issues

**Project Automation:**
- `ai-smart-commit.sh` - AI-powered commit message generation
- `check-deadlines.sh` - Check project deadlines
- `sync-progress.sh` - Sync project progress
- `generate-report.sh` - Generate project reports
- `compile_literature_review.sh` - Compile literature review

**CRISP-DM Workflow:**
- `create-crisp-dm-*.sh` - Various CRISP-DM creation scripts
- `update-crisp-dm-*.sh` - CRISP-DM update scripts

### Dependencies and Installation

**Core thiLLMo Dependencies:**
```bash
# Python packages (install via pip)
pip install neo4j pandas python-decouple

# PDF processing (for extract_proverbs_from_pdf.py)
pip install PyPDF2 pdfplumber PyMuPDF openpyxl

# Or use the automated installer
./scripts/install_thiLLMo_pdf_tools.sh
```

**Docker Services:**
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

## Usage

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
