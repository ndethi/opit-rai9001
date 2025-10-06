"""
Enhanced evaluation framework for thiLLMo OG-RAG system.

This module provides comprehensive evaluation capabilities including:
- LLM as a Judge evaluation with cultural specialization
- Cultural translation metrics for authenticity assessment
- Statistical analysis framework for research validation
- Comparative evaluation pipeline for system assessment
- Dynamic LLM configuration with multi-provider support
"""

from .llm_config import (
    DynamicLLMConfigurator,
    LLMProvider,
    LLMModelConfig,
    EvaluationConfig
)

from .llm_judge import (
    LLMJudgeEvaluator,
    CulturalEvaluationPrompts,
    TranslationEvaluation,
    EvaluationCriteria
)

try:
    from .comparative_pipeline import (
        ComparativeEvaluationPipeline
    )
except ImportError:
    ComparativeEvaluationPipeline = None

from .cultural_metrics import (
    CulturalTranslationMetrics,
    CulturalEvaluationResult,
    CulturalMetricsConfig
)

from .statistical_analysis import (
    EnhancedTranslationStatisticalAnalysis,
    StatisticalConfig
)

__version__ = "1.0.0"

# Core evaluation components
__all__ = [
    # LLM Configuration
    "DynamicLLMConfigurator",
    "LLMProvider", 
    "LLMModelConfig",
    "EvaluationConfig",
    
    # LLM as a Judge Evaluation
    "LLMJudgeEvaluator",
    "CulturalEvaluationPrompts",
    "TranslationEvaluation",
    "EvaluationCriteria",
    
    # Comparative Analysis
    "ComparativeEvaluationPipeline",
    
    # Cultural Metrics
    "CulturalTranslationMetrics", 
    "CulturalQualityAssessment",
    "TranslationFidelityMetrics",
    
    # Statistical Analysis
    "EnhancedTranslationStatisticalAnalysis",
    "StatisticalConfig"
]

# Framework metadata
FRAMEWORK_INFO = {
    "name": "thiLLMo Enhanced Evaluation Framework",
    "version": __version__,
    "description": "Comprehensive evaluation framework for cultural translation systems",
    "capabilities": [
        "LLM as a Judge evaluation with cultural specialization",
        "Multi-provider LLM configuration (Cohere, OpenAI, Anthropic)",
        "Cultural authenticity and translation fidelity metrics",
        "Statistical analysis with academic research validation",
        "Comparative evaluation pipeline with ensemble assessment",
        "Expert correlation analysis and reliability validation"
    ],
    "target_languages": ["Kikuyu", "English"],
    "evaluation_domains": ["Cultural Translation", "Business Relevance", "Traditional Wisdom"]
}

from .llm_config import DynamicLLMConfigurator, LLMProvider, LLMModelConfig, EvaluationConfig
from .llm_judge import LLMJudgeEvaluator, CulturalEvaluationPrompts
from .comparative_pipeline import ComparativeEvaluationPipeline
from .cultural_metrics import (
    CulturalTranslationMetrics, 
    CulturalMetricsConfig, 
    CulturalEvaluationResult,
    KikuyuCulturalPatterns
)

__version__ = "1.0.0"
__author__ = "thiLLMo Research Team"

# Core evaluation components
__all__ = [
    # LLM Configuration
    'DynamicLLMConfigurator',
    'LLMProvider', 
    'LLMModelConfig',
    'EvaluationConfig',
    
    # LLM Judge Evaluation
    'LLMJudgeEvaluator',
    'CulturalEvaluationPrompts',
    
    # Comparative Pipeline
    'ComparativeEvaluationPipeline',
    
    # Cultural Metrics
    'CulturalTranslationMetrics',
    'CulturalMetricsConfig',
    'CulturalEvaluationResult', 
    'KikuyuCulturalPatterns'
]

# Framework metadata
FRAMEWORK_INFO = {
    "name": "thiLLMo LLM as a Judge Evaluation Framework",
    "version": __version__,
    "description": "Culturally-specialized evaluation framework for Kikuyu proverb translation quality assessment",
    "capabilities": [
        "Multi-provider LLM judge evaluation (Cohere, OpenAI, Anthropic)",
        "Cultural authenticity assessment with Kikuyu-specific patterns",
        "Automated translation quality metrics (ROUGE, semantic similarity)",
        "Business relevance evaluation for entrepreneurship applications", 
        "Expert correlation analysis and statistical validation",
        "Ensemble evaluation with confidence scoring",
        "Comprehensive reporting and visualization"
    ],
    "target_languages": ["Kikuyu", "English"],
    "evaluation_domains": ["Cultural Translation", "Business Applications", "Traditional Wisdom"]
}

from .llm_config import DynamicLLMConfigurator, LLMProvider, LLMModelConfig, EvaluationConfig
from .llm_judge import (
    LLMJudgeEvaluator, 
    TranslationEvaluation, 
    EvaluationCriteria,
    CulturalEvaluationPrompts
)
from .comparative_pipeline import ComparativeEvaluationPipeline

__version__ = "1.0.0"
__author__ = "Charles Watson Ndethi Kibaki"

__all__ = [
    # Configuration
    "DynamicLLMConfigurator",
    "LLMProvider", 
    "LLMModelConfig",
    "EvaluationConfig",
    
    # LLM Judge Evaluation
    "LLMJudgeEvaluator",
    "TranslationEvaluation",
    "EvaluationCriteria", 
    "CulturalEvaluationPrompts",
    
    # Comparative Pipeline
    "ComparativeEvaluationPipeline"
]

# Framework info
FRAMEWORK_INFO = {
    "name": "thiLLMo Evaluation Framework",
    "description": "LLM as a Judge evaluation system for culturally faithful Kikuyu proverb translation",
    "version": __version__,
    "author": __author__,
    "institution": "Open Institute of Technology (OPIT)",
    "course": "MSc Responsible AI - RAI9001",
    "capabilities": [
        "Dynamic LLM provider configuration",
        "Cultural authenticity evaluation",
        "Multi-model ensemble assessment", 
        "Statistical significance testing",
        "Expert correlation analysis",
        "Comparative system evaluation"
    ]
}

def get_framework_info():
    """Get framework information."""
    return FRAMEWORK_INFO

def print_framework_info():
    """Print framework information."""
    info = get_framework_info()
    print(f"=== {info['name']} ===")
    print(f"Version: {info['version']}")
    print(f"Author: {info['author']}")
    print(f"Institution: {info['institution']}")
    print(f"Course: {info['course']}")
    print(f"\nDescription: {info['description']}")
    print(f"\nCapabilities:")
    for capability in info['capabilities']:
        print(f"  • {capability}")