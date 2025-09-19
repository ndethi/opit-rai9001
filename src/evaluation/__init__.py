"""
thiLLMo LLM as a Judge Evaluation Framework

Comprehensive evaluation system for Kikuyu proverb translation quality assessment
using culturally-specialized LLM judges and automated metrics.
"""

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