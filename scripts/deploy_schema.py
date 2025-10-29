#!/usr/bin/env python3
"""
Deploy Enhanced Neo4j Schema to AuraDB

This script deploys the comprehensive ontology schema to the configured Neo4j instance.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / '.env')

# Import directly to avoid package init issues
import importlib.util
spec = importlib.util.spec_from_file_location(
    "enhanced_neo4j_schema",
    project_root / "src/ontology/enhanced_neo4j_schema.py"
)
enhanced_schema_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(enhanced_schema_module)
EnhancedOntologySchema = enhanced_schema_module.EnhancedOntologySchema

def main():
    """Deploy schema to Neo4j"""
    
    # Get configuration from environment
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    username = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD')
    
    if not password:
        print("❌ Error: NEO4J_PASSWORD not found in .env file")
        return False
    
    print("=" * 70)
    print("ENHANCED SCHEMA DEPLOYMENT")
    print("=" * 70)
    print(f"\n🔗 Target Database: {uri}")
    print(f"👤 Username: {username}")
    print()
    
    try:
        # Initialize schema builder
        schema = EnhancedOntologySchema(
            uri=uri,
            user=username,
            password=password
        )
        
        # Deploy complete schema
        print("🚀 Deploying enhanced schema...")
        schema.create_complete_schema()
        
        # Close connection
        schema.close()
        
        print("\n" + "=" * 70)
        print("✅ SCHEMA DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        print("\n📝 Next steps:")
        print("   1. Extract priority concepts from gap analysis")
        print("   2. Populate proverb nodes (100 Ireri proverbs)")
        print("   3. Create concept nodes")
        print("   4. Link proverbs to concepts")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Schema deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
