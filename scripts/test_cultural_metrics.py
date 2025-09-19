#!/usr/bin/env python3
"""
Test script for Cultural Translation Evaluation Metrics.
Validates the metrics system functionality and integration.
"""

import sys
from pathlib import Path
import pandas as pd
import json
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_imports():
    """Test basic imports and initialization."""
    try:
        from src.evaluation.cultural_metrics import (
            CulturalTranslationMetrics, 
            CulturalMetricsConfig,
            KikuyuCulturalPatterns
        )
        logger.info("✅ Cultural metrics imports successful")
        return True
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def test_kikuyu_patterns():
    """Test Kikuyu cultural pattern analysis."""
    try:
        from src.evaluation.cultural_metrics import KikuyuCulturalPatterns
        
        patterns = KikuyuCulturalPatterns()
        
        # Test cultural concept analysis
        test_text = "The community works together with unity and respect for elders"
        cultural_analysis = patterns.analyze_cultural_concepts(test_text)
        
        logger.info("🏛️ Cultural Concept Analysis:")
        for category, score in cultural_analysis.items():
            logger.info(f"  {category}: {score:.3f}")
        
        # Test business concept analysis  
        business_text = "Entrepreneurship requires teamwork and resource management"
        business_analysis = patterns.analyze_business_concepts(business_text)
        
        logger.info("💼 Business Concept Analysis:")
        for category, score in business_analysis.items():
            logger.info(f"  {category}: {score:.3f}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Kikuyu patterns test failed: {e}")
        return False

def test_cultural_metrics():
    """Test cultural translation metrics calculation."""
    try:
        from src.evaluation.cultural_metrics import CulturalTranslationMetrics, CulturalMetricsConfig
        
        # Initialize with custom config
        config = CulturalMetricsConfig(
            cultural_weight=0.45,
            enable_kikuyu_specific=True
        )
        
        metrics = CulturalTranslationMetrics(config)
        
        # Test data
        translation = "Hard work and community cooperation lead to prosperity"
        expert_translation = "Diligent effort and unity bring collective wealth"
        cultural_context = "Traditional Kikuyu values emphasizing collective effort"
        business_application = "Teamwork and persistence drive business success"
        expert_business_context = "Collaborative entrepreneurship builds sustainable wealth"
        
        # Calculate comprehensive metrics
        quality_scores = metrics.calculate_overall_quality_score(
            translation=translation,
            expert_translation=expert_translation,
            cultural_context=cultural_context,
            business_application=business_application,
            expert_business_context=expert_business_context,
            expert_cultural_score=4.2,
            expert_translation_score=4.0,
            expert_business_score=3.8,
            expert_fluency_score=4.5
        )
        
        logger.info("📊 Cultural Translation Quality Metrics:")
        logger.info(f"  🏛️ Cultural Authenticity: {quality_scores['cultural_authenticity']:.3f}")
        logger.info(f"  📝 Translation Fidelity: {quality_scores['translation_fidelity']:.3f}")
        logger.info(f"  💼 Business Relevance: {quality_scores['business_relevance']:.3f}")
        logger.info(f"  👨‍🏫 Expert Alignment: {quality_scores['expert_alignment']:.3f}")
        logger.info(f"  🎯 Overall Quality: {quality_scores['overall_quality']:.3f}")
        logger.info(f"  🏆 Quality Grade: {quality_scores['quality_grade']}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Cultural metrics test failed: {e}")
        return False

def test_batch_evaluation():
    """Test batch evaluation functionality."""
    try:
        from src.evaluation.cultural_metrics import CulturalTranslationMetrics
        
        metrics = CulturalTranslationMetrics()
        
        # Create test dataset
        test_data = [
            {
                'proverb_id': 'TEST_001',
                'translation': 'Unity brings strength',
                'expert_translation': 'Together we are strong',
                'cultural_context': 'Community values',
                'business_application': 'Teamwork succeeds',
                'expert_business_context': 'Collaboration wins',
                'system_type': 'test_system'
            },
            {
                'proverb_id': 'TEST_002', 
                'translation': 'Hard work pays off',
                'expert_translation': 'Effort brings rewards',
                'cultural_context': 'Work ethic principles',
                'business_application': 'Persistence succeeds',
                'expert_business_context': 'Dedication works',
                'system_type': 'test_system'
            }
        ]
        
        test_df = pd.DataFrame(test_data)
        
        # Run batch evaluation
        results = metrics.evaluate_translation_batch(
            test_df, 
            save_results=False  # Don't save for test
        )
        
        logger.info(f"📊 Batch evaluation completed: {len(results)} results")
        for result in results:
            logger.info(f"  {result.proverb_id}: {result.overall_quality:.3f} ({result.quality_grade})")
        
        return True
    except Exception as e:
        logger.error(f"❌ Batch evaluation test failed: {e}")
        return False

def test_integrated_pipeline():
    """Test integration with translation comparison system."""
    try:
        from scripts.run_integrated_cultural_evaluation import IntegratedCulturalEvaluationPipeline
        
        # Just test initialization
        pipeline = IntegratedCulturalEvaluationPipeline()
        logger.info("✅ Integrated pipeline initialization successful")
        
        return True
    except Exception as e:
        logger.error(f"❌ Integrated pipeline test failed: {e}")
        return False

def main():
    """Run all cultural metrics tests."""
    print("🧪 Cultural Translation Evaluation Metrics Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Kikuyu Patterns", test_kikuyu_patterns),
        ("Cultural Metrics", test_cultural_metrics),
        ("Batch Evaluation", test_batch_evaluation),
        ("Integrated Pipeline", test_integrated_pipeline)
    ]
    
    results = {}
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        try:
            results[name] = test_func()
        except Exception as e:
            logger.error(f"Test {name} crashed: {e}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Cultural metrics system is ready.")
        print("💡 Next steps:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Run demo: python scripts/run_integrated_cultural_evaluation.py")
        print("  3. Integrate with your translation datasets")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Check dependencies and imports.")
        print("💡 Install missing packages:")
        print("  pip install sentence-transformers rouge-score nltk")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())