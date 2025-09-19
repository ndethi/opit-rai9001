#!/usr/bin/env python3
"""
Integration script for Cultural Translation Metrics with Enhanced Translation Comparison System.

Provides seamless integration between the cultural evaluation metrics and the 
translation comparison pipeline for comprehensive evaluation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import asyncio
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.evaluation.cultural_metrics import (
    CulturalTranslationMetrics, 
    CulturalMetricsConfig,
    CulturalEvaluationResult
)
from scripts.enhanced_translation_comparison import EnhancedTranslationComparisonSystem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegratedCulturalEvaluationPipeline:
    """Complete pipeline integrating translation comparison with cultural metrics."""
    
    def __init__(self, 
                 cultural_config: Optional[CulturalMetricsConfig] = None,
                 comparison_config_file: Optional[str] = None):
        """Initialize integrated evaluation pipeline."""
        
        # Initialize cultural metrics
        self.cultural_config = cultural_config or CulturalMetricsConfig(
            cultural_weight=0.45,      # Emphasize cultural authenticity
            fidelity_weight=0.30,      # Translation accuracy
            business_weight=0.15,      # Business relevance
            expert_weight=0.10,        # Expert alignment
            min_cultural_threshold=0.65,
            min_fidelity_threshold=0.55,
            min_business_threshold=0.45,
            enable_kikuyu_specific=True
        )
        
        self.cultural_metrics = CulturalTranslationMetrics(self.cultural_config)
        
        # Initialize translation comparison system
        self.comparison_system = EnhancedTranslationComparisonSystem(comparison_config_file)
        
        # Output directories
        self.output_dir = Path("data/evaluation/integrated_analysis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Integrated Cultural Evaluation Pipeline initialized")
    
    async def run_complete_evaluation_pipeline(self, 
                                             benchmark_file: str,
                                             include_cultural_metrics: bool = True,
                                             include_llm_judge: bool = True,
                                             save_intermediate: bool = True) -> Dict:
        """Run complete evaluation pipeline with cultural metrics integration."""
        
        logger.info("🚀 Starting Complete Cultural Evaluation Pipeline")
        
        # Step 1: Run translation comparison to generate translations
        logger.info("Step 1: Generating translation comparisons...")
        comparison_summary = await self.comparison_system.run_complete_comparison_pipeline(
            benchmark_file
        )
        
        # Step 2: Load comprehensive comparison dataset
        logger.info("Step 2: Loading comparison dataset for cultural evaluation...")
        comparison_file = self.comparison_system.output_dir / "comprehensive_translation_comparison.csv"
        
        if not comparison_file.exists():
            raise FileNotFoundError(f"Comparison dataset not found: {comparison_file}")
        
        comparison_df = pd.read_csv(comparison_file)
        
        # Step 3: Apply cultural metrics evaluation
        cultural_results = []
        if include_cultural_metrics:
            logger.info("Step 3: Applying cultural translation metrics...")
            cultural_results = await self._evaluate_with_cultural_metrics(comparison_df)
        
        # Step 4: Integrate results and generate comprehensive analysis
        logger.info("Step 4: Integrating results and generating analysis...")
        integrated_analysis = await self._generate_integrated_analysis(
            comparison_df, cultural_results, comparison_summary
        )
        
        # Step 5: Save comprehensive results
        if save_intermediate:
            logger.info("Step 5: Saving comprehensive evaluation results...")
            await self._save_integrated_results(integrated_analysis)
        
        logger.info("✅ Complete Cultural Evaluation Pipeline finished!")
        return integrated_analysis
    
    async def _evaluate_with_cultural_metrics(self, comparison_df: pd.DataFrame) -> List[CulturalEvaluationResult]:
        """Apply cultural metrics to translation comparison data."""
        
        # Prepare data for cultural evaluation
        evaluation_data = []
        
        for idx, row in comparison_df.iterrows():
            # Evaluate OG-RAG system
            og_rag_data = {
                'proverb_id': row['proverb_id'],
                'translation': row.get('og_rag_translation', ''),
                'expert_translation': row.get('expert_translation', ''),
                'cultural_context': row.get('expert_cultural_meaning', ''),
                'business_application': row.get('og_rag_business_relevance', ''),
                'expert_business_context': row.get('expert_business_relevance', ''),
                'og_rag_context': row.get('og_rag_cultural_meaning', ''),
                'og_rag_business_context': row.get('og_rag_business_relevance', ''),
                'expert_cultural_score': row.get('expert_cultural_faithfulness', 5.0),
                'expert_translation_score': row.get('expert_translation_accuracy', 5.0),
                'expert_business_score': row.get('expert_business_relevance', 5.0),
                'expert_fluency_score': row.get('expert_overall_fluency', 5.0),
                'system_type': 'og_rag'
            }
            evaluation_data.append(og_rag_data)
            
            # Evaluate Raw LLM system
            raw_llm_data = {
                'proverb_id': row['proverb_id'],
                'translation': row.get('raw_llm_translation', ''),
                'expert_translation': row.get('expert_translation', ''),
                'cultural_context': row.get('expert_cultural_meaning', ''),
                'business_application': row.get('raw_llm_business_relevance', ''),
                'expert_business_context': row.get('expert_business_relevance', ''),
                'og_rag_context': '',  # Raw LLM doesn't have OG-RAG context
                'og_rag_business_context': '',
                'expert_cultural_score': row.get('expert_cultural_faithfulness', 5.0),
                'expert_translation_score': row.get('expert_translation_accuracy', 5.0),
                'expert_business_score': row.get('expert_business_relevance', 5.0),
                'expert_fluency_score': row.get('expert_overall_fluency', 5.0),
                'system_type': 'raw_llm'
            }
            evaluation_data.append(raw_llm_data)
        
        # Convert to DataFrame and evaluate
        evaluation_df = pd.DataFrame(evaluation_data)
        cultural_results = self.cultural_metrics.evaluate_translation_batch(
            evaluation_df, 
            save_results=True,
            output_dir=str(self.output_dir / "cultural_metrics")
        )
        
        return cultural_results
    
    async def _generate_integrated_analysis(self, 
                                           comparison_df: pd.DataFrame,
                                           cultural_results: List[CulturalEvaluationResult],
                                           comparison_summary: Dict) -> Dict:
        """Generate comprehensive integrated analysis."""
        
        # Organize cultural results by system type
        og_rag_results = [r for r in cultural_results if r.translation_system == 'og_rag']
        raw_llm_results = [r for r in cultural_results if r.translation_system == 'raw_llm']
        
        # Calculate system-level statistics
        og_rag_stats = self._calculate_system_statistics(og_rag_results, "OG-RAG")
        raw_llm_stats = self._calculate_system_statistics(raw_llm_results, "Raw LLM")
        
        # Comparative analysis
        comparative_analysis = self._perform_comparative_analysis(og_rag_results, raw_llm_results)
        
        # Cultural preservation analysis
        cultural_preservation = self._analyze_cultural_preservation(cultural_results)
        
        # Business relevance analysis
        business_relevance = self._analyze_business_relevance(cultural_results)
        
        # Quality distribution analysis
        quality_distribution = self._analyze_quality_distribution(cultural_results)
        
        # Generate recommendations
        recommendations = self._generate_system_recommendations(
            og_rag_stats, raw_llm_stats, comparative_analysis
        )
        
        # Integrate with LLM judge results if available
        llm_judge_integration = {}
        if comparison_summary.get('llm_judge_evaluation'):
            llm_judge_integration = self._integrate_llm_judge_results(
                comparison_summary['llm_judge_evaluation'], cultural_results
            )
        
        integrated_analysis = {
            "evaluation_metadata": {
                "pipeline_completion_timestamp": datetime.now().isoformat(),
                "total_proverbs_evaluated": len(comparison_df),
                "cultural_evaluations_completed": len(cultural_results),
                "evaluation_framework_version": "1.0.0",
                "cultural_metrics_config": self.cultural_config.__dict__
            },
            "system_performance": {
                "og_rag_system": og_rag_stats,
                "raw_llm_system": raw_llm_stats,
                "comparative_analysis": comparative_analysis
            },
            "cultural_analysis": {
                "cultural_preservation": cultural_preservation,
                "business_relevance": business_relevance,
                "quality_distribution": quality_distribution
            },
            "llm_judge_integration": llm_judge_integration,
            "recommendations": recommendations,
            "detailed_results": {
                "cultural_evaluation_results": [r.__dict__ for r in cultural_results],
                "translation_comparison_summary": comparison_summary
            }
        }
        
        return integrated_analysis
    
    def _calculate_system_statistics(self, results: List[CulturalEvaluationResult], system_name: str) -> Dict:
        """Calculate comprehensive statistics for a translation system."""
        
        if not results:
            return {"system_name": system_name, "error": "No results available"}
        
        # Extract metrics
        cultural_scores = [r.cultural_authenticity for r in results]
        fidelity_scores = [r.translation_fidelity for r in results]
        business_scores = [r.business_relevance for r in results]
        expert_scores = [r.expert_alignment for r in results]
        overall_scores = [r.overall_quality for r in results]
        
        # Quality grade distribution
        grade_distribution = {}
        for result in results:
            grade = result.quality_grade
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
        
        # Calculate statistics
        stats = {
            "system_name": system_name,
            "total_evaluations": len(results),
            "performance_metrics": {
                "cultural_authenticity": {
                    "mean": np.mean(cultural_scores),
                    "std": np.std(cultural_scores),
                    "min": np.min(cultural_scores),
                    "max": np.max(cultural_scores),
                    "median": np.median(cultural_scores)
                },
                "translation_fidelity": {
                    "mean": np.mean(fidelity_scores),
                    "std": np.std(fidelity_scores),
                    "min": np.min(fidelity_scores),
                    "max": np.max(fidelity_scores),
                    "median": np.median(fidelity_scores)
                },
                "business_relevance": {
                    "mean": np.mean(business_scores),
                    "std": np.std(business_scores),
                    "min": np.min(business_scores),
                    "max": np.max(business_scores),
                    "median": np.median(business_scores)
                },
                "expert_alignment": {
                    "mean": np.mean(expert_scores),
                    "std": np.std(expert_scores),
                    "min": np.min(expert_scores),
                    "max": np.max(expert_scores),
                    "median": np.median(expert_scores)
                },
                "overall_quality": {
                    "mean": np.mean(overall_scores),
                    "std": np.std(overall_scores),
                    "min": np.min(overall_scores),
                    "max": np.max(overall_scores),
                    "median": np.median(overall_scores)
                }
            },
            "quality_distribution": grade_distribution,
            "threshold_analysis": {
                "above_cultural_threshold": sum(1 for s in cultural_scores if s >= self.cultural_config.min_cultural_threshold),
                "above_fidelity_threshold": sum(1 for s in fidelity_scores if s >= self.cultural_config.min_fidelity_threshold),
                "above_business_threshold": sum(1 for s in business_scores if s >= self.cultural_config.min_business_threshold)
            }
        }
        
        return stats
    
    def _perform_comparative_analysis(self, 
                                    og_rag_results: List[CulturalEvaluationResult],
                                    raw_llm_results: List[CulturalEvaluationResult]) -> Dict:
        """Perform comparative analysis between systems."""
        
        if not og_rag_results or not raw_llm_results:
            return {"error": "Insufficient data for comparison"}
        
        # Extract scores for comparison
        og_rag_cultural = [r.cultural_authenticity for r in og_rag_results]
        raw_llm_cultural = [r.cultural_authenticity for r in raw_llm_results]
        
        og_rag_fidelity = [r.translation_fidelity for r in og_rag_results]
        raw_llm_fidelity = [r.translation_fidelity for r in raw_llm_results]
        
        og_rag_business = [r.business_relevance for r in og_rag_results]
        raw_llm_business = [r.business_relevance for r in raw_llm_results]
        
        og_rag_overall = [r.overall_quality for r in og_rag_results]
        raw_llm_overall = [r.overall_quality for r in raw_llm_results]
        
        # Calculate differences
        comparative_analysis = {
            "cultural_authenticity_advantage": {
                "og_rag_mean": np.mean(og_rag_cultural),
                "raw_llm_mean": np.mean(raw_llm_cultural),
                "difference": np.mean(og_rag_cultural) - np.mean(raw_llm_cultural),
                "relative_improvement": ((np.mean(og_rag_cultural) - np.mean(raw_llm_cultural)) / np.mean(raw_llm_cultural)) * 100
            },
            "translation_fidelity_comparison": {
                "og_rag_mean": np.mean(og_rag_fidelity),
                "raw_llm_mean": np.mean(raw_llm_fidelity),
                "difference": np.mean(og_rag_fidelity) - np.mean(raw_llm_fidelity),
                "relative_improvement": ((np.mean(og_rag_fidelity) - np.mean(raw_llm_fidelity)) / np.mean(raw_llm_fidelity)) * 100
            },
            "business_relevance_comparison": {
                "og_rag_mean": np.mean(og_rag_business),
                "raw_llm_mean": np.mean(raw_llm_business),
                "difference": np.mean(og_rag_business) - np.mean(raw_llm_business),
                "relative_improvement": ((np.mean(og_rag_business) - np.mean(raw_llm_business)) / np.mean(raw_llm_business)) * 100
            },
            "overall_quality_comparison": {
                "og_rag_mean": np.mean(og_rag_overall),
                "raw_llm_mean": np.mean(raw_llm_overall),
                "difference": np.mean(og_rag_overall) - np.mean(raw_llm_overall),
                "relative_improvement": ((np.mean(og_rag_overall) - np.mean(raw_llm_overall)) / np.mean(raw_llm_overall)) * 100
            },
            "statistical_significance": {
                "note": "Statistical tests would require scipy.stats implementation",
                "sample_sizes": {"og_rag": len(og_rag_results), "raw_llm": len(raw_llm_results)}
            }
        }
        
        return comparative_analysis
    
    def _analyze_cultural_preservation(self, results: List[CulturalEvaluationResult]) -> Dict:
        """Analyze cultural preservation across systems."""
        
        cultural_scores = [r.cultural_authenticity for r in results]
        
        # Cultural preservation levels
        high_preservation = sum(1 for s in cultural_scores if s >= 0.8)
        medium_preservation = sum(1 for s in cultural_scores if 0.6 <= s < 0.8)
        low_preservation = sum(1 for s in cultural_scores if s < 0.6)
        
        analysis = {
            "preservation_distribution": {
                "high_preservation": high_preservation,
                "medium_preservation": medium_preservation,
                "low_preservation": low_preservation,
                "total_evaluations": len(results)
            },
            "preservation_statistics": {
                "mean_cultural_score": np.mean(cultural_scores),
                "cultural_score_std": np.std(cultural_scores),
                "preservation_rate": (high_preservation + medium_preservation) / len(results) * 100
            }
        }
        
        return analysis
    
    def _analyze_business_relevance(self, results: List[CulturalEvaluationResult]) -> Dict:
        """Analyze business relevance across systems."""
        
        business_scores = [r.business_relevance for r in results]
        
        # Business relevance levels
        high_relevance = sum(1 for s in business_scores if s >= 0.7)
        medium_relevance = sum(1 for s in business_scores if 0.5 <= s < 0.7)
        low_relevance = sum(1 for s in business_scores if s < 0.5)
        
        analysis = {
            "relevance_distribution": {
                "high_relevance": high_relevance,
                "medium_relevance": medium_relevance,
                "low_relevance": low_relevance,
                "total_evaluations": len(results)
            },
            "relevance_statistics": {
                "mean_business_score": np.mean(business_scores),
                "business_score_std": np.std(business_scores),
                "relevance_rate": (high_relevance + medium_relevance) / len(results) * 100
            }
        }
        
        return analysis
    
    def _analyze_quality_distribution(self, results: List[CulturalEvaluationResult]) -> Dict:
        """Analyze overall quality distribution."""
        
        grade_counts = {}
        for result in results:
            grade = result.quality_grade
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        # Calculate percentages
        total = len(results)
        grade_percentages = {grade: (count / total) * 100 for grade, count in grade_counts.items()}
        
        analysis = {
            "grade_distribution": grade_counts,
            "grade_percentages": grade_percentages,
            "total_evaluations": total,
            "excellence_rate": sum(grade_counts.get(grade, 0) for grade in ['A+', 'A', 'A-']) / total * 100,
            "satisfactory_rate": sum(grade_counts.get(grade, 0) for grade in ['A+', 'A', 'A-', 'B+', 'B', 'B-']) / total * 100
        }
        
        return analysis
    
    def _generate_system_recommendations(self, og_rag_stats: Dict, raw_llm_stats: Dict, comparison: Dict) -> List[str]:
        """Generate system improvement recommendations."""
        
        recommendations = []
        
        # Cultural authenticity recommendations
        if comparison.get('cultural_authenticity_advantage', {}).get('difference', 0) > 0.1:
            recommendations.append(
                f"✅ OG-RAG system shows significant cultural authenticity advantage "
                f"({comparison['cultural_authenticity_advantage']['difference']:.3f} points). "
                f"Continue leveraging cultural ontology for enhanced context."
            )
        else:
            recommendations.append(
                "⚠️ Limited cultural authenticity advantage detected. "
                "Consider enriching cultural ontology with more diverse traditional contexts."
            )
        
        # Translation fidelity recommendations
        if comparison.get('translation_fidelity_comparison', {}).get('difference', 0) > 0.05:
            recommendations.append(
                f"✅ OG-RAG system shows translation fidelity advantage "
                f"({comparison['translation_fidelity_comparison']['difference']:.3f} points)."
            )
        else:
            recommendations.append(
                "⚠️ Translation fidelity needs improvement. "
                "Consider fine-tuning retrieval strategies and response generation."
            )
        
        # Business relevance recommendations
        if comparison.get('business_relevance_comparison', {}).get('difference', 0) > 0.1:
            recommendations.append(
                f"✅ Strong business relevance advantage demonstrated "
                f"({comparison['business_relevance_comparison']['difference']:.3f} points)."
            )
        else:
            recommendations.append(
                "💼 Enhance business context integration. "
                "Expand entrepreneurship knowledge base and modern application examples."
            )
        
        # Overall quality recommendations
        og_rag_mean = og_rag_stats.get('performance_metrics', {}).get('overall_quality', {}).get('mean', 0)
        if og_rag_mean >= 0.8:
            recommendations.append("🏆 Excellent overall quality achieved. Focus on consistency across all proverbs.")
        elif og_rag_mean >= 0.7:
            recommendations.append("📈 Good quality foundation. Optimize weak areas identified in detailed analysis.")
        else:
            recommendations.append("🔧 Significant improvements needed. Review cultural context retrieval and generation strategies.")
        
        return recommendations
    
    def _integrate_llm_judge_results(self, llm_judge_data: Dict, cultural_results: List[CulturalEvaluationResult]) -> Dict:
        """Integrate LLM judge results with cultural metrics."""
        
        # This would integrate the LLM as a Judge evaluation results
        # with the cultural metrics for comprehensive analysis
        integration = {
            "llm_judge_cultural_correlation": "Analysis would compare LLM judge scores with cultural metrics",
            "ensemble_validation": "Cross-validation between automated cultural metrics and LLM judge evaluation",
            "consensus_analysis": "Identification of cases where metrics agree/disagree for further review"
        }
        
        return integration
    
    async def _save_integrated_results(self, integrated_analysis: Dict):
        """Save comprehensive integrated results."""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save comprehensive analysis
        analysis_file = self.output_dir / f"integrated_cultural_analysis_{timestamp}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(integrated_analysis, f, indent=2, ensure_ascii=False, default=str)
        
        # Save executive summary
        summary = {
            "evaluation_timestamp": integrated_analysis["evaluation_metadata"]["pipeline_completion_timestamp"],
            "total_proverbs": integrated_analysis["evaluation_metadata"]["total_proverbs_evaluated"],
            "og_rag_performance": integrated_analysis["system_performance"]["og_rag_system"]["performance_metrics"]["overall_quality"]["mean"],
            "raw_llm_performance": integrated_analysis["system_performance"]["raw_llm_system"]["performance_metrics"]["overall_quality"]["mean"],
            "cultural_advantage": integrated_analysis["system_performance"]["comparative_analysis"]["cultural_authenticity_advantage"]["difference"],
            "top_recommendations": integrated_analysis["recommendations"][:3]
        }
        
        summary_file = self.output_dir / f"executive_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Integrated analysis saved:")
        logger.info(f"  📄 Complete: {analysis_file}")
        logger.info(f"  📋 Summary: {summary_file}")

async def main():
    """Run integrated cultural evaluation pipeline demo."""
    
    # Create sample benchmark if needed
    benchmark_file = "data/evaluation/benchmark/sample_translation_benchmark.csv"
    
    if not Path(benchmark_file).exists():
        logger.info("Creating sample benchmark data...")
        from scripts.run_translation_comparison_demo import create_sample_benchmark_data
        benchmark_file = create_sample_benchmark_data()
    
    # Initialize integrated pipeline
    pipeline = IntegratedCulturalEvaluationPipeline()
    
    try:
        # Run complete pipeline
        logger.info("🚀 Starting Integrated Cultural Evaluation Pipeline")
        results = await pipeline.run_complete_evaluation_pipeline(
            benchmark_file=benchmark_file,
            include_cultural_metrics=True,
            include_llm_judge=True,
            save_intermediate=True
        )
        
        # Display summary
        print("\n🎯 INTEGRATED CULTURAL EVALUATION RESULTS")
        print("=" * 60)
        print(f"📊 Total proverbs evaluated: {results['evaluation_metadata']['total_proverbs_evaluated']}")
        print(f"🔄 Cultural evaluations: {results['evaluation_metadata']['cultural_evaluations_completed']}")
        
        if 'og_rag_system' in results['system_performance']:
            og_rag_score = results['system_performance']['og_rag_system']['performance_metrics']['overall_quality']['mean']
            print(f"🏛️ OG-RAG mean quality: {og_rag_score:.3f}")
        
        if 'raw_llm_system' in results['system_performance']:
            raw_llm_score = results['system_performance']['raw_llm_system']['performance_metrics']['overall_quality']['mean']
            print(f"🤖 Raw LLM mean quality: {raw_llm_score:.3f}")
        
        if 'comparative_analysis' in results['system_performance']:
            cultural_advantage = results['system_performance']['comparative_analysis']['cultural_authenticity_advantage']['difference']
            print(f"🏛️ Cultural authenticity advantage: {cultural_advantage:.3f}")
        
        print(f"\n💾 Results saved to: {pipeline.output_dir}")
        
        print("\n💡 Top Recommendations:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            print(f"  {i}. {rec}")
        
        print("\n✅ Integrated evaluation completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())