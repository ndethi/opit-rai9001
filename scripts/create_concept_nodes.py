#!/usr/bin/env python3
"""
Create Cultural Concept Nodes in Neo4j
=======================================
Phase 5 of Day 1: Foundation Setup

Creates 20 priority cultural concept nodes from the extracted
priority concepts list. These become the foundational nodes
for linking proverbs to cultural meanings.

Input:  data/processed/priority_concepts.csv
Output: 20 CulturalConcept nodes in Neo4j AuraDB
"""

import csv
from pathlib import Path
from datetime import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

def create_concept_nodes(csv_file: Path):
    """Create CulturalConcept nodes from priority concepts CSV."""
    
    print("="*70)
    print("CULTURAL CONCEPT NODE CREATION")
    print("="*70)
    print(f"\n📖 Source: {csv_file}")
    print(f"🎯 Target: Neo4j AuraDB\n")
    
    # Load environment
    project_root = Path(__file__).parent.parent
    load_dotenv(project_root / '.env')
    
    uri = os.getenv('NEO4J_URI')
    username = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    
    print(f"🔗 Connecting to: {uri}")
    print(f"👤 User: {username}\n")
    
    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    # Read concepts from CSV
    concepts = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            concept_data = {
                'concept_name': row['concept_name'],
                'priority': int(row['priority']),
                'failure_count': int(row['failure_count']),
                'importance_score': float(row['importance_score']),
                'domain': row['domain'],
                'critical_failures': int(row['critical_failures']),
                'high_failures': int(row['high_failures']),
                'medium_failures': int(row['medium_failures']),
                'failed_metaphors_count': int(row['failed_metaphors_count']),
                'lost_meanings_count': int(row['lost_meanings_count']),
                'example_proverbs': row['example_proverbs'].split(','),
                'created_date': datetime.now().isoformat(),
                'source': 'baseline_gap_analysis'
            }
            concepts.append(concept_data)
    
    print(f"📊 Loaded {len(concepts)} priority concepts from CSV")
    print(f"📈 Importance score range: {min(c['importance_score'] for c in concepts):.2f} - {max(c['importance_score'] for c in concepts):.2f}")
    print(f"🏆 Top concept: {concepts[0]['concept_name']} (priority 1, score {concepts[0]['importance_score']:.2f})\n")
    
    # Create concepts
    print("🚀 Creating CulturalConcept nodes...")
    print("-" * 70)
    
    with driver.session() as session:
        result = session.run("""
            UNWIND $concepts AS concept
            CREATE (c:CulturalConcept {
                concept_name: concept.concept_name,
                priority: concept.priority,
                failure_count: concept.failure_count,
                importance_score: concept.importance_score,
                domain: concept.domain,
                critical_failures: concept.critical_failures,
                high_failures: concept.high_failures,
                medium_failures: concept.medium_failures,
                failed_metaphors_count: concept.failed_metaphors_count,
                lost_meanings_count: concept.lost_meanings_count,
                example_proverbs: concept.example_proverbs,
                created_date: concept.created_date,
                source: concept.source
            })
            RETURN count(c) as created
        """, concepts=concepts)
        
        created = result.single()['created']
        print(f"   ✅ Created {created} CulturalConcept nodes")
    
    print("-" * 70)
    print(f"\n✅ Successfully created {created} concept nodes!\n")
    
    # Verify creation
    print("🔍 Verifying concept creation...")
    with driver.session() as session:
        result = session.run("""
            MATCH (c:CulturalConcept)
            RETURN 
                count(c) as total,
                avg(c.importance_score) as avg_score,
                collect(DISTINCT c.domain) as domains
        """)
        
        stats = result.single()
        print(f"   Total concepts: {stats['total']}")
        print(f"   Average importance score: {stats['avg_score']:.2f}")
        print(f"   Domains: {', '.join(stats['domains'])}")
    
    # Show priority concepts
    print(f"\n📝 Top 10 priority concepts:")
    with driver.session() as session:
        result = session.run("""
            MATCH (c:CulturalConcept)
            RETURN c.priority, c.concept_name, c.importance_score, c.domain
            ORDER BY c.priority ASC
            LIMIT 10
        """)
        
        for record in result:
            print(f"   {record['c.priority']:>2}. {record['c.concept_name']:<25} "
                  f"(score: {record['c.importance_score']:>5.1f}, domain: {record['c.domain']})")
    
    driver.close()
    
    print("\n" + "="*70)
    print("✅ CONCEPT NODE CREATION COMPLETE!")
    print("="*70)
    print(f"\n📝 Next steps:")
    print(f"   1. Proceed to Phase 6: Link proverbs to concepts")
    print(f"   2. Validate graph structure and relationships\n")


if __name__ == '__main__':
    # File paths
    project_root = Path(__file__).parent.parent
    csv_file = project_root / 'data/processed/priority_concepts.csv'
    
    # Create concept nodes
    create_concept_nodes(csv_file)
