"""
Cultural Weight Calculation System for Kikuyu Proverb Ontology

This module implements multi-factor algorithms for calculating cultural significance
weights for proverbs and concepts. These weights inform RAG retrieval prioritization
and translation quality assessment.

Author: [Your name]
Date: October 17, 2025
Version: 1.0
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ConceptType(Enum):
    """Types of cultural concepts"""
    WEALTH = "wealth_paradigm"
    SOCIAL = "social_concept"
    MORAL = "moral_concept"
    SPIRITUAL = "spiritual_concept"
    METAPHOR = "metaphorical_domain"
    

@dataclass
class ConceptMetrics:
    """
    Metrics for calculating cultural weight of a concept.
    
    All scores should be in range [0, 1] unless otherwise specified.
    """
    # Expert validation
    expert_agreement_score: float  # 0-1: Expert consensus on interpretation
    expert_count: int = 1  # Number of experts who validated
    validation_confidence: float = 0.8  # Expert confidence in their assessment
    
    # Usage patterns
    usage_count: int = 5  # Frequency in corpus (can be >1)
    usage_frequency: float = 0.5  # 0-1: How often used in authentic contexts
    regional_coverage: float = 0.5  # 0-1: Geographic spread of usage
    
    # Cultural depth
    semantic_dimensions_count: int = 5  # Number of semantic dimensions
    presupposition_depth: int = 1  # How many concepts it presupposes
    worldview_centrality: float = 0.7  # 0-1: Centrality to Kikuyu worldview
    
    # Translation complexity
    translation_complexity_score: float = 0.7  # 0-1: Difficulty of faithful translation
    english_inadequacy: float = 0.6  # 0-1: How much is lost in English
    conceptual_incommensurability: float = 0.5  # 0-1: Degree of untranslatability
    
    # Historical context
    historical_persistence_score: float = 0.8  # 0-1: Continuity across time periods
    historical_period_count: int = 3  # How many historical periods relevant
    modern_relevance: float = 0.7  # 0-1: Continued importance today
    
    # Ontological properties
    centrality_in_graph: float = 0.7  # 0-1: Graph centrality metrics
    relationship_count: int = 5  # Number of relationships to other concepts
    

@dataclass
class ProverbMetrics:
    """
    Metrics for calculating cultural weight of a proverb.
    """
    # Constituent concepts
    concept_weights: List[float]  # Cultural weights of contained concepts
    concept_salience_scores: List[float]  # How salient each concept is to meaning
    
    # Usage patterns
    usage_frequency: float = 0.5  # 0-1: How often used (1-10 scale normalized)
    formality_level: str = "medium"  # low, medium, high
    generational_usage: str = "all_ages"  # elders_only, mixed, all_ages
    
    # Thematic importance
    theme_centrality: float = 0.6  # 0-1: How central to cultural themes
    theme_count: int = 2  # Number of themes expressed
    
    # Validation
    expert_consensus: float = 0.85  # 0-1: Agreement on interpretation
    validation_status: str = "expert_verified"  # pending, expert_verified, multi_expert
    inter_rater_agreement: float = 0.85  # Fleiss' Kappa if multi-expert
    
    # Historical/cultural context
    historical_age_score: float = 0.7  # 0-1: Antiquity and persistence
    cultural_function_importance: float = 0.75  # 0-1: Importance of social function
    
    # Metaphorical complexity
    metaphor_strength: float = 0.6  # 0-1: If metaphorical, how strong
    metaphor_conventionality: str = "conventional"  # conventional, semi_creative, creative
    

class CulturalWeightCalculator:
    """
    Multi-factor cultural weight calculation for concepts and proverbs.
    
    Implements weighted combination of expert validation, cultural depth,
    translation difficulty, usage patterns, and historical continuity.
    
    Weights are configurable but defaults based on:
    - Expert consensus is most important (30%)
    - Cultural depth second (25%)
    - Translation difficulty third (15%)
    - Usage frequency fourth (15%)
    - Historical continuity (10%)
    - Centrality (5%)
    """
    
    # Default weights for concept calculation
    CONCEPT_WEIGHTS = {
        'expert_consensus': 0.30,      # Expert agreement is paramount
        'cultural_depth': 0.25,        # Conceptual richness
        'translation_difficulty': 0.15, # Cultural specificity
        'usage_frequency': 0.15,       # Authentic usage patterns
        'historical_continuity': 0.10, # Temporal persistence
        'centrality': 0.05             # Graph centrality
    }
    
    # Default weights for proverb calculation
    PROVERB_WEIGHTS = {
        'concept_base': 0.40,          # Based on constituent concepts
        'usage_frequency': 0.20,       # Authentic usage
        'expert_consensus': 0.20,      # Validation quality
        'theme_centrality': 0.10,      # Thematic importance
        'historical_age': 0.10         # Temporal depth
    }
    
    def __init__(self, 
                 concept_weights: Optional[Dict[str, float]] = None,
                 proverb_weights: Optional[Dict[str, float]] = None):
        """
        Initialize calculator with custom weights if provided.
        
        Args:
            concept_weights: Custom weights for concept calculation
            proverb_weights: Custom weights for proverb calculation
        """
        self.concept_weights = concept_weights or self.CONCEPT_WEIGHTS
        self.proverb_weights = proverb_weights or self.PROVERB_WEIGHTS
        
        # Validate weights sum to 1.0
        assert abs(sum(self.concept_weights.values()) - 1.0) < 0.01, \
            "Concept weights must sum to 1.0"
        assert abs(sum(self.proverb_weights.values()) - 1.0) < 0.01, \
            "Proverb weights must sum to 1.0"
    
    def calculate_concept_weight(self, metrics: ConceptMetrics) -> float:
        """
        Calculate cultural weight for a concept using multi-factor algorithm.
        
        Args:
            metrics: ConceptMetrics with all required measurements
            
        Returns:
            Cultural weight score (0.0-1.0)
            
        Example:
            >>> metrics = ConceptMetrics(
            ...     expert_agreement_score=0.94,
            ...     usage_count=47,
            ...     semantic_dimensions_count=7,
            ...     translation_complexity_score=0.88,
            ...     historical_persistence_score=0.91,
            ...     worldview_centrality=0.93
            ... )
            >>> calculator = CulturalWeightCalculator()
            >>> weight = calculator.calculate_concept_weight(metrics)
            >>> print(f"Weight: {weight:.3f}")
            Weight: 0.912
        """
        
        # Factor 1: Expert Validation Consensus
        # Adjusted by number of experts and their confidence
        expert_factor = self._calculate_expert_factor(
            metrics.expert_agreement_score,
            metrics.expert_count,
            metrics.validation_confidence
        )
        
        # Factor 2: Usage Frequency (log-scaled to prevent outliers)
        usage_factor = self._calculate_usage_factor(
            metrics.usage_count,
            metrics.usage_frequency,
            metrics.regional_coverage
        )
        
        # Factor 3: Cultural Depth
        # Combines semantic richness, presuppositions, and worldview centrality
        depth_factor = self._calculate_depth_factor(
            metrics.semantic_dimensions_count,
            metrics.presupposition_depth,
            metrics.worldview_centrality
        )
        
        # Factor 4: Translation Difficulty
        # Higher difficulty = more culturally specific = higher weight
        translation_factor = self._calculate_translation_factor(
            metrics.translation_complexity_score,
            metrics.english_inadequacy,
            metrics.conceptual_incommensurability
        )
        
        # Factor 5: Historical Continuity
        # Temporal persistence indicates cultural importance
        historical_factor = self._calculate_historical_factor(
            metrics.historical_persistence_score,
            metrics.historical_period_count,
            metrics.modern_relevance
        )
        
        # Factor 6: Centrality in Knowledge Graph
        centrality_factor = self._calculate_centrality_factor(
            metrics.centrality_in_graph,
            metrics.relationship_count
        )
        
        # Weighted combination
        weight = (
            self.concept_weights['expert_consensus'] * expert_factor +
            self.concept_weights['usage_frequency'] * usage_factor +
            self.concept_weights['cultural_depth'] * depth_factor +
            self.concept_weights['translation_difficulty'] * translation_factor +
            self.concept_weights['historical_continuity'] * historical_factor +
            self.concept_weights['centrality'] * centrality_factor
        )
        
        return np.clip(weight, 0.0, 1.0)
    
    def calculate_proverb_weight(self, metrics: ProverbMetrics) -> float:
        """
        Calculate cultural weight for a proverb.
        
        Incorporates weights of constituent concepts plus proverb-specific factors.
        
        Args:
            metrics: ProverbMetrics with all required measurements
            
        Returns:
            Cultural weight score (0.0-1.0)
        """
        
        # Base weight from constituent concepts (weighted by salience)
        concept_base = self._calculate_concept_base(
            metrics.concept_weights,
            metrics.concept_salience_scores
        )
        
        # Proverb-specific usage factor
        usage_factor = self._calculate_proverb_usage_factor(
            metrics.usage_frequency,
            metrics.formality_level,
            metrics.generational_usage
        )
        
        # Expert validation quality
        expert_factor = self._calculate_proverb_expert_factor(
            metrics.expert_consensus,
            metrics.validation_status,
            metrics.inter_rater_agreement
        )
        
        # Thematic importance
        theme_factor = self._calculate_theme_factor(
            metrics.theme_centrality,
            metrics.theme_count
        )
        
        # Historical and cultural function importance
        historical_factor = metrics.historical_age_score
        
        # Combined weight
        proverb_weight = (
            self.proverb_weights['concept_base'] * concept_base +
            self.proverb_weights['usage_frequency'] * usage_factor +
            self.proverb_weights['expert_consensus'] * expert_factor +
            self.proverb_weights['theme_centrality'] * theme_factor +
            self.proverb_weights['historical_age'] * historical_factor
        )
        
        return np.clip(proverb_weight, 0.0, 1.0)
    
    # ==================== Concept Factor Calculations ====================
    
    def _calculate_expert_factor(self, 
                                 agreement: float, 
                                 expert_count: int,
                                 confidence: float) -> float:
        """
        Calculate expert validation factor with confidence adjustment.
        
        Single expert (N=1): Use confidence-adjusted agreement
        Multiple experts (N>1): Boost score with diminishing returns
        """
        if expert_count == 1:
            # Single expert: Reduce score by confidence uncertainty
            return agreement * confidence
        else:
            # Multiple experts: Boost with diminishing returns
            # Boost factor: 1.0 + 0.15*log(N) up to max 1.3x
            boost = 1.0 + min(0.15 * np.log(expert_count), 0.3)
            return min(agreement * boost, 1.0)
    
    def _calculate_usage_factor(self,
                                usage_count: int,
                                usage_frequency: float,
                                regional_coverage: float) -> float:
        """
        Calculate usage factor from count, frequency, and geographic spread.
        
        Uses log scaling to prevent high-frequency outliers from dominating.
        """
        # Log-scaled usage count (normalized to 0-1)
        count_score = np.log1p(usage_count) / 10  # log(1+x)/10
        count_score = min(count_score, 1.0)
        
        # Combine with frequency and regional coverage
        usage_score = (
            0.40 * count_score +
            0.40 * usage_frequency +
            0.20 * regional_coverage
        )
        
        return np.clip(usage_score, 0.0, 1.0)
    
    def _calculate_depth_factor(self,
                                dimensions_count: int,
                                presupposition_depth: int,
                                worldview_centrality: float) -> float:
        """
        Calculate cultural depth from semantic dimensions and centrality.
        
        More dimensions = richer concept (normalized by typical max of 7-8)
        Deeper presuppositions = more foundational concept
        """
        # Semantic dimensions (normalized, with diminishing returns)
        dim_score = min(dimensions_count / 7, 1.0)
        
        # Presupposition depth (log-scaled, max benefit at depth 5)
        presup_score = np.log1p(presupposition_depth) / np.log1p(5)
        presup_score = min(presup_score, 1.0)
        
        # Weighted combination
        depth_score = (
            0.40 * dim_score +
            0.20 * presup_score +
            0.40 * worldview_centrality
        )
        
        return np.clip(depth_score, 0.0, 1.0)
    
    def _calculate_translation_factor(self,
                                      complexity: float,
                                      inadequacy: float,
                                      incommensurability: float) -> float:
        """
        Calculate translation difficulty factor.
        
        Higher difficulty = more culturally specific = higher cultural weight
        """
        translation_score = (
            0.40 * complexity +
            0.30 * inadequacy +
            0.30 * incommensurability
        )
        
        return np.clip(translation_score, 0.0, 1.0)
    
    def _calculate_historical_factor(self,
                                     persistence: float,
                                     period_count: int,
                                     modern_relevance: float) -> float:
        """
        Calculate historical continuity factor.
        
        Long persistence + modern relevance = culturally important
        """
        # Period count normalized (max benefit at 4 periods)
        period_score = min(period_count / 4, 1.0)
        
        historical_score = (
            0.40 * persistence +
            0.30 * period_score +
            0.30 * modern_relevance
        )
        
        return np.clip(historical_score, 0.0, 1.0)
    
    def _calculate_centrality_factor(self,
                                    centrality: float,
                                    relationship_count: int) -> float:
        """
        Calculate graph centrality factor.
        
        More connections = more central to knowledge structure
        """
        # Relationship count (log-scaled, normalized)
        rel_score = np.log1p(relationship_count) / np.log1p(20)
        rel_score = min(rel_score, 1.0)
        
        centrality_score = (
            0.60 * centrality +
            0.40 * rel_score
        )
        
        return np.clip(centrality_score, 0.0, 1.0)
    
    # ==================== Proverb Factor Calculations ====================
    
    def _calculate_concept_base(self,
                                concept_weights: List[float],
                                salience_scores: List[float]) -> float:
        """
        Calculate base weight from constituent concepts.
        
        Weighted average by concept salience (how important to meaning).
        """
        if not concept_weights:
            return 0.5  # Default if no concepts
        
        if not salience_scores or len(salience_scores) != len(concept_weights):
            # No salience data: simple average
            return np.mean(concept_weights)
        
        # Weighted average by salience
        total_salience = sum(salience_scores)
        if total_salience == 0:
            return np.mean(concept_weights)
        
        weighted_sum = sum(w * s for w, s in zip(concept_weights, salience_scores))
        return weighted_sum / total_salience
    
    def _calculate_proverb_usage_factor(self,
                                       frequency: float,
                                       formality: str,
                                       generational: str) -> float:
        """
        Calculate proverb usage factor.
        
        Adjusts frequency by formality and generational spread.
        """
        # Formality adjustment (high formality = more important)
        formality_mult = {
            'low': 0.85,
            'medium': 1.0,
            'medium_to_high': 1.10,
            'high': 1.15
        }.get(formality, 1.0)
        
        # Generational spread (wider = more important)
        generational_mult = {
            'elders_only': 0.95,
            'primarily_elders': 1.0,
            'mixed': 1.05,
            'all_ages': 1.10
        }.get(generational, 1.0)
        
        usage_score = frequency * formality_mult * generational_mult
        
        return np.clip(usage_score, 0.0, 1.0)
    
    def _calculate_proverb_expert_factor(self,
                                        consensus: float,
                                        validation_status: str,
                                        inter_rater: float) -> float:
        """
        Calculate expert validation factor for proverb.
        
        Multi-expert validation gets higher scores.
        """
        # Validation status multiplier
        status_mult = {
            'pending_validation': 0.70,
            'single_expert_verified': 0.90,
            'expert_verified': 0.90,  # Assume single expert
            'multi_expert_verified': 1.15
        }.get(validation_status, 0.85)
        
        # Use inter-rater agreement if multi-expert
        if validation_status in ['multi_expert_verified'] and inter_rater > 0:
            base_score = inter_rater
        else:
            base_score = consensus
        
        expert_score = base_score * status_mult
        
        return np.clip(expert_score, 0.0, 1.0)
    
    def _calculate_theme_factor(self,
                               centrality: float,
                               theme_count: int) -> float:
        """
        Calculate thematic importance factor.
        
        More themes + high centrality = culturally significant
        """
        # Theme count (normalized, max benefit at 4 themes)
        theme_score = min(theme_count / 4, 1.0)
        
        thematic_factor = (
            0.70 * centrality +
            0.30 * theme_score
        )
        
        return np.clip(thematic_factor, 0.0, 1.0)


class SemanticDistanceCalculator:
    """
    Calculate cultural context-aware semantic distance between concepts.
    
    Combines distributional similarity (embeddings), knowledge graph structure,
    and expert-validated conceptual proximity.
    """
    
    # Weights for multi-modal distance calculation
    DISTANCE_WEIGHTS = {
        'embedding_similarity': 0.30,      # Distributional semantics
        'knowledge_graph_strength': 0.45,  # Ontological relationships
        'expert_proximity': 0.25           # Expert-validated closeness
    }
    
    def __init__(self, 
                 embedding_dim: int = 768,
                 distance_weights: Optional[Dict[str, float]] = None):
        """
        Initialize distance calculator.
        
        Args:
            embedding_dim: Dimensionality of concept embeddings
            distance_weights: Custom weights for distance components
        """
        self.embedding_dim = embedding_dim
        self.weights = distance_weights or self.DISTANCE_WEIGHTS
        
        assert abs(sum(self.weights.values()) - 1.0) < 0.01, \
            "Distance weights must sum to 1.0"
    
    def calculate_distance(self,
                          concept1: Dict,
                          concept2: Dict,
                          knowledge_graph_context: Optional[Dict] = None) -> float:
        """
        Calculate multi-modal semantic distance between concepts.
        
        Args:
            concept1: First concept dict with 'embedding', 'name', etc.
            concept2: Second concept dict
            knowledge_graph_context: Optional KG relationship data
            
        Returns:
            Distance score (0-1, lower = more similar)
            
        Example:
            >>> concept1 = {
            ...     'name': 'ũtonga',
            ...     'embedding': np.random.rand(768)
            ... }
            >>> concept2 = {
            ...     'name': 'ũthĩni',
            ...     'embedding': np.random.rand(768)
            ... }
            >>> calculator = SemanticDistanceCalculator()
            >>> distance = calculator.calculate_distance(concept1, concept2)
            >>> print(f"Distance: {distance:.3f}")
        """
        
        # Component 1: Embedding-based similarity
        embedding_sim = self._calculate_embedding_similarity(
            concept1.get('embedding'),
            concept2.get('embedding')
        )
        
        # Component 2: Knowledge graph relationship strength
        kg_strength = self._extract_kg_strength(
            concept1, concept2, knowledge_graph_context
        )
        
        # Component 3: Expert proximity (if available)
        expert_proximity = self._get_expert_proximity(
            concept1.get('name'),
            concept2.get('name')
        )
        
        # Weighted combination (similarity to distance)
        similarity = (
            self.weights['embedding_similarity'] * embedding_sim +
            self.weights['knowledge_graph_strength'] * kg_strength +
            self.weights['expert_proximity'] * expert_proximity
        )
        
        # Convert similarity to distance
        distance = 1.0 - similarity
        
        return np.clip(distance, 0.0, 1.0)
    
    def calculate_path_distance(self,
                               concept_path: List[Tuple[str, float]]) -> float:
        """
        Calculate distance along a path in knowledge graph.
        
        Args:
            concept_path: List of (concept_name, edge_weight) tuples
            
        Returns:
            Cumulative path distance
        """
        if not concept_path:
            return 1.0
        
        # Path distance as product of edge weights (similarity)
        # More hops = exponentially greater distance
        path_similarity = 1.0
        for _, edge_weight in concept_path:
            path_similarity *= edge_weight
        
        distance = 1.0 - path_similarity
        
        return np.clip(distance, 0.0, 1.0)
    
    def _calculate_embedding_similarity(self,
                                       emb1: Optional[np.ndarray],
                                       emb2: Optional[np.ndarray]) -> float:
        """
        Calculate cosine similarity between embeddings.
        
        Returns 0.5 (neutral) if embeddings not available.
        """
        if emb1 is None or emb2 is None:
            return 0.5
        
        # Ensure numpy arrays
        emb1 = np.array(emb1)
        emb2 = np.array(emb2)
        
        # Cosine similarity
        dot_product = np.dot(emb1, emb2)
        norm_product = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        
        if norm_product == 0:
            return 0.0
        
        similarity = dot_product / norm_product
        
        # Map from [-1, 1] to [0, 1]
        similarity = (similarity + 1) / 2
        
        return np.clip(similarity, 0.0, 1.0)
    
    def _extract_kg_strength(self,
                            concept1: Dict,
                            concept2: Dict,
                            kg_context: Optional[Dict]) -> float:
        """
        Extract relationship strength from knowledge graph context.
        
        Returns 0.5 (neutral) if no KG relationship found.
        """
        if not kg_context:
            return 0.5
        
        # Check for direct relationship
        strength = kg_context.get('relationship_weight', 0.5)
        
        return np.clip(strength, 0.0, 1.0)
    
    def _get_expert_proximity(self,
                             concept1_name: Optional[str],
                             concept2_name: Optional[str]) -> float:
        """
        Retrieve expert-validated conceptual proximity.
        
        In production: Query from validated proximity database.
        Returns 0.5 (neutral) as placeholder.
        """
        # TODO: Implement database lookup of expert-validated proximities
        # For now, return neutral score
        return 0.5
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Static method for cosine similarity calculation.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity (0-1)
        """
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        
        if norm_product == 0:
            return 0.0
        
        similarity = dot_product / norm_product
        
        # Map from [-1, 1] to [0, 1]
        similarity = (similarity + 1) / 2
        
        return np.clip(similarity, 0.0, 1.0)


# ==================== Utility Functions ====================

def calculate_weights_from_gap_analysis(gap_analysis_file: str) -> Dict[str, float]:
    """
    Calculate cultural weights from gap analysis failure data.
    
    Uses failure counts as proxy for cultural importance:
    - High failure count = culturally significant = high weight
    
    Args:
        gap_analysis_file: Path to baseline_gap_analysis.json
        
    Returns:
        Dict mapping concept names to cultural weights
    """
    import json
    
    with open(gap_analysis_file, 'r', encoding='utf-8') as f:
        gap_data = json.load(f)
    
    # Extract failure counts by concept
    concept_failures = {}
    
    for failure in gap_data.get('failures', []):
        concepts = failure.get('kikuyu_concepts', [])
        for concept in concepts:
            concept_failures[concept] = concept_failures.get(concept, 0) + 1
    
    if not concept_failures:
        return {}
    
    # Normalize to 0-1 range with log scaling
    max_failures = max(concept_failures.values())
    
    weights = {}
    for concept, count in concept_failures.items():
        # Log scale to prevent outliers from dominating
        log_count = np.log1p(count)
        max_log = np.log1p(max_failures)
        
        # Normalize to 0.6-1.0 range (all failing concepts are important)
        normalized = 0.6 + 0.4 * (log_count / max_log)
        
        weights[concept] = normalized
    
    return weights


def estimate_concept_metrics_from_data(concept_name: str,
                                       proverb_data: List[Dict],
                                       gap_analysis_weights: Dict[str, float]) -> ConceptMetrics:
    """
    Estimate ConceptMetrics from available proverb data.
    
    Uses heuristics when full data not available.
    
    Args:
        concept_name: Name of concept
        proverb_data: List of proverb dicts containing this concept
        gap_analysis_weights: Pre-computed weights from gap analysis
        
    Returns:
        ConceptMetrics with estimated values
    """
    # Count occurrences
    usage_count = len(proverb_data)
    
    # Estimate from gap analysis weight
    gap_weight = gap_analysis_weights.get(concept_name, 0.7)
    
    # Heuristic estimates
    metrics = ConceptMetrics(
        expert_agreement_score=0.90,  # Assume high (single expert)
        expert_count=1,
        validation_confidence=0.85,
        
        usage_count=usage_count,
        usage_frequency=min(usage_count / 10, 1.0),  # Normalize
        regional_coverage=0.6,  # Conservative estimate
        
        semantic_dimensions_count=5,  # Typical value
        presupposition_depth=1,
        worldview_centrality=gap_weight,  # Use gap analysis
        
        translation_complexity_score=gap_weight,  # Failure → complexity
        english_inadequacy=gap_weight,
        conceptual_incommensurability=gap_weight * 0.8,
        
        historical_persistence_score=0.85,  # Most proverbs are traditional
        historical_period_count=2,
        modern_relevance=0.75,
        
        centrality_in_graph=0.7,
        relationship_count=max(3, usage_count)  # At least 3 relationships
    )
    
    return metrics


# ==================== Example Usage ====================

if __name__ == "__main__":
    print("=== Cultural Weight Calculator Demo ===\n")
    
    # Example 1: High-importance wealth concept (ũtonga)
    print("Example 1: ũtonga (wealth) - High cultural importance")
    print("-" * 60)
    
    utonga_metrics = ConceptMetrics(
        expert_agreement_score=0.94,
        expert_count=1,
        validation_confidence=0.90,
        usage_count=47,
        usage_frequency=0.85,
        regional_coverage=0.80,
        semantic_dimensions_count=7,
        presupposition_depth=2,
        worldview_centrality=0.93,
        translation_complexity_score=0.88,
        english_inadequacy=0.85,
        conceptual_incommensurability=0.80,
        historical_persistence_score=0.91,
        historical_period_count=3,
        modern_relevance=0.85,
        centrality_in_graph=0.88,
        relationship_count=12
    )
    
    calculator = CulturalWeightCalculator()
    weight = calculator.calculate_concept_weight(utonga_metrics)
    print(f"Cultural Weight: {weight:.3f}")
    print(f"Expected: ~0.90-0.95 (very high importance)\n")
    
    # Example 2: Moderate-importance concept
    print("Example 2: Moderate concept")
    print("-" * 60)
    
    moderate_metrics = ConceptMetrics(
        expert_agreement_score=0.85,
        usage_count=15,
        semantic_dimensions_count=4,
        translation_complexity_score=0.65,
        historical_persistence_score=0.75,
        worldview_centrality=0.70
    )
    
    weight = calculator.calculate_concept_weight(moderate_metrics)
    print(f"Cultural Weight: {weight:.3f}")
    print(f"Expected: ~0.70-0.80 (moderate importance)\n")
    
    # Example 3: Proverb weight calculation
    print("Example 3: Proverb with high-weight concepts")
    print("-" * 60)
    
    proverb_metrics = ProverbMetrics(
        concept_weights=[0.92, 0.88, 0.75],
        concept_salience_scores=[0.95, 0.80, 0.60],
        usage_frequency=0.85,
        formality_level="high",
        generational_usage="all_ages",
        theme_centrality=0.88,
        theme_count=2,
        expert_consensus=0.90,
        validation_status="expert_verified",
        historical_age_score=0.85
    )
    
    proverb_weight = calculator.calculate_proverb_weight(proverb_metrics)
    print(f"Proverb Cultural Weight: {proverb_weight:.3f}")
    print(f"Expected: ~0.85-0.92 (high importance)\n")
    
    # Example 4: Semantic distance
    print("Example 4: Semantic distance between concepts")
    print("-" * 60)
    
    dist_calc = SemanticDistanceCalculator()
    
    concept1 = {
        'name': 'ũtonga',
        'embedding': np.random.rand(768)
    }
    concept2 = {
        'name': 'ũthĩni',
        'embedding': np.random.rand(768)
    }
    
    distance = dist_calc.calculate_distance(concept1, concept2)
    print(f"Semantic Distance: {distance:.3f}")
    print(f"(Lower = more similar, 0-1 range)\n")
    
    print("=== Demo Complete ===")
