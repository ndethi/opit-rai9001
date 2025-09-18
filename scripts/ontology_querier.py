#!/usr/bin/env python3
"""Ontology Query Interface for OG-RAG Retrieval.

This module provides sophisticated querying capabilities for the Kikuyu proverbs
ontology, enabling efficient retrieval of culturally-relevant knowledge for
Ontology-Grounded Retrieval Augmented Generation systems.
"""

from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional, Tuple
import logging
import re
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class KikuyuProverbsQuerier:
    """Advanced query interface for Kikuyu proverbs ontology.
    
    This class provides sophisticated retrieval capabilities for OG-RAG systems,
    including semantic similarity search, cultural context retrieval, and
    business application mapping.
    """
    
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """Initialize Neo4j connection for ontology querying.
        
        Args:
            uri: Neo4j database URI
            username: Database username
            password: Database password
            database: Database name
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database = database
        
        # Query performance metrics
        self.query_stats = {
            'total_queries': 0,
            'avg_response_time': 0.0,
            'cache_hits': 0,
            'semantic_queries': 0,
            'cultural_context_queries': 0,
            'business_application_queries': 0
        }
        
        # Simple query cache for performance
        self._query_cache = {}
        self._cache_size_limit = 100
    
    def close(self):
        """Close Neo4j connection."""
        self.driver.close()
    
    def find_culturally_similar_proverbs(self, 
                                       query_text: str, 
                                       limit: int = 5,
                                       cultural_weight: float = 0.7,
                                       business_weight: float = 0.3) -> List[Dict]:
        """Find proverbs culturally similar to query text with comprehensive context.
        
        This method performs sophisticated semantic matching based on:
        - Cultural concept extraction and matching
        - Traditional usage context similarity
        - Business application relevance
        - Expert validation scores
        
        Args:
            query_text: Input text to find similar proverbs for
            limit: Maximum number of results to return
            cultural_weight: Weight for cultural similarity (0.0-1.0)
            business_weight: Weight for business relevance (0.0-1.0)
            
        Returns:
            List of proverb dictionaries with similarity scores and context
        """
        
        start_time = datetime.now()
        
        # Check cache first
        cache_key = f"similar_{hash(query_text)}_{limit}_{cultural_weight}_{business_weight}"
        if cache_key in self._query_cache:
            self.query_stats['cache_hits'] += 1
            return self._query_cache[cache_key]
        
        # Extract concepts from query for matching
        concepts = self._extract_concepts_from_query(query_text)
        business_terms = self._extract_business_terms(query_text)
        
        if not concepts and not business_terms:
            logger.warning(f"No concepts extracted from query: {query_text}")
            return []
        
        with self.driver.session(database=self.database) as session:
            # Complex query for culturally-aware similarity matching
            query = """
            // Find proverbs with matching concepts
            MATCH (p:Proverb)-[:HAS_CONCEPT]->(c:Concept)
            WHERE c.name IN $concepts OR c.name IN $business_terms
            
            // Calculate concept match score
            WITH p, 
                 count(DISTINCT c) as concept_matches,
                 collect(DISTINCT c.name) as matched_concepts
            
            // Get cultural contexts and business applications
            OPTIONAL MATCH (p)-[:USED_IN_CONTEXT]->(cc:CulturalContext)
            OPTIONAL MATCH (p)-[:APPLICABLE_TO]->(ba:BusinessApplication)
            OPTIONAL MATCH (p)-[:HAS_CONCEPT]->(all_concepts:Concept)
            
            // Calculate similarity scores
            WITH p, concept_matches, matched_concepts,
                 collect(DISTINCT cc) as cultural_contexts,
                 collect(DISTINCT ba) as business_applications,
                 collect(DISTINCT all_concepts) as all_concepts,
                 
                 // Cultural similarity score
                 CASE 
                   WHEN p.cultural_authenticity_score IS NOT NULL 
                   THEN (concept_matches * 1.0 / $concept_count) * (p.cultural_authenticity_score / 5.0) * $cultural_weight
                   ELSE (concept_matches * 1.0 / $concept_count) * 0.5 * $cultural_weight
                 END as cultural_score,
                 
                 // Business relevance score
                 CASE 
                   WHEN p.business_relevance_score IS NOT NULL 
                   THEN (p.business_relevance_score / 5.0) * $business_weight
                   ELSE 0.0
                 END as business_score
            
            // Calculate final similarity score
            WITH p, concept_matches, matched_concepts, cultural_contexts, business_applications, all_concepts,
                 cultural_score, business_score,
                 (cultural_score + business_score) as final_similarity_score
            
            // Order by similarity and expert validation
            ORDER BY final_similarity_score DESC, p.expert_validation_score DESC
            LIMIT $limit
            
            RETURN p, 
                   matched_concepts,
                   concept_matches,
                   cultural_contexts,
                   business_applications,
                   all_concepts,
                   final_similarity_score,
                   cultural_score,
                   business_score
            """
            
            result = session.run(query, 
                concepts=concepts,
                business_terms=business_terms,
                concept_count=max(len(concepts + business_terms), 1),
                cultural_weight=cultural_weight,
                business_weight=business_weight,
                limit=limit
            )
            
            proverbs = []
            for record in result:
                proverb_data = dict(record['p'])
                
                # Enrich with context and similarity information
                enriched_proverb = {
                    **proverb_data,
                    'matched_concepts': record['matched_concepts'],
                    'concept_matches': record['concept_matches'],
                    'cultural_contexts': [dict(cc) for cc in record['cultural_contexts']],
                    'business_applications': [dict(ba) for ba in record['business_applications']],
                    'all_concepts': [dict(c) for c in record['all_concepts']],
                    'similarity_scores': {
                        'overall': round(record['final_similarity_score'], 3),
                        'cultural': round(record['cultural_score'], 3),
                        'business': round(record['business_score'], 3)
                    },
                    'retrieval_metadata': {
                        'query_text': query_text,
                        'retrieval_timestamp': datetime.now().isoformat(),
                        'matching_strategy': 'cultural_semantic_similarity'
                    }
                }
                
                proverbs.append(enriched_proverb)
        
        # Cache result if cache not full
        if len(self._query_cache) < self._cache_size_limit:
            self._query_cache[cache_key] = proverbs
        
        # Update performance metrics
        self._update_query_stats(start_time, 'semantic_queries')
        
        return proverbs
    
    def get_comprehensive_cultural_context(self, proverb_id: str) -> Dict:
        """Get comprehensive cultural context for a specific proverb.
        
        This method retrieves all cultural information associated with a proverb:
        - Traditional usage contexts
        - Cultural concepts and their significance
        - Business applications and modern relevance
        - Related proverbs and cultural values
        - Expert validation and authenticity scores
        
        Args:
            proverb_id: Unique identifier of the proverb
            
        Returns:
            Dictionary containing comprehensive cultural context
        """
        
        start_time = datetime.now()
        
        with self.driver.session(database=self.database) as session:
            query = """
            MATCH (p:Proverb {id: $proverb_id})
            
            // Get all related entities
            OPTIONAL MATCH (p)-[:HAS_CONCEPT]->(c:Concept)
            OPTIONAL MATCH (p)-[:USED_IN_CONTEXT]->(cc:CulturalContext)
            OPTIONAL MATCH (p)-[:APPLICABLE_TO]->(ba:BusinessApplication)
            OPTIONAL MATCH (p)-[:EMBODIES_VALUE]->(cv:CulturalValue)
            OPTIONAL MATCH (p)-[:SIMILAR_TO]->(similar:Proverb)
            
            // Get concept relationships
            OPTIONAL MATCH (c)-[:RELATES_TO]->(related_concept:Concept)
            OPTIONAL MATCH (c)-[:SUPPORTS_APPLICATION]->(supported_app:BusinessApplication)
            
            RETURN p,
                   collect(DISTINCT {
                       concept: c,
                       related_concepts: collect(DISTINCT related_concept),
                       supported_applications: collect(DISTINCT supported_app)
                   }) as concepts_with_relations,
                   collect(DISTINCT cc) as cultural_contexts,
                   collect(DISTINCT ba) as business_applications,
                   collect(DISTINCT cv) as cultural_values,
                   collect(DISTINCT similar) as similar_proverbs
            """
            
            result = session.run(query, proverb_id=proverb_id)
            record = result.single()
            
            if not record:
                logger.warning(f"Proverb not found: {proverb_id}")
                return {}
            
            # Build comprehensive context
            proverb_data = dict(record['p'])
            
            # Process concepts with their relationships
            concepts_data = []
            for concept_relation in record['concepts_with_relations']:
                if concept_relation['concept']:
                    concept_data = dict(concept_relation['concept'])
                    concept_data['related_concepts'] = [dict(rc) for rc in concept_relation['related_concepts']]
                    concept_data['supported_applications'] = [dict(sa) for sa in concept_relation['supported_applications']]
                    concepts_data.append(concept_data)
            
            comprehensive_context = {
                'proverb': proverb_data,
                'cultural_concepts': concepts_data,
                'traditional_contexts': [dict(cc) for cc in record['cultural_contexts']],
                'business_applications': [dict(ba) for ba in record['business_applications']],
                'cultural_values': [dict(cv) for cv in record['cultural_values']],
                'similar_proverbs': [dict(sp) for sp in record['similar_proverbs']],
                'context_metadata': {
                    'retrieval_timestamp': datetime.now().isoformat(),
                    'context_completeness_score': self._calculate_context_completeness(record),
                    'cultural_richness_score': self._calculate_cultural_richness(concepts_data, record['cultural_contexts'])
                }
            }
        
        self._update_query_stats(start_time, 'cultural_context_queries')
        
        return comprehensive_context
    
    def find_business_relevant_proverbs(self, 
                                      business_domain: str, 
                                      min_relevance_score: float = 3.0,
                                      limit: int = 10) -> List[Dict]:
        """Find proverbs relevant to specific business domains.
        
        Args:
            business_domain: Business domain (e.g., 'leadership', 'entrepreneurship', 'teamwork')
            min_relevance_score: Minimum business relevance score (1-5)
            limit: Maximum number of results
            
        Returns:
            List of business-relevant proverbs with application context
        """
        
        start_time = datetime.now()
        
        with self.driver.session(database=self.database) as session:
            query = """
            // Find proverbs with business applications in the specified domain
            MATCH (p:Proverb)-[:APPLICABLE_TO]->(ba:BusinessApplication)
            WHERE ba.domain CONTAINS $business_domain 
               OR ba.type CONTAINS $business_domain
               OR ba.name CONTAINS $business_domain
            AND p.business_relevance_score >= $min_relevance_score
            
            // Get related concepts and contexts
            OPTIONAL MATCH (p)-[:HAS_CONCEPT]->(c:Concept)
            OPTIONAL MATCH (p)-[:USED_IN_CONTEXT]->(cc:CulturalContext)
            
            // Calculate business applicability score
            WITH p, ba, 
                 collect(DISTINCT c) as concepts,
                 collect(DISTINCT cc) as cultural_contexts,
                 (p.business_relevance_score + 
                  CASE WHEN ba.relevance_score IS NOT NULL THEN ba.relevance_score * 5 ELSE 0 END) / 2.0 as applicability_score
            
            ORDER BY applicability_score DESC, p.expert_validation_score DESC
            LIMIT $limit
            
            RETURN p, ba, concepts, cultural_contexts, applicability_score
            """
            
            result = session.run(query,
                business_domain=business_domain.lower(),
                min_relevance_score=min_relevance_score,
                limit=limit
            )
            
            business_proverbs = []
            for record in result:
                proverb_data = dict(record['p'])
                business_app = dict(record['ba'])
                
                enriched_proverb = {
                    **proverb_data,
                    'primary_business_application': business_app,
                    'related_concepts': [dict(c) for c in record['concepts']],
                    'cultural_contexts': [dict(cc) for cc in record['cultural_contexts']],
                    'business_scores': {
                        'applicability': round(record['applicability_score'], 2),
                        'relevance': proverb_data.get('business_relevance_score', 0),
                        'implementation_difficulty': business_app.get('implementation_difficulty', 'unknown')
                    },
                    'retrieval_metadata': {
                        'business_domain': business_domain,
                        'retrieval_timestamp': datetime.now().isoformat(),
                        'matching_strategy': 'business_domain_relevance'
                    }
                }
                
                business_proverbs.append(enriched_proverb)
        
        self._update_query_stats(start_time, 'business_application_queries')
        
        return business_proverbs
    
    def get_concept_network(self, concept_name: str, depth: int = 2) -> Dict:
        """Get concept network showing relationships and connections.
        
        Args:
            concept_name: Name of the central concept
            depth: Relationship traversal depth
            
        Returns:
            Dictionary containing concept network structure
        """
        
        with self.driver.session(database=self.database) as session:
            query = """
            MATCH (central:Concept {name: $concept_name})
            
            // Get direct relationships
            OPTIONAL MATCH (central)-[r1:RELATES_TO]->(related1:Concept)
            OPTIONAL MATCH (central)<-[r2:RELATES_TO]-(related2:Concept)
            
            // Get proverbs using this concept
            OPTIONAL MATCH (central)<-[:HAS_CONCEPT]-(p:Proverb)
            
            // Get supported business applications
            OPTIONAL MATCH (central)-[:SUPPORTS_APPLICATION]->(ba:BusinessApplication)
            
            RETURN central,
                   collect(DISTINCT {relationship: r1, concept: related1}) as outgoing_relations,
                   collect(DISTINCT {relationship: r2, concept: related2}) as incoming_relations,
                   collect(DISTINCT p) as related_proverbs,
                   collect(DISTINCT ba) as supported_applications
            """
            
            result = session.run(query, concept_name=concept_name)
            record = result.single()
            
            if not record:
                return {}
            
            return {
                'central_concept': dict(record['central']),
                'outgoing_relationships': [
                    {
                        'relationship': dict(rel['relationship']) if rel['relationship'] else {},
                        'target_concept': dict(rel['concept']) if rel['concept'] else {}
                    } for rel in record['outgoing_relations'] if rel['concept']
                ],
                'incoming_relationships': [
                    {
                        'relationship': dict(rel['relationship']) if rel['relationship'] else {},
                        'source_concept': dict(rel['concept']) if rel['concept'] else {}
                    } for rel in record['incoming_relations'] if rel['concept']
                ],
                'related_proverbs': [dict(p) for p in record['related_proverbs']],
                'supported_applications': [dict(ba) for ba in record['supported_applications']],
                'network_metadata': {
                    'retrieval_timestamp': datetime.now().isoformat(),
                    'traversal_depth': depth,
                    'network_size': len(record['related_proverbs'])
                }
            }
    
    def search_proverbs_by_keywords(self, 
                                  keywords: List[str], 
                                  search_fields: List[str] = None,
                                  limit: int = 10) -> List[Dict]:
        """Search proverbs using keyword matching across multiple fields.
        
        Args:
            keywords: List of keywords to search for
            search_fields: Fields to search in (default: all text fields)
            limit: Maximum number of results
            
        Returns:
            List of matching proverbs with relevance scores
        """
        
        if search_fields is None:
            search_fields = ['kikuyu_text', 'english_translation', 'cultural_meaning', 'traditional_usage']
        
        with self.driver.session(database=self.database) as session:
            # Build dynamic query based on search fields
            search_conditions = []
            for field in search_fields:
                for keyword in keywords:
                    search_conditions.append(f"p.{field} CONTAINS '{keyword}'")
            
            search_clause = " OR ".join(search_conditions) if search_conditions else "true"
            
            query = f"""
            MATCH (p:Proverb)
            WHERE {search_clause}
            
            // Calculate relevance score based on keyword matches
            WITH p, 
                 size([keyword IN $keywords WHERE p.kikuyu_text CONTAINS keyword]) as kikuyu_matches,
                 size([keyword IN $keywords WHERE p.english_translation CONTAINS keyword]) as english_matches,
                 size([keyword IN $keywords WHERE p.cultural_meaning CONTAINS keyword]) as cultural_matches
            
            WITH p, (kikuyu_matches * 3 + english_matches * 2 + cultural_matches * 1) as relevance_score
            
            // Get related context
            OPTIONAL MATCH (p)-[:HAS_CONCEPT]->(c:Concept)
            OPTIONAL MATCH (p)-[:APPLICABLE_TO]->(ba:BusinessApplication)
            
            ORDER BY relevance_score DESC, p.expert_validation_score DESC
            LIMIT $limit
            
            RETURN p, relevance_score, 
                   collect(DISTINCT c) as concepts,
                   collect(DISTINCT ba) as business_applications
            """
            
            result = session.run(query, keywords=keywords, limit=limit)
            
            search_results = []
            for record in result:
                proverb_data = dict(record['p'])
                
                enriched_result = {
                    **proverb_data,
                    'search_metadata': {
                        'keywords': keywords,
                        'relevance_score': record['relevance_score'],
                        'search_fields': search_fields,
                        'retrieval_timestamp': datetime.now().isoformat()
                    },
                    'related_concepts': [dict(c) for c in record['concepts']],
                    'business_applications': [dict(ba) for ba in record['business_applications']]
                }
                
                search_results.append(enriched_result)
            
            return search_results
    
    def _extract_concepts_from_query(self, query_text: str) -> List[str]:
        """Extract cultural concepts from query text for matching.
        
        Args:
            query_text: Input query text
            
        Returns:
            List of identified cultural concepts
        """
        
        # Cultural concept mappings for query understanding
        concept_mappings = {
            'work': ['work_ethics'],
            'business': ['entrepreneurship'],
            'success': ['prosperity'],
            'team': ['community', 'cooperation'],
            'patience': ['patience'],
            'planning': ['planning'],
            'leadership': ['leadership'],
            'leader': ['leadership'],
            'wealth': ['prosperity'],
            'community': ['community'],
            'wisdom': ['wisdom'],
            'cooperation': ['cooperation'],
            'collaboration': ['cooperation'],
            'respect': ['respect'],
            'perseverance': ['perseverance'],
            'persistence': ['perseverance']
        }
        
        concepts = []
        query_lower = query_text.lower()
        
        for term, mapped_concepts in concept_mappings.items():
            if term in query_lower:
                concepts.extend(mapped_concepts)
        
        return list(set(concepts))  # Remove duplicates
    
    def _extract_business_terms(self, query_text: str) -> List[str]:
        """Extract business-specific terms from query text.
        
        Args:
            query_text: Input query text
            
        Returns:
            List of business terms
        """
        
        business_terms = [
            'entrepreneurship', 'management', 'strategy', 'finance', 
            'marketing', 'sales', 'operations', 'innovation', 
            'investment', 'growth', 'profit', 'revenue'
        ]
        
        query_lower = query_text.lower()
        found_terms = [term for term in business_terms if term in query_lower]
        
        return found_terms
    
    def _calculate_context_completeness(self, record) -> float:
        """Calculate completeness score for cultural context.
        
        Args:
            record: Neo4j query result record
            
        Returns:
            Completeness score between 0.0 and 1.0
        """
        
        components = [
            len(record.get('concepts_with_relations', [])) > 0,
            len(record.get('cultural_contexts', [])) > 0,
            len(record.get('business_applications', [])) > 0,
            len(record.get('cultural_values', [])) > 0,
            len(record.get('similar_proverbs', [])) > 0
        ]
        
        return sum(components) / len(components)
    
    def _calculate_cultural_richness(self, concepts: List[Dict], contexts: List[Any]) -> float:
        """Calculate cultural richness score based on concepts and contexts.
        
        Args:
            concepts: List of concept dictionaries
            contexts: List of cultural contexts
            
        Returns:
            Cultural richness score between 0.0 and 1.0
        """
        
        # Count cultural concepts vs general concepts
        cultural_concepts = [c for c in concepts if c.get('category') == 'cultural_value']
        cultural_ratio = len(cultural_concepts) / max(len(concepts), 1)
        
        # Context diversity score
        context_types = set(c.get('type', '') for c in contexts if isinstance(c, dict))
        context_diversity = min(len(context_types) / 3.0, 1.0)  # Up to 3 types
        
        return (cultural_ratio * 0.7) + (context_diversity * 0.3)
    
    def _update_query_stats(self, start_time: datetime, query_type: str):
        """Update query performance statistics.
        
        Args:
            start_time: Query start timestamp
            query_type: Type of query executed
        """
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        self.query_stats['total_queries'] += 1
        self.query_stats[query_type] += 1
        
        # Update average response time
        total_time = self.query_stats['avg_response_time'] * (self.query_stats['total_queries'] - 1)
        self.query_stats['avg_response_time'] = (total_time + execution_time) / self.query_stats['total_queries']
    
    def get_query_statistics(self) -> Dict:
        """Get query performance statistics.
        
        Returns:
            Dictionary containing query performance metrics
        """
        
        return {
            **self.query_stats,
            'cache_size': len(self._query_cache),
            'cache_hit_rate': self.query_stats['cache_hits'] / max(self.query_stats['total_queries'], 1)
        }


def main():
    """Example usage of the Kikuyu Proverbs Querier."""
    
    # Initialize querier
    querier = KikuyuProverbsQuerier(
        uri="bolt://localhost:7687",
        username="neo4j", 
        password="kikuyu_proverbs_2024"
    )
    
    try:
        # Example 1: Find culturally similar proverbs
        print("🔍 Finding culturally similar proverbs...")
        similar_proverbs = querier.find_culturally_similar_proverbs(
            "importance of hard work and patience in business success",
            limit=3
        )
        
        for i, proverb in enumerate(similar_proverbs, 1):
            print(f"\n{i}. {proverb['kikuyu_text']}")
            print(f"   Translation: {proverb['english_translation']}")
            print(f"   Similarity Score: {proverb['similarity_scores']['overall']}")
            print(f"   Matched Concepts: {', '.join(proverb['matched_concepts'])}")
        
        # Example 2: Get comprehensive cultural context
        if similar_proverbs:
            print(f"\n📖 Cultural context for: {similar_proverbs[0]['id']}")
            context = querier.get_comprehensive_cultural_context(similar_proverbs[0]['id'])
            
            print(f"   Cultural Concepts: {len(context['cultural_concepts'])}")
            print(f"   Business Applications: {len(context['business_applications'])}")
            print(f"   Context Completeness: {context['context_metadata']['context_completeness_score']:.2f}")
        
        # Example 3: Find business-relevant proverbs
        print(f"\n💼 Business-relevant proverbs for 'leadership':")
        business_proverbs = querier.find_business_relevant_proverbs("leadership", limit=2)
        
        for proverb in business_proverbs:
            print(f"   • {proverb['kikuyu_text']}")
            print(f"     Business Score: {proverb['business_scores']['applicability']}")
        
        # Example 4: Query statistics
        print(f"\n📊 Query Statistics:")
        stats = querier.get_query_statistics()
        print(f"   Total Queries: {stats['total_queries']}")
        print(f"   Average Response Time: {stats['avg_response_time']:.3f}s")
        print(f"   Cache Hit Rate: {stats['cache_hit_rate']:.2%}")
        
    finally:
        querier.close()


if __name__ == "__main__":
    main()