#!/usr/bin/env python3
"""
Neo4j Connection Validation Script

This script validates the connection to Neo4j using configuration from .env file.
It checks connectivity, retrieves basic statistics, and confirms the database is ready.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / '.env')

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def validate_connection():
    """Validate Neo4j connection using .env configuration"""
    
    # Read configuration from environment variables
    config = {
        'uri': os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
        'username': os.getenv('NEO4J_USER', 'neo4j'),
        'password': os.getenv('NEO4J_PASSWORD', 'ograg2025'),
        'database': os.getenv('NEO4J_DATABASE', 'kikuyu-kg')
    }
    
    print("🔍 Neo4j Configuration:")
    print(f"   URI: {config['uri']}")
    print(f"   Username: {config['username']}")
    print(f"   Database: {config['database']}")
    print()
    
    # Validate configuration
    if not all([config['uri'], config['username'], config['password'], config['database']]):
        print("❌ Invalid configuration. Please check your .env file.")
        return False
    
    # Test connection
    logger.info("\n🔌 Testing connection...")
    
    try:
        driver = GraphDatabase.driver(
            config['uri'],
            auth=(config['username'], config['password'])
        )
        
        # Verify connectivity
        driver.verify_connectivity()
        logger.info("   ✅ Connection established")
        
        # Run test query
        with driver.session(database=config['database']) as session:
            result = session.run("RETURN 1 as test")
            value = result.single()['test']
            
            if value == 1:
                logger.info("   ✅ Query execution successful")
                
                # Get graph statistics
                logger.info("\n📊 Graph Statistics:")
                
                stats_query = """
                MATCH (n)
                WITH labels(n) as labels, count(n) as node_count
                RETURN labels, node_count
                ORDER BY node_count DESC
                """
                
                stats_result = session.run(stats_query)
                stats = list(stats_result)
                
                if stats:
                    total_nodes = sum(record['node_count'] for record in stats)
                    logger.info(f"   Total Nodes: {total_nodes}")
                    logger.info(f"   Node Types:")
                    for record in stats[:10]:  # Show top 10
                        labels_str = ':'.join(record['labels']) if record['labels'] else 'No Label'
                        logger.info(f"      {labels_str}: {record['node_count']}")
                else:
                    logger.info("   Total Nodes: 0 (empty database)")
                
                # Get relationship count
                rel_query = "MATCH ()-[r]->() RETURN count(r) as rel_count"
                rel_result = session.run(rel_query).single()
                logger.info(f"   Total Relationships: {rel_result['rel_count']}")
                
                # Check constraints
                constraints_query = "SHOW CONSTRAINTS"
                try:
                    constraints = list(session.run(constraints_query))
                    logger.info(f"\n🔒 Constraints: {len(constraints)} defined")
                    if constraints:
                        for constraint in constraints[:5]:  # Show first 5
                            logger.info(f"      {constraint.get('name', 'unnamed')}")
                except Exception as e:
                    logger.info(f"\n🔒 Constraints: Unable to query (may need schema deployment)")
                
                # Check indexes
                indexes_query = "SHOW INDEXES"
                try:
                    indexes = list(session.run(indexes_query))
                    logger.info(f"\n📇 Indexes: {len(indexes)} defined")
                    if indexes:
                        for index in indexes[:5]:  # Show first 5
                            logger.info(f"      {index.get('name', 'unnamed')}")
                except Exception as e:
                    logger.info(f"\n📇 Indexes: Unable to query (may need schema deployment)")
        
        driver.close()
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ NEO4J VALIDATION SUCCESSFUL!")
        logger.info("=" * 70)
        logger.info("\n📝 Status: Ready for schema deployment and data loading")
        
        return True
        
    except ServiceUnavailable as e:
        logger.error("\n❌ Connection failed: Neo4j service unavailable")
        logger.error(f"   Error: {e}")
        logger.error("\n💡 Troubleshooting:")
        logger.error("   1. Check if Neo4j is running:")
        logger.error("      - Local: neo4j status")
        logger.error("      - Homebrew: brew services list")
        logger.error("      - Docker: docker ps | grep neo4j")
        logger.error("   2. Verify URI is correct: bolt://localhost:7687")
        logger.error("   3. Check firewall settings")
        return False
        
    except AuthError as e:
        logger.error("\n❌ Authentication failed")
        logger.error(f"   Error: {e}")
        logger.error("\n💡 Check credentials in .env file:")
        logger.error(f"   NEO4J_USER={config['username']}")
        logger.error(f"   NEO4J_PASSWORD=<check your password>")
        return False
        
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        logger.error(f"   Type: {type(e).__name__}")
        return False


if __name__ == "__main__":
    success = validate_connection()
    sys.exit(0 if success else 1)
