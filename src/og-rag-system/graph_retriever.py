#!/usr/bin/env python3
"""
Neo4j Graph Retriever for OG-RAG System
========================================
Retrieves culturally-similar proverbs from AuraDB using triple-strategy hybrid approach:

1. Concept Matching (weight: 0.5) - Semantic concept similarity
2. Cultural Weight (weight: 0.3) - Expert importance scoring
3. Lexical Similarity (weight: 0.2) - Kikuyu text matching

Returns top-k proverbs with metadata for LLM context building.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RetrievedProverb:
    """A proverb retrieved from the knowledge graph."""
    proverb_id: str
    kikuyu_text: str
    expert_translation: str
    expert_cultural_meaning: str
    expert_business_relevance: str
    cultural_weight: float
    thematic_category: str
    similarity_score: float
    matched_concepts: List[str]
    retrieval_method: str


class GraphRetriever:
    """
    Retrieves culturally-similar proverbs from Neo4j AuraDB.
    
    Uses triple-strategy scoring:
    - Concept matching: Find proverbs expressing similar cultural concepts
    - Cultural weight: Prioritize high-importance proverbs
    - Lexical similarity: Match Kikuyu keywords
    """
    
    # Concept keyword mappings for extraction
    CONCEPT_KEYWORDS = {
        'wealth': ['utonga', 'money', 'mbeca', 'rich', 'wealth', 'prosperity', 'riches', 'fortune', 'mbia'],
        'poverty': ['thiini', 'poor', 'poverty', 'lack', 'scarcity', 'destitute', 'needy'],
        'ownership': ['owner', 'possession', 'property', 'belongs', 'owns', 'mine', 'yours'],
        'wealth acquisition': ['acquire', 'gain', 'accumulate', 'gather', 'collect', 'obtain', 'get'],
        'debt': ['debt', 'borrow', 'lend', 'owe', 'loan', 'credit', 'obligation'],
        'greed': ['greed', 'greedy', 'selfish', 'covet', 'envy', 'insatiable', 'hunger'],
        'investment': ['invest', 'plant', 'sow', 'seed', 'capital', 'venture'],
        'wisdom': ['ũũgĩ', 'wisdom', 'wise', 'prudent', 'smart', 'clever', 'intelligent', 'knowledge'],
        'hospitality': ['hospitality', 'welcome', 'guest', 'visitor', 'host', 'generous'],
        'self-reliance': ['self', 'independent', 'reliance', 'oneself', 'alone', 'own'],
        'collaboration': ['together', 'cooperation', 'collaborate', 'unity', 'teamwork', 'joint'],
        'resource management': ['manage', 'steward', 'care', 'preserve', 'maintain', 'husband'],
        'patience': ['patience', 'patient', 'wait', 'endure', 'persevere', 'kĩrĩa'],
        'pride': ['pride', 'proud', 'arrogance', 'boast', 'vain', 'ego'],
        'thief': ['thief', 'steal', 'theft', 'rob', 'burglar', 'mũici']
    }
    
    def __init__(self, uri: Optional[str] = None, username: Optional[str] = None, 
                 password: Optional[str] = None, database: str = 'neo4j'):
        """
        Initialize graph retriever with Neo4j connection.
        
        Args:
            uri: Neo4j URI (reads from .env if not provided)
            username: Neo4j username (reads from .env if not provided)
            password: Neo4j password (reads from .env if not provided)
            database: Neo4j database name
        """
        # Load environment if credentials not provided
        if not all([uri, username, password]):
            project_root = Path(__file__).parent.parent.parent
            load_dotenv(project_root / '.env')
            
            uri = uri or os.getenv('NEO4J_URI')
            username = username or os.getenv('NEO4J_USER')
            password = password or os.getenv('NEO4J_PASSWORD')
        
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database = database
        
        logger.info(f"✅ GraphRetriever connected to {uri}")
    
    def close(self):
        """Close Neo4j driver connection."""
        self.driver.close()
    
    def extract_concepts(self, text: str) -> List[str]:
        """
        Extract cultural concepts from Kikuyu or English text.
        
        Args:
            text: Kikuyu proverb or English translation
            
        Returns:
            List of matched concept names
        """
        text_lower = text.lower()
        matched_concepts = []
        
        for concept, keywords in self.CONCEPT_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                matched_concepts.append(concept)
        
        return matched_concepts
    
    def retrieve_by_concepts(self, concepts: List[str], k: int = 5, 
                            exclude_ids: Optional[List[str]] = None) -> List[RetrievedProverb]:
        """
        Retrieve proverbs that express similar cultural concepts.
        
        Args:
            concepts: List of concept names to match
            k: Number of proverbs to retrieve
            exclude_ids: Proverb IDs to exclude (e.g., input proverb)
            
        Returns:
            List of RetrievedProverb objects with concept-based similarity
        """
        if not concepts:
            logger.warning("No concepts provided for retrieval")
            return []
        
        exclude_ids = exclude_ids or []
        
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (c:CulturalConcept)<-[r:EXPRESSES_CONCEPT]-(p:Proverb)
                WHERE c.concept_name IN $concepts
                  AND NOT p.proverb_id IN $exclude_ids
                WITH p, collect(DISTINCT c.concept_name) as matched_concepts,
                     count(r) as concept_matches
                RETURN p.proverb_id as proverb_id,
                       p.kikuyu_text as kikuyu_text,
                       p.expert_translation as expert_translation,
                       p.expert_cultural_meaning as expert_cultural_meaning,
                       p.expert_business_relevance as expert_business_relevance,
                       p.cultural_weight as cultural_weight,
                       p.thematic_category as thematic_category,
                       matched_concepts,
                       concept_matches
                ORDER BY concept_matches DESC, p.cultural_weight DESC
                LIMIT $k
            """, concepts=concepts, exclude_ids=exclude_ids, k=k)
            
            proverbs = []
            for record in result:
                # Calculate concept similarity score (0.0-1.0)
                similarity = record['concept_matches'] / len(concepts)
                
                proverb = RetrievedProverb(
                    proverb_id=record['proverb_id'],
                    kikuyu_text=record['kikuyu_text'],
                    expert_translation=record['expert_translation'],
                    expert_cultural_meaning=record['expert_cultural_meaning'],
                    expert_business_relevance=record['expert_business_relevance'],
                    cultural_weight=record['cultural_weight'],
                    thematic_category=record['thematic_category'],
                    similarity_score=similarity,
                    matched_concepts=record['matched_concepts'],
                    retrieval_method='concept_matching'
                )
                proverbs.append(proverb)
            
            logger.info(f"📊 Retrieved {len(proverbs)} proverbs via concept matching")
            return proverbs
    
    def retrieve_by_cultural_weight(self, k: int = 5, 
                                   exclude_ids: Optional[List[str]] = None) -> List[RetrievedProverb]:
        """
        Retrieve highest cultural weight proverbs.
        
        Args:
            k: Number of proverbs to retrieve
            exclude_ids: Proverb IDs to exclude
            
        Returns:
            List of highest-weight proverbs
        """
        exclude_ids = exclude_ids or []
        
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (p:Proverb)
                WHERE NOT p.proverb_id IN $exclude_ids
                OPTIONAL MATCH (p)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
                WITH p, collect(DISTINCT c.concept_name) as concepts
                RETURN p.proverb_id as proverb_id,
                       p.kikuyu_text as kikuyu_text,
                       p.expert_translation as expert_translation,
                       p.expert_cultural_meaning as expert_cultural_meaning,
                       p.expert_business_relevance as expert_business_relevance,
                       p.cultural_weight as cultural_weight,
                       p.thematic_category as thematic_category,
                       concepts
                ORDER BY p.cultural_weight DESC
                LIMIT $k
            """, exclude_ids=exclude_ids, k=k)
            
            proverbs = []
            for record in result:
                proverb = RetrievedProverb(
                    proverb_id=record['proverb_id'],
                    kikuyu_text=record['kikuyu_text'],
                    expert_translation=record['expert_translation'],
                    expert_cultural_meaning=record['expert_cultural_meaning'],
                    expert_business_relevance=record['expert_business_relevance'],
                    cultural_weight=record['cultural_weight'],
                    thematic_category=record['thematic_category'],
                    similarity_score=1.0,  # All equally high weight
                    matched_concepts=record['concepts'],
                    retrieval_method='cultural_weight'
                )
                proverbs.append(proverb)
            
            logger.info(f"📊 Retrieved {len(proverbs)} proverbs via cultural weight")
            return proverbs
    
    def retrieve_by_lexical_similarity(self, kikuyu_text: str, k: int = 5,
                                      exclude_ids: Optional[List[str]] = None) -> List[RetrievedProverb]:
        """
        Retrieve proverbs with lexically similar Kikuyu text.
        
        Args:
            kikuyu_text: Input Kikuyu proverb text
            k: Number of proverbs to retrieve
            exclude_ids: Proverb IDs to exclude
            
        Returns:
            List of lexically similar proverbs
        """
        exclude_ids = exclude_ids or []
        
        # Extract keywords from input (simple word tokenization)
        keywords = [w.lower() for w in re.findall(r'\w+', kikuyu_text) if len(w) > 3]
        
        if not keywords:
            logger.warning("No keywords extracted from input text")
            return []
        
        # Build regex pattern for keyword matching
        pattern = '|'.join(keywords)
        
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (p:Proverb)
                WHERE toLower(p.kikuyu_text) =~ ('(?i).*(' + $pattern + ').*')
                  AND NOT p.proverb_id IN $exclude_ids
                OPTIONAL MATCH (p)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
                WITH p, collect(DISTINCT c.concept_name) as concepts
                RETURN p.proverb_id as proverb_id,
                       p.kikuyu_text as kikuyu_text,
                       p.expert_translation as expert_translation,
                       p.expert_cultural_meaning as expert_cultural_meaning,
                       p.expert_business_relevance as expert_business_relevance,
                       p.cultural_weight as cultural_weight,
                       p.thematic_category as thematic_category,
                       concepts
                ORDER BY p.cultural_weight DESC
                LIMIT $k
            """, pattern=pattern, exclude_ids=exclude_ids, k=k)
            
            proverbs = []
            for record in result:
                proverb = RetrievedProverb(
                    proverb_id=record['proverb_id'],
                    kikuyu_text=record['kikuyu_text'],
                    expert_translation=record['expert_translation'],
                    expert_cultural_meaning=record['expert_cultural_meaning'],
                    expert_business_relevance=record['expert_business_relevance'],
                    cultural_weight=record['cultural_weight'],
                    thematic_category=record['thematic_category'],
                    similarity_score=0.8,  # Fixed for keyword match
                    matched_concepts=record['concepts'],
                    retrieval_method='lexical_similarity'
                )
                proverbs.append(proverb)
            
            logger.info(f"📊 Retrieved {len(proverbs)} proverbs via lexical similarity")
            return proverbs
    
    def retrieve_hybrid(self, kikuyu_text: str, k: int = 5,
                       exclude_ids: Optional[List[str]] = None,
                       weights: Optional[Dict[str, float]] = None) -> List[RetrievedProverb]:
        """
        Retrieve proverbs using triple-strategy hybrid approach.
        
        Combines:
        1. Concept matching (default weight: 0.5)
        2. Cultural weight (default weight: 0.3)
        3. Lexical similarity (default weight: 0.2)
        
        Args:
            kikuyu_text: Input Kikuyu proverb
            k: Number of proverbs to retrieve
            exclude_ids: Proverb IDs to exclude
            weights: Custom weights dict {'concept': 0.5, 'cultural': 0.3, 'lexical': 0.2}
            
        Returns:
            Top-k proverbs ranked by weighted combined score
        """
        # Default weights
        if weights is None:
            weights = {'concept': 0.5, 'cultural': 0.3, 'lexical': 0.2}
        
        exclude_ids = exclude_ids or []
        
        # Extract concepts from input
        concepts = self.extract_concepts(kikuyu_text)
        logger.info(f"🔍 Extracted concepts: {concepts}")
        
        # Retrieve from each strategy (get more than k to ensure diversity)
        retrieve_count = k * 2
        
        concept_results = self.retrieve_by_concepts(concepts, k=retrieve_count, exclude_ids=exclude_ids)
        weight_results = self.retrieve_by_cultural_weight(k=retrieve_count, exclude_ids=exclude_ids)
        lexical_results = self.retrieve_by_lexical_similarity(kikuyu_text, k=retrieve_count, exclude_ids=exclude_ids)
        
        # Aggregate scores by proverb_id
        proverb_scores: Dict[str, Tuple[RetrievedProverb, float]] = {}
        
        for proverb in concept_results:
            score = proverb.similarity_score * weights['concept']
            if proverb.proverb_id not in proverb_scores:
                proverb_scores[proverb.proverb_id] = (proverb, score)
            else:
                existing_score = proverb_scores[proverb.proverb_id][1]
                proverb_scores[proverb.proverb_id] = (proverb, existing_score + score)
        
        for proverb in weight_results:
            # Normalize cultural weight (10.0 max) to 0-1 scale
            score = (proverb.cultural_weight / 10.0) * weights['cultural']
            if proverb.proverb_id not in proverb_scores:
                proverb_scores[proverb.proverb_id] = (proverb, score)
            else:
                existing_proverb, existing_score = proverb_scores[proverb.proverb_id]
                proverb_scores[proverb.proverb_id] = (existing_proverb, existing_score + score)
        
        for proverb in lexical_results:
            score = proverb.similarity_score * weights['lexical']
            if proverb.proverb_id not in proverb_scores:
                proverb_scores[proverb.proverb_id] = (proverb, score)
            else:
                existing_proverb, existing_score = proverb_scores[proverb.proverb_id]
                proverb_scores[proverb.proverb_id] = (existing_proverb, existing_score + score)
        
        # Sort by combined score and take top-k
        ranked_proverbs = sorted(
            proverb_scores.values(),
            key=lambda x: x[1],
            reverse=True
        )[:k]
        
        # Update similarity scores to reflect combined score
        final_results = []
        for proverb, combined_score in ranked_proverbs:
            proverb.similarity_score = combined_score
            proverb.retrieval_method = 'hybrid'
            final_results.append(proverb)
        
        logger.info(f"✅ Retrieved {len(final_results)} proverbs via hybrid strategy")
        logger.info(f"   Weights: concept={weights['concept']}, cultural={weights['cultural']}, lexical={weights['lexical']}")
        
        return final_results


if __name__ == '__main__':
    # Test the retriever
    print("="*70)
    print("GRAPH RETRIEVER TEST")
    print("="*70)
    
    retriever = GraphRetriever()
    
    # Test input
    test_proverb = "Aikaragia mbia ta njuu ngigi"
    print(f"\n📖 Test Input: {test_proverb}")
    print(f"   (He looks after his money the way storks pursue locusts)")
    
    # Extract concepts
    concepts = retriever.extract_concepts(test_proverb)
    print(f"\n🔍 Extracted Concepts: {concepts}")
    
    # Test hybrid retrieval
    print(f"\n🚀 Retrieving top-5 similar proverbs...")
    results = retriever.retrieve_hybrid(test_proverb, k=5)
    
    print(f"\n📊 RESULTS ({len(results)} proverbs):")
    print("-" * 70)
    for i, proverb in enumerate(results, 1):
        print(f"\n{i}. {proverb.proverb_id} (Score: {proverb.similarity_score:.3f})")
        print(f"   Kikuyu: {proverb.kikuyu_text[:60]}...")
        print(f"   Translation: {proverb.expert_translation[:60]}...")
        print(f"   Concepts: {', '.join(proverb.matched_concepts[:3])}")
        print(f"   Cultural Weight: {proverb.cultural_weight}")
    
    retriever.close()
    print("\n" + "="*70)
    print("✅ TEST COMPLETE")
    print("="*70)
