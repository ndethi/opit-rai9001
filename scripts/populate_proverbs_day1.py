#!/usr/bin/env python3
"""
Populate Proverb Nodes in Neo4j
================================
Phase 4 of Day 1: Foundation Setup

Loads 100 Ireri proverbs (Tier 1 corpus) into Neo4j with:
- Full metadata from expert annotations
- Calculated cultural weights (5.0-10.0 scale)
- Batch processing for efficiency

Input:  data/evaluation/gold_standard_ireri_deduplicated.csv
Output: 100 Proverb nodes in Neo4j AuraDB
"""

import csv
from pathlib import Path
from datetime import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

def calculate_cultural_weight(row: dict) -> float:
    """
    Calculate cultural weight for a proverb (5.0-10.0 scale).
    
    Based on:
    - Cultural authenticity (1-5 scale)
    - Length of cultural meaning (proxy for cultural depth)
    - Business relevance (length of business relevance text)
    """
    
    # Cultural authenticity (already 1-5, scale to 2-4 points)
    try:
        authenticity = float(row.get('cultural_authenticity', '3.0'))
    except (ValueError, TypeError):
        authenticity = 3.0
    authenticity_score = (authenticity / 5.0) * 4.0  # Max 4 points
    
    # Cultural depth (based on meaning length)
    meaning = row.get('expert_cultural_meaning', '')
    depth_score = min(len(meaning) / 50.0, 3.0)  # Max 3 points, 1 point per 50 chars
    
    # Business relevance (based on text length - proxy for depth)
    business_text = row.get('expert_business_relevance', '')
    business_score = min(len(business_text) / 100.0, 3.0)  # Max 3 points, 1 point per 100 chars
    
    # Total: 5.0 (base) + up to 10.0 points
    total_weight = 5.0 + authenticity_score + depth_score + business_score
    
    # Cap at 10.0
    return min(round(total_weight, 2), 10.0)


def load_proverbs_to_neo4j(csv_file: Path, batch_size: int = 10):
    """Load proverbs from CSV into Neo4j."""
    
    print("="*70)
    print("PROVERB NODE POPULATION")
    print("="*70)
    print(f"\n📖 Source: {csv_file}")
    print(f"📦 Batch size: {batch_size}")
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
    
    # Read proverbs from CSV
    proverbs = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Calculate cultural weight
            cultural_weight = calculate_cultural_weight(row)
            
            try:
                cultural_auth = float(row.get('cultural_authenticity', '3.0'))
            except (ValueError, TypeError):
                cultural_auth = 3.0
            
            proverb_data = {
                'proverb_id': row['proverb_id'],
                'kikuyu_text': row['kikuyu_text'],
                'expert_translation': row['expert_translation'],
                'expert_cultural_meaning': row['expert_cultural_meaning'],
                'expert_business_relevance': row.get('expert_business_relevance', ''),
                'thematic_category': row['thematic_category'],
                'cultural_authenticity': cultural_auth,
                'cultural_weight': cultural_weight,
                'domain': 'wealth_prosperity',  # Tier 1 domain
                'source': 'ireri_expert',
                'validation_status': 'validated',
                'created_date': datetime.now().isoformat(),
                'tier': 1
            }
            proverbs.append(proverb_data)
    
    print(f"📊 Loaded {len(proverbs)} proverbs from CSV")
    print(f"📈 Cultural weight range: {min(p['cultural_weight'] for p in proverbs):.2f} - {max(p['cultural_weight'] for p in proverbs):.2f}")
    print(f"📈 Average cultural weight: {sum(p['cultural_weight'] for p in proverbs) / len(proverbs):.2f}\n")
    
    # Create proverbs in batches
    print("🚀 Creating Proverb nodes...")
    print("-" * 70)
    
    with driver.session() as session:
        total_created = 0
        
        for i in range(0, len(proverbs), batch_size):
            batch = proverbs[i:i+batch_size]
            
            # Create batch
            result = session.run("""
                UNWIND $proverbs AS proverb
                CREATE (p:Proverb {
                    proverb_id: proverb.proverb_id,
                    kikuyu_text: proverb.kikuyu_text,
                    expert_translation: proverb.expert_translation,
                    expert_cultural_meaning: proverb.expert_cultural_meaning,
                    expert_business_relevance: proverb.expert_business_relevance,
                    thematic_category: proverb.thematic_category,
                    cultural_authenticity: proverb.cultural_authenticity,
                    cultural_weight: proverb.cultural_weight,
                    domain: proverb.domain,
                    source: proverb.source,
                    validation_status: proverb.validation_status,
                    created_date: proverb.created_date,
                    tier: proverb.tier
                })
                RETURN count(p) as created
            """, proverbs=batch)
            
            created = result.single()['created']
            total_created += created
            
            print(f"   ✅ Batch {(i//batch_size)+1}: Created {created} proverbs (IDs: {batch[0]['proverb_id']} - {batch[-1]['proverb_id']})")
    
    print("-" * 70)
    print(f"\n✅ Successfully created {total_created} Proverb nodes!\n")
    
    # Verify creation
    print("🔍 Verifying proverb creation...")
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Proverb)
            RETURN 
                count(p) as total,
                avg(p.cultural_weight) as avg_weight,
                min(p.cultural_weight) as min_weight,
                max(p.cultural_weight) as max_weight,
                collect(DISTINCT p.domain)[0..3] as sample_domains
        """)
        
        stats = result.single()
        print(f"   Total proverbs: {stats['total']}")
        print(f"   Average cultural weight: {stats['avg_weight']:.2f}")
        print(f"   Weight range: {stats['min_weight']:.2f} - {stats['max_weight']:.2f}")
        print(f"   Sample domains: {', '.join(stats['sample_domains'])}")
    
    # Sample proverbs
    print(f"\n📝 Sample proverbs:")
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Proverb)
            RETURN p.proverb_id, p.kikuyu_text, p.cultural_weight
            ORDER BY p.cultural_weight DESC
            LIMIT 3
        """)
        
        for i, record in enumerate(result, 1):
            print(f"   {i}. {record['p.proverb_id']}: {record['p.kikuyu_text'][:50]}... (weight: {record['p.cultural_weight']})")
    
    driver.close()
    
    print("\n" + "="*70)
    print("✅ PROVERB POPULATION COMPLETE!")
    print("="*70)
    print(f"\n📝 Next steps:")
    print(f"   1. Proceed to Phase 5: Create concept nodes")
    print(f"   2. Proceed to Phase 6: Link proverbs to concepts\n")


if __name__ == '__main__':
    # File paths
    project_root = Path(__file__).parent.parent
    csv_file = project_root / 'data/evaluation/gold_standard_ireri_deduplicated.csv'
    
    # Load proverbs
    load_proverbs_to_neo4j(csv_file, batch_size=10)
