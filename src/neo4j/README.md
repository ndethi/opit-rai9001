# Neo4j Knowledge Graph System

This directory contains the Neo4j knowledge graph implementation for the OG-RAG (Ontology-Grounded Retrieval-Augmented Generation) research project.

## Directory Structure

```
src/neo4j/
├── README.md              # This file
├── database/              # Neo4j database files and data
├── scripts/               # Python scripts for database operations
├── cypher/                # Cypher query files
├── schemas/               # Graph schema definitions
├── migrations/            # Database migration scripts
├── imports/               # Data import files (CSV, JSON, etc.)
├── backups/               # Database backup files
└── config/                # Neo4j configuration files
```

## Purpose

This Neo4j implementation supports the research on Ontology-Grounded RAG systems by providing:

1. **Structured Knowledge Storage** - Store ontological knowledge in graph format
2. **Relationship Modeling** - Capture complex entity relationships and hierarchies
3. **Efficient Retrieval** - Enable fast graph traversal for knowledge retrieval
4. **Hypergraph Support** - Model n-ary relationships for advanced OG-RAG architectures
5. **Cultural Heritage Data** - Store and organize cultural knowledge and proverbs

## Key Features

- **Ontology Integration** - Direct mapping from OWL ontologies to Neo4j graph structure
- **Proverb Knowledge Base** - Specialized nodes and relationships for cultural proverbs
- **Multi-language Support** - Unicode support for low-resource languages
- **Semantic Relationships** - Rich relationship modeling for contextual retrieval
- **Performance Optimization** - Indexed queries for real-time RAG applications

## Getting Started

1. **Install Neo4j** - Follow installation instructions in `config/`
2. **Load Schema** - Apply schema definitions from `schemas/`
3. **Import Data** - Use scripts in `imports/` to load initial data
4. **Run Queries** - Execute Cypher queries from `cypher/` directory

## Research Integration

This Neo4j system integrates with:
- Ontology processing (`../ontology/`)
- RAG system implementation (`../rag-system/`)
- Cultural heritage data processing (`../../data/`)

## Related Work

This implementation supports the research described in:
- Literature Review (Chapter 2) - Hypergraph-based architectures
- Microsoft OG-RAG framework adaptations
- GNN-RAG integration capabilities
