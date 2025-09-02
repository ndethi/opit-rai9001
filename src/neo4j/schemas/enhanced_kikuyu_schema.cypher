// Enhanced Kikuyu Proverb oGRAG Schema
// Cypher DDL for cultural ontology setup
// Best practices for low-resource language knowledge graphs

// ============================================================================
// CONSTRAINTS - Data Integrity for Cultural Preservation
// ============================================================================

// Core entity uniqueness
CREATE CONSTRAINT proverb_id_unique IF NOT EXISTS FOR (p:Proverb) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT proverb_kikuyu_unique IF NOT EXISTS FOR (p:Proverb) REQUIRE p.kikuyu_text IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:CulturalConcept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT lexeme_id_unique IF NOT EXISTS FOR (l:Lexeme) REQUIRE l.id IS UNIQUE;
CREATE CONSTRAINT translation_id_unique IF NOT EXISTS FOR (t:Translation) REQUIRE t.id IS UNIQUE;

// Essential properties
CREATE CONSTRAINT proverb_kikuyu_text IF NOT EXISTS FOR (p:Proverb) REQUIRE p.kikuyu_text IS NOT NULL;
CREATE CONSTRAINT concept_description IF NOT EXISTS FOR (c:CulturalConcept) REQUIRE c.description IS NOT NULL;
CREATE CONSTRAINT translation_source IF NOT EXISTS FOR (t:Translation) REQUIRE t.source_text IS NOT NULL;

// ============================================================================
// INDEXES - Performance Optimization for RAG Retrieval
// ============================================================================

// Full-text search indexes (critical for oGRAG)
CREATE FULLTEXT INDEX proverb_content_search IF NOT EXISTS 
FOR (p:Proverb) ON EACH [p.kikuyu_text, p.literal_translation, p.cultural_meaning];

CREATE FULLTEXT INDEX concept_content_search IF NOT EXISTS 
FOR (c:CulturalConcept) ON EACH [c.name, c.description, c.kikuyu_terms];

CREATE FULLTEXT INDEX translation_content_search IF NOT EXISTS 
FOR (t:Translation) ON EACH [t.source_text, t.target_text, t.translator_notes];

// Categorical indexes
CREATE INDEX semantic_field_domain IF NOT EXISTS FOR (sf:SemanticField) ON (sf.domain);
CREATE INDEX concept_category IF NOT EXISTS FOR (c:CulturalConcept) ON (c.category);
CREATE INDEX proverb_themes IF NOT EXISTS FOR (p:Proverb) ON (p.themes);

// Quality tracking indexes
CREATE INDEX translation_quality_score IF NOT EXISTS FOR (t:Translation) ON (t.quality_score);
CREATE INDEX proverb_validation_status IF NOT EXISTS FOR (p:Proverb) ON (p.validation_status);

// ============================================================================
// SAMPLE ONTOLOGY DATA - Cultural Foundation
// ============================================================================

// Core Semantic Fields for Kikuyu Culture
CREATE (kinship:SemanticField {
    id: 'kinship_relations',
    name: 'Kinship & Family',
    kikuyu_name: 'ũrata wa nyũmba',
    domain: 'social_structure',
    description: 'Family relationships, clan connections, and kinship obligations',
    cultural_importance: 'foundational'
});

CREATE (agriculture:SemanticField {
    id: 'agriculture_livelihood',
    name: 'Agriculture & Livelihood',
    kikuyu_name: 'ũrĩmi na mbeũ',
    domain: 'economic_activity', 
    description: 'Farming practices, land use, seasonal cycles',
    cultural_importance: 'foundational'
});

CREATE (wisdom_tradition:SemanticField {
    id: 'wisdom_knowledge',
    name: 'Wisdom & Knowledge',
    kikuyu_name: 'ũũgĩ na meciria',
    domain: 'epistemic_system',
    description: 'Traditional knowledge, wisdom practices, learning',
    cultural_importance: 'foundational'
});

// Cultural Concepts - Core Kikuyu Values
CREATE (ubuntu:CulturalConcept {
    id: 'ubuntu_umundu',
    name: 'Ubuntu/Ũmũndũ',
    category: 'core_philosophy',
    kikuyu_terms: ['ũmũndũ', 'ũrata', 'ũiguano'],
    description: 'Fundamental philosophy of shared humanity and mutual support',
    cultural_significance: 'foundational',
    translation_challenges: ['no_direct_equivalent', 'requires_explanation']
});

CREATE (ancestral_wisdom:CulturalConcept {
    id: 'ancestral_wisdom_tradition',
    name: 'Ancestral Wisdom',
    category: 'knowledge_system',
    kikuyu_terms: ['ũũgĩ wa aciari', 'mĩrũtanĩrĩ ya tene'],
    description: 'Wisdom and knowledge passed down from ancestors',
    cultural_significance: 'foundational',
    translation_challenges: ['cultural_specificity', 'sacred_knowledge']
});

CREATE (respect_authority:CulturalConcept {
    id: 'respect_hierarchy',
    name: 'Respect for Authority',
    category: 'social_values',
    kikuyu_terms: ['gĩtĩĩo', 'ũkuu', 'gwĩka ũkuu'],
    description: 'Cultural emphasis on respecting elders and social hierarchy',
    cultural_significance: 'high',
    translation_challenges: ['degree_of_formality', 'hierarchy_levels']
});

// Usage Contexts for Pragmatic Information
CREATE (elder_teaching:UsageContext {
    id: 'elder_wisdom_transmission',
    name: 'Elder Teaching',
    kikuyu_name: 'mũrutani wa athuuri',
    context_type: 'educational',
    formality_level: 'high',
    participants: ['mũthuri_mũkũrũ', 'aanake', 'airĩtu'],
    purpose: 'wisdom_transmission'
});

CREATE (ceremonial:UsageContext {
    id: 'ceremonial_occasions',
    name: 'Ceremonial Events',
    kikuyu_name: 'mĩhiko ya gĩkũyũ',
    context_type: 'ritual_ceremonial',
    formality_level: 'very_high',
    purpose: 'cultural_reinforcement'
});

// Translation Quality Framework
CREATE (linguistic_accuracy:QualityDimension {
    id: 'linguistic_fidelity',
    name: 'Linguistic Accuracy',
    description: 'Preservation of linguistic structure and meaning',
    weight: 0.35
});

CREATE (cultural_fidelity:QualityDimension {
    id: 'cultural_preservation',
    name: 'Cultural Fidelity', 
    description: 'Preservation of cultural concepts and contexts',
    weight: 0.40
});

CREATE (target_fluency:QualityDimension {
    id: 'english_naturalness',
    name: 'Target Language Fluency',
    description: 'Naturalness and readability in English',
    weight: 0.25
});

// Translation Strategies
CREATE (literal:TranslationStrategy {
    id: 'literal_preservation',
    name: 'Literal Translation',
    description: 'Word-for-word translation preserving structure',
    cultural_risk: 'medium'
});

CREATE (cultural_adaptation:TranslationStrategy {
    id: 'cultural_adaptation',
    name: 'Cultural Adaptation',
    description: 'Adaptation preserving cultural meaning over form',
    cultural_risk: 'low'
});

// ============================================================================
// SAMPLE PROVERBS - Demonstration Data
// ============================================================================

// Proverb 1: Community strength
CREATE (p1:Proverb {
    id: 'prov_muti_munene',
    kikuyu_text: 'Mũtĩ mũnene ndũkongoĩka na rũhũũ',
    phonetic_transcription: '[muti munene ndukongoika na ruhuu]',
    literal_translation: 'A big tree does not break with a small stick',
    cultural_meaning: 'Strong communities cannot be destroyed by minor conflicts',
    usage_notes: 'Used to encourage unity and discourage petty disputes',
    themes: ['unity', 'strength', 'community_resilience'],
    complexity_level: 'moderate',
    frequency_rating: 'common',
    validation_status: 'elder_verified',
    created_at: datetime(),
    last_updated: datetime()
});

// Proverb 2: Wisdom and patience
CREATE (p2:Proverb {
    id: 'prov_mundu_muugi',
    kikuyu_text: 'Mũndũ mũũgĩ ndarĩĩaga kĩrira kĩa hinya',
    phonetic_transcription: '[mundu muugi ndariaga kirira kia hinya]',
    literal_translation: 'A wise person does not eat strong food',
    cultural_meaning: 'Wise people avoid rushing into difficult situations without preparation',
    usage_notes: 'Advice about patience, careful consideration, and proper timing',
    themes: ['wisdom', 'patience', 'careful_planning'],
    complexity_level: 'simple',
    frequency_rating: 'very_common',
    validation_status: 'multiple_sources',
    created_at: datetime(),
    last_updated: datetime()
});

// Key Lexemes for Linguistic Analysis
CREATE (lex_muti:Lexeme {
    id: 'lex_muti',
    surface_form: 'mũtĩ',
    root: 'ti',
    noun_class: '3/4',
    plural_form: 'mĩtĩ',
    english_glosses: ['tree', 'plant', 'wood'],
    cultural_associations: ['strength', 'growth', 'community_symbol'],
    metaphorical_uses: ['community', 'lineage', 'stability']
});

CREATE (lex_uugi:Lexeme {
    id: 'lex_uugi',
    surface_form: 'ũũgĩ',
    root: 'ug',
    noun_class: '14',
    english_glosses: ['wisdom', 'intelligence', 'cleverness'],
    cultural_associations: ['elder_knowledge', 'life_experience'],
    metaphorical_uses: ['guidance', 'insight']
});

// High-Quality Translations
CREATE (t1_cultural:Translation {
    id: 'trans_p1_cultural',
    source_text: 'Mũtĩ mũnene ndũkongoĩka na rũhũũ',
    target_text: 'Strong communities withstand minor challenges',
    translation_type: 'cultural_adaptation',
    quality_score: 0.88,
    linguistic_accuracy: 0.7,
    cultural_fidelity: 0.95,
    target_fluency: 0.9,
    translator_notes: 'Focuses on cultural meaning over literal form',
    created_at: datetime()
});

CREATE (t2_cultural:Translation {
    id: 'trans_p2_cultural',
    source_text: 'Mũndũ mũũgĩ ndarĩĩaga kĩrira kĩa hinya',
    target_text: 'Wise people avoid difficult situations without proper preparation',
    translation_type: 'cultural_adaptation',
    quality_score: 0.91,
    linguistic_accuracy: 0.8,
    cultural_fidelity: 0.95,
    target_fluency: 0.95,
    translator_notes: 'Explains the metaphor for clarity',
    created_at: datetime()
});

// Sources for Provenance Tracking
CREATE (elder_source:Source {
    id: 'elder_interviews_2024',
    name: 'Elder Community Interviews',
    source_type: 'oral_tradition',
    authority_level: 'primary',
    reliability_score: 0.95,
    cultural_authenticity: 0.98,
    collection_location: 'central_kenya_kikuyu_regions'
});

// ============================================================================
// RELATIONSHIPS - Semantic Connections
// ============================================================================

// Connect proverbs to semantic domains
CREATE (p1)-[:BELONGS_TO_FIELD {relevance: 0.8}]->(kinship);
CREATE (p2)-[:BELONGS_TO_FIELD {relevance: 0.9}]->(wisdom_tradition);

// Connect to cultural concepts
CREATE (p1)-[:EMBODIES {strength: 0.9, confidence: 0.85}]->(ubuntu);
CREATE (p2)-[:EMBODIES {strength: 0.85, confidence: 0.9}]->(ancestral_wisdom);

// Connect to usage contexts
CREATE (p1)-[:APPROPRIATE_IN {frequency: 'common', effectiveness: 0.8}]->(elder_teaching);
CREATE (p1)-[:APPROPRIATE_IN {frequency: 'occasional', effectiveness: 0.7}]->(ceremonial);
CREATE (p2)-[:APPROPRIATE_IN {frequency: 'very_common', effectiveness: 0.9}]->(elder_teaching);

// Connect translations
CREATE (p1)-[:HAS_TRANSLATION]->(t1_cultural);
CREATE (p2)-[:HAS_TRANSLATION]->(t2_cultural);

// Connect to sources
CREATE (p1)-[:SOURCED_FROM {confidence: 0.9}]->(elder_source);
CREATE (p2)-[:SOURCED_FROM {confidence: 0.8}]->(elder_source);

// Connect lexemes to proverbs
CREATE (p1)-[:CONTAINS_LEXEME {position: 1, role: 'subject'}]->(lex_muti);
CREATE (p2)-[:CONTAINS_LEXEME {position: 2, role: 'modifier'}]->(lex_uugi);

// ============================================================================
// RAG OPTIMIZATION QUERIES - Sample Retrieval Patterns
// ============================================================================

// Query 1: Find culturally similar proverbs
// MATCH (p1:Proverb)-[:EMBODIES]->(c:CulturalConcept)<-[:EMBODIES]-(p2:Proverb)
// WHERE p1.kikuyu_text CONTAINS $search_term
// RETURN p1, p2, c
// ORDER BY c.cultural_significance DESC;

// Query 2: Get cultural context for translation
// MATCH (p:Proverb {kikuyu_text: $kikuyu_text})-[:EMBODIES]->(c:CulturalConcept)
// MATCH (p)-[:APPROPRIATE_IN]->(ctx:UsageContext)
// RETURN p, c, ctx;

// Query 3: Find best translation by quality
// MATCH (p:Proverb {kikuyu_text: $kikuyu_text})-[:HAS_TRANSLATION]->(t:Translation)
// RETURN t
// ORDER BY t.quality_score DESC
// LIMIT 1;

// ============================================================================
// VERIFICATION QUERIES
// ============================================================================

// Check schema completeness
// MATCH (n) RETURN labels(n) as node_type, count(n) as count ORDER BY count DESC;

// Check relationship distribution  
// MATCH ()-[r]->() RETURN type(r) as relationship, count(r) as count ORDER BY count DESC;

// Validate cultural concept coverage
// MATCH (p:Proverb)-[:EMBODIES]->(c:CulturalConcept)
// RETURN c.name, c.cultural_significance, count(p) as proverb_count
// ORDER BY proverb_count DESC;
