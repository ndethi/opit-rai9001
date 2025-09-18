# Comprehensive Ontology Construction Guide for thiLLMo OG-RAG

This guide provides detailed instructions for building, querying, and validating the Kikuyu proverbs ontology using the comprehensive construction system.

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Installation and Setup](#installation-and-setup)
5. [Ontology Construction](#ontology-construction)
6. [Advanced Querying](#advanced-querying)
7. [Quality Validation](#quality-validation)
8. [OG-RAG Integration](#og-rag-integration)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)

## Overview

The thiLLMo ontology construction system transforms expert-validated Kikuyu proverb data into a sophisticated knowledge graph optimized for Ontology-Grounded Retrieval Augmented Generation (OG-RAG). The system preserves cultural authenticity while enabling modern business applications through advanced semantic modeling.

### Key Components

- **Ontology Builder**: Transforms expert validation data into rich Neo4j knowledge graphs
- **Ontology Querier**: Advanced query interface for culturally-aware retrieval
- **Ontology Validator**: Comprehensive quality assurance and validation framework
- **Configuration Manager**: Environment-specific Neo4j configuration management

## System Architecture

### Knowledge Graph Structure

```
                    ┌─────────────────┐
                    │    Proverb      │
                    │   (Core Node)   │
                    └─────────┬───────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼───────┐ ┌───▼───┐ ┌───────▼────────┐
        │   Concept     │ │Theme  │ │BusinessApplicat│
        │  (Cultural/   │ │       │ │ion             │
        │  Business)    │ │       │ │                │
        └───────────────┘ └───────┘ └────────────────┘
                │                           │
        ┌───────▼───────┐           ┌───────▼────────┐
        │CulturalContext│           │   Metaphor     │
        │               │           │                │
        └───────────────┘           └────────────────┘
```

### Relationship Types

- `HAS_CONCEPT`: Links proverbs to extracted cultural/business concepts
- `APPLICABLE_TO`: Connects proverbs to modern business applications
- `USED_IN_CONTEXT`: Associates proverbs with traditional cultural contexts
- `RELATES_TO`: Semantic relationships between concepts
- `SIMILAR_TO`: Cultural/semantic similarity between proverbs
- `SUPPORTS_APPLICATION`: Concept support for business applications

## Prerequisites

### Software Requirements

- **Python 3.8+**: Core development environment
- **Neo4j 4.4+**: Graph database with APOC plugins
- **Dependencies**: pandas, neo4j-driver, python-dotenv

### Data Requirements

- Expert validation CSV with required fields:
  - `kikuyu_text`: Original Kikuyu proverb
  - `english_translation`: Expert-validated English translation
  - `cultural_meaning`: Cultural significance and context
  - `expert_validation_score`: Expert quality rating (1-5)
  - `cultural_authenticity_score`: Cultural authenticity rating (1-5)
  - `business_relevance_score`: Modern business relevance (0-1)

## Installation and Setup

### 1. Neo4j Database Setup

```bash
# Using Neo4j Desktop or Docker
# Neo4j Docker setup
docker run \
    --name neo4j-kikuyu \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/kikuyu_proverbs_2024 \
    -e NEO4J_PLUGINS='["apoc"]' \
    neo4j:latest

# Access Neo4j Browser at http://localhost:7474
```

### 2. Python Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas neo4j python-dotenv

# Or install from requirements.txt
pip install -r requirements.txt
```

### 3. Configuration Setup

Create `.env` file in project root:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=kikuyu_proverbs_2024
NEO4J_DATABASE=neo4j

# Validation Thresholds
MIN_EXPERT_SCORE=3.0
MIN_CULTURAL_AUTHENTICITY=3.0
MIN_BUSINESS_RELEVANCE=0.5
```

## Ontology Construction

### Basic Construction

```bash
# Basic ontology building from expert validation data
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --neo4j-uri bolt://localhost:7687 \
    --username neo4j \
    --password kikuyu_proverbs_2024
```

### Advanced Construction Options

```bash
# Comprehensive ontology with advanced cultural analysis
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --neo4j-uri bolt://localhost:7687 \
    --username neo4j \
    --password kikuyu_proverbs_2024 \
    --cultural-analysis-depth advanced \
    --business-mapping comprehensive \
    --relationship-strength-threshold 0.6 \
    --min-expert-score 3.0 \
    --min-cultural-authenticity 3.0 \
    --create-indexes \
    --create-constraints
```

### Construction Parameters

**Cultural Analysis Depth**:
- `basic`: Essential cultural concepts only
- `intermediate`: Cultural + traditional context analysis
- `advanced`: Complete cultural semantic analysis with metaphor extraction

**Business Mapping Levels**:
- `minimal`: Basic business relevance scoring
- `standard`: Business domain mapping with applications
- `comprehensive`: Complete business ecosystem integration

**Quality Thresholds**:
- `relationship-strength-threshold`: Minimum semantic relationship strength (0.0-1.0)
- `min-expert-score`: Minimum expert validation score (1.0-5.0)
- `min-cultural-authenticity`: Minimum cultural authenticity score (1.0-5.0)

### Construction Process

1. **Data Validation**: Validates input CSV format and required fields
2. **Cultural Concept Extraction**: Advanced semantic pattern recognition
3. **Business Domain Mapping**: Modern application relevance assessment
4. **Relationship Modeling**: Multi-layered semantic connection building
5. **Quality Integration**: Expert validation and authenticity scoring
6. **Neo4j Optimization**: Index and constraint creation for performance

## Advanced Querying

### Cultural Similarity Search

Find proverbs with similar cultural concepts and meanings:

```bash
python scripts/ontology_querier.py \
    --query-type cultural_similarity \
    --input "Mwanake mutari gitonga ni kirume" \
    --limit 5 \
    --cultural-weight 0.8 \
    --min-similarity 0.6
```

### Business Application Search

Discover proverbs relevant to specific business domains:

```bash
python scripts/ontology_querier.py \
    --query-type business_application \
    --domain leadership \
    --context modern_workplace \
    --limit 10 \
    --min-relevance 0.7 \
    --include-cultural-context
```

### Semantic Concept Search

Search by specific cultural or business concepts:

```bash
python scripts/ontology_querier.py \
    --query-type semantic_search \
    --concepts "work_ethics,responsibility,community" \
    --cultural-weight 0.8 \
    --business-weight 0.6 \
    --relationship-depth 2 \
    --min-expert-score 3.5
```

### Expert Validation Search

Find high-quality, expert-validated proverbs:

```bash
python scripts/ontology_querier.py \
    --query-type expert_validated \
    --min-expert-score 4.0 \
    --min-cultural-authenticity 4.0 \
    --domains "leadership,entrepreneurship,teamwork" \
    --sort-by validation_score \
    --limit 20
```

### Contextual Subgraph Retrieval (OG-RAG)

Extract rich context subgraphs for RAG applications:

```bash
python scripts/ontology_querier.py \
    --query-type contextual_subgraph \
    --input-proverb "Gutiri utuku utakira" \
    --context-radius 2 \
    --include-business-applications \
    --include-cultural-contexts \
    --include-related-concepts \
    --max-relationships 50
```

### Query Output Formats

**JSON Output** (default):
```json
{
  "query_info": {
    "query_type": "cultural_similarity",
    "input": "Mwanake mutari gitonga ni kirume",
    "parameters": {...}
  },
  "results": [
    {
      "proverb": {
        "id": "PROV_0042",
        "kikuyu_text": "...",
        "english_translation": "...",
        "similarity_score": 0.87
      },
      "cultural_context": {...},
      "business_applications": [...]
    }
  ]
}
```

**Detailed Context** (for OG-RAG):
```json
{
  "context_subgraph": {
    "central_proverb": {...},
    "related_concepts": [...],
    "cultural_contexts": [...],
    "business_applications": [...],
    "semantic_relationships": [...]
  },
  "retrieval_metadata": {
    "context_radius": 2,
    "total_relationships": 23,
    "cultural_authenticity_avg": 4.2
  }
}
```

## Quality Validation

### Comprehensive Validation Suite

```bash
# Run complete validation with detailed reporting
python scripts/ontology_validator.py \
    --save-results \
    --output-dir reports/validation \
    --uri bolt://localhost:7687 \
    --username neo4j \
    --password kikuyu_proverbs_2024
```

### Validation Dimensions

**1. Structural Validation**
- Node and relationship counts
- Constraint and index validation
- Database integrity checks

**2. Data Quality Assessment**
- Field completeness analysis
- Data consistency validation
- Missing data identification

**3. Semantic Consistency**
- Relationship integrity validation
- Concept clustering analysis
- Semantic network health assessment

**4. Cultural Authenticity**
- Expert validation score analysis
- Cultural coverage assessment
- Traditional usage validation

**5. Performance Metrics**
- Query response time analysis
- Index utilization assessment
- OG-RAG optimization validation

**6. Coverage Analysis**
- Concept coverage across proverbs
- Business application mapping completeness
- Domain distribution analysis

### Quality Scoring System

The validator produces scores across multiple dimensions:

- **Individual Scores**: 0.0-1.0 for each validation dimension
- **Overall Quality Score**: Weighted average of all dimensions
- **Quality Grade**: Letter grade (A+ to F) based on overall score
- **Criteria Assessment**: Pass/fail against predefined thresholds

### Quality Thresholds

Default validation criteria:
- Concept Coverage: ≥80% of proverbs should have concepts
- Business Coverage: ≥60% should have business applications
- Cultural Authenticity: ≥3.0 average score
- Expert Validation: ≥3.0 average score
- Query Performance: ≤2.0 seconds maximum response time

### Validation Reports

Generated reports include:
- `ontology_validation_comprehensive_YYYYMMDD_HHMMSS.json`: Complete validation results
- `ontology_validation_summary_YYYYMMDD_HHMMSS.json`: Executive summary
- Console output with quality scores and recommendations

## OG-RAG Integration

### Contextual Retrieval for RAG

The ontology system is optimized for OG-RAG applications:

1. **Rich Context Extraction**: Retrieve culturally-grounded context subgraphs
2. **Semantic Similarity**: Advanced algorithms for relevant proverb discovery  
3. **Cultural Preservation**: Maintain authenticity throughout translation
4. **Business Application**: Enable modern context while preserving wisdom

### Integration Example

```python
from scripts.ontology_querier import KikuyuProverbsQuerier

# Initialize querier
querier = KikuyuProverbsQuerier(
    uri="bolt://localhost:7687",
    username="neo4j", 
    password="kikuyu_proverbs_2024"
)

# Get contextual subgraph for RAG
context = querier.get_contextual_subgraph_for_rag(
    input_text="Need proverbs about leadership",
    context_radius=2,
    include_business_applications=True,
    max_relationships=30
)

# Extract cultural context for prompt enhancement
cultural_context = context['context_subgraph']['cultural_contexts']
business_apps = context['context_subgraph']['business_applications']
related_proverbs = context['results']

# Use context to enhance LLM prompt
enhanced_prompt = f"""
Cultural Context: {cultural_context}
Business Applications: {business_apps}
Related Proverbs: {related_proverbs}

Please provide a culturally faithful translation considering this context.
"""
```

### Expected Performance Improvements

Research indicates OG-RAG with comprehensive ontologies provides:
- **55% increase** in factual accuracy
- **40% improvement** in response correctness
- **30% faster** attribution and **27% better** fact-based reasoning
- Superior cultural faithfulness compared to raw LLM translation

## Performance Optimization

### Neo4j Optimization

**Essential Indexes**:
```cypher
// Create performance indexes
CREATE INDEX proverb_id_index FOR (p:Proverb) ON (p.id);
CREATE INDEX concept_name_index FOR (c:Concept) ON (c.name);
CREATE INDEX business_domain_index FOR (ba:BusinessApplication) ON (ba.domain);
CREATE TEXT INDEX proverb_text_index FOR (p:Proverb) ON (p.kikuyu_text);
```

**Essential Constraints**:
```cypher
// Ensure data integrity
CREATE CONSTRAINT proverb_id_unique FOR (p:Proverb) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT concept_name_unique FOR (c:Concept) REQUIRE c.name IS UNIQUE;
```

### Query Optimization Tips

1. **Use Specific Filters**: Apply expert score and relevance filters early
2. **Limit Result Sets**: Use appropriate LIMIT clauses for large queries
3. **Index Utilization**: Ensure queries use created indexes effectively
4. **Relationship Depth**: Limit relationship traversal depth for performance

### Memory Configuration

For large ontologies, optimize Neo4j memory settings:
```
# neo4j.conf
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=2G
```

## Troubleshooting

### Common Issues

**1. Connection Problems**
```bash
# Test Neo4j connection
python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password'))
with driver.session() as session:
    result = session.run('RETURN 1')
    print('Connection successful!')
driver.close()
"
```

**2. Memory Issues**
- Increase Neo4j heap size
- Process data in smaller batches
- Optimize query patterns

**3. Performance Issues**
- Verify index creation
- Check constraint existence
- Analyze query execution plans

**4. Data Quality Issues**
- Run comprehensive validation
- Check expert validation score distribution
- Verify CSV data format

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python scripts/ontology_builder.py \
    --csv-file data/processed/expert_validation.csv \
    --debug \
    --verbose
```

### Support and Resources

- **Neo4j Documentation**: https://neo4j.com/docs/
- **APOC Procedures**: https://neo4j.com/labs/apoc/
- **Project Issues**: Create issue in project repository
- **Expert Validation**: See `data/processed/expert_validation_instructions.md`

## Best Practices

### Data Preparation
1. Ensure expert validation data completeness
2. Validate CSV format before construction
3. Set appropriate quality thresholds
4. Review cultural authenticity scores

### Ontology Construction
1. Start with basic construction for testing
2. Use advanced options for production
3. Create indexes and constraints
4. Validate construction quality

### Query Optimization
1. Use specific query types for better performance
2. Apply appropriate filters and limits
3. Monitor query execution times
4. Utilize cultural and business weights effectively

### Quality Assurance
1. Run validation after construction
2. Monitor performance metrics regularly
3. Review cultural authenticity regularly
4. Update quality thresholds as needed

---

*This comprehensive guide enables the creation of sophisticated, culturally-aware ontologies optimized for OG-RAG applications while preserving the authentic cultural wisdom of Kikuyu proverbs.*