#!/usr/bin/env python3
"""
Dynamic LLM Configuration System for thiLLMo Evaluation Framework

Provides environment-based configuration for multiple LLM providers with Cohere as primary
and fallback providers for robust evaluation infrastructure.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers for evaluation."""
    COHERE = "cohere"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

@dataclass
class LLMModelConfig:
    """Configuration for a specific LLM model."""
    provider: LLMProvider
    model_name: str
    api_key: str
    temperature: float = 0.3
    max_tokens: int = 1500
    timeout: int = 30
    supports_cultural_eval: bool = True
    cost_per_1k_tokens: float = 0.001
    
@dataclass
class EvaluationConfig:
    """Configuration for evaluation framework."""
    mode: str = "comprehensive"
    cultural_weight: float = 0.4
    translation_weight: float = 0.3
    business_weight: float = 0.2
    fluency_weight: float = 0.1
    enable_ensemble: bool = True
    ensemble_count: int = 3
    
class DynamicLLMConfigurator:
    """Dynamic LLM configuration system with environment-based settings."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configurator with optional environment file."""
        self.env_file = env_file
        self._load_environment()
        self._validate_configuration()
        
        # Initialize model configurations
        self.available_models: Dict[LLMProvider, LLMModelConfig] = {}
        self.primary_provider: Optional[LLMProvider] = None
        self.fallback_providers: List[LLMProvider] = []
        self.evaluation_config: EvaluationConfig = EvaluationConfig()
        
        self._setup_model_configurations()
        self._setup_evaluation_configuration()
        
    def _load_environment(self):
        """Load environment variables from file if specified."""
        if self.env_file and Path(self.env_file).exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                logger.info(f"Loaded environment from {self.env_file}")
            except Exception as e:
                logger.warning(f"Failed to load environment file {self.env_file}: {e}")
                
    def _validate_configuration(self):
        """Validate required environment variables are present."""
        required_vars = [
            'LLM_JUDGE_PRIMARY_PROVIDER',
            'LLM_JUDGE_COHERE_MODEL'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.warning(f"Missing environment variables: {missing_vars}")
            
    def _setup_model_configurations(self):
        """Setup model configurations based on environment variables."""
        # Get provider settings
        primary_provider_str = os.getenv('LLM_JUDGE_PRIMARY_PROVIDER', 'cohere').lower()
        fallback_providers_str = os.getenv('LLM_JUDGE_FALLBACK_PROVIDERS', 'openai,anthropic')
        
        try:
            self.primary_provider = LLMProvider(primary_provider_str)
        except ValueError:
            logger.error(f"Invalid primary provider: {primary_provider_str}")
            self.primary_provider = LLMProvider.COHERE
            
        # Parse fallback providers
        self.fallback_providers = []
        for provider_str in fallback_providers_str.split(','):
            try:
                provider = LLMProvider(provider_str.strip().lower())
                if provider != self.primary_provider:
                    self.fallback_providers.append(provider)
            except ValueError:
                logger.warning(f"Invalid fallback provider: {provider_str}")
                
        # Setup individual model configurations
        self._setup_cohere_config()
        self._setup_openai_config()
        self._setup_anthropic_config()
        self._setup_google_config()
        
        logger.info(f"Primary provider: {self.primary_provider.value}")
        logger.info(f"Fallback providers: {[p.value for p in self.fallback_providers]}")
        
    def _setup_cohere_config(self):
        """Setup Cohere model configuration."""
        api_key = os.getenv('COHERE_API_KEY')
        if not api_key or api_key == 'your_cohere_api_key_here':
            logger.warning("Cohere API key not configured")
            return
            
        model_name = os.getenv('LLM_JUDGE_COHERE_MODEL', 'command-r-plus')
        
        self.available_models[LLMProvider.COHERE] = LLMModelConfig(
            provider=LLMProvider.COHERE,
            model_name=model_name,
            api_key=api_key,
            temperature=float(os.getenv('LLM_JUDGE_TEMPERATURE', '0.3')),
            max_tokens=int(os.getenv('LLM_JUDGE_MAX_TOKENS', '1500')),
            timeout=int(os.getenv('LLM_JUDGE_TIMEOUT', '30')),
            supports_cultural_eval=True,
            cost_per_1k_tokens=0.003  # Cohere Command R+ pricing
        )
        
    def _setup_openai_config(self):
        """Setup OpenAI model configuration."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            logger.warning("OpenAI API key not configured")
            return
            
        model_name = os.getenv('LLM_JUDGE_OPENAI_MODEL', 'gpt-4-turbo')
        
        self.available_models[LLMProvider.OPENAI] = LLMModelConfig(
            provider=LLMProvider.OPENAI,
            model_name=model_name,
            api_key=api_key,
            temperature=float(os.getenv('LLM_JUDGE_TEMPERATURE', '0.3')),
            max_tokens=int(os.getenv('LLM_JUDGE_MAX_TOKENS', '1500')),
            timeout=int(os.getenv('LLM_JUDGE_TIMEOUT', '30')),
            supports_cultural_eval=True,
            cost_per_1k_tokens=0.01  # GPT-4 Turbo pricing
        )
        
    def _setup_anthropic_config(self):
        """Setup Anthropic model configuration."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key == 'your_anthropic_api_key_here':
            logger.warning("Anthropic API key not configured")
            return
            
        model_name = os.getenv('LLM_JUDGE_ANTHROPIC_MODEL', 'claude-3-opus-20240229')
        
        self.available_models[LLMProvider.ANTHROPIC] = LLMModelConfig(
            provider=LLMProvider.ANTHROPIC,
            model_name=model_name,
            api_key=api_key,
            temperature=float(os.getenv('LLM_JUDGE_TEMPERATURE', '0.3')),
            max_tokens=int(os.getenv('LLM_JUDGE_MAX_TOKENS', '1500')),
            timeout=int(os.getenv('LLM_JUDGE_TIMEOUT', '30')),
            supports_cultural_eval=True,
            cost_per_1k_tokens=0.015  # Claude 3 Opus pricing
        )
        
    def _setup_google_config(self):
        """Setup Google model configuration."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'your_google_api_key_here':
            logger.warning("Google API key not configured")
            return
            
        model_name = os.getenv('LLM_JUDGE_GOOGLE_MODEL', 'gemini-1.5-pro')
        
        self.available_models[LLMProvider.GOOGLE] = LLMModelConfig(
            provider=LLMProvider.GOOGLE,
            model_name=model_name,
            api_key=api_key,
            temperature=float(os.getenv('LLM_JUDGE_TEMPERATURE', '0.3')),
            max_tokens=int(os.getenv('LLM_JUDGE_MAX_TOKENS', '1500')),
            timeout=int(os.getenv('LLM_JUDGE_TIMEOUT', '30')),
            supports_cultural_eval=True,
            cost_per_1k_tokens=0.005  # Gemini 1.5 Pro pricing
        )
        
    def _setup_evaluation_configuration(self):
        """Setup evaluation framework configuration."""
        self.evaluation_config = EvaluationConfig(
            mode=os.getenv('EVALUATION_MODE', 'comprehensive'),
            cultural_weight=float(os.getenv('CULTURAL_EVAL_WEIGHT', '0.4')),
            translation_weight=float(os.getenv('TRANSLATION_EVAL_WEIGHT', '0.3')),
            business_weight=float(os.getenv('BUSINESS_EVAL_WEIGHT', '0.2')),
            fluency_weight=float(os.getenv('FLUENCY_EVAL_WEIGHT', '0.1')),
            enable_ensemble=os.getenv('ENABLE_ENSEMBLE_EVALUATION', 'true').lower() == 'true',
            ensemble_count=int(os.getenv('ENSEMBLE_MODEL_COUNT', '3'))
        )
        
    def get_primary_model(self) -> Optional[LLMModelConfig]:
        """Get primary model configuration."""
        if self.primary_provider in self.available_models:
            return self.available_models[self.primary_provider]
        return None
        
    def get_fallback_models(self) -> List[LLMModelConfig]:
        """Get list of fallback model configurations."""
        fallback_models = []
        for provider in self.fallback_providers:
            if provider in self.available_models:
                fallback_models.append(self.available_models[provider])
        return fallback_models
        
    def get_ensemble_models(self) -> List[LLMModelConfig]:
        """Get models for ensemble evaluation."""
        all_models = []
        
        # Add primary model first
        primary = self.get_primary_model()
        if primary:
            all_models.append(primary)
            
        # Add fallback models
        fallback_models = self.get_fallback_models()
        all_models.extend(fallback_models)
        
        # Return up to ensemble_count models
        return all_models[:self.evaluation_config.ensemble_count]
        
    def get_model_by_provider(self, provider: Union[str, LLMProvider]) -> Optional[LLMModelConfig]:
        """Get model configuration by provider."""
        if isinstance(provider, str):
            try:
                provider = LLMProvider(provider.lower())
            except ValueError:
                return None
                
        return self.available_models.get(provider)
        
    def is_provider_available(self, provider: Union[str, LLMProvider]) -> bool:
        """Check if a provider is available."""
        if isinstance(provider, str):
            try:
                provider = LLMProvider(provider.lower())
            except ValueError:
                return False
                
        return provider in self.available_models
        
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration."""
        return {
            "primary_provider": self.primary_provider.value if self.primary_provider else None,
            "fallback_providers": [p.value for p in self.fallback_providers],
            "available_models": [
                {
                    "provider": config.provider.value,
                    "model": config.model_name,
                    "cultural_eval_support": config.supports_cultural_eval,
                    "cost_per_1k": config.cost_per_1k_tokens
                }
                for config in self.available_models.values()
            ],
            "evaluation_config": {
                "mode": self.evaluation_config.mode,
                "weights": {
                    "cultural": self.evaluation_config.cultural_weight,
                    "translation": self.evaluation_config.translation_weight,
                    "business": self.evaluation_config.business_weight,
                    "fluency": self.evaluation_config.fluency_weight
                },
                "ensemble_enabled": self.evaluation_config.enable_ensemble,
                "ensemble_count": self.evaluation_config.ensemble_count
            }
        }
        
    def save_configuration(self, output_file: str):
        """Save current configuration to JSON file."""
        config_summary = self.get_configuration_summary()
        
        with open(output_file, 'w') as f:
            json.dump(config_summary, f, indent=2)
            
        logger.info(f"Configuration saved to {output_file}")
        
def main():
    """Main function for testing configuration."""
    # Initialize configurator
    configurator = DynamicLLMConfigurator()
    
    # Print configuration summary
    print("=== LLM Configuration Summary ===")
    config_summary = configurator.get_configuration_summary()
    print(json.dumps(config_summary, indent=2))
    
    # Test primary model
    primary_model = configurator.get_primary_model()
    if primary_model:
        print(f"\n=== Primary Model ===")
        print(f"Provider: {primary_model.provider.value}")
        print(f"Model: {primary_model.model_name}")
        print(f"Cultural Evaluation Support: {primary_model.supports_cultural_eval}")
    else:
        print("\n⚠️ No primary model configured")
        
    # Test ensemble models
    ensemble_models = configurator.get_ensemble_models()
    if ensemble_models:
        print(f"\n=== Ensemble Models ({len(ensemble_models)}) ===")
        for i, model in enumerate(ensemble_models, 1):
            print(f"{i}. {model.provider.value}: {model.model_name}")
    else:
        print("\n⚠️ No ensemble models available")

if __name__ == "__main__":
    main()