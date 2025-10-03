#!/usr/bin/env python3
"""
Ontology Gap Analyzer for Baseline Translation Evaluation

Analyzes translations to identify missing cultural concepts that the ontology should capture.
Compares translations against expert translations to determine what cultural knowledge is lost.
"""

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class OntologyGapAnalysis:
    """Analysis of cultural concepts missing from a translation."""
    missing_concepts: List[str]  # Concepts present in expert but missing in translation
    misinterpreted_concepts: List[str]  # Concepts translated incorrectly
    cultural_context_score: float  # 0-1 score of cultural preservation
    recommended_ontology_nodes: List[str]  # Ontology nodes that should be added
    gap_summary: str  # Human-readable summary of gaps


class OntologyGapAnalyzer:
    """
    Analyzes translation gaps to inform ontology construction.
    
    Identifies cultural concepts, metaphors, and traditional wisdom
    that are lost or misinterpreted in automated translations.
    """
    
    def __init__(self):
        """Initialize with Kikuyu cultural concept patterns."""
        
        # Core cultural concepts from ontology builder
        self.cultural_concepts = {
            'work_ethics': {
                'keywords': ['work', 'diligent', 'labor', 'effort', 'industry', 'toil'],
                'kikuyu_terms': ['kũruta', 'wĩra', 'kũndũ', 'gũtũũra', 'ũrutani'],
                'ontology_relevance': 'Traditional Kikuyu work ethic values'
            },
            'community': {
                'keywords': ['community', 'together', 'people', 'collective', 'unity', 'cooperation'],
                'kikuyu_terms': ['andũ', 'mũndũ', 'ũrata', 'kĩrĩndĩ', 'gũtaarana', 'ũnyiitania'],
                'ontology_relevance': 'Ubuntu philosophy and collective identity'
            },
            'wisdom': {
                'keywords': ['wisdom', 'knowledge', 'experience', 'understanding', 'insight', 'elder'],
                'kikuyu_terms': ['ũũgĩ', 'ũmenyo', 'kũmenya', 'gũtaũkĩrwo', 'meciiria'],
                'ontology_relevance': 'Traditional knowledge and decision-making'
            },
            'prosperity': {
                'keywords': ['wealth', 'prosperity', 'riches', 'abundance', 'success', 'fortune'],
                'kikuyu_terms': ['ũtonga', 'kũgaacĩra', 'indo', 'mbeeca', 'ũgaacĩru', 'gĩthaka'],
                'ontology_relevance': 'Holistic understanding of wealth'
            },
            'patience': {
                'keywords': ['patience', 'wait', 'time', 'gradual', 'perseverance', 'endurance'],
                'kikuyu_terms': ['gũkirĩrĩria', 'gũeterera', 'ũkirĩrĩria', 'gũikara', 'kũũrĩria'],
                'ontology_relevance': 'Long-term thinking and delayed gratification'
            },
            'leadership': {
                'keywords': ['leader', 'leadership', 'guide', 'authority', 'chief', 'elder'],
                'kikuyu_terms': ['atongoria', 'gũtongoria', 'mũnene', 'mũtongoria', 'ũtongoria'],
                'ontology_relevance': 'Traditional leadership principles'
            },
            'cooperation': {
                'keywords': ['cooperation', 'collaboration', 'teamwork', 'mutual', 'assistance', 'help'],
                'kikuyu_terms': ['ũrũmwe', 'gũtaarana', 'ũnyiitania', 'kũrũmana', 'gũteithania'],
                'ontology_relevance': 'Collaborative work principles (harambee)'
            },
            'resource_management': {
                'keywords': ['save', 'manage', 'resource', 'conserve', 'allocate', 'plan'],
                'kikuyu_terms': ['kũiga', 'gũthondeka', 'kũmenyerera', 'gũtungata'],
                'ontology_relevance': 'Traditional resource stewardship'
            },
            'consequences': {
                'keywords': ['consequence', 'result', 'outcome', 'effect', 'harvest', 'reap'],
                'kikuyu_terms': ['maciaro', 'kũgetha', 'ũndũ', 'matunda'],
                'ontology_relevance': 'Cause and effect in traditional wisdom'
            },
            'respect': {
                'keywords': ['respect', 'honor', 'dignity', 'reverence', 'esteem'],
                'kikuyu_terms': ['gũtĩĩa', 'kũheana', 'ũtĩĩi', 'ũheani'],
                'ontology_relevance': 'Social hierarchy and respect systems'
            }
        }
        
        # Common translation pitfalls
        self.common_losses = {
            'metaphorical_depth': 'Literal translation loses metaphorical meaning',
            'cultural_context': 'Cultural significance not captured',
            'traditional_wisdom': 'Traditional knowledge reference lost',
            'social_structure': 'Social hierarchy/relationships unclear',
            'agricultural_metaphor': 'Agricultural reference not translated',
            'animal_symbolism': 'Animal symbolic meaning lost',
            'proverb_structure': 'Traditional proverb structure altered'
        }
    
    def analyze_translation_gap(
        self,
        expert_translation: str,
        machine_translation: str,
        expert_cultural_meaning: str = "",
        kikuyu_text: str = ""
    ) -> OntologyGapAnalysis:
        """
        Analyze gaps between expert and machine translation.
        
        Args:
            expert_translation: Expert human translation
            machine_translation: Automated system translation
            expert_cultural_meaning: Cultural context from expert
            kikuyu_text: Original Kikuyu text
            
        Returns:
            OntologyGapAnalysis with identified gaps and recommendations
        """
        expert_lower = expert_translation.lower()
        machine_lower = machine_translation.lower()
        cultural_lower = expert_cultural_meaning.lower() if expert_cultural_meaning else ""
        
        # Identify concepts in expert translation
        expert_concepts = self._extract_concepts(expert_lower, cultural_lower)
        machine_concepts = self._extract_concepts(machine_lower, "")
        
        # Find missing concepts
        missing_concepts = list(expert_concepts - machine_concepts)
        
        # Find misinterpretations (opposite meanings, wrong metaphors)
        misinterpreted = self._detect_misinterpretations(
            expert_translation, machine_translation, expert_concepts
        )
        
        # Calculate cultural preservation score
        if not expert_concepts:
            cultural_score = 0.5  # No concepts to compare
        else:
            preserved = len(expert_concepts & machine_concepts)
            cultural_score = preserved / len(expert_concepts)
        
        # Recommend ontology nodes
        ontology_recommendations = self._recommend_ontology_nodes(
            missing_concepts, misinterpreted, expert_cultural_meaning
        )
        
        # Generate gap summary
        gap_summary = self._generate_gap_summary(
            missing_concepts, misinterpreted, cultural_score
        )
        
        return OntologyGapAnalysis(
            missing_concepts=missing_concepts,
            misinterpreted_concepts=misinterpreted,
            cultural_context_score=cultural_score,
            recommended_ontology_nodes=ontology_recommendations,
            gap_summary=gap_summary
        )
    
    def _extract_concepts(self, text: str, cultural_context: str = "") -> Set[str]:
        """Extract cultural concepts from text."""
        concepts = set()
        
        combined_text = f"{text} {cultural_context}"
        
        for concept_name, concept_data in self.cultural_concepts.items():
            # Check if any keywords are present
            for keyword in concept_data['keywords']:
                if keyword in combined_text:
                    concepts.add(concept_name)
                    break
        
        return concepts
    
    def _detect_misinterpretations(
        self,
        expert: str,
        machine: str,
        expert_concepts: Set[str]
    ) -> List[str]:
        """Detect concepts that are misinterpreted rather than missing."""
        misinterpreted = []
        
        # Check for opposite meanings
        opposites = {
            'wealth': ['poverty', 'lack', 'scarcity'],
            'wisdom': ['foolish', 'ignorance', 'unwise'],
            'patience': ['haste', 'rush', 'impatience'],
            'cooperation': ['conflict', 'competition', 'division']
        }
        
        expert_lower = expert.lower()
        machine_lower = machine.lower()
        
        for concept in expert_concepts:
            if concept in opposites:
                # Check if opposite meaning appears in machine translation
                for opposite in opposites[concept]:
                    if opposite in machine_lower and opposite not in expert_lower:
                        misinterpreted.append(f"{concept}_as_{opposite}")
        
        return misinterpreted
    
    def _recommend_ontology_nodes(
        self,
        missing_concepts: List[str],
        misinterpreted: List[str],
        cultural_meaning: str
    ) -> List[str]:
        """Recommend ontology nodes to add based on gaps."""
        recommendations = []
        
        for concept in missing_concepts:
            if concept in self.cultural_concepts:
                relevance = self.cultural_concepts[concept]['ontology_relevance']
                recommendations.append(f"{concept}: {relevance}")
        
        # Add recommendations based on cultural meaning
        if cultural_meaning:
            cultural_lower = cultural_meaning.lower()
            
            # Check for specific cultural elements
            if 'proverb' in cultural_lower or 'saying' in cultural_lower:
                recommendations.append("proverb_structure: Traditional saying structure and usage")
            
            if 'metaphor' in cultural_lower or 'symbol' in cultural_lower:
                recommendations.append("metaphorical_mapping: Cultural metaphor relationships")
            
            if 'business' in cultural_lower or 'entrepreneurship' in cultural_lower:
                recommendations.append("business_application: Modern business context mapping")
        
        return recommendations
    
    def _generate_gap_summary(
        self,
        missing: List[str],
        misinterpreted: List[str],
        score: float
    ) -> str:
        """Generate human-readable summary of gaps."""
        if score >= 0.8:
            quality = "GOOD"
            issue = "Minor gaps"
        elif score >= 0.5:
            quality = "MODERATE"
            issue = "Significant cultural loss"
        else:
            quality = "POOR"
            issue = "Major cultural concepts missing"
        
        parts = [f"{quality}: {issue}"]
        
        if missing:
            parts.append(f"Missing: {', '.join(missing[:3])}")
        
        if misinterpreted:
            parts.append(f"Misinterpreted: {len(misinterpreted)} concepts")
        
        return " | ".join(parts)
