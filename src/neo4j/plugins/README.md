# Neo4j Plugins for Kikuyu oGRAG System

This directory contains Neo4j plugins required for the oGRAG (Ontology-guided Retrieval Augmented Generation) system focused on Kikuyu proverbs.

## Required Plugins

For optimal functioning of the knowledge graph and retrieval system, the following plugins are required:

### 1. Graph Data Science Library (GDS)

**Version**: Latest (5.15.0 or newer recommended)
**File Size**: ~55 MB

**Download From**:
- Official site: https://neo4j.com/download-center/#community-graph-data-science
- Direct link (verify version): https://neo4j.com/download-thanks/?edition=graph-data-science-library

**Installation**:
1. Download the JAR file (e.g., `graph-data-science-2.5.0.jar`)
2. Place it in this directory (`src/neo4j/plugins/`)
3. Ensure the Docker container has read access to this directory

### 2. APOC (Awesome Procedures On Cypher)

**Version**: Latest (compatible with Neo4j 5.x)
**File Size**: ~13 MB

**Download From**:
- Official site: https://neo4j.com/labs/apoc/
- GitHub releases: https://github.com/neo4j/apoc/releases

**Installation**:
1. Download the JAR file (e.g., `apoc-5.15.0-core.jar`)
2. Place it in this directory (`src/neo4j/plugins/`)
3. Ensure the Docker container has read access to this directory

## Plugin Configuration

The Docker Compose configuration already mounts this directory to the Neo4j container. If you encounter issues with plugin loading, check:

1. File permissions (ensure Neo4j user in Docker can read these files)
2. Docker volume mounting configuration in `docker-compose.yml`
3. Neo4j configuration in `src/neo4j/config/neo4j.conf`

## Note on Version Control

The actual JAR files are excluded from version control due to their large size. Each developer needs to download these files separately following the instructions above.

## Troubleshooting

If plugins aren't loading:
1. Check Neo4j logs: `src/neo4j/logs/`
2. Verify JAR file integrity and compatibility with your Neo4j version
3. Restart the Neo4j container after adding plugins: `docker-compose restart neo4j`
