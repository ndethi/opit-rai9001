# Neo4j Database Configuration

## Installation

### Option 1: Docker (Recommended for Development)
```bash
# Pull Neo4j Docker image
docker pull neo4j:latest

# Run Neo4j container
docker run \
    --name neo4j-og-rag \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $PWD/database:/data \
    -v $PWD/imports:/var/lib/neo4j/import \
    -v $PWD/config:/var/lib/neo4j/conf \
    --env NEO4J_AUTH=neo4j/ograg2025 \
    neo4j:latest
```

### Option 2: Local Installation
```bash
# macOS with Homebrew
brew install neo4j

# Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.4' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
```

## Configuration Files

- `neo4j.conf` - Main Neo4j configuration
- `apoc.conf` - APOC plugin configuration  
- `security.conf` - Security and authentication settings

## Default Settings

- **HTTP Port**: 7474 (Web interface)
- **Bolt Port**: 7687 (Driver connections)
- **Username**: neo4j
- **Password**: ograg2025 (change in production)

## Performance Tuning

For OG-RAG workloads, consider:
- Increase `dbms.memory.heap.initial_size`
- Optimize `dbms.memory.pagecache.size`
- Enable query caching
- Configure appropriate indexes

## Security Notes

- Change default password in production
- Configure SSL certificates
- Restrict network access
- Enable audit logging
