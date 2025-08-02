# Graph Schema for OG-RAG Cultural Heritage Knowledge Graph

This directory contains the graph schema definitions for the ontology-grounded knowledge graph supporting cultural heritage and proverb research.

## Schema Files

- `cultural_heritage_schema.cypher` - Core cultural heritage entities and relationships
- `proverb_schema.cypher` - Proverb-specific schema with semantic relationships
- `ontology_schema.cypher` - Ontological concepts and hierarchies
- `constraints.cypher` - Database constraints and indexes
- `indexes.cypher` - Performance optimization indexes

## Core Node Types

### Cultural Heritage Entities
- **Proverb** - Cultural sayings and wisdom
- **Culture** - Cultural groups and traditions
- **Language** - Language systems and variants
- **Concept** - Abstract concepts and themes
- **Category** - Semantic categories and classifications

### Ontological Entities
- **OntologyClass** - Formal ontology classes
- **Property** - Ontological properties and attributes
- **Individual** - Specific instances and examples
- **Axiom** - Logical axioms and constraints

## Core Relationship Types

### Semantic Relationships
- **EXPRESSES** - Proverb expresses concept
- **BELONGS_TO** - Entity belongs to culture/language
- **SIMILAR_TO** - Semantic similarity
- **CONTRASTS_WITH** - Semantic opposition
- **IMPLIES** - Logical implication

### Ontological Relationships
- **SUBCLASS_OF** - Class hierarchy
- **INSTANCE_OF** - Class instantiation
- **HAS_PROPERTY** - Property association
- **EQUIVALENT_TO** - Semantic equivalence

### Contextual Relationships
- **USED_IN** - Context of usage
- **DERIVED_FROM** - Historical derivation
- **RELATED_TO** - General association
- **PART_OF** - Compositional relationship

## Schema Evolution

The schema supports:
- Incremental updates through migrations
- Backward compatibility preservation
- Ontology versioning and evolution
- Multi-language content support

## Usage in OG-RAG

This schema enables:
- Hypergraph representation of cultural knowledge
- Efficient retrieval for contextual generation
- Semantic relationship traversal
- Cross-cultural knowledge mapping
