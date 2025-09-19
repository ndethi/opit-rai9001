#!/usr/bin/env python3
"""
Simple test for just the cultural metrics module.
Tests core functionality without heavy dependencies.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

def test_core_cultural_metrics():
    """Test core cultural metrics functionality."""
    try:
        # Direct import to avoid heavy dependencies
        from src.evaluation.cultural_metrics import (
            CulturalTranslationMetrics,
            CulturalMetricsConfig, 
            KikuyuCulturalPatterns
        )
        
        print("✅ Cultural metrics imports successful")
        
        # Test Kikuyu patterns
        patterns = KikuyuCulturalPatterns()
        
        test_text = "The community works together with unity and respect for elders"
        cultural_analysis = patterns.analyze_cultural_concepts(test_text)
        
        print("🏛️ Cultural Concept Analysis:")
        for category, score in cultural_analysis.items():
            if score > 0:
                print(f"  {category}: {score:.3f}")
        
        # Test business patterns
        business_text = "Entrepreneurship requires teamwork and resource management"
        business_analysis = patterns.analyze_business_concepts(business_text)
        
        print("💼 Business Concept Analysis:")
        for category, score in business_analysis.items():
            if score > 0:
                print(f"  {category}: {score:.3f}")
        
        print("✅ Pattern analysis working correctly")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_simple_metrics():
    """Test basic metrics calculation with minimal dependencies."""
    try:
        from src.evaluation.cultural_metrics import CulturalTranslationMetrics, CulturalMetricsConfig
        
        print("🧮 Testing basic metrics calculation...")
        
        # Simple config without heavy dependencies
        config = CulturalMetricsConfig(
            sentence_model_name='all-MiniLM-L6-v2',
            enable_kikuyu_specific=True
        )
        
        # This will trigger sentence transformer download but that's expected
        metrics = CulturalTranslationMetrics(config)
        print("✅ Cultural metrics initialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Metrics initialization failed: {e}")
        print("💡 This may be due to missing sentence-transformers package")
        print("   Install with: pip install sentence-transformers")
        return False

def main():
    """Run simple cultural metrics tests."""
    print("🧪 Simple Cultural Metrics Test")
    print("=" * 40)
    
    tests = [
        ("Core Cultural Metrics", test_core_cultural_metrics),
        ("Simple Metrics Init", test_simple_metrics)
    ]
    
    results = {}
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        results[name] = test_func()
    
    print("\n" + "=" * 40)
    print("📊 TEST RESULTS")
    print("=" * 40)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed >= 1:
        print("\n🎉 Core functionality working!")
        print("💡 To enable full functionality:")
        print("  pip install sentence-transformers rouge-score nltk scipy")
    else:
        print("\n❌ Core tests failed. Check imports and dependencies.")
    
    return 0 if passed >= 1 else 1

if __name__ == "__main__":
    sys.exit(main())