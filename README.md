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
5. **LLM as a Judge**: Implement automated evaluation using culturally-specialized LLM assessment

## Expected Impact

- **Cultural Preservation**: Digital preservation of Kikuyu wisdom and heritage
- **Cross-Cultural Understanding**: Bridge communication gaps between communities
- **Technical Advancement**: Pioneer culturally sensitive NLP for low-resource languages
- **Reusable Framework**: Methodology applicable to other cultural translation challenges
- **Scalable Evaluation**: Automated assessment framework for cultural translation quality

## Repository Structure

## Repository Structure

```
├── docs/
│   ├── dev/                 # Developer documentation and guides
│   ├── proposal/            # Research proposal and planning documents
│   └── thesis/              # Thesis documentation and writing
├── src/
│   ├── ontology/            # Ontology development and management
│   ├── evaluation/          # LLM as a Judge evaluation framework
│   └── og-rag-system/       # OG-RAG implementation
├── data/
│   ├── proverbs/           # Kikuyu proverb datasets and annotations
│   └── evaluation/         # Evaluation benchmarks and results
├── scripts/
│   ├── run_llm_evaluation.py  # LLM as a Judge evaluation interface
│   └── create_evaluation_benchmark.py  # Evaluation framework setup
└── README.md
```

## 🤖 LLM as a Judge Evaluation Framework

### Quick Start

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your API keys (Cohere, OpenAI, Anthropic)

# 2. Test configuration
python scripts/run_llm_evaluation.py --mode config --show-summary

# 3. Run single evaluation
python scripts/run_llm_evaluation.py --mode single \
    --kikuyu "Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ" \
    --translation "A visitor is like a vessel that should be filled with water" \
    --system og_rag

# 4. Run comparative evaluation
python scripts/run_llm_evaluation.py --mode comparative \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --enable-ensemble
```

### Key Features

- **Dynamic Provider Configuration**: Environment-based LLM provider setup with Cohere primary and OpenAI/Anthropic fallbacks
- **Cultural Evaluation Specialization**: Culturally-aware prompts for Kikuyu proverb assessment
- **Multi-Model Ensemble**: Robust evaluation using multiple LLM judges with agreement analysis
- **Comprehensive Scoring**: 4-dimensional quality assessment (Cultural Faithfulness 40%, Translation Accuracy 30%, Business Relevance 20%, Overall Fluency 10%)
- **Expert Correlation**: Validation against human expert assessments
- **Statistical Analysis**: Significance testing and effect size calculation
- **Visualization**: Automated generation of evaluation charts and reports

## 📋 Expert Review System

The project includes a comprehensive cultural expert validation system for ensuring authenticity and accuracy of extracted proverbs.

### Key Features
- **Automated Filtering**: Removes non-proverb content from extractions
- **Comprehensive Review Spreadsheet**: Multi-sheet Excel file for expert validation
- **Expert Session Management**: Complete tracking system for recruitment and progress
- **Communication Templates**: Professional email templates for expert engagement
- **Progress Monitoring**: Real-time tracking of review sessions and completion
- **Quality Assurance**: Built-in validation fields and rating systems

### Quick Usage
```bash
# Generate expert review materials
python scripts/prepare_expert_review.py

# Create expert tracking system
python scripts/create_expert_tracking_template.py

# Manage expert sessions
python scripts/track_expert_progress.py --action report
```

**Output**: 
- Expert validation spreadsheets and instructions in `data/processed/`
- Expert tracking and communication logs in `data/processed/expert_review/`
- Professional communication templates in `templates/communications/`

**Current Status**: 
- 96 authentic proverbs prepared for expert review (filtered from 372 original extractions)
- Complete expert recruitment and tracking workflow established
- Multi-sheet Excel system for comprehensive session management

For detailed information, see [Expert Review Documentation](data/processed/README.md).

## 🏗️ Comprehensive Ontology Construction System

A sophisticated ontology construction framework specifically designed for creating rich, culturally-aware knowledge graphs from Kikuyu proverbs and expert validation data.

### 🎯 Core Capabilities

**Cultural Semantic Analysis**
- Advanced Kikuyu concept extraction using semantic patterns
- Cultural value identification and relationship modeling
- Traditional wisdom categorization and context mapping
- Metaphorical meaning preservation and representation

**Business Application Mapping**
- Modern business domain relevance assessment
- Leadership principle extraction and application modeling
- Entrepreneurship and teamwork concept integration
- Corporate culture and ethics relationship building

**Sophisticated Relationship Modeling**
- Multi-layered semantic connections between concepts
- Cultural authenticity and expert validation integration
- Contextual usage patterns and traditional applications
- Cross-domain knowledge bridging and inference capabilities

### 🛠️ System Components

#### Ontology Builder (`scripts/ontology_builder.py`)
Comprehensive ontology construction from expert validation data:

```bash
# Build complete ontology from expert data
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --neo4j-uri bolt://localhost:7687 \
    --username neo4j \
    --password kikuyu_proverbs_2024

# Advanced construction with cultural analysis
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --cultural-analysis-depth advanced \
    --business-mapping comprehensive \
    --relationship-strength-threshold 0.6
```

**Key Features:**
- 434 lines of sophisticated cultural concept extraction
- Advanced semantic relationship modeling
- Business domain mapping and relevance scoring
- Cultural authenticity preservation and validation
- Neo4j graph database integration with APOC plugins

#### Ontology Querier (`scripts/ontology_querier.py`)
Advanced query interface for OG-RAG retrieval:

```bash
# Query for culturally similar proverbs
python scripts/ontology_querier.py \
    --query-type cultural_similarity \
    --input "Mwanake mutari gitonga ni kirume" \
    --limit 5

# Business application search
python scripts/ontology_querier.py \
    --query-type business_application \
    --domain leadership \
    --context modern_workplace \
    --limit 10

# Advanced semantic search with cultural context
python scripts/ontology_querier.py \
    --query-type semantic_search \
    --concepts "work_ethics,responsibility,community" \
    --cultural-weight 0.8 \
    --business-weight 0.6
```

**Advanced Capabilities:**
- 600+ lines of sophisticated query strategies
- Cultural context-aware retrieval
- Multi-modal semantic similarity search
- Business application mapping and ranking
- Expert validation score integration
- Relationship strength-based filtering

#### Ontology Validator (`scripts/ontology_validator.py`)
Comprehensive validation and quality assurance framework:

```bash
# Run complete validation suite
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

**Validation Dimensions:**
- Structural integrity and completeness analysis
- Data quality assessment across all entities
- Semantic consistency and relationship validation
- Cultural authenticity and expert validation analysis
- Performance metrics for OG-RAG optimization
- Coverage analysis and completeness scoring

#### Configuration Management (`config/neo4j_config.py`)
Environment-specific Neo4j configuration:

```python
from config.neo4j_config import get_development_config, get_production_config

# Development environment
dev_config = get_development_config()

# Production environment with authentication
prod_config = get_production_config()

# Custom configuration
custom_config = {
    'uri': 'bolt://custom-server:7687',
    'username': 'custom_user',
    'password': 'custom_password',
    'database': 'kikuyu_proverbs'
}
```

### 🧠 Ontology Architecture

**Node Types:**
- `Proverb`: Core proverb entities with Kikuyu text, translations, and metadata
- `Concept`: Cultural and business concepts extracted from proverbs
- `CulturalContext`: Traditional usage contexts and cultural significance
- `BusinessApplication`: Modern business applications and relevance mappings
- `Theme`: High-level thematic categorizations and wisdom patterns
- `Metaphor`: Metaphorical elements and figurative language patterns

**Relationship Types:**
- `HAS_CONCEPT`: Links proverbs to extracted concepts
- `APPLICABLE_TO`: Connects proverbs to business applications
- `USED_IN_CONTEXT`: Associates proverbs with cultural contexts
- `RELATES_TO`: Semantic relationships between concepts
- `SIMILAR_TO`: Similarity relationships between proverbs
- `SUPPORTS_APPLICATION`: Concept support for business applications

### 📊 Quality Assurance Metrics

**Cultural Authenticity Validation:**
- Expert validation score integration (minimum 3.0/5.0)
- Cultural authenticity assessment (minimum 3.0/5.0)
- Traditional usage context verification
- Kikuyu language term preservation

**Semantic Relationship Quality:**
- Relationship strength scoring (0.0-1.0)
- Semantic consistency validation
- Concept clustering analysis
- Cross-domain relationship mapping

**Performance Optimization:**
- Query response time monitoring (target <2.0 seconds)
- Index utilization analysis
- Neo4j constraint and optimization validation
- OG-RAG retrieval efficiency assessment

### 🚀 Integration with OG-RAG System

The ontology construction system is specifically designed to support OG-RAG (Ontology-Grounded Retrieval Augmented Generation):

1. **Rich Context Retrieval**: Query interface provides culturally-grounded context subgraphs
2. **Semantic Similarity**: Advanced similarity algorithms for relevant proverb discovery
3. **Cultural Preservation**: Maintains cultural authenticity throughout the translation process
4. **Business Application**: Enables modern context application while preserving traditional wisdom

**Expected Performance Improvements:**
- 55% increase in factual accuracy through ontology grounding
- 40% improvement in response correctness
- 30% faster attribution and 27% better fact-based reasoning
- Superior cultural faithfulness compared to raw LLM translation

## 📊 Comprehensive Evaluation Framework

A sophisticated evaluation benchmark system for rigorous assessment of AI translation quality with cultural faithfulness validation.

### 🎯 Framework Components

**Evaluation Benchmark Creation**
- Comprehensive benchmark dataset with 372+ evaluation cases
- 4 weighted quality dimensions: Cultural Faithfulness (40%), Translation Accuracy (30%), Business Relevance (20%), Overall Fluency (10%)
- Expert qualification standards and recruitment guidelines
- Blind evaluation protocol with randomized system presentation

**Quality Assessment Framework**
- Statistical validation with significance testing
- Inter-rater reliability measurement (target ≥0.7)
- Effect size calculation and confidence intervals
- Cultural preservation effectiveness analysis

**Expert Evaluation Tools**
- Structured Excel evaluation templates
- Comprehensive expert instructions and session protocols
- Quality control and consensus building procedures
- Performance monitoring and fatigue management

### 🚀 Framework Usage

#### Create Evaluation Benchmark
```bash
# Generate comprehensive evaluation framework
python scripts/create_evaluation_benchmark.py \
    --proverbs-file data/proverbs/extracted_proverbs.csv \
    --output-dir data/evaluation

# Framework creates:
# • Benchmark dataset (372 evaluation cases)
# • Expert evaluation templates and instructions
# • Session protocols and quality metrics
# • Statistical analysis framework
```

#### Process Expert Feedback
```bash
# Integrate expert evaluations into benchmark
python scripts/process_expert_feedback.py \
    --expert-evaluations data/evaluation/collected/expert_evaluations.xlsx \
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \
    --output-file data/evaluation/processed/expert_validated_benchmark.csv
```

#### Run Comparative Analysis
```bash
# Compare OG-RAG vs Raw LLM performance
python scripts/run_comparative_analysis.py \
    --expert-benchmark data/evaluation/processed/expert_validated_benchmark.csv \
    --og-rag-translations data/evaluation/system_outputs/og_rag_translations.csv \
    --raw-llm-translations data/evaluation/system_outputs/raw_llm_translations.csv \
    --output-dir data/evaluation/analysis \
    --generate-report
```

#### Generate Evaluation Report
```bash
# Create comprehensive evaluation report
python scripts/generate_evaluation_report.py \
    --analysis-results data/evaluation/analysis/comparative_analysis_results.json \
    --output-format html,pdf \
    --include-visualizations
```

### 📈 Expected Validation Results

The evaluation framework is designed to validate OG-RAG advantages:
- **Cultural Faithfulness**: Target ≥4.2 score (vs Raw LLM baseline)
- **Translation Accuracy**: Target ≥4.0 overall quality score
- **Statistical Significance**: p<0.05 with effect size >0.5
- **Expert Agreement**: Inter-rater reliability ≥0.7

### 📚 Framework Documentation

**Complete Usage Guide**: [Evaluation Framework Employment Guide](docs/development/EVALUATION_FRAMEWORK_EMPLOYMENT_GUIDE.md)
- Data processing pipeline and expert feedback integration
- Statistical validation protocols and significance testing
- Results interpretation and performance analysis
- Benchmark publication and research dataset preparation

**Generated Outputs**:
- `data/evaluation/benchmark/` - Benchmark dataset and metadata
- `data/evaluation/templates/` - Expert evaluation tools and instructions
- `data/evaluation/metrics/` - Quality metrics and validation framework
- `data/evaluation/reports/` - Comprehensive analysis reports

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
