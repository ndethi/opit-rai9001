# Cypher Queries for OG-RAG Knowledge Graph

This directory contains pre-written Cypher queries for common operations on the cultural heritage knowledge graph.

## Query Categories

### Basic Queries
- `basic_queries.cypher` - Simple node and relationship queries
- `statistics.cypher` - Database statistics and metrics
- `health_checks.cypher` - Database health monitoring queries

### Cultural Heritage Queries  
- `proverb_queries.cypher` - Proverb search and analysis queries
- `cultural_analysis.cypher` - Cross-cultural comparison queries
- `semantic_search.cypher` - Semantic similarity and relationship queries

### OG-RAG Specific Queries
- `retrieval_queries.cypher` - Knowledge retrieval for RAG pipeline
- `context_building.cypher` - Context construction for generation
- `hypergraph_queries.cypher` - Hypergraph traversal and selection

### Analytics Queries
- `graph_metrics.cypher` - Graph analysis and centrality measures
- `relationship_analysis.cypher` - Relationship pattern analysis
- `clustering_queries.cypher` - Community detection and clustering

## Usage

These queries can be:
- Executed directly in Neo4j Browser
- Used in Python scripts via the neo4j driver
- Integrated into the OG-RAG retrieval pipeline
- Modified for specific research questions

## Query Optimization

All queries are optimized for:
- Index usage where possible
- Efficient graph traversal patterns
- Minimal memory footprint
- Fast execution on large datasets

## Examples

```cypher
// Find proverbs about wealth from specific culture
MATCH (p:Proverb)-[:BELONGS_TO]->(c:Culture {name: 'Kikuyu'})
WHERE p.text CONTAINS 'wealth' OR p.text CONTAINS 'prosperity'
RETURN p.text, p.meaning

// Find semantically similar concepts
MATCH (c1:Concept)-[:SIMILAR_TO]->(c2:Concept)
WHERE c1.name = 'hard work'
RETURN c2.name, c2.definition
```
