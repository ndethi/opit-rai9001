# OG-RAG Docker Setup Guide

This guide will help you set up the complete Docker environment for your Ontology-Grounded RAG research project.

## Quick Start

1. **Initialize the project** (first time only):
   ```bash
   ./docker-manage.sh init
   ```

2. **Start development environment**:
   ```bash
   ./docker-manage.sh start
   ```

3. **Access services**:
   - Neo4j Browser: http://localhost:7474 (neo4j/ograg2025)
   - Jupyter Lab: http://localhost:8888 (token: ograg2025)
   - Redis: localhost:6379

## Services Overview

### Core Services (Always Running)

#### Neo4j Graph Database
- **Purpose**: Store Kikuyu proverb ontology and knowledge graph
- **Access**: http://localhost:7474
- **Credentials**: neo4j/ograg2025
- **Volume**: `./src/neo4j/database` (persistent storage)
- **Plugins**: APOC, Graph Data Science

#### Jupyter Lab
- **Purpose**: Research notebooks and experimentation
- **Access**: http://localhost:8888
- **Token**: ograg2025
- **Volume**: Current directory mounted as `/workspace`
- **Features**: All research dependencies pre-installed

#### Redis
- **Purpose**: Caching embeddings and API responses
- **Access**: localhost:6379
- **Volume**: Persistent data storage

### Optional Services

#### Ollama (Local LLM)
```bash
docker-compose --profile local-llm up -d ollama
```
- **Purpose**: Local LLM inference for offline development
- **Access**: http://localhost:11434

#### Development Environment
```bash
./docker-manage.sh dev
```
- **Purpose**: Containerized Python development environment
- **Features**: All dependencies, development tools, shell access

## Management Commands

### Basic Operations
```bash
# Start core services
./docker-manage.sh start

# Stop all services
./docker-manage.sh stop

# Restart services
./docker-manage.sh restart

# Check service status
./docker-manage.sh status

# View logs
./docker-manage.sh logs           # All services
./docker-manage.sh logs neo4j     # Specific service
```

### Development
```bash
# Enter development shell
./docker-manage.sh dev

# Enter Jupyter container
./docker-manage.sh jupyter

# Start all services (including optional)
./docker-manage.sh start-all
```

### Data Management
```bash
# Backup Neo4j database
./docker-manage.sh backup

# Restore from backup
./docker-manage.sh restore backup_20250802_1400_full.dump

# Clean up everything (DESTRUCTIVE)
./docker-manage.sh cleanup
```

### Maintenance
```bash
# Update Docker images
./docker-manage.sh update

# Initialize project (first time)
./docker-manage.sh init
```

## Development Workflow

### 1. Research Setup
```bash
# Initialize project
./docker-manage.sh init

# Start services
./docker-manage.sh start

# Open Jupyter Lab
open http://localhost:8888
```

### 2. Ontology Development
- Use Neo4j Browser for interactive graph exploration
- Run Cypher queries from `src/neo4j/cypher/`
- Import data using scripts in `src/neo4j/scripts/`

### 3. OG-RAG Implementation
- Develop in Jupyter notebooks
- Use Python scripts in `src/` directory
- Test retrieval mechanisms against Neo4j

### 4. Evaluation
- Run evaluation notebooks
- Generate reports and visualizations
- Export results for thesis writing

## Environment Configuration

### 1. Copy environment template
```bash
cp .env.example .env
```

### 2. Add your API keys
```bash
# Edit .env file
OPENAI_API_KEY=your_actual_key_here
GOOGLE_API_KEY=your_actual_key_here
ANTHROPIC_API_KEY=your_actual_key_here
```

### 3. Customize paths if needed
```bash
# Adjust data directories
DATA_DIR=./data
MODELS_DIR=./models
```

## Data Directories

The Docker setup creates and mounts these directories:

```
├── src/neo4j/database/     # Neo4j data (persistent)
├── src/neo4j/imports/      # Data import staging
├── src/neo4j/backups/      # Database backups
├── notebooks/              # Jupyter notebooks
├── data/                   # Research data
│   ├── raw/               # Raw proverb collections
│   ├── processed/         # Cleaned datasets
│   └── external/          # External resources
└── outputs/               # Results and evaluations
```

## Troubleshooting

### Neo4j Won't Start
```bash
# Check logs
./docker-manage.sh logs neo4j

# Common issues:
# - Port 7474 already in use
# - Insufficient memory
# - Permission issues with data directory
```

### Jupyter Can't Connect to Neo4j
```bash
# Verify network connectivity
docker-compose exec jupyter ping neo4j

# Check environment variables
docker-compose exec jupyter env | grep NEO4J
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER src/neo4j/database
```

### Memory Issues
```bash
# Increase Docker memory limits
# Docker Desktop: Settings > Resources > Memory > 8GB+
```

## Performance Optimization

### Neo4j Tuning
- Adjust memory settings in `src/neo4j/config/neo4j.conf`
- Monitor query performance in Neo4j Browser
- Create appropriate indexes for your queries

### Jupyter Performance
- Use Redis for caching expensive operations
- Save intermediate results to avoid recomputation
- Use GPU if available for ML operations

## Security Notes

### Development Environment
- Default passwords are for development only
- Change passwords in production
- Don't commit `.env` file with real API keys

### Data Protection
- Regular backups of Neo4j data
- Version control for ontology files
- Secure storage of research data

## Integration with Research

This Docker setup directly supports your research methodology:

1. **CRISP-DM Data Understanding**: Jupyter notebooks for data exploration
2. **Ontology Construction**: Neo4j for graph modeling and validation
3. **OG-RAG Development**: Complete Python environment with all dependencies
4. **Evaluation**: Metrics calculation and visualization tools
5. **Cultural Preservation**: Structured storage and backup of cultural knowledge

## Next Steps

1. Initialize the project: `./docker-manage.sh init`
2. Explore the sample schema in Neo4j Browser
3. Create your first research notebook
4. Start building your Kikuyu proverb ontology
5. Implement your OG-RAG retrieval mechanism

Happy researching! 🚀
