# Data Import Files

This directory contains data files and scripts for importing cultural heritage data into the Neo4j knowledge graph.

## File Types

### CSV Files
- `cultures.csv` - Cultural group information
- `languages.csv` - Language data and metadata  
- `concepts.csv` - Semantic concepts and definitions
- `proverbs.csv` - Proverb texts and metadata
- `relationships.csv` - Semantic relationships between entities

### JSON Files  
- `kikuyu_proverbs.json` - Kikuyu cultural proverbs
- `luo_proverbs.json` - Luo cultural proverbs
- `ontology_mappings.json` - Ontology to graph mappings
- `cultural_themes.json` - Thematic categorizations

### OWL Files
- `cultural_heritage.owl` - Cultural heritage ontology
- `proverb_ontology.owl` - Proverb-specific ontology
- `wealth_prosperity.owl` - Domain-specific ontology for wealth themes

## Import Scripts
- `import_all.cypher` - Master import script
- `import_cultures.cypher` - Culture and language import
- `import_proverbs.cypher` - Proverb data import
- `import_relationships.cypher` - Relationship creation

## Data Sources

The data in this directory comes from:
- Research data collection (`../../data/sources/`)
- Ontology engineering work (`../ontology/`)
- Cultural heritage digitization projects
- Linguistic databases and resources

## Import Process

1. **Prepare Data** - Clean and format source data
2. **Load Entities** - Import nodes (cultures, languages, concepts, proverbs)
3. **Create Relationships** - Establish semantic and hierarchical relationships
4. **Validate Data** - Run quality checks and constraint validation
5. **Optimize Performance** - Create indexes and analyze query performance

## Usage

```bash
# Load all data using Neo4j Browser or cypher-shell
cat import_all.cypher | cypher-shell -u neo4j -p ograg2025

# Or use Python import scripts
python ../scripts/import_proverbs.py kikuyu_proverbs.json
```

## Data Format Examples

### Proverb CSV Format
```csv
id,text,meaning,language,culture,themes,source
1,"Hiti ndihoyagwo","A hyena is not stirred with a stick",kikuyu,Kikuyu,"caution,wisdom",oral_tradition
```

### Relationship CSV Format  
```csv
source_id,source_type,target_id,target_type,relationship_type,properties
concept_1,Concept,concept_2,Concept,SIMILAR_TO,"{""strength"": 0.8}"
```
