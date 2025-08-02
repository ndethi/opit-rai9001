#!/bin/bash

# OG-RAG Docker Management Script
# Provides convenient commands for managing the Docker environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to start core services
start_core() {
    print_status "Starting core OG-RAG services (Neo4j, Redis, Jupyter)..."
    docker-compose up -d neo4j redis jupyter
    print_success "Core services started!"
    print_status "Access points:"
    echo "  - Neo4j Browser: http://localhost:7474 (neo4j/ograg2025)"
    echo "  - Jupyter Lab: http://localhost:8888 (token: ograg2025)"
    echo "  - Redis: localhost:6379"
}

# Function to start all services
start_all() {
    print_status "Starting all OG-RAG services..."
    docker-compose --profile local-llm --profile dev up -d
    print_success "All services started!"
    show_status
}

# Function to stop services
stop() {
    print_status "Stopping OG-RAG services..."
    docker-compose down
    print_success "Services stopped!"
}

# Function to restart services
restart() {
    print_status "Restarting OG-RAG services..."
    docker-compose restart
    print_success "Services restarted!"
}

# Function to show service status
show_status() {
    print_status "Service Status:"
    docker-compose ps
}

# Function to view logs
logs() {
    if [ -z "$1" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $1..."
        docker-compose logs -f "$1"
    fi
}

# Function to enter development environment
dev_shell() {
    print_status "Starting development shell..."
    docker-compose --profile dev up -d dev-env
    docker-compose exec dev-env bash
}

# Function to run Jupyter shell
jupyter_shell() {
    print_status "Starting Jupyter shell..."
    docker-compose exec jupyter bash
}

# Function to backup Neo4j data
backup_neo4j() {
    BACKUP_DIR="./src/neo4j/backups"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="backup_${TIMESTAMP}_full.dump"
    
    print_status "Creating Neo4j backup..."
    mkdir -p "$BACKUP_DIR"
    
    docker-compose exec neo4j neo4j-admin database backup \
        --database=neo4j \
        --to-path=/backups \
        "$BACKUP_FILE"
    
    print_success "Backup created: $BACKUP_DIR/$BACKUP_FILE"
}

# Function to restore Neo4j data
restore_neo4j() {
    if [ -z "$1" ]; then
        print_error "Please specify backup file name"
        print_status "Available backups:"
        ls -la ./src/neo4j/backups/
        exit 1
    fi
    
    print_warning "This will replace all existing data. Are you sure? (y/N)"
    read -r confirm
    if [[ $confirm != [yY] ]]; then
        print_status "Restore cancelled."
        exit 0
    fi
    
    print_status "Stopping Neo4j..."
    docker-compose stop neo4j
    
    print_status "Restoring from backup: $1"
    docker-compose run --rm neo4j neo4j-admin database restore \
        --from-path="/backups/$1" \
        --database=neo4j \
        --overwrite-destination
    
    print_status "Starting Neo4j..."
    docker-compose up -d neo4j
    
    print_success "Restore completed!"
}

# Function to clean up Docker resources
cleanup() {
    print_warning "This will remove all containers, volumes, and networks. Are you sure? (y/N)"
    read -r confirm
    if [[ $confirm != [yY] ]]; then
        print_status "Cleanup cancelled."
        exit 0
    fi
    
    print_status "Cleaning up Docker resources..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    print_success "Cleanup completed!"
}

# Function to update dependencies
update() {
    print_status "Updating Docker images..."
    docker-compose pull
    
    print_status "Rebuilding custom images..."
    docker-compose build --no-cache
    
    print_success "Update completed!"
}

# Function to initialize the project
init() {
    print_status "Initializing OG-RAG project..."
    
    # Create necessary directories
    mkdir -p src/neo4j/{database,imports,backups}
    mkdir -p notebooks
    mkdir -p data/{raw,processed,external}
    
    # Start core services
    start_core
    
    # Wait for Neo4j to be ready
    print_status "Waiting for Neo4j to be ready..."
    sleep 30
    
    # Apply initial schema
    if [ -f "src/neo4j/schemas/cultural_heritage_schema.cypher" ]; then
        print_status "Applying initial schema..."
        docker-compose exec neo4j cypher-shell -u neo4j -p ograg2025 \
            -f /var/lib/neo4j/import/../schemas/cultural_heritage_schema.cypher
    fi
    
    print_success "Project initialized!"
    print_status "Next steps:"
    echo "  1. Open Jupyter Lab: http://localhost:8888"
    echo "  2. Open Neo4j Browser: http://localhost:7474"
    echo "  3. Start developing your OG-RAG system!"
}

# Main script logic
case "$1" in
    "start"|"up")
        check_docker
        start_core
        ;;
    "start-all")
        check_docker
        start_all
        ;;
    "stop"|"down")
        stop
        ;;
    "restart")
        check_docker
        restart
        ;;
    "status"|"ps")
        show_status
        ;;
    "logs")
        logs "$2"
        ;;
    "dev")
        check_docker
        dev_shell
        ;;
    "jupyter")
        check_docker
        jupyter_shell
        ;;
    "backup")
        check_docker
        backup_neo4j
        ;;
    "restore")
        check_docker
        restore_neo4j "$2"
        ;;
    "cleanup")
        cleanup
        ;;
    "update")
        check_docker
        update
        ;;
    "init")
        check_docker
        init
        ;;
    *)
        echo "OG-RAG Docker Management Script"
        echo "Usage: $0 {command}"
        echo ""
        echo "Commands:"
        echo "  start|up        Start core services (Neo4j, Redis, Jupyter)"
        echo "  start-all       Start all services including optional ones"
        echo "  stop|down       Stop all services"
        echo "  restart         Restart all services"
        echo "  status|ps       Show service status"
        echo "  logs [service]  Show logs (all services or specific service)"
        echo "  dev             Enter development shell"
        echo "  jupyter         Enter Jupyter container shell"
        echo "  backup          Create Neo4j backup"
        echo "  restore <file>  Restore Neo4j from backup"
        echo "  cleanup         Remove all containers and volumes"
        echo "  update          Update Docker images and rebuild"
        echo "  init            Initialize project (first time setup)"
        echo ""
        echo "Examples:"
        echo "  $0 start              # Start core services"
        echo "  $0 logs neo4j         # Show Neo4j logs"
        echo "  $0 backup             # Create database backup"
        echo "  $0 restore backup.dump # Restore from backup"
        ;;
esac
