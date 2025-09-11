#!/usr/bin/env python3
"""
thiLLMo Complete Setup Script - Culturally Faithful Kikuyu OG-RAG System

Orchestrates the entire thiLLMo system setup process for culturally faithful
Kikuyu proverb translation using Ontology-Grounded RAG:

1. Environment verification and Neo4j connection
2. Rich ontological structure creation with Kikuyu cultural concepts
3. Dynamic proverb data loading with cultural validation
4. OG-RAG optimization for translation tasks
5. System verification and cultural knowledge testing

This script implements the complete pipeline for the thiLLMo research project
focusing on preserving Kikuyu cultural heritage through AI translation.

Usage: 
    python scripts/thiLLMo_setup.py
    python scripts/thiLLMo_setup.py --skip-confirmation
    python scripts/thiLLMo_setup.py --test-data-only

Project: thiLLMo - OPIT RAI9001 Research Project
Authors: See AUTHORS.md in project root
Institution: Open Institute of Technology (OPIT)
License: MIT (see LICENSE)
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add src to path for thiLLMo imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

try:
    from ontology.kikuyu_proverb_ontology import IntegratedKikuyuOntology
    from data_loading.proverb_loader import WealthEntrepreneurshipProverbLoader
    from decouple import Config
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Please ensure you're running from the project root and dependencies are installed:")
    print("   pip install -r requirements.txt")
    print("   pip install neo4j pandas python-decouple")
    sys.exit(1)

# Configure logging for thiLLMo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - thiLLMo - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def verify_environment() -> bool:
    """Verify thiLLMo environment configuration."""
    print("⚙️ Verifying thiLLMo environment...")
    
    # Check .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ .env file not found")
        print("💡 Please create .env file with Neo4j configuration")
        return False
    
    # Check essential directories
    essential_dirs = [
        "src/ontology",
        "src/data_loading",
        "data/proverbs",
        "data/processed"
    ]
    
    for dir_path in essential_dirs:
        if not (project_root / dir_path).exists():
            print(f"❌ Missing directory: {dir_path}")
            return False
    
    print("✅ Environment verified")
    return True


def test_neo4j_connection() -> bool:
    """Test connection to Neo4j database."""
    print("🔌 Testing Neo4j connection...")
    
    try:
        # Create temporary ontology instance to test connection
        ontology = IntegratedKikuyuOntology()
        
        # Test basic query
        with ontology.driver.session() as session:
            result = session.run("RETURN 'thiLLMo connection test' as message")
            message = result.single()['message']
        
        ontology.close()
        print(f"✅ Neo4j connection successful: {message}")
        return True
        
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        print("💡 Troubleshooting:")
        print("   • Start Neo4j: docker-compose up -d neo4j")
        print("   • Check credentials in .env file")
        print("   • Verify Neo4j is running: docker-compose ps")
        return False


def main():
    """Run the complete thiLLMo OG-RAG system setup."""
    parser = argparse.ArgumentParser(
        description="thiLLMo Complete Setup - Culturally Faithful Kikuyu Translation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--skip-confirmation', 
        action='store_true',
        help='Skip interactive confirmations'
    )
    
    parser.add_argument(
        '--test-data-only',
        action='store_true',
        help='Use minimal test data only'
    )
    
    args = parser.parse_args()
    
    print("🚀 thiLLMo Complete Setup - Culturally Faithful Kikuyu Translation")
    print("=" * 70)
    print("Ontology-Grounded RAG for Cultural Preservation")
    print()
    print("This will create:")
    print("• 🏛️ Rich Kikuyu cultural and linguistic ontology")
    print("• 📚 Dynamic proverb loading with cultural validation")
    print("• 🔍 OG-RAG optimized knowledge graph")
    print("• 🌐 Full-text search for cultural concepts")
    print("• 🔗 Semantic relationship mapping")
    print("• ✅ Cultural authenticity verification")
    print()
    
    start_time = time.time()
    
    try:
        # Pre-flight checks
        print("📋 Pre-flight Checks")
        print("-" * 20)
        
        if not verify_environment():
            sys.exit(1)
            
        if not test_neo4j_connection():
            sys.exit(1)
        
        # Initialize thiLLMo ontology
        print("\n🏗️ Initializing thiLLMo Ontology...")
        ontology = IntegratedKikuyuOntology()
        
        # Safety confirmation
        if not args.skip_confirmation:
            response = input("\nProceed with complete thiLLMo setup? This will clear existing data. (y/N): ")
            if response.lower() != 'y':
                print("Setup cancelled.")
                return
        
        # Phase 1: Database preparation
        print("\n🔧 Phase 1: Database Preparation")
        print("-" * 35)
        print("   Clearing existing data...")
        ontology.clear_database()
        
        print("   Creating database constraints...")
        ontology.create_comprehensive_constraints()
        
        print("   Creating performance indexes...")
        ontology.create_comprehensive_indexes()
        
        # Phase 2: Ontological structure creation
        print("\n🏛️ Phase 2: Cultural Ontology Creation")
        print("-" * 40)
        print("   Building Kikuyu cultural framework...")
        ontology.setup_complete_ontology()
        
        # Phase 3: Cultural data loading
        print("\n📚 Phase 3: Cultural Data Integration")
        print("-" * 38)
        
        proverb_loader = WealthEntrepreneurshipProverbLoader()
        
        # Check for existing data or create test data
        data_dir = Path("data/proverbs")
        existing_files = list(data_dir.glob("*.csv"))
        
        if existing_files and not args.test_data_only:
            print(f"   Found {len(existing_files)} data files")
            for file_path in existing_files[:3]:  # Show first 3
                print(f"   📄 {file_path.name}")
            if len(existing_files) > 3:
                print(f"   ... and {len(existing_files) - 3} more files")
            
            # Use first available file
            proverbs = proverb_loader.load_and_process_proverbs(existing_files[0])
        else:
            print("   Creating minimal Kikuyu test data...")
            csv_file, json_file = proverb_loader.create_minimal_test_data()
            proverbs = proverb_loader.load_and_process_proverbs(csv_file)
        
        print(f"   ✅ Loaded {len(proverbs)} culturally validated proverbs")
        
        # Phase 4: System verification
        print("\n🧪 Phase 4: System Verification")
        print("-" * 32)
        print("   Running comprehensive checks...")
        stats = ontology.verify_integrated_setup()
        
        # Test cultural search capabilities
        with ontology.driver.session() as session:
            # Test Kikuyu content search
            search_result = session.run("""
                CALL db.index.fulltext.queryNodes('proverb_content_fulltext', 'wira business') 
                YIELD node 
                RETURN count(node) as kikuyu_search_results
            """)
            kikuyu_results = search_result.single()['kikuyu_search_results']
            
            # Test cultural concept connections
            concept_result = session.run("""
                MATCH (p:Proverb)-[:EMBODIES]->(c:CulturalConcept)
                RETURN count(DISTINCT c) as cultural_concepts
            """)
            cultural_concepts = concept_result.single()['cultural_concepts']
        
        # Success summary
        setup_time = time.time() - start_time
        
        print("\n" + "🎉 " + "="*65 + " 🎉")
        print("thiLLMo SETUP COMPLETE - READY FOR CULTURAL TRANSLATION!")
        print("="*71)
        
        print(f"\n📊 thiLLMo Knowledge Graph Statistics:")
        print(f"   • Cultural nodes: {stats['total_nodes']:,}")
        print(f"   • Semantic relationships: {stats['total_relationships']:,}")
        print(f"   • Kikuyu proverbs: {len(proverbs)}")
        print(f"   • Searchable content: {kikuyu_results}")
        print(f"   • Cultural concepts: {cultural_concepts}")
        print(f"   • Database constraints: {stats['constraints']}")
        print(f"   • Performance indexes: {stats['indexes']}")
        print(f"   • Setup time: {setup_time:.1f} seconds")
        
        print(f"\n🌐 Access your thiLLMo system:")
        print(f"   • Neo4j Browser: http://localhost:7474")
        print(f"   • Login: neo4j / ograg2025")
        print(f"   • Jupyter Lab: http://localhost:8888 (token: ograg2025)")
        
        print(f"\n🧪 Test your cultural translation system:")
        print(f"   • Query Kikuyu knowledge: python scripts/test_kikuyu_search.py")
        print(f"   • Add proverbs: Edit data/proverbs/*.csv")
        print(f"   • Cultural validation: python scripts/validate_cultural_data.py")
        
        print(f"\n📚 Research development:")
        print(f"   • Jupyter notebooks ready for thiLLMo experiments")
        print(f"   • OG-RAG pipeline ready for translation tasks")
        print(f"   • Cultural knowledge graph ready for exploration")
        
        print(f"\n🏛️ thiLLMo: Preserving Kikuyu culture through AI! 🇰🇪")
        
    except KeyboardInterrupt:
        print("\n⏹️ Setup interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ thiLLMo setup failed: {e}")
        print(f"\n💡 Troubleshooting thiLLMo:")
        print(f"   • Check Docker services: docker-compose ps")
        print(f"   • Verify .env configuration")
        print(f"   • Check Neo4j status: docker-compose logs neo4j")
        print(f"   • Ensure all dependencies installed: pip install -r requirements.txt")
        print(f"   • Contact supervisor: Marzieh Bakhshandeh")
        sys.exit(1)
        
    finally:
        try:
            ontology.close()
        except:
            pass


if __name__ == "__main__":
    main()
