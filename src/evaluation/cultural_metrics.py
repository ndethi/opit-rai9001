#!/usr/bin/env python3
"""
Cultural Translation Evaluation Metrics for thiLLMo OG-RAG System

Comprehensive evaluation metrics specifically designed for Kikuyu proverb translation
quality assessment, integrating cultural authenticity, linguistic fidelity, and 
business relevance measures.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from rouge_score import rouge_scorer
import json
import logging
from datetime import datetime
from pathlib import Path
import asyncio
from dataclasses import dataclass, asdict
import re

# Download required NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CulturalMetricsConfig:
    """Configuration for cultural translation metrics."""
    sentence_model_name: str = 'all-MiniLM-L6-v2'
    rouge_types: List[str] = None
    cultural_weight: float = 0.40
    fidelity_weight: float = 0.35
    business_weight: float = 0.15
    expert_weight: float = 0.10
    min_cultural_threshold: float = 0.6
    min_fidelity_threshold: float = 0.5
    min_business_threshold: float = 0.4
    enable_kikuyu_specific: bool = True
    
    def __post_init__(self):
        if self.rouge_types is None:
            self.rouge_types = ['rouge1', 'rouge2', 'rougeL']

@dataclass
class CulturalEvaluationResult:
    """Comprehensive cultural evaluation result."""
    proverb_id: str
    translation_system: str
    cultural_authenticity: float
    translation_fidelity: float
    business_relevance: float
    expert_alignment: float
    overall_quality: float
    detailed_metrics: Dict
    kikuyu_specific_metrics: Dict
    evaluation_timestamp: str
    quality_grade: str
    recommendations: List[str]

class KikuyuCulturalPatterns:
    """Kikuyu-specific cultural patterns and concepts for evaluation."""
    
    def __init__(self):
        self.cultural_concepts = {
            'community_values': [
                'ubuntu', 'togetherness', 'community', 'sharing', 'collective',
                'family', 'clan', 'tribe', 'unity', 'cooperation', 'harambee'
            ],
            'traditional_wisdom': [
                'elder', 'ancestor', 'tradition', 'custom', 'heritage',
                'proverb', 'wisdom', 'teaching', 'lesson', 'guidance'
            ],
            'agricultural_metaphors': [
                'harvest', 'seed', 'plant', 'farm', 'field', 'season',
                'rain', 'drought', 'cultivation', 'growth', 'fruit'
            ],
            'animal_symbolism': [
                'elephant', 'lion', 'hyena', 'bird', 'goat', 'cow',
                'hare', 'tortoise', 'snake', 'bee', 'ant'
            ],
            'social_hierarchy': [
                'respect', 'authority', 'leadership', 'elder', 'young',
                'teacher', 'student', 'master', 'apprentice'
            ],
            'moral_values': [
                'honesty', 'integrity', 'patience', 'perseverance', 'humility',
                'generosity', 'kindness', 'justice', 'truth', 'honor'
            ]
        }
        
        self.business_concepts = {
            'entrepreneurship': [
                'business', 'trade', 'market', 'profit', 'investment',
                'venture', 'opportunity', 'risk', 'innovation', 'growth'
            ],
            'wealth_creation': [
                'wealth', 'prosperity', 'riches', 'abundance', 'success',
                'achievement', 'accumulation', 'saving', 'earning'
            ],
            'resource_management': [
                'resource', 'manage', 'allocate', 'distribute', 'optimize',
                'efficiency', 'productivity', 'utilization', 'conservation'
            ],
            'collaboration': [
                'partnership', 'teamwork', 'cooperation', 'alliance',
                'network', 'relationship', 'trust', 'collaboration'
            ]
        }
        
        # Compile patterns for efficient matching
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for cultural concept detection."""
        self.cultural_patterns = {}
        self.business_patterns = {}
        
        for category, concepts in self.cultural_concepts.items():
            pattern = r'\b(?:' + '|'.join(concepts) + r')\b'
            self.cultural_patterns[category] = re.compile(pattern, re.IGNORECASE)
        
        for category, concepts in self.business_concepts.items():
            pattern = r'\b(?:' + '|'.join(concepts) + r')\b'
            self.business_patterns[category] = re.compile(pattern, re.IGNORECASE)
    
    def analyze_cultural_concepts(self, text: str) -> Dict[str, float]:
        """Analyze presence of Kikuyu cultural concepts in text."""
        if not text:
            return {}
        
        concept_scores = {}
        total_words = len(text.split())
        
        for category, pattern in self.cultural_patterns.items():
            matches = pattern.findall(text)
            concept_scores[category] = len(matches) / max(total_words, 1)
        
        return concept_scores
    
    def analyze_business_concepts(self, text: str) -> Dict[str, float]:
        """Analyze presence of business concepts in text."""
        if not text:
            return {}
        
        concept_scores = {}
        total_words = len(text.split())
        
        for category, pattern in self.business_patterns.items():
            matches = pattern.findall(text)
            concept_scores[category] = len(matches) / max(total_words, 1)
        
        return concept_scores

class CulturalTranslationMetrics:
    """Comprehensive cultural translation evaluation metrics for Kikuyu proverbs."""
    
    def __init__(self, config: Optional[CulturalMetricsConfig] = None):
        """Initialize cultural evaluation metrics."""
        self.config = config or CulturalMetricsConfig()
        
        # Initialize models
        logger.info(f"Loading sentence transformer: {self.config.sentence_model_name}")
        self.sentence_model = SentenceTransformer(self.config.sentence_model_name)
        
        # Initialize ROUGE scorer
        self.rouge_scorer = rouge_scorer.RougeScorer(
            self.config.rouge_types, 
            use_stemmer=True
        )
        
        # Initialize Kikuyu-specific patterns
        if self.config.enable_kikuyu_specific:
            self.kikuyu_patterns = KikuyuCulturalPatterns()
        
        logger.info("Cultural translation metrics initialized")
    
    def calculate_cultural_authenticity_score(self, 
                                            translation: str,
                                            expert_translation: str,
                                            cultural_context: str = "",
                                            og_rag_context: str = "") -> Dict[str, float]:
        """Calculate comprehensive cultural authenticity preservation score."""
        
        if not translation or not expert_translation:
            return {'cultural_authenticity': 0.0, 'error': 'Missing translation text'}
        
        # Semantic similarity to expert translation
        translation_emb = self.sentence_model.encode([translation])
        expert_emb = self.sentence_model.encode([expert_translation])
        semantic_similarity = cosine_similarity(translation_emb, expert_emb)[0][0]
        
        # Cultural context inclusion (if provided)
        context_preservation = 1.0
        if cultural_context:
            context_emb = self.sentence_model.encode([cultural_context])
            context_similarity = cosine_similarity(translation_emb, context_emb)[0][0]
            context_preservation = context_similarity
        
        # OG-RAG cultural context utilization
        og_rag_utilization = 1.0
        if og_rag_context:
            og_rag_emb = self.sentence_model.encode([og_rag_context])
            og_rag_similarity = cosine_similarity(translation_emb, og_rag_emb)[0][0]
            og_rag_utilization = og_rag_similarity
        
        # Kikuyu-specific cultural concept analysis
        kikuyu_analysis = {}
        if self.config.enable_kikuyu_specific:
            translation_concepts = self.kikuyu_patterns.analyze_cultural_concepts(translation)
            expert_concepts = self.kikuyu_patterns.analyze_cultural_concepts(expert_translation)
            
            # Calculate concept preservation
            concept_preservation = []
            for category in translation_concepts:
                if category in expert_concepts:
                    preservation = min(translation_concepts[category], expert_concepts[category]) / max(expert_concepts[category], 0.001)
                    concept_preservation.append(preservation)
            
            kikuyu_analysis = {
                'translation_concepts': translation_concepts,
                'expert_concepts': expert_concepts,
                'concept_preservation': np.mean(concept_preservation) if concept_preservation else 0.0
            }
        
        # Combined cultural authenticity score
        cultural_authenticity = (
            semantic_similarity * 0.4 + 
            context_preservation * 0.25 + 
            og_rag_utilization * 0.20 +
            kikuyu_analysis.get('concept_preservation', 0.0) * 0.15
        )
        
        return {
            'cultural_authenticity': cultural_authenticity,
            'semantic_similarity': semantic_similarity,
            'context_preservation': context_preservation,
            'og_rag_utilization': og_rag_utilization,
            'kikuyu_analysis': kikuyu_analysis
        }
    
    def calculate_translation_fidelity(self, 
                                     translation: str,
                                     expert_translation: str) -> Dict[str, float]:
        """Calculate comprehensive translation fidelity using multiple metrics."""
        
        if not translation or not expert_translation:
            return {'overall_fidelity': 0.0, 'error': 'Missing translation text'}
        
        # ROUGE scores for lexical overlap
        rouge_scores = self.rouge_scorer.score(expert_translation, translation)
        
        # Semantic similarity
        translation_emb = self.sentence_model.encode([translation])
        expert_emb = self.sentence_model.encode([expert_translation])
        semantic_sim = cosine_similarity(translation_emb, expert_emb)[0][0]
        
        # Length ratio (penalty for too short/long translations)
        length_ratio = min(len(translation), len(expert_translation)) / max(len(translation), len(expert_translation))
        
        # Word overlap analysis
        translation_words = set(translation.lower().split())
        expert_words = set(expert_translation.lower().split())
        word_overlap = len(translation_words.intersection(expert_words)) / len(expert_words.union(translation_words))
        
        # Structural similarity (sentence structure)
        translation_tokens = nltk.word_tokenize(translation.lower())
        expert_tokens = nltk.word_tokenize(expert_translation.lower())
        structural_similarity = len(set(translation_tokens).intersection(set(expert_tokens))) / len(set(expert_tokens).union(set(translation_tokens)))
        
        fidelity_metrics = {
            'rouge1_f': rouge_scores['rouge1'].fmeasure,
            'rouge2_f': rouge_scores['rouge2'].fmeasure,
            'rougeL_f': rouge_scores['rougeL'].fmeasure,
            'semantic_similarity': semantic_sim,
            'length_ratio': length_ratio,
            'word_overlap': word_overlap,
            'structural_similarity': structural_similarity,
            'overall_fidelity': (
                rouge_scores['rougeL'].fmeasure * 0.25 + 
                semantic_sim * 0.35 + 
                length_ratio * 0.15 +
                word_overlap * 0.15 +
                structural_similarity * 0.10
            )
        }
        
        return fidelity_metrics
    
    def calculate_business_relevance_score(self,
                                         business_application: str,
                                         expert_business_context: str,
                                         og_rag_business_context: str = "") -> Dict[str, float]:
        """Calculate comprehensive business relevance preservation score."""
        
        if not business_application or not expert_business_context:
            return {'business_relevance': 0.0, 'error': 'Missing business context'}
        
        # Semantic similarity to expert business context
        business_emb = self.sentence_model.encode([business_application])
        expert_business_emb = self.sentence_model.encode([expert_business_context])
        business_similarity = cosine_similarity(business_emb, expert_business_emb)[0][0]
        
        # OG-RAG business context utilization
        og_rag_business_sim = 1.0
        if og_rag_business_context:
            og_rag_business_emb = self.sentence_model.encode([og_rag_business_context])
            og_rag_business_sim = cosine_similarity(business_emb, og_rag_business_emb)[0][0]
        
        # Business concept analysis
        business_analysis = {}
        if self.config.enable_kikuyu_specific:
            application_concepts = self.kikuyu_patterns.analyze_business_concepts(business_application)
            expert_concepts = self.kikuyu_patterns.analyze_business_concepts(expert_business_context)
            
            # Calculate business concept preservation
            concept_preservation = []
            for category in application_concepts:
                if category in expert_concepts:
                    preservation = min(application_concepts[category], expert_concepts[category]) / max(expert_concepts[category], 0.001)
                    concept_preservation.append(preservation)
            
            business_analysis = {
                'application_concepts': application_concepts,
                'expert_concepts': expert_concepts,
                'business_concept_preservation': np.mean(concept_preservation) if concept_preservation else 0.0
            }
        
        # Combined business relevance score
        business_relevance = (
            business_similarity * 0.5 + 
            og_rag_business_sim * 0.3 +
            business_analysis.get('business_concept_preservation', 0.0) * 0.2
        )
        
        return {
            'business_relevance': business_relevance,
            'business_similarity': business_similarity,
            'og_rag_business_utilization': og_rag_business_sim,
            'business_analysis': business_analysis
        }
    
    def calculate_expert_alignment_score(self,
                                       expert_cultural_score: float,
                                       expert_translation_score: float,
                                       expert_business_score: float,
                                       expert_fluency_score: float,
                                       max_score: float = 5.0) -> Dict[str, float]:
        """Calculate alignment with expert evaluation scores."""
        
        # Normalize expert scores to 0-1 range
        cultural_alignment = expert_cultural_score / max_score
        translation_alignment = expert_translation_score / max_score
        business_alignment = expert_business_score / max_score
        fluency_alignment = expert_fluency_score / max_score
        
        # Weighted expert alignment (matching our evaluation weights)
        expert_alignment = (
            cultural_alignment * 0.40 +
            translation_alignment * 0.35 +
            business_alignment * 0.15 +
            fluency_alignment * 0.10
        )
        
        return {
            'expert_alignment': expert_alignment,
            'cultural_alignment': cultural_alignment,
            'translation_alignment': translation_alignment,
            'business_alignment': business_alignment,
            'fluency_alignment': fluency_alignment
        }
    
    def calculate_overall_quality_score(self,
                                      translation: str,
                                      expert_translation: str,
                                      cultural_context: str = "",
                                      business_application: str = "",
                                      expert_business_context: str = "",
                                      og_rag_context: str = "",
                                      og_rag_business_context: str = "",
                                      expert_cultural_score: float = 5.0,
                                      expert_translation_score: float = 5.0,
                                      expert_business_score: float = 5.0,
                                      expert_fluency_score: float = 5.0) -> Dict[str, Union[float, Dict]]:
        """Calculate comprehensive translation quality score."""
        
        # Cultural authenticity (configurable weight, default 40%)
        cultural_metrics = self.calculate_cultural_authenticity_score(
            translation, expert_translation, cultural_context, og_rag_context
        )
        cultural_auth = cultural_metrics['cultural_authenticity']
        
        # Translation fidelity (configurable weight, default 35%)
        fidelity_metrics = self.calculate_translation_fidelity(translation, expert_translation)
        translation_fidelity = fidelity_metrics['overall_fidelity']
        
        # Business relevance (configurable weight, default 15%)
        business_metrics = self.calculate_business_relevance_score(
            business_application, expert_business_context, og_rag_business_context
        )
        business_relevance = business_metrics['business_relevance']
        
        # Expert validation alignment (configurable weight, default 10%)
        expert_metrics = self.calculate_expert_alignment_score(
            expert_cultural_score, expert_translation_score, 
            expert_business_score, expert_fluency_score
        )
        expert_alignment = expert_metrics['expert_alignment']
        
        # Overall quality score
        overall_quality = (
            cultural_auth * self.config.cultural_weight +
            translation_fidelity * self.config.fidelity_weight +
            business_relevance * self.config.business_weight +
            expert_alignment * self.config.expert_weight
        )
        
        # Quality grade assignment
        quality_grade = self._assign_quality_grade(overall_quality)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            cultural_auth, translation_fidelity, business_relevance, expert_alignment
        )
        
        quality_scores = {
            'cultural_authenticity': cultural_auth,
            'translation_fidelity': translation_fidelity,
            'business_relevance': business_relevance,
            'expert_alignment': expert_alignment,
            'overall_quality': overall_quality,
            'quality_grade': quality_grade,
            'recommendations': recommendations,
            'detailed_metrics': {
                'cultural_metrics': cultural_metrics,
                'fidelity_metrics': fidelity_metrics,
                'business_metrics': business_metrics,
                'expert_metrics': expert_metrics
            },
            'evaluation_config': asdict(self.config)
        }
        
        return quality_scores
    
    def _assign_quality_grade(self, overall_quality: float) -> str:
        """Assign quality grade based on overall score."""
        if overall_quality >= 0.90:
            return "A+"
        elif overall_quality >= 0.85:
            return "A"
        elif overall_quality >= 0.80:
            return "A-"
        elif overall_quality >= 0.75:
            return "B+"
        elif overall_quality >= 0.70:
            return "B"
        elif overall_quality >= 0.65:
            return "B-"
        elif overall_quality >= 0.60:
            return "C+"
        elif overall_quality >= 0.55:
            return "C"
        elif overall_quality >= 0.50:
            return "C-"
        else:
            return "F"
    
    def _generate_recommendations(self, cultural: float, fidelity: float, 
                                business: float, expert: float) -> List[str]:
        """Generate improvement recommendations based on metric scores."""
        recommendations = []
        
        if cultural < self.config.min_cultural_threshold:
            recommendations.append(
                f"Improve cultural authenticity (current: {cultural:.2f}, target: ≥{self.config.min_cultural_threshold:.2f}). "
                "Consider incorporating more traditional Kikuyu concepts and cultural context."
            )
        
        if fidelity < self.config.min_fidelity_threshold:
            recommendations.append(
                f"Enhance translation fidelity (current: {fidelity:.2f}, target: ≥{self.config.min_fidelity_threshold:.2f}). "
                "Focus on semantic accuracy and structural similarity to expert translations."
            )
        
        if business < self.config.min_business_threshold:
            recommendations.append(
                f"Strengthen business relevance (current: {business:.2f}, target: ≥{self.config.min_business_threshold:.2f}). "
                "Better integrate entrepreneurship applications and modern business contexts."
            )
        
        if expert < 0.7:
            recommendations.append(
                f"Improve alignment with expert evaluations (current: {expert:.2f}). "
                "Review expert feedback and adjust translation approach accordingly."
            )
        
        if not recommendations:
            recommendations.append("Excellent translation quality achieved across all metrics!")
        
        return recommendations
    
    def evaluate_translation_batch(self, 
                                 translations_df: pd.DataFrame,
                                 save_results: bool = True,
                                 output_dir: str = "data/evaluation/metrics") -> List[CulturalEvaluationResult]:
        """Evaluate a batch of translations with comprehensive metrics."""
        
        logger.info(f"Evaluating batch of {len(translations_df)} translations")
        
        results = []
        for idx, row in translations_df.iterrows():
            try:
                # Extract required fields
                proverb_id = row.get('proverb_id', f'unknown_{idx}')
                translation = row.get('translation', row.get('og_rag_translation', ''))
                expert_translation = row.get('expert_translation', '')
                
                # Optional fields
                cultural_context = row.get('cultural_context', row.get('expert_cultural_meaning', ''))
                business_application = row.get('business_application', row.get('og_rag_business_relevance', ''))
                expert_business_context = row.get('expert_business_relevance', '')
                og_rag_context = row.get('og_rag_cultural_meaning', '')
                og_rag_business_context = row.get('og_rag_business_relevance', '')
                
                # Expert scores (default to 5.0 if not provided)
                expert_cultural_score = row.get('expert_cultural_faithfulness', 5.0)
                expert_translation_score = row.get('expert_translation_accuracy', 5.0)
                expert_business_score = row.get('expert_business_relevance', 5.0)
                expert_fluency_score = row.get('expert_overall_fluency', 5.0)
                
                # System identification
                system_type = row.get('system_type', 'unknown')
                
                # Calculate comprehensive metrics
                quality_scores = self.calculate_overall_quality_score(
                    translation=translation,
                    expert_translation=expert_translation,
                    cultural_context=cultural_context,
                    business_application=business_application,
                    expert_business_context=expert_business_context,
                    og_rag_context=og_rag_context,
                    og_rag_business_context=og_rag_business_context,
                    expert_cultural_score=expert_cultural_score,
                    expert_translation_score=expert_translation_score,
                    expert_business_score=expert_business_score,
                    expert_fluency_score=expert_fluency_score
                )
                
                # Create evaluation result
                result = CulturalEvaluationResult(
                    proverb_id=proverb_id,
                    translation_system=system_type,
                    cultural_authenticity=quality_scores['cultural_authenticity'],
                    translation_fidelity=quality_scores['translation_fidelity'],
                    business_relevance=quality_scores['business_relevance'],
                    expert_alignment=quality_scores['expert_alignment'],
                    overall_quality=quality_scores['overall_quality'],
                    detailed_metrics=quality_scores['detailed_metrics'],
                    kikuyu_specific_metrics=quality_scores['detailed_metrics']['cultural_metrics'].get('kikuyu_analysis', {}),
                    evaluation_timestamp=datetime.now().isoformat(),
                    quality_grade=quality_scores['quality_grade'],
                    recommendations=quality_scores['recommendations']
                )
                
                results.append(result)
                
                if idx % 10 == 0:
                    logger.info(f"Evaluated {idx + 1}/{len(translations_df)} translations")
                
            except Exception as e:
                logger.error(f"Failed to evaluate translation {idx}: {e}")
                continue
        
        logger.info(f"✅ Batch evaluation completed: {len(results)} successful evaluations")
        
        # Save results if requested
        if save_results:
            self._save_evaluation_results(results, output_dir)
        
        return results
    
    def _save_evaluation_results(self, results: List[CulturalEvaluationResult], output_dir: str):
        """Save evaluation results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save detailed results as JSON
        results_data = [asdict(result) for result in results]
        json_file = output_path / f"cultural_evaluation_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        # Save summary as CSV
        summary_data = []
        for result in results:
            summary_data.append({
                'proverb_id': result.proverb_id,
                'translation_system': result.translation_system,
                'cultural_authenticity': result.cultural_authenticity,
                'translation_fidelity': result.translation_fidelity,
                'business_relevance': result.business_relevance,
                'expert_alignment': result.expert_alignment,
                'overall_quality': result.overall_quality,
                'quality_grade': result.quality_grade,
                'evaluation_timestamp': result.evaluation_timestamp
            })
        
        summary_df = pd.DataFrame(summary_data)
        csv_file = output_path / f"cultural_evaluation_summary_{timestamp}.csv"
        summary_df.to_csv(csv_file, index=False, encoding='utf-8')
        
        logger.info(f"💾 Evaluation results saved:")
        logger.info(f"  📄 Detailed: {json_file}")
        logger.info(f"  📊 Summary: {csv_file}")

def main():
    """Demonstrate cultural translation metrics with sample data."""
    
    # Initialize metrics with custom configuration
    config = CulturalMetricsConfig(
        cultural_weight=0.45,  # Emphasize cultural authenticity for Kikuyu
        fidelity_weight=0.30,
        business_weight=0.15,
        expert_weight=0.10,
        min_cultural_threshold=0.65  # Higher threshold for cultural preservation
    )
    
    metrics = CulturalTranslationMetrics(config)
    
    # Sample evaluation data
    sample_data = {
        'proverb_id': 'KP001',
        'translation': 'Hard work leads to success and prosperity',
        'expert_translation': 'Diligent effort brings prosperity and wealth',
        'cultural_context': 'Traditional Kikuyu values emphasizing community effort and collective prosperity',
        'business_application': 'Entrepreneurship requires persistent effort and community support',
        'expert_business_context': 'Business success comes from consistent work and collaborative relationships',
        'og_rag_context': 'Kikuyu proverb teaching about work ethic and community values',
        'og_rag_business_context': 'Modern business applications of traditional work principles',
        'expert_cultural_score': 4.2,
        'expert_translation_score': 4.0,
        'expert_business_score': 3.8,
        'expert_fluency_score': 4.5,
        'system_type': 'og_rag'
    }
    
    # Calculate comprehensive quality scores
    quality_scores = metrics.calculate_overall_quality_score(
        translation=sample_data['translation'],
        expert_translation=sample_data['expert_translation'],
        cultural_context=sample_data['cultural_context'],
        business_application=sample_data['business_application'],
        expert_business_context=sample_data['expert_business_context'],
        og_rag_context=sample_data['og_rag_context'],
        og_rag_business_context=sample_data['og_rag_business_context'],
        expert_cultural_score=sample_data['expert_cultural_score'],
        expert_translation_score=sample_data['expert_translation_score'],
        expert_business_score=sample_data['expert_business_score'],
        expert_fluency_score=sample_data['expert_fluency_score']
    )
    
    # Display results
    print("🎯 Cultural Translation Quality Metrics Demo")
    print("=" * 60)
    print(f"📝 Translation: {sample_data['translation']}")
    print(f"👨‍🏫 Expert: {sample_data['expert_translation']}")
    print(f"🏛️ Cultural Context: {sample_data['cultural_context'][:80]}...")
    print()
    print("📊 Quality Scores:")
    print(f"  🏛️ Cultural Authenticity: {quality_scores['cultural_authenticity']:.3f}")
    print(f"  📝 Translation Fidelity: {quality_scores['translation_fidelity']:.3f}")
    print(f"  💼 Business Relevance: {quality_scores['business_relevance']:.3f}")
    print(f"  👨‍🏫 Expert Alignment: {quality_scores['expert_alignment']:.3f}")
    print(f"  🎯 Overall Quality: {quality_scores['overall_quality']:.3f}")
    print(f"  🏆 Quality Grade: {quality_scores['quality_grade']}")
    print()
    print("💡 Recommendations:")
    for i, rec in enumerate(quality_scores['recommendations'], 1):
        print(f"  {i}. {rec}")

if __name__ == "__main__":
    main()