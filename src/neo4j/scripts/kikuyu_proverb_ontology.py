#!/usr/bin/env python3
"""
Enhanced Neo4j Schema for Kikuyu Proverb oGRAG System

This module implements a culturally faithful ontology for Kikuyu-English proverb
translation following best practices for low-resource language (LRL) knowledge graphs.

Features:
- Cultural concept preservation
- Multilingual semantic mapping  
- Translation quality assessment
- RAG-optimized retrieval paths
- Comprehensive linguistic analysis

Author: Neo4j Schema Designer
Date: September 2025
"""

from neo4j import GraphDatabase
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KikuyuProverbOntology:
    """
    Enhanced ontology setup for Kikuyu proverb knowledge graph.
    
    Implements best practices for:
    - Cultural concept preservation
    - Multilingual semantic mapping
    - Translation quality assessment
    - RAG-optimized retrieval paths
    """
    
    def __init__(
        self, 
        uri: str = "bolt://localhost:7687", 
        user: str = "neo4j", 
        password: str = "ograg2025"
    ):
        """Initialize connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ Connected to Neo4j database")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Neo4j: {e}")
            raise
    
    def close(self) -> None:
        """Close database connection."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def clear_database(self) -> None:
        """Clear all data from database. Use with caution!"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.warning("🗑️  Database cleared - all data deleted")
    
    def create_constraints(self) -> None:
        """Create comprehensive constraints for data integrity."""
        constraints = [
            # Core entity uniqueness constraints
            "CREATE CONSTRAINT proverb_id_unique IF NOT EXISTS FOR (p:Proverb) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT proverb_kikuyu_unique IF NOT EXISTS FOR (p:Proverb) REQUIRE p.kikuyu_text IS UNIQUE",
            "CREATE CONSTRAINT lexeme_id_unique IF NOT EXISTS FOR (l:Lexeme) REQUIRE l.id IS UNIQUE",
            "CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:CulturalConcept) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT semantic_field_id_unique IF NOT EXISTS FOR (sf:SemanticField) REQUIRE sf.id IS UNIQUE",
            "CREATE CONSTRAINT translation_id_unique IF NOT EXISTS FOR (t:Translation) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT source_id_unique IF NOT EXISTS FOR (s:Source) REQUIRE s.id IS UNIQUE",
            
            # Essential property constraints
            "CREATE CONSTRAINT proverb_kikuyu_text IF NOT EXISTS FOR (p:Proverb) REQUIRE p.kikuyu_text IS NOT NULL",
            "CREATE CONSTRAINT concept_description IF NOT EXISTS FOR (c:CulturalConcept) REQUIRE c.description IS NOT NULL",
            "CREATE CONSTRAINT translation_source IF NOT EXISTS FOR (t:Translation) REQUIRE t.source_text IS NOT NULL",
            "CREATE CONSTRAINT translation_target IF NOT EXISTS FOR (t:Translation) REQUIRE t.target_text IS NOT NULL",
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    constraint_name = constraint.split()[2]
                    logger.info(f"✅ Created constraint: {constraint_name}")
                except Exception as e:
                    constraint_name = constraint.split()[2] if len(constraint.split()) > 2 else "unknown"
                    logger.debug(f"⚠️  Constraint {constraint_name} may already exist")
    
    def create_indexes(self) -> None:
        """Create comprehensive indexes optimized for oGRAG retrieval."""
        indexes = [
            # Full-text search indexes (critical for RAG)
            "CREATE FULLTEXT INDEX proverb_content_fulltext IF NOT EXISTS FOR (p:Proverb) ON EACH [p.kikuyu_text, p.literal_translation, p.cultural_meaning, p.usage_notes]",
            "CREATE FULLTEXT INDEX concept_content_fulltext IF NOT EXISTS FOR (c:CulturalConcept) ON EACH [c.name, c.description, c.kikuyu_terms]",
            "CREATE FULLTEXT INDEX translation_content_fulltext IF NOT EXISTS FOR (t:Translation) ON EACH [t.source_text, t.target_text, t.translator_notes]",
            
            # Precise matching indexes
            "CREATE INDEX proverb_kikuyu_text IF NOT EXISTS FOR (p:Proverb) ON (p.kikuyu_text)",
            "CREATE INDEX lexeme_surface_form IF NOT EXISTS FOR (l:Lexeme) ON (l.surface_form)",
            "CREATE INDEX concept_category IF NOT EXISTS FOR (c:CulturalConcept) ON (c.category)",
            
            # Semantic and categorical indexes
            "CREATE INDEX semantic_field_domain IF NOT EXISTS FOR (sf:SemanticField) ON (sf.domain)",
            "CREATE INDEX proverb_themes IF NOT EXISTS FOR (p:Proverb) ON (p.themes)",
            "CREATE INDEX concept_significance IF NOT EXISTS FOR (c:CulturalConcept) ON (c.cultural_significance)",
            
            # Quality and source tracking
            "CREATE INDEX proverb_validation_status IF NOT EXISTS FOR (p:Proverb) ON (p.validation_status)",
            "CREATE INDEX translation_quality_score IF NOT EXISTS FOR (t:Translation) ON (t.quality_score)",
            "CREATE INDEX source_authority_level IF NOT EXISTS FOR (s:Source) ON (s.authority_level)",
            
            # Temporal indexes for versioning
            "CREATE INDEX proverb_created_at IF NOT EXISTS FOR (p:Proverb) ON (p.created_at)",
        ]
        
        with self.driver.session() as session:
            for index in indexes:
                try:
                    session.run(index)
                    index_name = index.split()[2]
                    logger.info(f"✅ Created index: {index_name}")
                except Exception as e:
                    index_name = index.split()[2] if len(index.split()) > 2 else "unknown"
                    logger.debug(f"⚠️  Index {index_name} may already exist")
    
    def create_linguistic_foundation(self) -> None:
        """Create foundational linguistic structures for Kikuyu language."""
        with self.driver.session() as session:
            linguistic_query = """
            // Morphological categories specific to Kikuyu
            CREATE (noun:MorphCategory {
                id: 'kikuyu_noun',
                name: 'Kikuyu Noun',
                kikuyu_name: 'rĩtwa',
                class_system: 'bantu_noun_classes',
                description: 'Kikuyu nominal categories with class prefixes',
                common_classes: ['mu_mi', 'ki_i', 'ka_tu', 'ri_ma']
            })
            
            CREATE (verb:MorphCategory {
                id: 'kikuyu_verb',
                name: 'Kikuyu Verb',
                kikuyu_name: 'kiuga',
                tense_system: 'complex_aspectual',
                description: 'Kikuyu verbal system with rich aspectual marking'
            })
            
            // Core semantic fields for Kikuyu culture
            CREATE (kinship:SemanticField {
                id: 'kinship_relations',
                name: 'Kinship & Family',
                kikuyu_name: 'ũrata wa nyũmba',
                domain: 'social_structure',
                description: 'Family relationships, clan connections, and kinship obligations',
                core_lexemes: ['nyina', 'baba', 'mũthuri', 'mũndũ-wa-nyũmba'],
                cultural_importance: 'foundational'
            })
            
            CREATE (agriculture:SemanticField {
                id: 'agriculture_livelihood',
                name: 'Agriculture & Livelihood',
                kikuyu_name: 'ũrĩmi na mbeũ',
                domain: 'economic_activity',
                description: 'Farming practices, land use, seasonal cycles',
                core_lexemes: ['mũgũnda', 'magetha', 'mbura', 'ngombe'],
                cultural_importance: 'foundational'
            })
            
            CREATE (wisdom_tradition:SemanticField {
                id: 'wisdom_knowledge',
                name: 'Wisdom & Knowledge',
                kikuyu_name: 'ũũgĩ na meciria',
                domain: 'epistemic_system',
                description: 'Traditional knowledge, wisdom practices, learning',
                core_lexemes: ['ũũgĩ', 'gũtaaro', 'mĩrũtanĩrĩ'],
                cultural_importance: 'foundational'
            })
            
            // Discourse patterns common in Kikuyu proverbs
            CREATE (metaphor:DiscoursePattern {
                id: 'metaphorical_mapping',
                pattern_type: 'figurative_language',
                name: 'Metaphorical Structure',
                kikuyu_markers: ['ta', 'o ta', 'kana'],
                description: 'Proverbs using metaphorical mappings',
                frequency: 'very_high'
            })
            
            CREATE (parallelism:DiscoursePattern {
                id: 'parallel_construction',
                pattern_type: 'syntactic_structure',
                name: 'Parallel Structures', 
                kikuyu_markers: ['na', 'no', 'o na'],
                description: 'Proverbs with parallel grammatical constructions',
                frequency: 'high'
            })
            """
            session.run(linguistic_query)
            logger.info("✅ Linguistic foundation created")
    
    def create_cultural_concepts(self) -> None:
        """Create core Kikuyu cultural concepts for faithful translation."""
        with self.driver.session() as session:
            cultural_query = """
            // Foundational Kikuyu cultural concepts
            CREATE (ubuntu:CulturalConcept {
                id: 'ubuntu_umundu',
                name: 'Ubuntu/Ũmũndũ',
                category: 'core_philosophy',
                kikuyu_terms: ['ũmũndũ', 'ũrata', 'ũiguano'],
                english_approximations: ['ubuntu', 'humanity', 'interconnectedness'],
                description: 'Fundamental philosophy of shared humanity and mutual support',
                cultural_significance: 'foundational',
                translation_challenges: ['no_direct_equivalent', 'requires_explanation'],
                related_practices: ['community_decision_making', 'mutual_aid']
            })
            
            CREATE (ancestral_wisdom:CulturalConcept {
                id: 'ancestral_wisdom_tradition',
                name: 'Ancestral Wisdom',
                category: 'knowledge_system',
                kikuyu_terms: ['ũũgĩ wa aciari', 'mĩrũtanĩrĩ ya tene'],
                english_approximations: ['ancestral_wisdom', 'traditional_knowledge'],
                description: 'Wisdom and knowledge passed down from ancestors',
                cultural_significance: 'foundational',
                translation_challenges: ['cultural_specificity', 'sacred_knowledge'],
                related_practices: ['oral_tradition', 'elder_consultation']
            })
            
            CREATE (respect_authority:CulturalConcept {
                id: 'respect_hierarchy',
                name: 'Respect for Authority',
                category: 'social_values',
                kikuyu_terms: ['gĩtĩĩo', 'ũkuu', 'gwĩka ũkuu'],
                english_approximations: ['respect', 'reverence', 'deference'],
                description: 'Cultural emphasis on respecting elders and social hierarchy',
                cultural_significance: 'high',
                translation_challenges: ['degree_of_formality', 'hierarchy_levels'],
                related_practices: ['elder_greeting', 'formal_address']
            })
            
            CREATE (communal_responsibility:CulturalConcept {
                id: 'communal_obligation',
                name: 'Communal Responsibility',
                category: 'social_obligation',
                kikuyu_terms: ['wĩra wa mũingĩ', 'gũteithania'],
                english_approximations: ['collective_responsibility', 'community_duty'],
                description: 'Individual responsibility toward community welfare',
                cultural_significance: 'high',
                translation_challenges: ['individualism_vs_collectivism'],
                related_practices: ['harambee', 'community_work']
            })
            """
            session.run(cultural_query)
            logger.info("✅ Cultural concepts created")
    
    def create_usage_contexts(self) -> None:
        """Create comprehensive usage context taxonomy."""
        with self.driver.session() as session:
            contexts_query = """
            // Educational contexts
            CREATE (elder_teaching:UsageContext {
                id: 'elder_wisdom_transmission',
                name: 'Elder Teaching',
                kikuyu_name: 'mũrutani wa athuuri',
                context_type: 'educational',
                formality_level: 'high',
                participants: ['mũthuri_mũkũrũ', 'aanake', 'airĩtu'],
                setting: 'mũciĩ_wa_ũtũũrĩre',
                purpose: 'wisdom_transmission',
                cultural_protocols: ['greeting_elders', 'listening_posture']
            })
            
            CREATE (peer_guidance:UsageContext {
                id: 'peer_advice_sharing',
                name: 'Peer Guidance',
                kikuyu_name: 'mataaro ma rika',
                context_type: 'social_guidance',
                formality_level: 'medium',
                participants: ['andũ_a_rika'],
                setting: 'kiama_kĩa_rika',
                purpose: 'mutual_support'
            })
            
            CREATE (ceremonial:UsageContext {
                id: 'ceremonial_occasions',
                name: 'Ceremonial Events',
                kikuyu_name: 'mĩhiko ya gĩkũyũ',
                context_type: 'ritual_ceremonial',
                formality_level: 'very_high',
                participants: ['mũruthi', 'andũ_a_itũũra'],
                setting: 'kĩrĩra_kĩa_ũtũũrĩre',
                purpose: 'cultural_reinforcement'
            })
            
            CREATE (mediation:UsageContext {
                id: 'dispute_resolution',
                name: 'Conflict Mediation',
                kikuyu_name: 'gũthabania ngarari',
                context_type: 'judicial_mediation',
                formality_level: 'high',
                participants: ['mũciirithania', 'andũ_a_ngarari'],
                setting: 'kĩama_kĩa_itũũra',
                purpose: 'harmony_restoration'
            })
            """
            session.run(contexts_query)
            logger.info("✅ Usage contexts created")
    
    def create_translation_framework(self) -> None:
        """Create framework for managing translation quality and variants."""
        with self.driver.session() as session:
            translation_query = """
            // Translation quality dimensions
            CREATE (linguistic_accuracy:QualityDimension {
                id: 'linguistic_fidelity',
                name: 'Linguistic Accuracy',
                description: 'Preservation of linguistic structure and meaning',
                weight: 0.35,
                criteria: ['grammatical_correctness', 'semantic_preservation']
            })
            
            CREATE (cultural_fidelity:QualityDimension {
                id: 'cultural_preservation',
                name: 'Cultural Fidelity',
                description: 'Preservation of cultural concepts and contexts',
                weight: 0.40,
                criteria: ['concept_preservation', 'cultural_appropriateness']
            })
            
            CREATE (target_fluency:QualityDimension {
                id: 'english_naturalness',
                name: 'Target Language Fluency',
                description: 'Naturalness and readability in English',
                weight: 0.25,
                criteria: ['readability', 'idiomaticity', 'clarity']
            })
            
            // Translation strategies
            CREATE (literal:TranslationStrategy {
                id: 'literal_preservation',
                name: 'Literal Translation',
                description: 'Word-for-word translation preserving structure',
                use_cases: ['linguistic_analysis', 'structure_preservation'],
                cultural_risk: 'medium'
            })
            
            CREATE (cultural_adaptation:TranslationStrategy {
                id: 'cultural_adaptation',
                name: 'Cultural Adaptation',
                description: 'Adaptation preserving cultural meaning over form',
                use_cases: ['cultural_education', 'meaning_preservation'],
                cultural_risk: 'low'
            })
            
            CREATE (functional_equivalent:TranslationStrategy {
                id: 'functional_equivalent',
                name: 'Functional Equivalent',
                description: 'Finding equivalent proverbs in target culture',
                use_cases: ['cross_cultural_communication'],
                cultural_risk: 'high'
            })
            """
            session.run(translation_query)
            logger.info("✅ Translation framework created")
    
    def create_sample_proverbs(self) -> None:
        """Create sample proverbs with rich linguistic and cultural annotations."""
        with self.driver.session() as session:
            proverbs_query = """
            // Sample Proverb 1: Community strength
            CREATE (p1:Proverb {
                id: 'prov_muti_munene',
                kikuyu_text: 'Mũtĩ mũnene ndũkongoĩka na rũhũũ',
                phonetic_transcription: '[muti munene ndukongoika na ruhuu]',
                morphological_analysis: 'mũ-tĩ mũ-nene ndu-kong-o-ĩk-a na rũ-hũũ',
                literal_translation: 'Tree big NEG-break-PASS-HAB-FV with stick',
                cultural_meaning: 'Strong communities cannot be destroyed by minor conflicts',
                usage_notes: 'Used to encourage unity and discourage petty disputes',
                metaphorical_structure: '{"vehicle": "big_tree", "tenor": "strong_community", "mapping": "strength_resistance"}',
                themes: ['unity', 'strength', 'community_resilience'],
                complexity_level: 'moderate',
                frequency_rating: 'common',
                validation_status: 'elder_verified',
                source_type: 'oral_tradition',
                region_variants: ['central_kenya', 'muranga'],
                created_at: datetime(),
                last_updated: datetime()
            })
            
            // Sample Proverb 2: Wisdom and patience  
            CREATE (p2:Proverb {
                id: 'prov_mundu_muugi',
                kikuyu_text: 'Mũndũ mũũgĩ ndarĩĩaga kĩrira kĩa hinya',
                phonetic_transcription: '[mundu muugi ndariaga kirira kia hinya]',
                morphological_analysis: 'mũ-ndũ mũ-ũg-ĩ nda-rĩ-ag-a kĩ-rira kĩa hinya',
                literal_translation: 'Person wise NEG-eat-HAB-FV food of strength',
                cultural_meaning: 'Wise people avoid rushing into difficult situations without preparation',
                usage_notes: 'Advice about patience, careful consideration, and proper timing',
                metaphorical_structure: '{"vehicle": "eating_strong_food", "tenor": "engaging_difficult_situations"}',
                themes: ['wisdom', 'patience', 'careful_planning'],
                complexity_level: 'simple',
                frequency_rating: 'very_common',
                validation_status: 'multiple_sources',
                source_type: 'literature_and_oral',
                created_at: datetime(),
                last_updated: datetime()
            })
            
            // Create key lexical entries
            CREATE (lex_muti:Lexeme {
                id: 'lex_muti',
                surface_form: 'mũtĩ',
                root: 'ti',
                noun_class: '3/4',
                plural_form: 'mĩtĩ',
                semantic_roles: ['agent', 'metaphor_vehicle'],
                english_glosses: ['tree', 'plant', 'wood'],
                cultural_associations: ['strength', 'growth', 'community_symbol'],
                metaphorical_uses: ['community', 'lineage', 'stability']
            })
            
            CREATE (lex_mundu:Lexeme {
                id: 'lex_mundu',
                surface_form: 'mũndũ',
                root: 'ndu',
                noun_class: '1/2',
                plural_form: 'andũ',
                semantic_roles: ['agent', 'experiencer'],
                english_glosses: ['person', 'human_being'],
                cultural_associations: ['humanity', 'community_member'],
                metaphorical_uses: ['representative', 'archetype']
            })
            
            CREATE (lex_uugi:Lexeme {
                id: 'lex_uugi',
                surface_form: 'ũũgĩ',
                root: 'ug',
                noun_class: '14',
                semantic_roles: ['abstract_quality'],
                english_glosses: ['wisdom', 'intelligence', 'cleverness'],
                cultural_associations: ['elder_knowledge', 'life_experience'],
                metaphorical_uses: ['guidance', 'insight']
            })
            """
            session.run(proverbs_query)
            logger.info("✅ Sample proverbs with linguistic analysis created")
    
    def create_translation_variants(self) -> None:
        """Create multiple translation variants for quality assessment."""
        with self.driver.session() as session:
            translations_query = """
            MATCH (p1:Proverb {id: 'prov_muti_munene'})
            MATCH (p2:Proverb {id: 'prov_mundu_muugi'})
            
            // High-quality translations for Proverb 1
            CREATE (t1_literal:Translation {
                id: 'trans_p1_literal',
                source_text: p1.kikuyu_text,
                target_text: 'A big tree does not break with a small stick',
                translation_type: 'literal',
                quality_score: 0.75,
                linguistic_accuracy: 0.9,
                cultural_fidelity: 0.6,
                target_fluency: 0.8,
                translator_type: 'native_speaker',
                translator_notes: 'Preserves grammatical structure and word order',
                created_at: datetime()
            })
            
            CREATE (t1_cultural:Translation {
                id: 'trans_p1_cultural',
                source_text: p1.kikuyu_text,
                target_text: 'Strong communities withstand minor challenges',
                translation_type: 'cultural_adaptation',
                quality_score: 0.88,
                linguistic_accuracy: 0.7,
                cultural_fidelity: 0.95,
                target_fluency: 0.9,
                translator_type: 'cultural_expert',
                translator_notes: 'Focuses on cultural meaning over literal form',
                created_at: datetime()
            })
            
            // Translations for Proverb 2
            CREATE (t2_literal:Translation {
                id: 'trans_p2_literal',
                source_text: p2.kikuyu_text,
                target_text: 'A wise person does not eat strong food',
                translation_type: 'literal',
                quality_score: 0.72,
                linguistic_accuracy: 0.95,
                cultural_fidelity: 0.5,
                target_fluency: 0.7,
                translator_type: 'linguist',
                translator_notes: 'Direct translation may confuse English readers',
                created_at: datetime()
            })
            
            CREATE (t2_cultural:Translation {
                id: 'trans_p2_cultural',
                source_text: p2.kikuyu_text,
                target_text: 'Wise people avoid difficult situations without proper preparation',
                translation_type: 'cultural_adaptation',
                quality_score: 0.91,
                linguistic_accuracy: 0.8,
                cultural_fidelity: 0.95,
                target_fluency: 0.95,
                translator_type: 'cultural_expert',
                translator_notes: 'Explains the metaphor for clarity',
                created_at: datetime()
            })
            
            // Create translation relationships
            CREATE (p1)-[:HAS_TRANSLATION]->(t1_literal)
            CREATE (p1)-[:HAS_TRANSLATION]->(t1_cultural)
            CREATE (p2)-[:HAS_TRANSLATION]->(t2_literal)
            CREATE (p2)-[:HAS_TRANSLATION]->(t2_cultural)
            """
            session.run(translations_query)
            logger.info("✅ Translation variants created")
    
    def create_semantic_relationships(self) -> None:
        """Create rich semantic relationships between entities."""
        with self.driver.session() as session:
            relationships_query = """
            // Connect proverbs to semantic fields
            MATCH (p1:Proverb {id: 'prov_muti_munene'})
            MATCH (p2:Proverb {id: 'prov_mundu_muugi'})
            MATCH (kinship:SemanticField {id: 'kinship_relations'})
            MATCH (wisdom:SemanticField {id: 'wisdom_knowledge'})
            MATCH (agriculture:SemanticField {id: 'agriculture_livelihood'})
            
            CREATE (p1)-[:BELONGS_TO_FIELD {relevance: 0.8}]->(kinship)
            CREATE (p1)-[:BELONGS_TO_FIELD {relevance: 0.6}]->(agriculture)
            CREATE (p2)-[:BELONGS_TO_FIELD {relevance: 0.9}]->(wisdom)
            
            // Connect to cultural concepts
            MATCH (ubuntu:CulturalConcept {id: 'ubuntu_umundu'})
            MATCH (communal:CulturalConcept {id: 'communal_obligation'})
            MATCH (ancestral:CulturalConcept {id: 'ancestral_wisdom_tradition'})
            MATCH (respect:CulturalConcept {id: 'respect_hierarchy'})
            
            CREATE (p1)-[:EMBODIES {strength: 0.9, confidence: 0.85}]->(ubuntu)
            CREATE (p1)-[:EMBODIES {strength: 0.8, confidence: 0.8}]->(communal)
            CREATE (p2)-[:EMBODIES {strength: 0.85, confidence: 0.9}]->(ancestral)
            CREATE (p2)-[:EMBODIES {strength: 0.7, confidence: 0.8}]->(respect)
            
            // Connect to usage contexts
            MATCH (elder:UsageContext {id: 'elder_wisdom_transmission'})
            MATCH (peer:UsageContext {id: 'peer_advice_sharing'})
            MATCH (ceremonial:UsageContext {id: 'ceremonial_occasions'})
            MATCH (mediation:UsageContext {id: 'dispute_resolution'})
            
            CREATE (p1)-[:APPROPRIATE_IN {frequency: 'common', effectiveness: 0.8}]->(elder)
            CREATE (p1)-[:APPROPRIATE_IN {frequency: 'occasional', effectiveness: 0.7}]->(ceremonial)
            CREATE (p1)-[:APPROPRIATE_IN {frequency: 'rare', effectiveness: 0.9}]->(mediation)
            CREATE (p2)-[:APPROPRIATE_IN {frequency: 'very_common', effectiveness: 0.9}]->(elder)
            CREATE (p2)-[:APPROPRIATE_IN {frequency: 'common', effectiveness: 0.7}]->(peer)
            
            // Connect to discourse patterns
            MATCH (metaphor:DiscoursePattern {id: 'metaphorical_mapping'})
            MATCH (parallel:DiscoursePattern {id: 'parallel_construction'})
            
            CREATE (p1)-[:FOLLOWS_PATTERN {strength: 0.95}]->(metaphor)
            CREATE (p2)-[:FOLLOWS_PATTERN {strength: 0.8}]->(metaphor)
            
            // Connect lexemes to proverbs
            MATCH (lex_muti:Lexeme {id: 'lex_muti'})
            MATCH (lex_mundu:Lexeme {id: 'lex_mundu'})
            MATCH (lex_uugi:Lexeme {id: 'lex_uugi'})
            
            CREATE (p1)-[:CONTAINS_LEXEME {position: 1, role: 'subject'}]->(lex_muti)
            CREATE (p2)-[:CONTAINS_LEXEME {position: 1, role: 'subject'}]->(lex_mundu)
            CREATE (p2)-[:CONTAINS_LEXEME {position: 2, role: 'modifier'}]->(lex_uugi)
            """
            session.run(relationships_query)
            logger.info("✅ Semantic relationships created")
    
    def create_rag_optimization(self) -> None:
        """Create structures specifically for RAG retrieval optimization."""
        with self.driver.session() as session:
            rag_query = """
            // Query patterns for translation requests
            CREATE (cultural_context_query:QueryPattern {
                id: 'cultural_context_request',
                pattern_type: 'cultural_explanation',
                typical_inputs: ['why this proverb', 'cultural meaning', 'context explanation'],
                retrieval_strategy: 'concept_expansion_with_context',
                target_node_types: ['CulturalConcept', 'UsageContext', 'SemanticField'],
                traversal_depth: 2
            })
            
            CREATE (similar_proverb_query:QueryPattern {
                id: 'similar_proverb_search',
                pattern_type: 'semantic_similarity',
                typical_inputs: ['similar proverbs', 'related sayings'],
                retrieval_strategy: 'embedding_similarity_plus_graph',
                target_node_types: ['Proverb', 'Translation'],
                traversal_depth: 3
            })
            
            // Retrieval paths optimized for oGRAG
            CREATE (proverb_to_culture:RetrievalPath {
                id: 'proverb_cultural_context',
                cypher_pattern: '(p:Proverb)-[:EMBODIES]->(c:CulturalConcept)-[:EXPRESSED_IN]->(ctx:UsageContext)',
                description: 'Retrieve cultural context for proverbs',
                use_case: 'cultural_explanation',
                expected_depth: 2,
                weight: 0.9
            })
            
            CREATE (concept_to_similar:RetrievalPath {
                id: 'concept_similar_proverbs', 
                cypher_pattern: '(c:CulturalConcept)<-[:EMBODIES]-(p1:Proverb), (c)<-[:EMBODIES]-(p2:Proverb)',
                description: 'Find proverbs sharing cultural concepts',
                use_case: 'similar_proverb_discovery',
                expected_depth: 2,
                weight: 0.85
            })
            """
            session.run(rag_query)
            logger.info("✅ RAG optimization structures created")
    
    def create_provenance_tracking(self) -> None:
        """Create comprehensive source and quality tracking."""
        with self.driver.session() as session:
            provenance_query = """
            // Source authorities
            CREATE (elder_interviews:Source {
                id: 'elder_interviews_2024',
                name: 'Elder Community Interviews',
                source_type: 'oral_tradition',
                authority_level: 'primary',
                reliability_score: 0.95,
                cultural_authenticity: 0.98,
                collection_method: 'structured_interviews',
                collection_location: 'central_kenya_kikuyu_regions',
                validation_method: 'elder_consensus',
                collection_date: date('2024-01-15')
            })
            
            CREATE (academic_literature:Source {
                id: 'published_research',
                name: 'Academic Literature',
                source_type: 'scholarly_publication',
                authority_level: 'secondary',
                reliability_score: 0.8,
                cultural_authenticity: 0.7,
                validation_method: 'peer_review'
            })
            
            // Connect sources to proverbs
            MATCH (p1:Proverb {id: 'prov_muti_munene'})
            MATCH (p2:Proverb {id: 'prov_mundu_muugi'})
            MATCH (elder_source:Source {id: 'elder_interviews_2024'})
            MATCH (academic_source:Source {id: 'published_research'})
            
            CREATE (p1)-[:SOURCED_FROM {confidence: 0.9}]->(elder_source)
            CREATE (p2)-[:SOURCED_FROM {confidence: 0.8}]->(elder_source)
            CREATE (p2)-[:SOURCED_FROM {confidence: 0.7}]->(academic_source)
            """
            session.run(provenance_query)
            logger.info("✅ Provenance tracking created")
    
    def setup_complete_ontology(self) -> None:
        """Execute complete ontology setup in proper order."""
        logger.info("🏗️  Creating linguistic foundation...")
        self.create_linguistic_foundation()
        
        logger.info("🎭 Creating cultural concepts...")
        self.create_cultural_concepts()
        
        logger.info("📍 Creating usage contexts...")
        self.create_usage_contexts()
        
        logger.info("🔄 Creating translation framework...")
        self.create_translation_framework()
        
        logger.info("📚 Creating sample proverbs...")
        self.create_sample_proverbs()
        
        logger.info("🌐 Creating translation variants...")
        self.create_translation_variants()
        
        logger.info("🔗 Creating semantic relationships...")
        self.create_semantic_relationships()
        
        logger.info("⚡ Creating RAG optimization...")
        self.create_rag_optimization()
        
        logger.info("📖 Creating provenance tracking...")
        self.create_provenance_tracking()
    
    def verify_enhanced_setup(self) -> Dict[str, Any]:
        """Comprehensive verification of the enhanced schema."""
        with self.driver.session() as session:
            # Check all node types
            node_labels = [
                'Proverb', 'CulturalConcept', 'SemanticField', 'DiscoursePattern',
                'UsageContext', 'Lexeme', 'Translation', 'TranslationStrategy',
                'QualityDimension', 'Source', 'QueryPattern', 'RetrievalPath',
                'MorphCategory'
            ]
            
            node_counts = {}
            for label in node_labels:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                record = result.single()
                count = record['count'] if record else 0
                node_counts[label] = count
                if count > 0:
                    logger.info(f"📊 {label}: {count} nodes")
            
            # Check relationship types
            rel_result = session.run("""
                MATCH ()-[r]->() 
                RETURN type(r) as rel_type, count(r) as count 
                ORDER BY count DESC
            """)
            
            relationships = {}
            for record in rel_result:
                relationships[record['rel_type']] = record['count']
                logger.info(f"🔗 {record['rel_type']}: {record['count']} relationships")
            
            # Check constraints and indexes
            constraints_result = session.run("SHOW CONSTRAINTS")
            constraints_count = len(list(constraints_result))
            
            indexes_result = session.run("SHOW INDEXES")
            indexes_count = len(list(indexes_result))
            
            return {
                'node_counts': node_counts,
                'relationship_counts': relationships,
                'constraints': constraints_count,
                'indexes': indexes_count,
                'total_nodes': sum(node_counts.values()),
                'total_relationships': sum(relationships.values())
            }
    
    def export_ontology_documentation(self) -> str:
        """Generate comprehensive ontology documentation."""
        stats = self.verify_enhanced_setup()
        
        documentation = f"""# Kikuyu Proverb oGRAG Ontology

## Overview
This ontology supports culturally faithful translation of Kikuyu proverbs into English,
designed specifically for retrieval-augmented generation (RAG) systems.

## Schema Statistics
- **Total Nodes**: {stats['total_nodes']}
- **Total Relationships**: {stats['total_relationships']}
- **Constraints**: {stats['constraints']}
- **Indexes**: {stats['indexes']}

## Core Node Types

### Primary Entities
"""
        
        primary_entities = ['Proverb', 'CulturalConcept', 'Translation', 'Lexeme']
        for entity in primary_entities:
            count = stats['node_counts'].get(entity, 0)
            documentation += f"- **{entity}**: {count} nodes\n"
        
        documentation += """
### Supporting Structures
"""
        supporting_entities = ['SemanticField', 'UsageContext', 'DiscoursePattern', 'TranslationStrategy']
        for entity in supporting_entities:
            count = stats['node_counts'].get(entity, 0)
            documentation += f"- **{entity}**: {count} nodes\n"
        
        documentation += f"""

## Key Relationships
"""
        for rel_type, count in stats['relationship_counts'].items():
            documentation += f"- **{rel_type}**: {count} connections\n"
        
        documentation += f"""

## oGRAG Features
1. **Multilingual Support**: Native Kikuyu with multiple English translations
2. **Cultural Preservation**: Rich cultural concept annotations
3. **Quality Assessment**: Multi-dimensional translation quality scoring
4. **Semantic Navigation**: Graph-based concept exploration
5. **RAG Optimization**: Full-text search and retrieval path optimization
6. **Provenance Tracking**: Source authority and validation metadata

## Usage for Translation Enhancement
The ontology enables LLMs to:
- Access cultural context for accurate interpretation
- Retrieve similar proverbs for translation consistency
- Assess translation quality across multiple dimensions
- Navigate semantic relationships for deeper understanding

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return documentation


def main() -> None:
    """Main function to set up the enhanced Kikuyu proverb ontology."""
    print("🚀 Setting up Enhanced Neo4j Schema for Kikuyu Proverb oGRAG...")
    print("🎯 Designed for culturally faithful translation with RAG optimization")
    
    # Use the correct password from docker-compose.yml
    ontology = KikuyuProverbOntology(password="ograg2025")
    
    try:
        # Safety check for database clearing
        print("\n⚠️  WARNING: This will modify your Neo4j database")
        response = input("Clear existing database and create fresh schema? (y/N): ")
        
        if response.lower() == 'y':
            ontology.clear_database()
        
        # Create constraints first (order matters)
        print("\n📋 Creating data integrity constraints...")
        ontology.create_constraints()
        
        # Create indexes for performance
        print("🔍 Creating performance indexes...")
        ontology.create_indexes()
        
        # Setup complete ontology structure
        print("🏗️  Setting up complete ontology...")
        ontology.setup_complete_ontology()
        
        # Verify everything was created correctly
        print("📊 Verifying schema setup...")
        stats = ontology.verify_enhanced_setup()
        
        # Generate documentation
        documentation = ontology.export_ontology_documentation()
        
        # Display results
        print("\n" + "="*70)
        print("🎉 KIKUYU PROVERB oGRAG ONTOLOGY COMPLETE!")
        print("="*70)
        print(f"📊 Created {stats['total_nodes']} nodes across {len([k for k,v in stats['node_counts'].items() if v > 0])} types")
        print(f"🔗 Created {stats['total_relationships']} relationships")
        print(f"📋 Applied {stats['constraints']} constraints")
        print(f"🔍 Created {stats['indexes']} indexes")
        
        print("\n🌐 Access Neo4j Browser: http://localhost:7474")
        print("🔑 Login: neo4j / ograg2025")
        print("🗃️  Database: kikuyu-kg")
        
        # Save documentation
        try:
            with open('kikuyu_ontology_documentation.md', 'w', encoding='utf-8') as f:
                f.write(documentation)
            print(f"\n📖 Documentation saved to: kikuyu_ontology_documentation.md")
            logger.info("📄 Documentation saved successfully")
        except Exception as e:
            logger.warning(f"⚠️  Could not save documentation: {e}")
        
        print("\n🎯 Next Steps:")
        print("1. Run this script to set up the ontology")
        print("2. Load your proverb data using the data import scripts")
        print("3. Generate embeddings for vector similarity search")
        print("4. Test RAG queries for translation enhancement")
        
    except Exception as e:
        logger.error(f"❌ Schema setup failed: {e}")
        raise
    finally:
        ontology.close()


if __name__ == "__main__":
    main()
