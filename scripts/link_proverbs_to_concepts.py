#!/usr/bin/env python3
"""
Link Proverbs to Cultural Concepts
===================================
Phase 6 of Day 1: Foundation Setup

Creates EXPRESSES_CONCEPT relationships between Proverb and
CulturalConcept nodes using keyword matching on proverb text
and cultural meanings.

Input:  Proverb and CulturalConcept nodes in Neo4j
Output: EXPRESSES_CONCEPT relationships with strength scores
"""

from pathlib import Path
from datetime import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Concept keyword mappings (Kikuyu and English)
CONCEPT_KEYWORDS = {
    'wealth': ['utonga', 'money', 'mbeca', 'rich', 'wealth', 'prosperity', 'riches', 'fortune'],
    'poverty': ['thiini', 'poor', 'poverty', 'lack', 'scarcity', 'destitute', 'needy'],
    'ownership': ['owner', 'possession', 'property', 'belongs', 'owns', 'mine', 'yours'],
    'wealth acquisition': ['acquire', 'gain', 'accumulate', 'gather', 'collect', 'obtain', 'get'],
    'debt': ['debt', 'borrow', 'lend', 'owe', 'loan', 'credit', 'obligation'],
    'greed': ['greed', 'greedy', 'selfish', 'covet', 'envy', 'insatiable', 'hunger'],
    'investment': ['invest', 'plant', 'sow', 'seed', 'capital', 'venture'],
    'impermanence of wealth': ['temporary', 'fleeting', 'transient', 'ephemeral', 'brief', 'short-lived'],
    'wisdom': ['ũũgĩ', 'wisdom', 'wise', 'prudent', 'smart', 'clever', 'intelligent', 'knowledge'],
    'hospitality': ['hospitality', 'welcome', 'guest', 'visitor', 'host', 'generous'],
    'self-reliance': ['self', 'independent', 'reliance', 'oneself', 'alone', 'own'],
    'collaboration': ['together', 'cooperation', 'collaborate', 'unity', 'teamwork', 'joint'],
    'resource management': ['manage', 'steward', 'care', 'preserve', 'maintain', 'husband'],
    'stewardship': ['steward', 'guardian', 'keeper', 'custodian', 'caretaker', 'trustee'],
    'pride': ['pride', 'proud', 'arrogance', 'boast', 'vain', 'ego'],
    'thief': ['thief', 'steal', 'theft', 'rob', 'burglar', 'mũici'],
    'patience': ['patience', 'patient', 'wait', 'endure', 'persevere', 'kĩrĩa'],
    'utonga': ['utonga', 'wealth', 'riches', 'prosperity', 'affluence'],
    'money management': ['manage', 'budget', 'spend', 'save', 'financial', 'economy'],
    'pursuit': ['pursue', 'chase', 'hunt', 'seek', 'follow', 'track']
}


def link_proverbs_to_concepts():
    """Create EXPRESSES_CONCEPT relationships using keyword matching."""
    
    print("="*70)
    print("PROVERB-CONCEPT RELATIONSHIP CREATION")
    print("="*70)
    print(f"\n🎯 Target: Create EXPRESSES_CONCEPT relationships")
    print(f"📖 Method: Keyword matching\n")
    
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
    
    # Get current graph stats
    print("📊 Current graph state:")
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Proverb) 
            WITH count(p) as proverb_count
            MATCH (c:CulturalConcept)
            RETURN proverb_count, count(c) as concept_count
        """)
        
        stats = result.single()
        print(f"   Proverbs: {stats['proverb_count']}")
        print(f"   Concepts: {stats['concept_count']}")
    
    print(f"\n🔍 Mapping {len(CONCEPT_KEYWORDS)} concepts with keyword patterns...\n")
    
    # Create relationships for each concept
    print("🚀 Creating relationships...")
    print("-" * 70)
    
    total_relationships = 0
    
    with driver.session() as session:
        for concept_name, keywords in CONCEPT_KEYWORDS.items():
            # Build keyword pattern for regex matching (case-insensitive)
            keyword_pattern = '|'.join(keywords)
            
            # Find proverbs matching the concept keywords
            result = session.run("""
                MATCH (p:Proverb)
                MATCH (c:CulturalConcept {concept_name: $concept_name})
                WHERE toLower(p.kikuyu_text) =~ ('(?i).*(' + $keyword_pattern + ').*')
                   OR toLower(p.expert_translation) =~ ('(?i).*(' + $keyword_pattern + ').*')
                   OR toLower(p.expert_cultural_meaning) =~ ('(?i).*(' + $keyword_pattern + ').*')
                CREATE (p)-[r:EXPRESSES_CONCEPT {
                    strength: 0.8,
                    extraction_method: 'keyword_matching',
                    keywords_used: $keywords,
                    created_date: $created_date
                }]->(c)
                RETURN count(r) as relationships_created
            """, 
                concept_name=concept_name,
                keyword_pattern=keyword_pattern,
                keywords=keywords,
                created_date=datetime.now().isoformat()
            )
            
            count = result.single()['relationships_created']
            if count > 0:
                total_relationships += count
                print(f"   ✅ {concept_name:<30} → {count:>3} proverbs linked")
    
    print("-" * 70)
    print(f"\n✅ Successfully created {total_relationships} relationships!\n")
    
    # Verify relationships
    print("🔍 Verifying relationship creation...")
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Proverb)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
            RETURN 
                count(r) as total_relationships,
                count(DISTINCT p) as proverbs_with_concepts,
                count(DISTINCT c) as concepts_with_proverbs,
                avg(r.strength) as avg_strength
        """)
        
        stats = result.single()
        print(f"   Total relationships: {stats['total_relationships']}")
        print(f"   Proverbs with concepts: {stats['proverbs_with_concepts']}")
        print(f"   Concepts with proverbs: {stats['concepts_with_proverbs']}")
        print(f"   Average strength: {stats['avg_strength']:.2f}")
    
    # Show top connected concepts
    print(f"\n📊 Top 5 most connected concepts:")
    with driver.session() as session:
        result = session.run("""
            MATCH (c:CulturalConcept)<-[r:EXPRESSES_CONCEPT]-(p:Proverb)
            WITH c, count(r) as connection_count
            ORDER BY connection_count DESC
            LIMIT 5
            RETURN c.concept_name, connection_count, c.importance_score
        """)
        
        for i, record in enumerate(result, 1):
            print(f"   {i}. {record['c.concept_name']:<30} "
                  f"({record['connection_count']:>2} proverbs, "
                  f"importance: {record['c.importance_score']:>5.1f})")
    
    # Sample relationships
    print(f"\n📝 Sample proverb-concept relationships:")
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Proverb)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
            RETURN p.proverb_id, p.kikuyu_text, c.concept_name, r.strength
            ORDER BY c.importance_score DESC
            LIMIT 3
        """)
        
        for i, record in enumerate(result, 1):
            print(f"   {i}. {record['p.proverb_id']}: {record['p.kikuyu_text'][:40]}...")
            print(f"      → {record['c.concept_name']} (strength: {record['r.strength']})")
    
    driver.close()
    
    print("\n" + "="*70)
    print("✅ RELATIONSHIP CREATION COMPLETE!")
    print("="*70)
    print(f"\n📝 Next steps:")
    print(f"   1. Validate complete graph structure")
    print(f"   2. Run quality checks on relationships")
    print(f"   3. Generate Day 1 summary statistics\n")


if __name__ == '__main__':
    link_proverbs_to_concepts()
