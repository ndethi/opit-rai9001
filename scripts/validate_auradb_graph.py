#!/usr/bin/env python3
"""
Validate AuraDB Knowledge Graph Structure

Quick validation script to verify reconstituted graph matches thesis specifications.

Usage:
    python scripts/validate_auradb_graph.py

Expected Output:
    ✅ All checks pass if graph matches thesis Chapter 4 specification
"""

import os
import sys
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / '.env')


class GraphValidator:
    """Validate reconstituted Neo4j graph against thesis specifications."""
    
    def __init__(self, uri: str, username: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.issues = []
        self.warnings = []
    
    def close(self):
        self.driver.close()
    
    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("="*70)
        print("AURADB KNOWLEDGE GRAPH VALIDATION")
        print("Thesis Chapter 4 Compliance Check")
        print("="*70)
        
        checks = [
            ("Connection", self.check_connection),
            ("Node Counts", self.check_node_counts),
            ("Relationship Counts", self.check_relationship_counts),
            ("Schema Constraints", self.check_constraints),
            ("Schema Indexes", self.check_indexes),
            ("Proverb Completeness", self.check_proverb_completeness),
            ("Cultural Weights", self.check_cultural_weights),
            ("Graph Connectivity", self.check_connectivity),
        ]
        
        print()
        for name, check_func in checks:
            print(f"🔍 Checking {name}...")
            try:
                check_func()
                print(f"   ✅ PASS\n")
            except AssertionError as e:
                print(f"   ❌ FAIL: {e}\n")
                self.issues.append(f"{name}: {e}")
            except Exception as e:
                print(f"   ⚠️  ERROR: {e}\n")
                self.warnings.append(f"{name}: {e}")
        
        # Print summary
        print("="*70)
        if not self.issues and not self.warnings:
            print("✅ ALL VALIDATION CHECKS PASSED!")
            print("="*70)
            print("\n🎯 Graph is thesis-compliant and ready for OG-RAG queries.\n")
            return True
        else:
            print("⚠️  VALIDATION ISSUES FOUND")
            print("="*70)
            
            if self.issues:
                print(f"\n❌ {len(self.issues)} Critical Issues:")
                for issue in self.issues:
                    print(f"   • {issue}")
            
            if self.warnings:
                print(f"\n⚠️  {len(self.warnings)} Warnings:")
                for warning in self.warnings:
                    print(f"   • {warning}")
            
            print("\n📖 Review docs/setup/AURADB_RECONSTITUTION_GUIDE.md for troubleshooting.\n")
            return False
    
    def check_connection(self):
        """Test database connection."""
        with self.driver.session() as session:
            result = session.run("RETURN 1 as test")
            assert result.single()['test'] == 1
    
    def check_node_counts(self):
        """Validate node counts match thesis ranges."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
            """)
            
            counts = {record['label']: record['count'] for record in result}
            
            # Expected ranges from thesis
            expected = {
                'Proverb': (100, 100),  # Exact
                'CulturalConcept': (50, 900),  # Variable based on extraction
                'UsageContext': (5, 50),
                'MoralLesson': (5, 50)
            }
            
            for label, (min_count, max_count) in expected.items():
                actual = counts.get(label, 0)
                assert min_count <= actual <= max_count, \
                    f"{label} count {actual} outside expected range [{min_count}, {max_count}]"
                print(f"      {label}: {actual} (expected {min_count}-{max_count})")
    
    def check_relationship_counts(self):
        """Validate relationship counts."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
            """)
            
            counts = {record['rel_type']: record['count'] for record in result}
            
            # Expected relationship types from thesis
            expected_types = [
                'EXPRESSES_CONCEPT',
                'TEACHES_LESSON',
                'USED_IN',
                'RELATES_TO',
                'SUBSUMES'
            ]
            
            for rel_type in expected_types:
                actual = counts.get(rel_type, 0)
                assert actual > 0, f"Missing {rel_type} relationships"
                print(f"      {rel_type}: {actual}")
            
            total = sum(counts.values())
            assert total >= 500, f"Total relationships {total} too low (expected >500)"
    
    def check_constraints(self):
        """Validate uniqueness constraints exist."""
        with self.driver.session() as session:
            result = session.run("SHOW CONSTRAINTS")
            constraints = [record['name'] for record in result]
            
            # Expected constraints
            expected = ['proverb_id', 'concept_name', 'context_id', 'moral_id']
            
            for constraint_name in expected:
                # Check if any constraint contains the expected name
                found = any(constraint_name in c for c in constraints)
                assert found, f"Missing constraint for {constraint_name}"
                print(f"      ✅ {constraint_name}")
    
    def check_indexes(self):
        """Validate property indexes exist."""
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            indexes = [record for record in result]
            
            # Should have multiple indexes
            assert len(indexes) >= 4, f"Expected >=4 indexes, found {len(indexes)}"
            print(f"      Found {len(indexes)} indexes")
    
    def check_proverb_completeness(self):
        """Validate all proverbs have required fields."""
        with self.driver.session() as session:
            # Check for missing required fields
            result = session.run("""
                MATCH (p:Proverb)
                WHERE p.proverb_id IS NULL 
                   OR p.kikuyu_text IS NULL 
                   OR p.expert_translation IS NULL
                   OR p.cultural_weight IS NULL
                RETURN count(p) as incomplete
            """)
            
            incomplete = result.single()['incomplete']
            assert incomplete == 0, f"{incomplete} proverbs missing required fields"
            
            # Check cultural weight range
            result = session.run("""
                MATCH (p:Proverb)
                RETURN min(p.cultural_weight) as min_weight,
                       max(p.cultural_weight) as max_weight,
                       avg(p.cultural_weight) as avg_weight
            """)
            
            stats = result.single()
            min_w = stats['min_weight']
            max_w = stats['max_weight']
            avg_w = stats['avg_weight']
            
            assert 0.0 <= min_w <= 1.0, f"Min weight {min_w} out of range [0.0, 1.0]"
            assert 0.0 <= max_w <= 1.0, f"Max weight {max_w} out of range [0.0, 1.0]"
            assert 0.3 <= avg_w <= 0.9, f"Avg weight {avg_w} unexpected (expected 0.3-0.9)"
            
            print(f"      Weight range: {min_w:.3f} - {max_w:.3f} (avg: {avg_w:.3f})")
    
    def check_cultural_weights(self):
        """Validate cultural weights are properly normalized."""
        with self.driver.session() as session:
            # Check concepts have cultural weights
            result = session.run("""
                MATCH (c:CulturalConcept)
                WHERE c.cultural_weight IS NULL
                RETURN count(c) as missing_weight
            """)
            
            missing = result.single()['missing_weight']
            assert missing == 0, f"{missing} concepts missing cultural_weight"
            
            # Check EXPRESSES_CONCEPT has salience scores
            result = session.run("""
                MATCH ()-[r:EXPRESSES_CONCEPT]->()
                WHERE r.salience IS NULL
                RETURN count(r) as missing_salience
            """)
            
            missing = result.single()['missing_salience']
            assert missing == 0, f"{missing} EXPRESSES_CONCEPT edges missing salience"
            
            print(f"      All cultural weights present")
    
    def check_connectivity(self):
        """Validate graph is well-connected (no isolated components)."""
        with self.driver.session() as session:
            # Check for orphan proverbs (no outgoing relationships)
            result = session.run("""
                MATCH (p:Proverb)
                WHERE NOT (p)-->()
                RETURN count(p) as orphan_proverbs
            """)
            
            orphans = result.single()['orphan_proverbs']
            assert orphans == 0, f"{orphans} proverbs have no relationships"
            
            # Check proverb-concept connectivity
            result = session.run("""
                MATCH (p:Proverb)-[:EXPRESSES_CONCEPT]->(c:CulturalConcept)
                WITH p, count(c) as concept_count
                RETURN avg(concept_count) as avg_concepts_per_proverb
            """)
            
            avg_concepts = result.single()['avg_concepts_per_proverb']
            assert avg_concepts >= 2, \
                f"Avg concepts per proverb {avg_concepts:.1f} too low (expected >=2)"
            
            print(f"      Avg concepts per proverb: {avg_concepts:.1f}")


def main():
    """Run validation."""
    
    # Get credentials
    uri = os.getenv('NEO4J_URI')
    username = os.getenv('NEO4J_USER', os.getenv('NEO4J_USERNAME', 'neo4j'))
    password = os.getenv('NEO4J_PASSWORD')
    
    if not all([uri, password]):
        print("❌ ERROR: Missing Neo4j credentials in .env file")
        print("\n   Required: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD")
        return False
    
    print(f"\n🔗 Connecting to: {uri}")
    print(f"👤 Username: {username}\n")
    
    # Run validation
    validator = GraphValidator(uri, username, password)
    
    try:
        success = validator.validate_all()
        return success
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        validator.close()


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
