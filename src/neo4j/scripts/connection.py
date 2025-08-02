"""
Neo4j Connection Utilities for OG-RAG Research
Provides secure connection management and query execution utilities.
"""

from neo4j import GraphDatabase
import os
from typing import List, Dict, Any, Optional
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jConnection:
    """
    Neo4j database connection manager for OG-RAG knowledge graph operations.
    """
    
    def __init__(self, 
                 uri: str = None, 
                 user: str = None, 
                 password: str = None,
                 database: str = "neo4j"):
        """
        Initialize Neo4j connection.
        
        Args:
            uri: Neo4j URI (default: bolt://localhost:7687)
            user: Username (default: from environment or 'neo4j')
            password: Password (default: from environment)
            database: Database name (default: 'neo4j')
        """
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = user or os.getenv('NEO4J_USER', 'neo4j')
        self.password = password or os.getenv('NEO4J_PASSWORD', 'ograg2025')
        self.database = database
        
        self.driver = None
        self.connect()
    
    def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            # Test connection
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self) -> None:
        """Close database connection."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    @contextmanager
    def session(self):
        """Context manager for Neo4j sessions."""
        session = self.driver.session(database=self.database)
        try:
            yield session
        finally:
            session.close()
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict]:
        """
        Execute a Cypher query and return results.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records as dictionaries
        """
        with self.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def execute_write(self, query: str, parameters: Dict[str, Any] = None) -> None:
        """
        Execute a write transaction.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
        """
        def write_tx(tx):
            return tx.run(query, parameters or {})
        
        with self.session() as session:
            session.execute_write(write_tx)
    
    def execute_batch(self, queries: List[str], parameters_list: List[Dict] = None) -> None:
        """
        Execute multiple queries in a single transaction.
        
        Args:
            queries: List of Cypher queries
            parameters_list: List of parameter dictionaries for each query
        """
        if parameters_list is None:
            parameters_list = [{}] * len(queries)
        
        def batch_tx(tx):
            for query, params in zip(queries, parameters_list):
                tx.run(query, params)
        
        with self.session() as session:
            session.execute_write(batch_tx)
    
    def create_indexes(self) -> None:
        """Create necessary indexes for performance optimization."""
        index_queries = [
            "CREATE INDEX proverb_text_index IF NOT EXISTS FOR (p:Proverb) ON (p.text)",
            "CREATE INDEX concept_name_index IF NOT EXISTS FOR (c:Concept) ON (c.name)",
            "CREATE INDEX culture_name_index IF NOT EXISTS FOR (c:Culture) ON (c.name)",
            "CREATE INDEX language_code_index IF NOT EXISTS FOR (l:Language) ON (l.code)",
        ]
        
        for query in index_queries:
            try:
                self.execute_write(query)
                logger.info(f"Created index: {query}")
            except Exception as e:
                logger.warning(f"Index creation failed: {e}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats_query = """
        MATCH (n)
        RETURN 
            labels(n) as labels,
            count(n) as count
        """
        
        results = self.execute_query(stats_query)
        stats = {}
        
        for record in results:
            label = record['labels'][0] if record['labels'] else 'Unknown'
            stats[label] = record['count']
        
        return stats
    
    def health_check(self) -> bool:
        """Perform database health check."""
        try:
            result = self.execute_query("RETURN 'healthy' as status")
            return len(result) > 0 and result[0]['status'] == 'healthy'
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

# Global connection instance
_connection = None

def get_connection() -> Neo4jConnection:
    """Get or create global Neo4j connection."""
    global _connection
    if _connection is None:
        _connection = Neo4jConnection()
    return _connection

def close_connection() -> None:
    """Close global connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None

# Example usage
if __name__ == "__main__":
    # Test connection
    db = Neo4jConnection()
    
    # Test query
    results = db.execute_query("MATCH (n) RETURN count(n) as total_nodes")
    print(f"Total nodes in database: {results[0]['total_nodes']}")
    
    # Health check
    if db.health_check():
        print("Database is healthy")
    
    # Get stats
    stats = db.get_database_stats()
    print("Database statistics:", stats)
    
    db.close()
