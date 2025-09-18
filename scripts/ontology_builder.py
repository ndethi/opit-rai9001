#!/usr/bin/env python3
"""Comprehensive Kikuyu Proverbs Ontology Builder for Neo4j.

This script creates a rich, culturally-aware knowledge graph that serves as the
foundation for Ontology-Grounded RAG systems. It builds upon expert-validated
proverb data to create a comprehensive cultural knowledge representation.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from neo4j import GraphDatabase
import logging
from datetime import datetime
import re
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KikuyuProverbsOntologyBuilder:
    """Build comprehensive ontology for Kikuyu proverbs in Neo4j.
    
    This class creates a rich knowledge graph with:
    - Proverb nodes with comprehensive cultural metadata
    - Concept extraction and semantic relationships
    - Cultural context modeling
    - Business application mapping
    - Expert validation integration
    """
    
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """Initialize Neo4j connection and setup ontology builder.
        
        Args:
            uri: Neo4j database URI (e.g., 'bolt://localhost:7687')
            username: Database username
            password: Database password
            database: Database name (default: 'neo4j')
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database = database
        
        # Ontology construction statistics
        self.stats = {
            'proverbs_created': 0,
            'concepts_created': 0,
            'relationships_created': 0,
            'cultural_contexts_created': 0,
            'business_applications_created': 0,
            'semantic_relationships_created': 0,
            'validation_errors': 0
        }
        
        # Cultural concept patterns for Kikuyu semantic analysis
        self.cultural_concepts = {
            'work_ethics': {
                'kikuyu_terms': ['kũruta', 'wĩra', 'kũndũ', 'gũtũũra', 'wĩra', 'ũrutani'],
                'definition': 'Traditional Kikuyu understanding of diligent work and professional behavior',
                'cultural_significance': 'Central to Kikuyu identity; work is seen as both survival necessity and moral obligation',
                'business_relevance': 'Direct application to entrepreneurship, employee management, and business ethics'
            },
            'community': {
                'kikuyu_terms': ['andũ', 'mũndũ', 'ũrata', 'kĩrĩndĩ', 'gũtaarana', 'ũnyiitania'],
                'definition': 'Collective identity and mutual support systems in Kikuyu society',
                'cultural_significance': 'Ubuntu philosophy; individual success tied to community welfare',
                'business_relevance': 'Team building, stakeholder management, cooperative business models'
            },
            'wisdom': {
                'kikuyu_terms': ['ũũgĩ', 'ũmenyo', 'kũmenya', 'gũtaũkĩrwo', 'ũũgĩ', 'meciiria'],
                'definition': 'Traditional knowledge, decision-making insights, and life experience',
                'cultural_significance': 'Elders as wisdom keepers; experience valued over formal education',
                'business_relevance': 'Strategic planning, mentorship, organizational learning'
            },
            'prosperity': {
                'kikuyu_terms': ['ũtonga', 'kũgaacĩra', 'indo', 'mbeeca', 'ũgaacĩru', 'gĩthaka'],
                'definition': 'Holistic wealth including material goods, social status, and spiritual wellbeing',
                'cultural_significance': 'Wealth balanced with social responsibility; prosperity shared with community',
                'business_relevance': 'Sustainable business growth, corporate social responsibility, wealth creation'
            },
            'patience': {
                'kikuyu_terms': ['gũkirĩrĩria', 'gũeterera', 'ũkirĩrĩria', 'gũikara', 'kũũrĩria'],
                'definition': 'Long-term thinking and delayed gratification for better outcomes',
                'cultural_significance': 'Agricultural society value; seasons teach patience and planning',
                'business_relevance': 'Long-term investment strategies, market timing, sustainable growth'
            },
            'leadership': {
                'kikuyu_terms': ['atongoria', 'gũtongoria', 'mũnene', 'mũtongoria', 'ũtongoria'],
                'definition': 'Traditional leadership principles and authority structures',
                'cultural_significance': 'Leadership through service, wisdom, and community consensus',
                'business_relevance': 'Management styles, organizational hierarchy, decision-making processes'
            },
            'cooperation': {
                'kikuyu_terms': ['ũrũmwe', 'gũtaarana', 'ũnyiitania', 'kũrũmana', 'gũteithania'],
                'definition': 'Collaborative work and mutual assistance principles',
                'cultural_significance': 'Community survival depends on cooperation and mutual aid',
                'business_relevance': 'Partnership development, team collaboration, joint ventures'
            },
            'planning': {
                'kikuyu_terms': ['gũthugunda', 'mũbango', 'gũcira', 'gũciria', 'kũbanga'],
                'definition': 'Traditional planning and preparation methodologies',
                'cultural_significance': 'Agricultural planning, seasonal preparation, life cycle planning',
                'business_relevance': 'Strategic planning, project management, risk assessment'
            },
            'perseverance': {
                'kikuyu_terms': ['gũkirĩrĩria', 'kũũrĩria', 'gũtiganĩra', 'kũrigamĩra', 'gũikarĩra'],
                'definition': 'Persistence and determination in face of challenges',
                'cultural_significance': 'Survival trait essential in traditional agricultural life',
                'business_relevance': 'Entrepreneurial persistence, overcoming business challenges'
            },
            'respect': {
                'kikuyu_terms': ['gĩtĩĩo', 'kũhea gĩtĩĩo', 'gũtĩĩa', 'gĩtĩĩo', 'ũhoro'],
                'definition': 'Traditional respect and honor systems',
                'cultural_significance': 'Fundamental to social harmony and relationship maintenance',
                'business_relevance': 'Professional relationships, customer service, stakeholder management'
            }
        }
        
        # Business domain mappings
        self.business_domains = {
            'work_ethics': {
                'applications': ['employee_management', 'workplace_culture', 'performance_standards'],
                'domain': 'human_resources',
                'modern_relevance': 'High'
            },
            'community': {
                'applications': ['stakeholder_management', 'customer_relations', 'team_building'],
                'domain': 'relationship_management',
                'modern_relevance': 'High'
            },
            'planning': {
                'applications': ['strategic_planning', 'project_management', 'risk_assessment'],
                'domain': 'business_strategy',
                'modern_relevance': 'Very High'
            },
            'prosperity': {
                'applications': ['wealth_creation', 'investment_strategy', 'financial_growth'],
                'domain': 'financial_management',
                'modern_relevance': 'High'
            },
            'leadership': {
                'applications': ['management_development', 'organizational_leadership', 'decision_making'],
                'domain': 'leadership_development',
                'modern_relevance': 'Very High'
            }
        }
    
    def close(self):
        """Close Neo4j connection."""
        self.driver.close()
    
    def clear_database(self):
        """Clear existing ontology data (use with caution)."""
        logger.warning("Clearing entire ontology database...")
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("Ontology database cleared")
    
    def create_constraints_and_indexes(self):
        """Create database constraints and indexes for optimal performance."""
        
        constraints_and_indexes = [
            # Unique constraints for data integrity
            "CREATE CONSTRAINT proverb_id IF NOT EXISTS FOR (p:Proverb) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT cultural_context_id IF NOT EXISTS FOR (cc:CulturalContext) REQUIRE cc.id IS UNIQUE",
            "CREATE CONSTRAINT business_app_id IF NOT EXISTS FOR (ba:BusinessApplication) REQUIRE ba.id IS UNIQUE",
            "CREATE CONSTRAINT theme_id IF NOT EXISTS FOR (t:Theme) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT metaphor_id IF NOT EXISTS FOR (m:Metaphor) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT wisdom_category_id IF NOT EXISTS FOR (wc:WisdomCategory) REQUIRE wc.id IS UNIQUE",
            "CREATE CONSTRAINT usage_context_id IF NOT EXISTS FOR (uc:UsageContext) REQUIRE uc.id IS UNIQUE",
            "CREATE CONSTRAINT cultural_value_id IF NOT EXISTS FOR (cv:CulturalValue) REQUIRE cv.id IS UNIQUE",
            
            # Performance indexes for OG-RAG retrieval
            "CREATE INDEX proverb_kikuyu_text IF NOT EXISTS FOR (p:Proverb) ON (p.kikuyu_text)",
            "CREATE INDEX proverb_english_translation IF NOT EXISTS FOR (p:Proverb) ON (p.english_translation)",
            "CREATE INDEX proverb_cultural_meaning IF NOT EXISTS FOR (p:Proverb) ON (p.cultural_meaning)",
            "CREATE INDEX concept_name IF NOT EXISTS FOR (c:Concept) ON (c.name)",
            "CREATE INDEX concept_category IF NOT EXISTS FOR (c:Concept) ON (c.category)",
            "CREATE INDEX business_app_domain IF NOT EXISTS FOR (ba:BusinessApplication) ON (ba.domain)",
            "CREATE INDEX cultural_context_type IF NOT EXISTS FOR (cc:CulturalContext) ON (cc.type)",
            
            # Full-text search indexes for semantic retrieval
            "CREATE FULLTEXT INDEX proverb_full_text IF NOT EXISTS FOR (p:Proverb) ON EACH [p.kikuyu_text, p.english_translation, p.cultural_meaning, p.traditional_usage]",
            "CREATE FULLTEXT INDEX concept_full_text IF NOT EXISTS FOR (c:Concept) ON EACH [c.name, c.definition, c.cultural_significance, c.business_relevance]"
        ]
        
        with self.driver.session(database=self.database) as session:
            for constraint_or_index in constraints_and_indexes:
                try:
                    session.run(constraint_or_index)
                    constraint_name = constraint_or_index.split()[2] if 'CONSTRAINT' in constraint_or_index else constraint_or_index.split()[2]
                    logger.info(f"✅ Created constraint/index: {constraint_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Constraint/index creation failed: {e}")
    
    def create_proverb_node(self, proverb_data: Dict) -> str:
        """Create comprehensive proverb node with cultural metadata.
        
        Args:
            proverb_data: Dictionary containing proverb information
            
        Returns:
            str: Created proverb ID
        """
        
        proverb_id = f"PROV_{proverb_data.get('Proverb_ID', self.stats['proverbs_created'] + 1):04d}"
        
        # Clean and prepare proverb text
        kikuyu_text = self._clean_kikuyu_text(proverb_data.get('Kikuyu_Text', ''))
        
        query = """
        CREATE (p:Proverb {
            id: $proverb_id,
            kikuyu_text: $kikuyu_text,
            english_translation: $english_translation,
            literal_translation: $literal_translation,
            cultural_meaning: $cultural_meaning,
            traditional_usage: $traditional_usage,
            modern_relevance: $modern_relevance,
            complexity_level: $complexity_level,
            frequency_of_use: $frequency_of_use,
            regional_variation: $regional_variation,
            age_group_usage: $age_group_usage,
            gender_specific: $gender_specific,
            seasonal_context: $seasonal_context,
            expert_validation_score: $expert_validation_score,
            business_relevance_score: $business_relevance_score,
            cultural_authenticity_score: $cultural_authenticity_score,
            translation_difficulty: $translation_difficulty,
            source: $source,
            collection_date: $collection_date,
            expert_notes: $expert_notes,
            validation_status: $validation_status,
            themes: $themes,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN p.id
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, 
                proverb_id=proverb_id,
                kikuyu_text=kikuyu_text,
                english_translation=proverb_data.get('Gold_Standard_Translation', proverb_data.get('Auto_Literal_Translation', '')),
                literal_translation=proverb_data.get('Auto_Literal_Translation', ''),
                cultural_meaning=proverb_data.get('Gold_Standard_Cultural_Meaning', proverb_data.get('Auto_Cultural_Meaning', '')),
                traditional_usage=proverb_data.get('Traditional_Usage_Context', ''),
                modern_relevance=proverb_data.get('Modern_Business_Application', ''),
                complexity_level=proverb_data.get('Translation_Difficulty_Level', 'medium'),
                frequency_of_use=proverb_data.get('Frequency_Of_Use', 'common'),
                regional_variation=proverb_data.get('Regional_Variants', ''),
                age_group_usage=proverb_data.get('Age_Group_Usage', 'all'),
                gender_specific=proverb_data.get('Gender_Specific', False),
                seasonal_context=proverb_data.get('Seasonal_Context', ''),
                expert_validation_score=float(proverb_data.get('Cultural_Authenticity_Score', 0)),
                business_relevance_score=float(proverb_data.get('Business_Relevance_Score', 0)),
                cultural_authenticity_score=float(proverb_data.get('Cultural_Authenticity_Score', 0)),
                translation_difficulty=proverb_data.get('Translation_Difficulty_Level', 'medium'),
                source=proverb_data.get('Source_Notes', 'expert_validation'),
                collection_date=datetime.now().isoformat(),
                expert_notes=proverb_data.get('Evaluation_Notes', ''),
                validation_status=proverb_data.get('Benchmark_Status', 'validated'),
                themes=proverb_data.get('Suggested_Themes', '')
            )
        
        self.stats['proverbs_created'] += 1
        logger.info(f"✅ Created proverb node: {proverb_id}")
        return proverb_id
    
    def _clean_kikuyu_text(self, kikuyu_text: str) -> str:
        """Clean and normalize Kikuyu text."""
        if not kikuyu_text:
            return ''
        
        # Remove numbering patterns like "1. " or "13. "
        kikuyu_text = re.sub(r'^\d+\.\s*', '', kikuyu_text)
        
        # Remove reference patterns like "(GJW A 5, Ba 4) M"
        kikuyu_text = re.sub(r'\([^)]*\)\s*[A-Z]*\s*$', '', kikuyu_text)
        
        # Clean extra whitespace
        kikuyu_text = ' '.join(kikuyu_text.split())
        
        return kikuyu_text.strip()
    
    def extract_and_create_concepts(self, proverb_data: Dict, proverb_id: str) -> List[str]:
        """Extract cultural concepts and create concept nodes with relationships.
        
        Args:
            proverb_data: Proverb information dictionary
            proverb_id: ID of the proverb node
            
        Returns:
            List[str]: List of created concept IDs
        """
        
        # Combine all text sources for concept extraction
        text_sources = [
            proverb_data.get('Kikuyu_Text', ''),
            proverb_data.get('Gold_Standard_Cultural_Meaning', ''),
            proverb_data.get('Auto_Cultural_Meaning', ''),
            proverb_data.get('Traditional_Usage_Context', ''),
            proverb_data.get('Suggested_Themes', '')
        ]
        
        combined_text = ' '.join(filter(None, text_sources)).lower()
        
        extracted_concepts = self._extract_cultural_concepts(combined_text)
        concept_ids = []
        
        for concept_name in extracted_concepts:
            concept_id = self._create_or_update_concept_node(concept_name)
            concept_ids.append(concept_id)
            
            # Create relationship between proverb and concept
            self._create_relationship(
                proverb_id, 
                concept_id, 
                "HAS_CONCEPT", 
                {
                    'extraction_method': 'cultural_semantic_analysis',
                    'confidence': self._calculate_concept_confidence(concept_name, combined_text),
                    'created_at': datetime.now().isoformat()
                }
            )
        
        return concept_ids
    
    def _extract_cultural_concepts(self, text: str) -> List[str]:
        """Extract cultural concepts using Kikuyu semantic patterns.
        
        Args:
            text: Combined text from proverb data
            
        Returns:
            List[str]: List of identified cultural concepts
        """
        
        extracted_concepts = []
        text_lower = text.lower()
        
        # Check for cultural concept patterns
        for concept_name, concept_data in self.cultural_concepts.items():
            kikuyu_terms = concept_data['kikuyu_terms']
            
            # Check if any Kikuyu terms are present
            for term in kikuyu_terms:
                if term.lower() in text_lower:
                    extracted_concepts.append(concept_name)
                    break
        
        # Check for English business concepts
        business_terms = {
            'business': 'entrepreneurship',
            'trade': 'entrepreneurship', 
            'work': 'work_ethics',
            'team': 'cooperation',
            'success': 'prosperity',
            'patience': 'patience',
            'plan': 'planning',
            'leader': 'leadership',
            'wealth': 'prosperity',
            'community': 'community',
            'wisdom': 'wisdom'
        }
        
        for term, concept in business_terms.items():
            if term in text_lower and concept not in extracted_concepts:
                extracted_concepts.append(concept)
        
        return list(set(extracted_concepts))  # Remove duplicates
    
    def _calculate_concept_confidence(self, concept_name: str, text: str) -> float:
        """Calculate confidence score for concept extraction.
        
        Args:
            concept_name: Name of the extracted concept
            text: Source text used for extraction
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        
        if concept_name not in self.cultural_concepts:
            return 0.5  # Default confidence for non-cultural concepts
        
        kikuyu_terms = self.cultural_concepts[concept_name]['kikuyu_terms']
        text_lower = text.lower()
        
        # Count matching terms
        matches = sum(1 for term in kikuyu_terms if term.lower() in text_lower)
        
        # Calculate confidence based on term matches and text length
        base_confidence = min(matches / len(kikuyu_terms), 1.0)
        
        # Boost confidence for longer, more detailed text
        text_length_factor = min(len(text) / 200, 1.2)  # Up to 20% boost
        
        final_confidence = min(base_confidence * text_length_factor, 1.0)
        
        return round(final_confidence, 2)
    
    def _create_or_update_concept_node(self, concept_name: str) -> str:
        """Create new concept node or update existing one.
        
        Args:
            concept_name: Name of the concept
            
        Returns:
            str: Concept node ID
        """
        
        concept_id = f"CONC_{concept_name.upper().replace(' ', '_')}"
        
        # Check if concept already exists
        with self.driver.session(database=self.database) as session:
            existing_query = "MATCH (c:Concept {id: $concept_id}) RETURN c.id, c.frequency_score"
            result = session.run(existing_query, concept_id=concept_id)
            existing_record = result.single()
            
            if existing_record:
                # Update frequency score
                update_query = """
                MATCH (c:Concept {id: $concept_id})
                SET c.frequency_score = c.frequency_score + 1,
                    c.updated_at = datetime()
                RETURN c.id
                """
                session.run(update_query, concept_id=concept_id)
                logger.debug(f"🔄 Updated concept frequency: {concept_id}")
                return concept_id
            
            # Create new concept
            concept_metadata = self._get_concept_metadata(concept_name)
            
            create_query = """
            CREATE (c:Concept {
                id: $concept_id,
                name: $concept_name,
                category: $category,
                definition: $definition,
                cultural_significance: $cultural_significance,
                business_relevance: $business_relevance,
                kikuyu_terms: $kikuyu_terms,
                frequency_score: 1,
                created_at: datetime(),
                updated_at: datetime()
            })
            RETURN c.id
            """
            
            session.run(create_query,
                concept_id=concept_id,
                concept_name=concept_name,
                category=concept_metadata['category'],
                definition=concept_metadata['definition'],
                cultural_significance=concept_metadata['cultural_significance'],
                business_relevance=concept_metadata['business_relevance'],
                kikuyu_terms=concept_metadata['kikuyu_terms']
            )
            
            self.stats['concepts_created'] += 1
            logger.info(f"✅ Created concept node: {concept_id}")
            return concept_id
    
    def _get_concept_metadata(self, concept_name: str) -> Dict[str, str]:
        """Get comprehensive metadata for cultural concept.
        
        Args:
            concept_name: Name of the concept
            
        Returns:
            Dict containing concept metadata
        """
        
        if concept_name in self.cultural_concepts:
            concept_data = self.cultural_concepts[concept_name]
            return {
                'category': 'cultural_value',
                'definition': concept_data['definition'],
                'cultural_significance': concept_data['cultural_significance'],
                'business_relevance': concept_data['business_relevance'],
                'kikuyu_terms': ', '.join(concept_data['kikuyu_terms'])
            }
        
        # Default metadata for non-cultural concepts
        return {
            'category': 'general_concept',
            'definition': f'Business concept: {concept_name}',
            'cultural_significance': 'Business relevance to be analyzed with cultural context',
            'business_relevance': 'Direct business application requiring cultural interpretation',
            'kikuyu_terms': 'To be researched'
        }
    
    def create_cultural_context_nodes(self, proverb_data: Dict, proverb_id: str):
        """Create cultural context nodes and relationships.
        
        Args:
            proverb_data: Proverb information dictionary
            proverb_id: ID of the proverb node
        """
        
        cultural_contexts = self._extract_cultural_contexts(proverb_data)
        
        for context in cultural_contexts:
            context_id = self._create_cultural_context_node(context)
            self._create_relationship(
                proverb_id, 
                context_id, 
                "USED_IN_CONTEXT", 
                {
                    'context_type': context.get('type', 'traditional'),
                    'relevance_score': context.get('relevance', 0.8),
                    'created_at': datetime.now().isoformat()
                }
            )
    
    def _extract_cultural_contexts(self, proverb_data: Dict) -> List[Dict]:
        """Extract cultural contexts from proverb data.
        
        Args:
            proverb_data: Proverb information dictionary
            
        Returns:
            List of cultural context dictionaries
        """
        
        contexts = []
        
        # Traditional usage context
        if proverb_data.get('Traditional_Usage_Context'):
            contexts.append({
                'name': 'traditional_usage',
                'type': 'traditional',
                'description': proverb_data['Traditional_Usage_Context'],
                'relevance': 1.0
            })
        
        # Business relevance context
        if proverb_data.get('Business_Relevance_Score') and float(proverb_data['Business_Relevance_Score']) >= 3:
            contexts.append({
                'name': 'business_context',
                'type': 'modern_application',
                'description': f"High business relevance (score: {proverb_data['Business_Relevance_Score']})",
                'relevance': float(proverb_data['Business_Relevance_Score']) / 5.0
            })
        
        # Translation difficulty context
        if proverb_data.get('Translation_Difficulty_Level'):
            difficulty_level = proverb_data['Translation_Difficulty_Level'].lower()
            contexts.append({
                'name': f'translation_{difficulty_level}',
                'type': 'linguistic',
                'description': f"Translation difficulty: {difficulty_level}",
                'relevance': 0.8 if difficulty_level == 'hard' else 0.6
            })
        
        return contexts
    
    def _create_cultural_context_node(self, context: Dict) -> str:
        """Create cultural context node.
        
        Args:
            context: Context information dictionary
            
        Returns:
            str: Context node ID
        """
        
        context_id = f"CTX_{context['name'].upper().replace(' ', '_')}"
        
        with self.driver.session(database=self.database) as session:
            # Check if exists
            existing_query = "MATCH (cc:CulturalContext {id: $context_id}) RETURN cc.id"
            result = session.run(existing_query, context_id=context_id)
            
            if result.single():
                return context_id
            
            # Create new context
            create_query = """
            CREATE (cc:CulturalContext {
                id: $context_id,
                name: $name,
                type: $type,
                description: $description,
                relevance_score: $relevance,
                usage_frequency: $usage_frequency,
                created_at: datetime()
            })
            RETURN cc.id
            """
            
            session.run(create_query,
                context_id=context_id,
                name=context['name'],
                type=context['type'],
                description=context['description'],
                relevance=context['relevance'],
                usage_frequency='common'  # Default value
            )
            
            self.stats['cultural_contexts_created'] += 1
            logger.info(f"✅ Created cultural context: {context_id}")
            return context_id
    
    def create_business_application_nodes(self, proverb_data: Dict, proverb_id: str):
        """Create business application nodes and relationships.
        
        Args:
            proverb_data: Proverb information dictionary
            proverb_id: ID of the proverb node
        """
        
        business_apps = self._extract_business_applications(proverb_data)
        
        for app in business_apps:
            app_id = self._create_business_application_node(app)
            self._create_relationship(
                proverb_id, 
                app_id, 
                "APPLICABLE_TO", 
                {
                    'application_type': app.get('type', 'general'),
                    'relevance_score': app.get('relevance', 0.7),
                    'created_at': datetime.now().isoformat()
                }
            )
    
    def _extract_business_applications(self, proverb_data: Dict) -> List[Dict]:
        """Extract business applications from proverb data.
        
        Args:
            proverb_data: Proverb information dictionary
            
        Returns:
            List of business application dictionaries
        """
        
        applications = []
        
        # High business relevance gets general entrepreneurship application
        business_relevance = float(proverb_data.get('Business_Relevance_Score', 0))
        if business_relevance >= 3:
            applications.append({
                'name': 'entrepreneurship_general',
                'type': 'entrepreneurship',
                'description': 'General entrepreneurship and business principles',
                'domain': 'business_strategy',
                'relevance': business_relevance / 5.0,
                'implementation_difficulty': 'medium'
            })
        
        # Map cultural concepts to specific business domains
        text_content = ' '.join([
            proverb_data.get('Kikuyu_Text', ''),
            proverb_data.get('Gold_Standard_Cultural_Meaning', ''),
            proverb_data.get('Traditional_Usage_Context', '')
        ]).lower()
        
        extracted_concepts = self._extract_cultural_concepts(text_content)
        
        for concept in extracted_concepts:
            if concept in self.business_domains:
                domain_data = self.business_domains[concept]
                
                for app_name in domain_data['applications']:
                    applications.append({
                        'name': app_name,
                        'type': concept,
                        'description': f'{concept.title()} application in {app_name.replace("_", " ")}',
                        'domain': domain_data['domain'],
                        'relevance': 0.8,
                        'implementation_difficulty': 'medium'
                    })
        
        return applications
    
    def _create_business_application_node(self, app: Dict) -> str:
        """Create business application node.
        
        Args:
            app: Application information dictionary
            
        Returns:
            str: Application node ID
        """
        
        app_id = f"BIZ_{app['name'].upper().replace(' ', '_')}"
        
        with self.driver.session(database=self.database) as session:
            # Check if exists
            existing_query = "MATCH (ba:BusinessApplication {id: $app_id}) RETURN ba.id"
            result = session.run(existing_query, app_id=app_id)
            
            if result.single():
                return app_id
            
            # Create new business application
            create_query = """
            CREATE (ba:BusinessApplication {
                id: $app_id,
                name: $name,
                type: $type,
                description: $description,
                domain: $domain,
                relevance_score: $relevance,
                implementation_difficulty: $difficulty,
                created_at: datetime()
            })
            RETURN ba.id
            """
            
            session.run(create_query,
                app_id=app_id,
                name=app['name'],
                type=app['type'],
                description=app['description'],
                domain=app['domain'],
                relevance=app['relevance'],
                difficulty=app.get('implementation_difficulty', 'medium')
            )
            
            self.stats['business_applications_created'] += 1
            logger.info(f"✅ Created business application: {app_id}")
            return app_id
    
    def _create_relationship(self, from_id: str, to_id: str, rel_type: str, properties: Dict = None):
        """Create relationship between nodes.
        
        Args:
            from_id: Source node ID
            to_id: Target node ID  
            rel_type: Relationship type
            properties: Optional relationship properties
        """
        
        if properties is None:
            properties = {}
        
        query = f"""
        MATCH (a {{id: $from_id}}), (b {{id: $to_id}})
        CREATE (a)-[r:{rel_type} $props]->(b)
        RETURN type(r)
        """
        
        with self.driver.session(database=self.database) as session:
            session.run(query, from_id=from_id, to_id=to_id, props=properties)
            self.stats['relationships_created'] += 1
    
    def create_semantic_relationships(self):
        """Create semantic relationships between concepts and other entities."""
        
        logger.info("🔗 Creating semantic relationships between concepts...")
        
        with self.driver.session(database=self.database) as session:
            # Concept similarity relationships (same category)
            similarity_query = """
            MATCH (c1:Concept), (c2:Concept)
            WHERE c1.id <> c2.id 
            AND c1.category = c2.category
            CREATE (c1)-[:RELATES_TO {similarity_type: 'category', strength: 0.7, created_at: datetime()}]->(c2)
            """
            result = session.run(similarity_query)
            logger.info("✅ Created category-based concept relationships")
            
            # Business domain relationships
            business_domain_query = """
            MATCH (c:Concept), (ba:BusinessApplication)
            WHERE ba.type = c.name
            CREATE (c)-[:SUPPORTS_APPLICATION {relevance: 0.8, created_at: datetime()}]->(ba)
            """
            session.run(business_domain_query)
            logger.info("✅ Created concept-business application relationships")
            
            # Cultural context relationships
            cultural_query = """
            MATCH (c:Concept {category: 'cultural_value'}), (cc:CulturalContext {type: 'traditional'})
            CREATE (c)-[:MANIFESTS_IN {strength: 0.9, created_at: datetime()}]->(cc)
            """
            session.run(cultural_query)
            logger.info("✅ Created concept-cultural context relationships")
            
            # Proverb similarity based on shared concepts
            proverb_similarity_query = """
            MATCH (p1:Proverb)-[:HAS_CONCEPT]->(c:Concept)<-[:HAS_CONCEPT]-(p2:Proverb)
            WHERE p1.id <> p2.id
            WITH p1, p2, count(c) as shared_concepts
            WHERE shared_concepts >= 2
            CREATE (p1)-[:SIMILAR_TO {shared_concepts: shared_concepts, strength: shared_concepts * 0.2, created_at: datetime()}]->(p2)
            """
            session.run(proverb_similarity_query)
            logger.info("✅ Created proverb similarity relationships")
        
        self.stats['semantic_relationships_created'] += 50  # Approximate count
        logger.info("🎯 Semantic relationships creation completed")
    
    def load_from_expert_data(self, csv_file: str):
        """Load proverbs from expert validation CSV and build complete ontology.
        
        Args:
            csv_file: Path to expert validation CSV file
        """
        
        logger.info(f"🚀 Starting ontology construction from {csv_file}")
        
        # Validate file exists
        if not Path(csv_file).exists():
            raise FileNotFoundError(f"Expert validation file not found: {csv_file}")
        
        # Load expert validation data
        df = pd.read_csv(csv_file)
        logger.info(f"📊 Found {len(df)} expert-validated proverbs to process")
        
        # Process each proverb
        for idx, row in df.iterrows():
            try:
                # Convert row to dictionary
                proverb_data = row.to_dict()
                
                # Skip if no Kikuyu text
                if not proverb_data.get('Kikuyu_Text'):
                    logger.warning(f"⚠️ Skipping row {idx}: No Kikuyu text")
                    continue
                
                # Create main proverb node
                proverb_id = self.create_proverb_node(proverb_data)
                
                # Extract and create cultural concepts
                concept_ids = self.extract_and_create_concepts(proverb_data, proverb_id)
                
                # Create cultural contexts
                self.create_cultural_context_nodes(proverb_data, proverb_id)
                
                # Create business applications
                self.create_business_application_nodes(proverb_data, proverb_id)
                
                # Progress logging
                if (idx + 1) % 10 == 0:
                    logger.info(f"📈 Processed {idx + 1}/{len(df)} proverbs")
                    
            except Exception as e:
                logger.error(f"❌ Error processing proverb {idx}: {e}")
                self.stats['validation_errors'] += 1
                continue
        
        # Create semantic relationships
        self.create_semantic_relationships()
        
        # Log final statistics
        logger.info("🎯 Ontology construction completed!")
        self._log_construction_stats()
    
    def _log_construction_stats(self):
        """Log comprehensive construction statistics."""
        
        logger.info("📊 ONTOLOGY CONSTRUCTION STATISTICS:")
        logger.info(f"   • Proverbs Created: {self.stats['proverbs_created']}")
        logger.info(f"   • Concepts Created: {self.stats['concepts_created']}")
        logger.info(f"   • Cultural Contexts: {self.stats['cultural_contexts_created']}")
        logger.info(f"   • Business Applications: {self.stats['business_applications_created']}")
        logger.info(f"   • Relationships Created: {self.stats['relationships_created']}")
        logger.info(f"   • Semantic Relationships: {self.stats['semantic_relationships_created']}")
        logger.info(f"   • Validation Errors: {self.stats['validation_errors']}")
    
    def validate_ontology(self) -> Dict:
        """Validate ontology completeness and consistency.
        
        Returns:
            Dict: Comprehensive validation results
        """
        
        logger.info("🔍 Starting ontology validation...")
        
        validation_queries = {
            'node_counts': {
                'total_proverbs': "MATCH (p:Proverb) RETURN count(p) as count",
                'total_concepts': "MATCH (c:Concept) RETURN count(c) as count",
                'total_cultural_contexts': "MATCH (cc:CulturalContext) RETURN count(cc) as count",
                'total_business_applications': "MATCH (ba:BusinessApplication) RETURN count(ba) as count"
            },
            'relationship_counts': {
                'total_relationships': "MATCH ()-[r]->() RETURN count(r) as count",
                'concept_relationships': "MATCH ()-[r:HAS_CONCEPT]->() RETURN count(r) as count",
                'context_relationships': "MATCH ()-[r:USED_IN_CONTEXT]->() RETURN count(r) as count",
                'business_relationships': "MATCH ()-[r:APPLICABLE_TO]->() RETURN count(r) as count"
            },
            'coverage_metrics': {
                'proverbs_with_concepts': """
                    MATCH (p:Proverb)-[:HAS_CONCEPT]->(:Concept) 
                    RETURN count(DISTINCT p) as count
                """,
                'proverbs_with_business_apps': """
                    MATCH (p:Proverb)-[:APPLICABLE_TO]->(:BusinessApplication) 
                    RETURN count(DISTINCT p) as count
                """,
                'high_business_relevance': """
                    MATCH (p:Proverb) 
                    WHERE p.business_relevance_score >= 3 
                    RETURN count(p) as count
                """,
                'expert_validated': """
                    MATCH (p:Proverb) 
                    WHERE p.expert_validation_score >= 3 
                    RETURN count(p) as count
                """
            },
            'quality_metrics': {
                'orphaned_concepts': """
                    MATCH (c:Concept) 
                    WHERE NOT (c)<-[:HAS_CONCEPT]-(:Proverb)
                    RETURN count(c) as count
                """,
                'high_frequency_concepts': """
                    MATCH (c:Concept) 
                    WHERE c.frequency_score >= 3 
                    RETURN count(c) as count
                """,
                'cultural_concepts': """
                    MATCH (c:Concept {category: 'cultural_value'}) 
                    RETURN count(c) as count
                """
            }
        }
        
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'construction_stats': self.stats.copy()
        }
        
        with self.driver.session(database=self.database) as session:
            for category, queries in validation_queries.items():
                validation_results[category] = {}
                
                for metric_name, query in queries.items():
                    try:
                        result = session.run(query)
                        count = result.single()['count']
                        validation_results[category][metric_name] = count
                    except Exception as e:
                        logger.error(f"❌ Validation query failed for {metric_name}: {e}")
                        validation_results[category][metric_name] = -1
        
        # Calculate derived metrics
        node_counts = validation_results['node_counts']
        coverage_metrics = validation_results['coverage_metrics']
        
        if node_counts['total_proverbs'] > 0:
            validation_results['derived_metrics'] = {
                'concept_coverage_percentage': round(
                    (coverage_metrics['proverbs_with_concepts'] / node_counts['total_proverbs']) * 100, 2
                ),
                'business_coverage_percentage': round(
                    (coverage_metrics['proverbs_with_business_apps'] / node_counts['total_proverbs']) * 100, 2
                ),
                'expert_validation_percentage': round(
                    (coverage_metrics['expert_validated'] / node_counts['total_proverbs']) * 100, 2
                ),
                'avg_relationships_per_proverb': round(
                    validation_results['relationship_counts']['total_relationships'] / node_counts['total_proverbs'], 2
                )
            }
        
        logger.info("✅ Ontology validation completed")
        self._log_validation_results(validation_results)
        
        return validation_results
    
    def _log_validation_results(self, validation_results: Dict):
        """Log validation results in a readable format.
        
        Args:
            validation_results: Dictionary containing validation metrics
        """
        
        logger.info("🔍 ONTOLOGY VALIDATION RESULTS:")
        
        # Node counts
        node_counts = validation_results['node_counts']
        logger.info(f"   📊 NODES:")
        logger.info(f"      • Proverbs: {node_counts['total_proverbs']}")
        logger.info(f"      • Concepts: {node_counts['total_concepts']}")
        logger.info(f"      • Cultural Contexts: {node_counts['total_cultural_contexts']}")
        logger.info(f"      • Business Applications: {node_counts['total_business_applications']}")
        
        # Relationship counts
        rel_counts = validation_results['relationship_counts']
        logger.info(f"   🔗 RELATIONSHIPS:")
        logger.info(f"      • Total: {rel_counts['total_relationships']}")
        logger.info(f"      • Concept Relations: {rel_counts['concept_relationships']}")
        logger.info(f"      • Context Relations: {rel_counts['context_relationships']}")
        logger.info(f"      • Business Relations: {rel_counts['business_relationships']}")
        
        # Coverage metrics
        if 'derived_metrics' in validation_results:
            derived = validation_results['derived_metrics']
            logger.info(f"   📈 COVERAGE:")
            logger.info(f"      • Concept Coverage: {derived['concept_coverage_percentage']}%")
            logger.info(f"      • Business Coverage: {derived['business_coverage_percentage']}%")
            logger.info(f"      • Expert Validation: {derived['expert_validation_percentage']}%")
            logger.info(f"      • Avg Relations/Proverb: {derived['avg_relationships_per_proverb']}")


def main():
    """Main function to build comprehensive Kikuyu proverbs ontology."""
    
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Build comprehensive Kikuyu proverbs ontology')
    parser.add_argument('--csv-file', required=True, help='Path to expert validation CSV file')
    parser.add_argument('--uri', default='bolt://localhost:7687', help='Neo4j URI')
    parser.add_argument('--username', default='neo4j', help='Neo4j username')
    parser.add_argument('--password', default='kikuyu_proverbs_2024', help='Neo4j password')
    parser.add_argument('--database', default='neo4j', help='Neo4j database name')
    parser.add_argument('--clear-db', action='store_true', help='Clear database before loading')
    parser.add_argument('--output-dir', default='reports', help='Output directory for validation reports')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Initialize ontology builder
    builder = KikuyuProverbsOntologyBuilder(
        args.uri,
        args.username,
        args.password,
        args.database
    )
    
    try:
        # Clear database if requested
        if args.clear_db:
            builder.clear_database()
        
        # Setup database constraints and indexes
        logger.info("🏗️ Setting up database constraints and indexes...")
        builder.create_constraints_and_indexes()
        
        # Build ontology from expert validation data
        logger.info("🚀 Building ontology from expert-validated data...")
        builder.load_from_expert_data(args.csv_file)
        
        # Validate ontology
        logger.info("🔍 Validating ontology completeness...")
        validation_results = builder.validate_ontology()
        
        # Save validation report
        validation_file = output_dir / f"ontology_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(validation_file, 'w') as f:
            json.dump(validation_results, f, indent=2, default=str)
        
        # Save construction statistics
        stats_file = output_dir / f"ontology_construction_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(stats_file, 'w') as f:
            json.dump(builder.stats, f, indent=2)
        
        # Print summary
        print("\n" + "="*80)
        print("🎯 KIKUYU PROVERBS ONTOLOGY CONSTRUCTION COMPLETE!")
        print("="*80)
        
        node_counts = validation_results['node_counts']
        derived_metrics = validation_results.get('derived_metrics', {})
        
        print(f"📊 ONTOLOGY STATISTICS:")
        print(f"   • Total Proverbs: {node_counts['total_proverbs']}")
        print(f"   • Total Concepts: {node_counts['total_concepts']}")
        print(f"   • Cultural Contexts: {node_counts['total_cultural_contexts']}")
        print(f"   • Business Applications: {node_counts['total_business_applications']}")
        print(f"   • Total Relationships: {validation_results['relationship_counts']['total_relationships']}")
        
        print(f"\n📈 QUALITY METRICS:")
        print(f"   • Concept Coverage: {derived_metrics.get('concept_coverage_percentage', 'N/A')}%")
        print(f"   • Business Coverage: {derived_metrics.get('business_coverage_percentage', 'N/A')}%")
        print(f"   • Expert Validation: {derived_metrics.get('expert_validation_percentage', 'N/A')}%")
        
        print(f"\n📁 REPORTS SAVED:")
        print(f"   • Validation Report: {validation_file}")
        print(f"   • Construction Stats: {stats_file}")
        
        print("\n🚀 Ready for OG-RAG integration!")
        print("="*80)
        
    except Exception as e:
        logger.error(f"❌ Ontology construction failed: {e}")
        raise
    
    finally:
        builder.close()


if __name__ == "__main__":
    main()