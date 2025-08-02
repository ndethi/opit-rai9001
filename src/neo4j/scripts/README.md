# Python Scripts for Neo4j Operations

This directory contains Python scripts for managing the Neo4j knowledge graph database.

## Script Categories

### Database Management
- `connection.py` - Neo4j connection utilities
- `setup_database.py` - Initial database setup and configuration
- `backup_restore.py` - Database backup and restoration operations

### Data Import/Export  
- `import_ontologies.py` - Import OWL ontologies into graph format
- `import_proverbs.py` - Import cultural proverbs and metadata
- `export_knowledge.py` - Export graph data for analysis

### Knowledge Graph Operations
- `graph_builder.py` - Build knowledge graph from structured data
- `relationship_mapper.py` - Create semantic relationships
- `hypergraph_creator.py` - Create hypergraph structures for OG-RAG

### Query and Analysis
- `semantic_search.py` - Semantic search and retrieval operations
- `graph_analytics.py` - Graph analysis and metrics
- `similarity_calculator.py` - Calculate semantic similarities

### OG-RAG Integration
- `rag_retriever.py` - Knowledge retrieval for RAG pipeline
- `context_builder.py` - Build contextual information for generation
- `ontology_grounding.py` - Ground retrieved knowledge in ontologies

## Usage Examples

```python
# Connect to database
from connection import Neo4jConnection
db = Neo4jConnection()

# Import cultural data
from import_proverbs import ProverbImporter
importer = ProverbImporter(db)
importer.import_from_file('../../data/proverbs/kikuyu_proverbs.json')

# Perform semantic search
from semantic_search import SemanticSearcher
searcher = SemanticSearcher(db)
results = searcher.find_similar_proverbs("hard work brings success")
```

## Dependencies

These scripts require:
- neo4j (Python driver)
- owlready2 (ontology processing)
- sentence-transformers (semantic embeddings)
- networkx (graph algorithms)
- pandas (data manipulation)
