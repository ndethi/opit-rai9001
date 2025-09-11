#!/usr/bin/env python3
"""
thiLLMo System Test Script

Quick verification tests for the thiLLMo cultural translation system.
Run this after setup to ensure everything is working correctly.

Usage: python scripts/test_thiLLMo_system.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from neo4j import GraphDatabase
    from decouple import Config
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Install with: pip install neo4j python-decouple")
    sys.exit(1)

def test_neo4j_connection():
    """Test basic Neo4j connection."""
    print("🔌 Testing Neo4j connection...")
    
    config = Config()
    uri = config('NEO4J_URI', default='bolt://localhost:7687')
    user = config('NEO4J_USER', default='neo4j')
    password = config('NEO4J_PASSWORD', default='ograg2025')
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 'thiLLMo test' as message")
            message = result.single()['message']
        driver.close()
        print(f"✅ Connection successful: {message}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_cultural_data():
    """Test if cultural data is loaded."""
    print("📚 Testing cultural data...")
    
    config = Config()
    uri = config('NEO4J_URI', default='bolt://localhost:7687')
    user = config('NEO4J_USER', default='neo4j')
    password = config('NEO4J_PASSWORD', default='ograg2025')
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            # Count proverbs
            result = session.run("MATCH (p:Proverb) RETURN count(p) as proverb_count")
            proverb_count = result.single()['proverb_count']
            
            # Count cultural concepts
            result = session.run("MATCH (c:CulturalConcept) RETURN count(c) as concept_count")
            concept_count = result.single()['concept_count']
            
            # Test search capability
            result = session.run("""
                CALL db.index.fulltext.queryNodes('proverb_content_fulltext', 'wira') 
                YIELD node 
                RETURN count(node) as search_results
            """)
            search_results = result.single()['search_results']
            
        driver.close()
        
        print(f"✅ Found {proverb_count} Kikuyu proverbs")
        print(f"✅ Found {concept_count} cultural concepts")
        print(f"✅ Search functionality: {search_results} results for 'wira'")
        
        return proverb_count > 0 and concept_count > 0
        
    except Exception as e:
        print(f"❌ Cultural data test failed: {e}")
        return False

def test_sample_query():
    """Test a sample cultural query."""
    print("🧪 Testing sample cultural query...")
    
    config = Config()
    uri = config('NEO4J_URI', default='bolt://localhost:7687')
    user = config('NEO4J_USER', default='neo4j')
    password = config('NEO4J_PASSWORD', default='ograg2025')
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            # Find proverbs about work/business
            result = session.run("""
                MATCH (p:Proverb)
                WHERE p.kikuyu_text CONTAINS 'wira' OR p.themes CONTAINS 'business'
                RETURN p.kikuyu_text, p.literal_translation
                LIMIT 3
            """)
            
            proverbs = list(result)
            
        driver.close()
        
        if proverbs:
            print("✅ Sample proverbs found:")
            for i, record in enumerate(proverbs, 1):
                print(f"   {i}. {record['p.kikuyu_text']}")
                print(f"      → {record['p.literal_translation']}")
            return True
        else:
            print("❌ No proverbs found")
            return False
            
    except Exception as e:
        print(f"❌ Sample query failed: {e}")
        return False

def main():
    """Run all thiLLMo system tests."""
    print("🧪 thiLLMo System Tests")
    print("=" * 30)
    print("Testing culturally faithful Kikuyu translation system...\n")
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Connection
    if test_neo4j_connection():
        tests_passed += 1
    print()
    
    # Test 2: Cultural data
    if test_cultural_data():
        tests_passed += 1
    print()
    
    # Test 3: Sample query
    if test_sample_query():
        tests_passed += 1
    print()
    
    # Summary
    print("📊 Test Results")
    print("-" * 15)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! thiLLMo system is ready for cultural translation.")
        print("\n🚀 Next steps:")
        print("   • Explore Neo4j Browser: http://localhost:7474")
        print("   • Start Jupyter Lab: http://localhost:8888")
        print("   • Add your own Kikuyu proverbs to data/proverbs/")
    else:
        print("❌ Some tests failed. Please check your setup.")
        print("\n💡 Troubleshooting:")
        print("   • Run setup again: python scripts/thiLLMo_setup.py")
        print("   • Check Docker: docker-compose ps")
        print("   • Verify .env file configuration")

if __name__ == "__main__":
    main()
