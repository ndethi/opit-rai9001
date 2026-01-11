#!/bin/bash

# Quick Neo4j Restoration Script
# This script provides a simple command-line interface for common restoration tasks

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Neo4j Knowledge Graph Quick Restore${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to display menu
show_menu() {
    echo -e "${GREEN}Available Actions:${NC}"
    echo "  1) Restore to LOCAL Neo4j (development)"
    echo "  2) Restore to AURADB (production)"
    echo "  3) Create backup from LOCAL Neo4j"
    echo "  4) Create backup from AURADB"
    echo "  5) Show database statistics"
    echo "  6) Validate connection"
    echo "  7) Exit"
    echo ""
}

# Function to restore local
restore_local() {
    echo -e "${YELLOW}Restoring to LOCAL Neo4j...${NC}"
    echo ""
    read -p "Clear existing data? (yes/no): " clear_data
    
    if [ "$clear_data" = "yes" ]; then
        python3 "$PROJECT_ROOT/scripts/restore_neo4j_from_repo.py" --env development --clear
    else
        python3 "$PROJECT_ROOT/scripts/restore_neo4j_from_repo.py" --env development
    fi
}

# Function to restore AuraDB
restore_auradb() {
    echo -e "${YELLOW}Restoring to AURADB...${NC}"
    echo ""
    echo -e "${RED}WARNING: This will modify your production database!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        echo "Aborted."
        return
    fi
    
    read -p "Clear existing data? (yes/no): " clear_data
    
    if [ "$clear_data" = "yes" ]; then
        python3 "$PROJECT_ROOT/scripts/restore_neo4j_from_repo.py" --env production --auradb --clear
    else
        python3 "$PROJECT_ROOT/scripts/restore_neo4j_from_repo.py" --env production --auradb
    fi
}

# Function to backup local
backup_local() {
    echo -e "${YELLOW}Backing up LOCAL Neo4j...${NC}"
    echo ""
    python3 "$PROJECT_ROOT/scripts/backup_neo4j.py" --format both
    echo ""
    echo -e "${GREEN}Backup complete!${NC}"
    echo "Files saved to: $PROJECT_ROOT/src/neo4j/backups/"
}

# Function to backup AuraDB
backup_auradb() {
    echo -e "${YELLOW}Backing up AURADB...${NC}"
    echo ""
    python3 "$PROJECT_ROOT/scripts/backup_neo4j.py" --auradb --format both
    echo ""
    echo -e "${GREEN}Backup complete!${NC}"
    echo "Files saved to: $PROJECT_ROOT/src/neo4j/backups/"
}

# Function to show stats
show_stats() {
    echo -e "${YELLOW}Database Statistics:${NC}"
    echo ""
    read -p "Which database? (local/auradb): " db_choice
    
    if [ "$db_choice" = "local" ]; then
        python3 "$PROJECT_ROOT/scripts/validate_neo4j_connection.py"
    elif [ "$db_choice" = "auradb" ]; then
        NEO4J_ENV=production python3 "$PROJECT_ROOT/scripts/validate_neo4j_connection.py"
    else
        echo "Invalid choice"
    fi
}

# Function to validate connection
validate_connection() {
    echo -e "${YELLOW}Validating Neo4j Connection:${NC}"
    echo ""
    read -p "Which database? (local/auradb): " db_choice
    
    if [ "$db_choice" = "local" ]; then
        python3 "$PROJECT_ROOT/scripts/validate_neo4j_connection.py"
    elif [ "$db_choice" = "auradb" ]; then
        NEO4J_ENV=production python3 "$PROJECT_ROOT/scripts/validate_neo4j_connection.py"
    else
        echo "Invalid choice"
    fi
}

# Main loop
while true; do
    echo ""
    show_menu
    read -p "Select option (1-7): " choice
    echo ""
    
    case $choice in
        1)
            restore_local
            ;;
        2)
            restore_auradb
            ;;
        3)
            backup_local
            ;;
        4)
            backup_auradb
            ;;
        5)
            show_stats
            ;;
        6)
            validate_connection
            ;;
        7)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please select 1-7.${NC}"
            ;;
    esac
    
    read -p "Press Enter to continue..."
done
