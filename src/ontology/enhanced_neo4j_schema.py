"""
Enhanced Neo4j Schema for Kikuyu Proverb Ontology

This script creates a comprehensive Neo4j schema with:
- Enhanced node properties (validation metadata, cultural weights)
- Rich relationship properties (strength, confidence, salience)
- Constraints and indexes for data integrity and performance
- Full-text search capabilities
- Cultural weight integration

Based on comprehensive ontology creation guide best practices.

Author: [Your name]
Date: October 17, 2025
Version: 2.0 (Enhanced)
"""

from neo4j import GraphDatabase
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedOntologySchema:
    """
    Creates and manages enhanced Neo4j schema for Kikuyu Proverb Ontology.
    """
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize connection to Neo4j database.
        
        Args:
            uri: Neo4j connection URI (e.g., 'bolt://localhost:7687')
            user: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info(f"Connected to Neo4j at {uri}")
    
    def close(self):
        """Close database connection."""
        self.driver.close()
        logger.info("Closed Neo4j connection")
    
    def create_complete_schema(self):
        """
        Create complete enhanced schema with all components.
        
        Executes:
        1. Constraints (uniqueness, existence)
        2. Indexes (property, composite, full-text)
        3. Example nodes with enhanced properties
        """
        logger.info("Creating complete enhanced schema...")
        
        with self.driver.session() as session:
            # Drop existing constraints/indexes if recreating
            # Commented out for safety - uncomment if intentional recreation
            # self._drop_all_constraints_and_indexes(session)
            
            # Create constraints
            self._create_constraints(session)
            
            # Create indexes
            self._create_indexes(session)
            
            # Create full-text indexes
            self._create_fulltext_indexes(session)
            
            # Create example nodes (optional - for testing)
            # self._create_example_nodes(session)
            
            logger.info("Schema creation complete!")
    
    def _create_constraints(self, session):
        """Create uniqueness constraints for all node types."""
        logger.info("Creating constraints...")
        
        constraints = [
            # Proverb uniqueness
            """
            CREATE CONSTRAINT proverb_id IF NOT EXISTS
            FOR (p:Proverb) REQUIRE p.id IS UNIQUE
            """,
            
            # CulturalConcept uniqueness
            """
            CREATE CONSTRAINT concept_name IF NOT EXISTS
            FOR (c:CulturalConcept) REQUIRE c.name IS UNIQUE
            """,
            
            # KikuyuEntity uniqueness (from Phase 2a extraction)
            """
            CREATE CONSTRAINT entity_id IF NOT EXISTS
            FOR (e:KikuyuEntity) REQUIRE e.id IS UNIQUE
            """,
            
            # KikuyuAction uniqueness
            """
            CREATE CONSTRAINT action_id IF NOT EXISTS
            FOR (a:KikuyuAction) REQUIRE a.id IS UNIQUE
            """,
            
            # Metaphor uniqueness
            """
            CREATE CONSTRAINT metaphor_id IF NOT EXISTS
            FOR (m:Metaphor) REQUIRE m.id IS UNIQUE
            """,
            
            # WealthTheme uniqueness
            """
            CREATE CONSTRAINT theme_id IF NOT EXISTS
            FOR (t:WealthTheme) REQUIRE t.id IS UNIQUE
            """,
            
            # SocialContext uniqueness
            """
            CREATE CONSTRAINT context_id IF NOT EXISTS
            FOR (sc:SocialContext) REQUIRE sc.context_id IS UNIQUE
            """,
            
            # MetaphoricalDomain uniqueness
            """
            CREATE CONSTRAINT domain_id IF NOT EXISTS
            FOR (md:MetaphoricalDomain) REQUIRE md.domain_id IS UNIQUE
            """,
            
            # HistoricalPeriod uniqueness
            """
            CREATE CONSTRAINT period_id IF NOT EXISTS
            FOR (hp:HistoricalPeriod) REQUIRE hp.period_id IS UNIQUE
            """,
            
            # Moral uniqueness
            """
            CREATE CONSTRAINT moral_id IF NOT EXISTS
            FOR (mo:Moral) REQUIRE mo.id IS UNIQUE
            """,
            
            # BiblicalParallel uniqueness
            """
            CREATE CONSTRAINT biblical_id IF NOT EXISTS
            FOR (bp:BiblicalParallel) REQUIRE bp.id IS UNIQUE
            """
        ]
        
        for constraint in constraints:
            try:
                session.run(constraint)
                logger.info(f"Created constraint: {constraint.split()[1]}")
            except Exception as e:
                logger.warning(f"Constraint may already exist: {e}")
    
    def _create_indexes(self, session):
        """Create property indexes for efficient querying."""
        logger.info("Creating property indexes...")
        
        indexes = [
            # ========== Proverb Indexes ==========
            # Text search on Kikuyu proverb text
            """
            CREATE INDEX proverb_kikuyu_text IF NOT EXISTS
            FOR (p:Proverb) ON (p.kikuyu_text)
            """,
            
            # Cultural weight filtering (high-importance proverbs)
            """
            CREATE INDEX proverb_cultural_weight IF NOT EXISTS
            FOR (p:Proverb) ON (p.cultural_weight)
            """,
            
            # Validation status filtering
            """
            CREATE INDEX proverb_validation_status IF NOT EXISTS
            FOR (p:Proverb) ON (p.validation_status)
            """,
            
            # Usage frequency filtering
            """
            CREATE INDEX proverb_usage_frequency IF NOT EXISTS
            FOR (p:Proverb) ON (p.usage_frequency)
            """,
            
            # Region filtering
            """
            CREATE INDEX proverb_region IF NOT EXISTS
            FOR (p:Proverb) ON (p.region)
            """,
            
            # ========== CulturalConcept Indexes ==========
            # Kikuyu term search
            """
            CREATE INDEX concept_kikuyu_term IF NOT EXISTS
            FOR (c:CulturalConcept) ON (c.kikuyu_term)
            """,
            
            # Cultural weight filtering
            """
            CREATE INDEX concept_cultural_weight IF NOT EXISTS
            FOR (c:CulturalConcept) ON (c.cultural_weight)
            """,
            
            # Concept type filtering
            """
            CREATE INDEX concept_type IF NOT EXISTS
            FOR (c:CulturalConcept) ON (c.concept_type)
            """,
            
            # Translation difficulty filtering
            """
            CREATE INDEX concept_translation_difficulty IF NOT EXISTS
            FOR (c:CulturalConcept) ON (c.translation_difficulty)
            """,
            
            # ========== Entity Indexes ==========
            # Entity text search
            """
            CREATE INDEX entity_text IF NOT EXISTS
            FOR (e:KikuyuEntity) ON (e.text)
            """,
            
            # Entity type filtering
            """
            CREATE INDEX entity_type IF NOT EXISTS
            FOR (e:KikuyuEntity) ON (e.entity_type)
            """,
            
            # ========== Metaphor Indexes ==========
            # Source domain search
            """
            CREATE INDEX metaphor_source IF NOT EXISTS
            FOR (m:Metaphor) ON (m.source_domain)
            """,
            
            # Target domain search
            """
            CREATE INDEX metaphor_target IF NOT EXISTS
            FOR (m:Metaphor) ON (m.target_domain)
            """,
            
            # ========== Theme Indexes ==========
            # Theme name search
            """
            CREATE INDEX theme_name IF NOT EXISTS
            FOR (t:WealthTheme) ON (t.theme_name)
            """,
            
            # Theme cultural weight
            """
            CREATE INDEX theme_cultural_weight IF NOT EXISTS
            FOR (t:WealthTheme) ON (t.cultural_weight)
            """
        ]
        
        for index in indexes:
            try:
                session.run(index)
                logger.info(f"Created index: {index.split()[2]}")
            except Exception as e:
                logger.warning(f"Index may already exist: {e}")
    
    def _create_fulltext_indexes(self, session):
        """Create full-text search indexes."""
        logger.info("Creating full-text indexes...")
        
        # Check if indexes already exist
        try:
            # Proverb full-text search (Kikuyu text, translations, meanings)
            session.run("""
                CREATE FULLTEXT INDEX proverbFullText IF NOT EXISTS
                FOR (p:Proverb)
                ON EACH [
                    p.kikuyu_text,
                    p.literal_translation,
                    p.expert_translation,
                    p.cultural_meaning,
                    p.moral_instruction
                ]
            """)
            logger.info("Created full-text index: proverbFullText")
        except Exception as e:
            logger.warning(f"Proverb full-text index may already exist: {e}")
        
        try:
            # Concept full-text search (terms, notes, translations)
            session.run("""
                CREATE FULLTEXT INDEX conceptFullText IF NOT EXISTS
                FOR (c:CulturalConcept)
                ON EACH [
                    c.name,
                    c.kikuyu_term,
                    c.cultural_notes,
                    c.english_approximation,
                    c.worldview_implications
                ]
            """)
            logger.info("Created full-text index: conceptFullText")
        except Exception as e:
            logger.warning(f"Concept full-text index may already exist: {e}")
    
    def _drop_all_constraints_and_indexes(self, session):
        """
        Drop all existing constraints and indexes.
        
        WARNING: Use with caution! Only for schema recreation.
        """
        logger.warning("Dropping all constraints and indexes...")
        
        # Get all constraints
        result = session.run("SHOW CONSTRAINTS")
        for record in result:
            constraint_name = record.get('name')
            try:
                session.run(f"DROP CONSTRAINT {constraint_name}")
                logger.info(f"Dropped constraint: {constraint_name}")
            except Exception as e:
                logger.error(f"Error dropping constraint {constraint_name}: {e}")
        
        # Get all indexes
        result = session.run("SHOW INDEXES")
        for record in result:
            index_name = record.get('name')
            # Skip constraint-backed indexes
            if 'constraint' not in index_name.lower():
                try:
                    session.run(f"DROP INDEX {index_name}")
                    logger.info(f"Dropped index: {index_name}")
                except Exception as e:
                    logger.error(f"Error dropping index {index_name}: {e}")
    
    def verify_schema(self) -> Dict:
        """
        Verify schema was created successfully.
        
        Returns:
            Dict with counts of constraints, indexes, and nodes
        """
        logger.info("Verifying schema...")
        
        with self.driver.session() as session:
            # Count constraints
            result = session.run("SHOW CONSTRAINTS")
            constraints = [record for record in result]
            constraint_count = len(constraints)
            
            # Count indexes
            result = session.run("SHOW INDEXES")
            indexes = [record for record in result]
            index_count = len(indexes)
            
            # Count nodes by label
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            node_counts = {record['label']: record['count'] for record in result}
            
            # Count relationships
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            rel_counts = {record['rel_type']: record['count'] for record in result}
            
            verification = {
                'constraints': constraint_count,
                'indexes': index_count,
                'node_counts': node_counts,
                'relationship_counts': rel_counts,
                'constraint_details': [
                    {'name': c.get('name'), 'type': c.get('type')} 
                    for c in constraints
                ],
                'index_details': [
                    {'name': i.get('name'), 'type': i.get('type')} 
                    for i in indexes
                ]
            }
            
            logger.info(f"Schema verification complete:")
            logger.info(f"  - Constraints: {constraint_count}")
            logger.info(f"  - Indexes: {index_count}")
            logger.info(f"  - Node labels: {len(node_counts)}")
            logger.info(f"  - Relationship types: {len(rel_counts)}")
            
            return verification
    
    def create_example_data(self):
        """
        Create example nodes with enhanced properties for testing.
        
        WARNING: Only use for testing! Will create duplicate data.
        """
        logger.info("Creating example data...")
        
        with self.driver.session() as session:
            # Example Proverb with full enhanced properties
            session.run("""
                MERGE (p:Proverb {id: 'KP_EXAMPLE_001'})
                SET p = {
                    id: 'KP_EXAMPLE_001',
                    
                    // Linguistic Data
                    kikuyu_text: 'Mũndũ mũũgĩ ndahĩtagwo igũrũ',
                    kikuyu_phonetic: 'Mũndũ mũũgĩ ndahĩtagwo igũrũ',
                    literal_translation: 'A wise person is not sought in the heights',
                    
                    // Translation Data
                    expert_translation: 'True wisdom comes from humility, not elevation',
                    alternative_translations: [
                        'Genuine wisdom is found in groundedness, not superiority',
                        'The truly wise remain humble and connected to their roots'
                    ],
                    
                    // Cultural Semantics
                    cultural_meaning: 'Emphasizes that genuine wisdom requires humility and connection to community rather than social elevation or separation. Warns against conflating status with understanding.',
                    moral_instruction: 'Remain grounded and humble; true wisdom comes from connection, not separation',
                    social_function: 'Correcting prideful behavior, teaching humility, guiding leadership',
                    
                    // Metaphorical Structure
                    metaphor_source: 'physical_height',
                    metaphor_target: 'social_status',
                    metaphor_mapping: 'UP IS HIGH STATUS / DOWN IS LOW STATUS',
                    
                    // Pragmatic Data
                    usage_frequency: 8.5,
                    formality_level: 'medium_to_high',
                    emotional_valence: 'instructive_corrective',
                    generational_usage: 'all_ages',
                    
                    // Cultural Weight (ENHANCED)
                    cultural_weight: 0.92,
                    preservation_priority: 'high',
                    
                    // Validation Metadata (ENHANCED)
                    validation_status: 'expert_verified',
                    validator_ids: ['ireri_mbaabu'],
                    validation_date: '2025-10-17',
                    validation_confidence: 0.90,
                    inter_rater_agreement: 1.0,  // Single expert
                    expert_consensus: 0.90,
                    
                    // Collection Metadata
                    collection_date: '2024-10-20',
                    collector_id: 'researcher_001',
                    region: 'Murang\'a',
                    district: 'Kiharu',
                    speaker_age_range: '60-75',
                    
                    // Usage Restrictions
                    sacred_knowledge: false,
                    public_dissemination_approved: true,
                    educational_use_approved: true,
                    commercial_use_requires_consent: true,
                    
                    // Provenance (ENHANCED)
                    data_source: 'expert_consultation',
                    documentation_quality: 'high',
                    needs_review: false
                }
            """)
            logger.info("Created example Proverb node")
            
            # Example CulturalConcept with enhanced properties
            session.run("""
                MERGE (c:CulturalConcept {name: 'ũtonga'})
                SET c = {
                    // Identity
                    name: 'ũtonga',
                    concept_id: 'CC_WEALTH_001',
                    concept_type: 'wealth_paradigm',
                    
                    // Linguistic Data
                    kikuyu_term: 'ũtonga',
                    kikuyu_root: 'tonga',
                    morphological_class: 'noun_class_14',
                    
                    // Semantic Dimensions (ENHANCED - Multi-dimensional)
                    semantic_dimensions: [
                        'material_resources',
                        'social_capital', 
                        'livestock_ownership',
                        'land_stewardship',
                        'family_size',
                        'ancestral_blessings',
                        'community_standing',
                        'generational_continuity'
                    ],
                    
                    // Translation Data
                    english_approximation: 'wealth/prosperity/abundance',
                    literal_english: 'wealth',
                    inadequate_translations: ['money', 'riches', 'fortune'],
                    preferred_translations: [
                        'prosperity (encompassing social and material well-being)',
                        'abundance (including livestock, land, and community)',
                        'blessed state of plenty',
                        'multi-generational wealth'
                    ],
                    translation_loss: 'English wealth lacks social, spiritual, and communal dimensions',
                    
                    // Cultural Notes (ENHANCED)
                    cultural_notes: 'Multi-dimensional concept absent in Western individualistic wealth. Fundamentally relational - wealth that does not benefit community is not true ũtonga. Includes livestock (especially cattle) as primary wealth marker, land as ancestral inheritance, large families as prosperity indicator, and social networks as wealth multiplier.',
                    
                    worldview_implications: 'Reflects communal rather than individualistic value system. Wealth as stewardship rather than ownership. Intergenerational rather than personal accumulation.',
                    
                    historical_context: 'Pre-colonial pastoral-agricultural economy where cattle and land were primary wealth forms. Colonial disruption changed meanings but core concepts persist.',
                    
                    // Presuppositions
                    presupposed_concepts: [
                        'community_interdependence',
                        'ancestral_connection', 
                        'livestock_as_currency',
                        'land_as_heritage'
                    ],
                    
                    // Cultural Weight (ENHANCED - Multi-factor calculation)
                    cultural_weight: 0.95,
                    centrality_score: 0.93,
                    translation_difficulty: 0.88,
                    usage_frequency_score: 0.85,
                    historical_persistence: 0.91,
                    
                    // Validation (ENHANCED)
                    expert_consensus: 0.94,
                    validation_method: 'single_expert_validated',
                    expert_count: 1,
                    validation_confidence: 0.90,
                    
                    // Metadata
                    date_documented: '2024-10-22',
                    last_updated: '2025-10-17',
                    documentation_quality: 'high'
                }
            """)
            logger.info("Created example CulturalConcept node")
            
            # Example WealthTheme
            session.run("""
                MERGE (wt:WealthTheme {id: 'WT_EXAMPLE_001'})
                SET wt = {
                    id: 'WT_EXAMPLE_001',
                    theme_name: 'Collective_Prosperity',
                    theme_name_kikuyu: 'Ũgaacĩru wa Mũingĩ',
                    
                    description: 'Wealth understood through lens of community benefit rather than individual accumulation. Prosperity measured by community well-being.',
                    
                    core_values: [
                        'communalism',
                        'ubuntu', 
                        'mutual_support',
                        'collective_advancement'
                    ],
                    
                    contrasts_with: [
                        'individualism',
                        'zero_sum_thinking',
                        'hoarding',
                        'selfish_accumulation'
                    ],
                    
                    proverb_count: 23,
                    representation_strength: 'high',
                    
                    cultural_weight: 0.89
                }
            """)
            logger.info("Created example WealthTheme node")
            
            # Example MetaphoricalDomain
            session.run("""
                MERGE (md:MetaphoricalDomain {domain_id: 'MD_EXAMPLE_001'})
                SET md = {
                    domain_id: 'MD_EXAMPLE_001',
                    domain_type: 'agricultural',
                    domain_name: 'Agricultural/Pastoral Domain',
                    
                    source_elements: [
                        'planting',
                        'harvest', 
                        'soil_preparation',
                        'rain',
                        'drought',
                        'weeding',
                        'livestock_husbandry',
                        'grazing_patterns'
                    ],
                    
                    target_concepts: [
                        'investment_effort',
                        'reward_benefit',
                        'preparation_planning',
                        'opportunity',
                        'hardship_scarcity',
                        'maintenance_vigilance',
                        'resource_management',
                        'strategic_planning'
                    ],
                    
                    mapping_principles: [
                        'PLANTING IS INVESTING',
                        'HARVEST IS REWARD',
                        'SOIL QUALITY IS OPPORTUNITY QUALITY',
                        'RAIN IS FAVORABLE CONDITIONS',
                        'WEEDS ARE PROBLEMS_TO_ADDRESS'
                    ],
                    
                    cultural_grounding: 'Kikuyu agricultural heritage and pastoral economy provide embodied experience basis for abstract reasoning',
                    
                    conventionality: 'highly_conventional',
                    productivity: 'highly_productive',
                    proverb_usage_count: 34,
                    
                    cultural_weight: 0.91
                }
            """)
            logger.info("Created example MetaphoricalDomain node")
            
            # Example Relationships with enhanced properties
            session.run("""
                MATCH (p:Proverb {id: 'KP_EXAMPLE_001'})
                MATCH (c:CulturalConcept {name: 'ũtonga'})
                MERGE (p)-[r:CONTAINS_CONCEPT]->(c)
                SET r = {
                    // Salience (ENHANCED)
                    salience: 0.92,
                    concept_role: 'central',
                    
                    // Invocation Type
                    invocation_type: 'explicit',
                    metaphor_type: 'direct',
                    
                    // Cultural Importance (ENHANCED)
                    cultural_necessity: 0.89,
                    translation_criticality: 0.94,
                    
                    // Validation (ENHANCED)
                    confidence: 0.90,
                    evidence_type: 'expert_annotation',
                    validator_id: 'ireri_mbaabu',
                    
                    // Metadata
                    relationship_date: '2025-10-17',
                    last_verified: '2025-10-17'
                }
            """)
            logger.info("Created example CONTAINS_CONCEPT relationship")
            
            session.run("""
                MATCH (p:Proverb {id: 'KP_EXAMPLE_001'})
                MATCH (wt:WealthTheme {id: 'WT_EXAMPLE_001'})
                MERGE (p)-[r:EXPRESSES]->(wt)
                SET r = {
                    // Strength (ENHANCED)
                    strength: 0.88,
                    directionality: 'primary',
                    
                    // Explicitness
                    explicitness: 'implicit',
                    
                    // Validation (ENHANCED)
                    cultural_validation: 'expert_confirmed',
                    confidence: 0.92,
                    annotator_agreement: 0.85,
                    
                    // Metadata
                    relationship_date: '2025-10-17'
                }
            """)
            logger.info("Created example EXPRESSES relationship")
            
            session.run("""
                MATCH (p:Proverb {id: 'KP_EXAMPLE_001'})
                MATCH (md:MetaphoricalDomain {domain_id: 'MD_EXAMPLE_001'})
                MERGE (p)-[r:EMPLOYS_METAPHOR]->(md)
                SET r = {
                    // Mapping Strength (ENHANCED)
                    mapping_strength: 0.87,
                    conventional: true,
                    
                    // Creativity
                    creativity: 'conventional',
                    centrality: 'core',
                    
                    // Validation (ENHANCED)
                    confidence: 0.85,
                    
                    // Metadata
                    relationship_date: '2025-10-17'
                }
            """)
            logger.info("Created example EMPLOYS_METAPHOR relationship")
            
        logger.info("Example data creation complete!")


def main():
    """Main execution function."""
    import sys
    
    # Configuration
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "your_password_here"  # CHANGE THIS!
    
    if NEO4J_PASSWORD == "your_password_here":
        logger.error("Please set your Neo4j password in the script!")
        sys.exit(1)
    
    # Create schema
    schema = EnhancedOntologySchema(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Create complete schema
        schema.create_complete_schema()
        
        # Verify schema
        verification = schema.verify_schema()
        
        print("\n" + "="*70)
        print("SCHEMA VERIFICATION SUMMARY")
        print("="*70)
        print(f"Constraints created: {verification['constraints']}")
        print(f"Indexes created: {verification['indexes']}")
        print(f"\nNode counts by label:")
        for label, count in verification['node_counts'].items():
            print(f"  {label}: {count}")
        print(f"\nRelationship counts by type:")
        for rel_type, count in verification['relationship_counts'].items():
            print(f"  {rel_type}: {count}")
        print("="*70)
        
        # Optionally create example data
        create_examples = input("\nCreate example data for testing? (y/n): ")
        if create_examples.lower() == 'y':
            schema.create_example_data()
            print("\nExample data created successfully!")
        
    finally:
        schema.close()
    
    print("\n✅ Enhanced schema creation complete!")
    print("\nNext steps:")
    print("1. Review schema in Neo4j Browser")
    print("2. Run CALL db.schema.visualization() to see structure")
    print("3. Proceed with data loading (Week 1 Days 3-4)")


if __name__ == "__main__":
    main()
