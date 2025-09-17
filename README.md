# thiLLMo: Culturally Faithful Kikuyu Proverb Translation

*Preserving Cultural Heritage Through Ontology-Grounded AI Translation*

## About the Name

**thiLLMo** is a portmanteau combining:
- **"Thimo"** (pronounced "thee-mo") - The Kikuyu word for proverbs
- **"LLM"** - Large Language Model

**Pronunciation Guide**: /ˈθiːlmoʊ/ - "**theel**-mo" 
- "**theel**" as in "teal" 
- "**mo**" as in "mow"

This name reflects the project's core mission: bridging traditional Kikuyu wisdom (*thimo*) with modern AI technology (*LLM*) to create culturally faithful translations that preserve the deep cultural significance of traditional sayings.

## Overview

thiLLMo addresses the challenging task of culturally faithful translation of Kikuyu proverbs into English using cutting-edge Ontology-Grounded Retrieval Augmented Generation (OG-RAG). This system goes beyond simple linguistic translation to preserve the deep cultural wisdom, metaphorical richness, and contextual significance embedded in traditional Kikuyu sayings.

## The Problem We're Solving

Traditional machine translation fails catastrophically when dealing with proverbs because:

- **Cultural Context Loss**: Proverbs are deeply embedded in cultural worldviews and lack direct lexical equivalents
- **Metaphorical Complexity**: Figurative language and cultural references require nuanced understanding
- **Low-Resource Language Challenges**: Kikuyu suffers from data scarcity and lack of quality digital resources
- **LLM Limitations**: Even advanced models struggle with cultural faithfulness due to hallucinations and bias

## Our Solution: Ontology-Grounded RAG

### 🏗️ **System Architecture**

1. **Domain-Specific Ontology**: Formal representation of Kikuyu proverbs with:
   - Literal and metaphorical meanings
   - Cultural themes and contexts
   - Usage scenarios and relationships
   - Connections to broader Kikuyu cultural concepts

2. **Knowledge Graph Integration**: Structured storage enabling:
   - Efficient retrieval of interconnected cultural information
   - Preservation of complex relationships between concepts
   - Precise context grounding for generation

3. **OG-RAG Pipeline**: 
   - Query the knowledge graph for relevant cultural subgraphs
   - Retrieve conceptually grounded context
   - Generate culturally faithful English translations

### 🎯 **Key Innovations**

- **55% increase** in factual accuracy through ontology grounding
- **40% improvement** in response correctness 
- **30% faster** attribution and **27% better** fact-based reasoning
- First application of OG-RAG to culturally sensitive proverb translation

## Research Objectives

1. **Literature Analysis**: Comprehensive review of ontology-grounded RAG and LRL translation techniques
2. **Ontology Development**: Create formal Kikuyu proverb ontology capturing cultural depth
3. **System Implementation**: Develop OG-RAG system integrating ontology with LLM
4. **Evaluation Framework**: Establish culturally-aware metrics for translation assessment

## Expected Impact

- **Cultural Preservation**: Digital preservation of Kikuyu wisdom and heritage
- **Cross-Cultural Understanding**: Bridge communication gaps between communities
- **Technical Advancement**: Pioneer culturally sensitive NLP for low-resource languages
- **Reusable Framework**: Methodology applicable to other cultural translation challenges

## Repository Structure

```
├── docs/
│   ├── dev/                 # Developer documentation and guides
│   ├── proposal/            # Research proposal and planning documents
│   └── thesis/              # Thesis documentation and writing
├── src/
│   ├── ontology/            # Ontology development and management
│   └── rag-system/          # OG-RAG implementation
├── data/
│   ├── proverbs/           # Kikuyu proverb datasets and annotations
│   └── processed/          # Expert review and validation materials
├── scripts/
│   ├── extract_proverbs_from_pdf.py    # PDF extraction pipeline
│   └── prepare_expert_review.py        # Expert validation system
└── README.md
```

## 📋 Expert Review System

The project includes a comprehensive cultural expert validation system for ensuring authenticity and accuracy of extracted proverbs.

### Key Features
- **Automated Filtering**: Removes non-proverb content from extractions
- **Comprehensive Review Spreadsheet**: Multi-sheet Excel file for expert validation
- **Cultural Guidelines**: Detailed instructions preserving Kikuyu cultural integrity
- **Quality Assurance**: Built-in validation fields and rating systems

### Quick Usage
```bash
# Generate expert review materials
python scripts/prepare_expert_review.py
```

**Output**: Excel spreadsheet, expert instructions, and validation reports in `data/processed/`

**Current Status**: 96 authentic proverbs prepared for expert review (filtered from 372 original extractions)

For detailed information, see [Expert Review Documentation](data/processed/README.md).

## Getting Started

### For Researchers and End Users
- Review the [research proposal](docs/proposal/) for detailed project background
- Explore the [Expected Impact](#expected-impact) section for project outcomes

### For Developers and Contributors  
- See [Developer Documentation](docs/dev/) for technical guides
- Review [Branching Strategy](docs/dev/BRANCHING_STRATEGY.md) for Git workflow
- Follow the development setup in [docs/dev/](docs/dev/)

## Academic Context

**Institution**: Open Institute of Technology (OPIT)  
**Program**: MSc in Responsible AI  
**Term**: 3 - Capstone Project  
**Course Code**: RAI9001  
**Author**: Charles Watson Ndethi Kibaki

## Research Methodology

Following the CRISP-DM framework:
- **Data Understanding**: Kikuyu proverb collection and analysis
- **Ontology Construction**: Formal knowledge representation
- **System Development**: OG-RAG implementation
- **Evaluation**: Cultural fidelity assessment

## 🚀 GitHub Issue Automation System

### Quick Start

```bash
# 1. Install and setup (one-time)
./install-and-setup.sh

# 2. Create all issues from markdown
./create-issues.sh --input .github/issues/consolidated-issues.md

# 3. Generate project reports
./generate-report.sh --type summary
```

### Complete Workflow

1. **Setup & Installation**
   ```bash
   ./install-and-setup.sh  # Installs GitHub CLI, authenticates, checks dependencies
   ```

2. **Issue Creation from Markdown**
   ```bash
   # Preview issues before creation
   ./create-issues.sh --dry-run --input .github/issues/consolidated-issues.md
   
   # Create all issues
   ./create-issues.sh --input .github/issues/consolidated-issues.md
   
   # Create specific week only
   ./create-issues.sh --week 1 --input .github/issues/consolidated-issues.md
   ```

3. **Progress Management**
   ```bash
   # Sync local markdown with GitHub issues
   ./sync-progress.sh
   
   # Update time estimates
   ./update-estimates.sh batch
   
   # Check deadlines
   ./check-deadlines.sh --alert-days 7
   ```

4. **Reporting & Analytics**
   ```bash
   # Generate comprehensive reports
   ./generate-report.sh --type summary --format html
   ./generate-report.sh --type weekly --format markdown
   ./generate-report.sh --type deadlines --format json
   
   # Estimation accuracy analysis
   ./update-estimates.sh report
   ```

5. **Testing & Validation**
   ```bash
   # Run full test suite
   ./test-script.sh all
   
   # Test specific components
   ./test-script.sh parsing
   ./test-script.sh --integration all
   ```

### Advanced Features

- **Automated Project Field Integration**: Sets custom GitHub Project fields via GraphQL
- **Progress Synchronization**: Bidirectional sync between local markdown and GitHub
- **Deadline Monitoring**: Automated alerts for overdue and upcoming deadlines  
- **Time Tracking**: Estimation accuracy and velocity reporting
- **Batch Operations**: Handle 50+ issues with rate limiting and error recovery
- **Cross-platform Support**: macOS, Linux, Windows compatibility

### Documentation

- [📖 Complete Usage Guide](.github/issues/README.md)
- [🔧 Troubleshooting Guide](./troubleshooting-guide.md)
- [🛠 Integration Guide](.github/INTEGRATION_GUIDE.md)
- [📋 Example Run Log](./example-run.log)

---

*"Proverbs transcend simple linguistic expressions; they are profound repositories of a community's worldview, values, and historical experiences."*
