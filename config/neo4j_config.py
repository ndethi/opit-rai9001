"""Neo4j Configuration for Kikuyu Proverbs Ontology.

This module provides configuration settings for connecting to the Neo4j database
that stores the comprehensive Kikuyu proverbs ontology for OG-RAG systems.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()

class Neo4jConfig:
    """Configuration management for Neo4j connections."""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        'uri': 'bolt://localhost:7687',
        'username': 'neo4j',
        'password': 'kikuyu_proverbs_2024',
        'database': 'neo4j',
        'max_connection_lifetime': 3600,
        'max_connection_pool_size': 50,
        'connection_acquisition_timeout': 60,
        'connection_timeout': 30,
        'max_retry_time': 30,
        'resolver_function': None
    }
    
    @classmethod
    def get_config(cls, environment: str = 'development') -> Dict[str, any]:
        """Get Neo4j configuration for specified environment.
        
        Args:
            environment: Environment name ('development', 'production', 'testing')
            
        Returns:
            Dictionary containing Neo4j connection configuration
        """
        
        config = cls.DEFAULT_CONFIG.copy()
        
        # Environment-specific overrides
        if environment == 'development':
            config.update({
                'uri': os.getenv('NEO4J_DEV_URI', config['uri']),
                'username': os.getenv('NEO4J_DEV_USERNAME', config['username']),
                'password': os.getenv('NEO4J_DEV_PASSWORD', config['password']),
                'database': os.getenv('NEO4J_DEV_DATABASE', config['database'])
            })
        elif environment == 'production':
            config.update({
                'uri': os.getenv('NEO4J_PROD_URI', config['uri']),
                'username': os.getenv('NEO4J_PROD_USERNAME', config['username']),
                'password': os.getenv('NEO4J_PROD_PASSWORD', config['password']),
                'database': os.getenv('NEO4J_PROD_DATABASE', config['database']),
                'max_connection_pool_size': 100,
                'connection_timeout': 60
            })
        elif environment == 'testing':
            config.update({
                'uri': os.getenv('NEO4J_TEST_URI', 'bolt://localhost:7688'),
                'username': os.getenv('NEO4J_TEST_USERNAME', 'neo4j'),
                'password': os.getenv('NEO4J_TEST_PASSWORD', 'test_password'),
                'database': os.getenv('NEO4J_TEST_DATABASE', 'test_kikuyu_proverbs'),
                'max_connection_pool_size': 10
            })
        
        # General environment variable overrides
        config.update({
            'uri': os.getenv('NEO4J_URI', config['uri']),
            'username': os.getenv('NEO4J_USERNAME', config['username']),
            'password': os.getenv('NEO4J_PASSWORD', config['password']),
            'database': os.getenv('NEO4J_DATABASE', config['database'])
        })
        
        return config
    
    @classmethod
    def validate_config(cls, config: Dict) -> bool:
        """Validate Neo4j configuration parameters.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            True if configuration is valid, False otherwise
        """
        
        required_fields = ['uri', 'username', 'password', 'database']
        
        for field in required_fields:
            if not config.get(field):
                print(f"❌ Missing required Neo4j configuration: {field}")
                return False
        
        # Validate URI format
        uri = config['uri']
        if not (uri.startswith('bolt://') or uri.startswith('neo4j://') or uri.startswith('neo4j+s://')):
            print(f"❌ Invalid Neo4j URI format: {uri}")
            return False
        
        return True
    
    @classmethod
    def get_docker_compose_config(cls) -> Dict[str, str]:
        """Get configuration for Docker Compose Neo4j setup.
        
        Returns:
            Dictionary with Docker Compose environment variables
        """
        
        return {
            'NEO4J_AUTH': 'neo4j/kikuyu_proverbs_2024',
            'NEO4J_PLUGINS': '["apoc"]',
            'NEO4J_dbms_security_procedures_unrestricted': 'apoc.*',
            'NEO4J_dbms_security_procedures_allowlist': 'apoc.*',
            'NEO4J_apoc_export_file_enabled': 'true',
            'NEO4J_apoc_import_file_enabled': 'true',
            'NEO4J_apoc_import_file_use__neo4j__config': 'true'
        }


# Convenience functions for common configurations
def get_development_config() -> Dict[str, any]:
    """Get development environment Neo4j configuration."""
    return Neo4jConfig.get_config('development')

def get_production_config() -> Dict[str, any]:
    """Get production environment Neo4j configuration.""" 
    return Neo4jConfig.get_config('production')

def get_testing_config() -> Dict[str, any]:
    """Get testing environment Neo4j configuration."""
    return Neo4jConfig.get_config('testing')

def create_env_template() -> str:
    """Create .env file template for Neo4j configuration.
    
    Returns:
        String containing .env template content
    """
    
    template = """
# Neo4j Configuration for Kikuyu Proverbs Ontology
# Copy this file to .env and update with your actual values

# Development Environment
NEO4J_DEV_URI=bolt://localhost:7687
NEO4J_DEV_USERNAME=neo4j
NEO4J_DEV_PASSWORD=kikuyu_proverbs_2024
NEO4J_DEV_DATABASE=neo4j

# Production Environment
NEO4J_PROD_URI=bolt://your-production-server:7687
NEO4J_PROD_USERNAME=neo4j
NEO4J_PROD_PASSWORD=your-secure-production-password
NEO4J_PROD_DATABASE=kikuyu_proverbs_prod

# Testing Environment
NEO4J_TEST_URI=bolt://localhost:7688
NEO4J_TEST_USERNAME=neo4j
NEO4J_TEST_PASSWORD=test_password
NEO4J_TEST_DATABASE=test_kikuyu_proverbs

# General Overrides (will override environment-specific values)
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=your-password
# NEO4J_DATABASE=neo4j
"""
    
    return template.strip()


# Default configurations for easy import
DEV_CONFIG = get_development_config()
PROD_CONFIG = get_production_config()
TEST_CONFIG = get_testing_config()

# Docker setup helper
DOCKER_ENV = Neo4jConfig.get_docker_compose_config()