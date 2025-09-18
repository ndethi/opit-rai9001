"""
thiLLMo Evaluation Framework

Comprehensive evaluation system for Kikuyu proverb translation quality assessment
including LLM as a Judge, expert validation, and statistical analysis.
"""

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