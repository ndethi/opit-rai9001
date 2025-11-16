#!/usr/bin/env python3
"""
LLM as a Judge Evaluation Framework for thiLLMo

Implements comprehensive LLM-based evaluation system for Kikuyu proverb translation quality
with cultural authenticity, translation accuracy, business relevance, and fluency assessment.
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import pandas as pd
from pathlib import Path
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Import our configuration system
from .llm_config import DynamicLLMConfigurator, LLMModelConfig, LLMProvider

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class EvaluationCriteria:
    """Evaluation criteria for translation quality assessment."""
    cultural_faithfulness: float
    translation_accuracy: float
    business_relevance: float
    overall_fluency: float
    detailed_feedback: str
    confidence_score: float

@dataclass
class TranslationEvaluation:
    """Complete evaluation result for a translation."""
    proverb_id: str
    kikuyu_original: str
    english_translation: str
    system_type: str  # 'og_rag' or 'raw_llm'
    evaluator_model: str
    evaluation_criteria: EvaluationCriteria
    weighted_score: float
    evaluation_timestamp: datetime
    evaluation_metadata: Dict[str, Any]

class CulturalEvaluationPrompts:
    """Specialized prompts for cultural evaluation of Kikuyu proverb translations."""
    
    @staticmethod
    def get_cultural_assessment_prompt(kikuyu_proverb: str, english_translation: str) -> str:
        """Generate culturally-aware evaluation prompt for Kikuyu proverb translation."""
        return f"""
You are an expert evaluator specializing in cross-cultural translation assessment with deep knowledge of Kikuyu culture and wisdom traditions. Your task is to evaluate the quality of English translations of Kikuyu proverbs.

**ORIGINAL KIKUYU PROVERB**: {kikuyu_proverb}
**ENGLISH TRANSLATION**: {english_translation}

**EVALUATION FRAMEWORK**:
Assess the translation across four critical dimensions:

**1. CULTURAL FAITHFULNESS (40% weight)**
- Does the translation preserve the cultural wisdom and meaning?
- Are traditional concepts and metaphors appropriately conveyed?
- Is the cultural context maintained for English speakers?
- Does it respect the depth of Kikuyu traditional knowledge?

**2. TRANSLATION ACCURACY (30% weight)**
- Is the semantic meaning correctly transferred?
- Are there any linguistic errors or mistranslations?
- Does the translation maintain the original's intent?
- Is the vocabulary appropriate and precise?

**3. BUSINESS RELEVANCE (20% weight)**
- Can this translation be meaningfully applied in modern business contexts?
- Does it provide actionable wisdom for contemporary professional settings?
- Is the language appropriate for business communication?
- Does it maintain relevance while preserving traditional wisdom?

**4. OVERALL FLUENCY (10% weight)**
- Is the English natural and well-flowing?
- Is it easily understood by English speakers?
- Does it read smoothly and professionally?
- Is the expression clear and engaging?

**RESPONSE FORMAT**:
Provide your evaluation as a JSON object with the following structure:
{{
    "cultural_faithfulness": <score 1-5>,
    "translation_accuracy": <score 1-5>,
    "business_relevance": <score 1-5>,
    "overall_fluency": <score 1-5>,
    "detailed_feedback": "<comprehensive explanation of your assessment>",
    "confidence_score": <confidence in evaluation 0.0-1.0>
}}

**SCORING GUIDE**:
- 5: Excellent - Outstanding quality with no significant issues
- 4: Good - High quality with minor issues
- 3: Acceptable - Adequate quality with some issues
- 2: Poor - Significant issues affecting quality
- 1: Unacceptable - Major issues making translation unsuitable

**CULTURAL CONTEXT CONSIDERATIONS**:
- Kikuyu proverbs often contain profound wisdom about life, relationships, work, and community
- Traditional metaphors may need adaptation while preserving core meaning
- Business applications should honor traditional wisdom while being practically relevant
- Respect for Kikuyu cultural heritage is paramount

Evaluate thoughtfully, considering both linguistic accuracy and cultural sensitivity.
"""

    @staticmethod
    def get_comparative_assessment_prompt(kikuyu_proverb: str, 
                                        og_rag_translation: str, 
                                        raw_llm_translation: str) -> str:
        """Generate comparative evaluation prompt for OG-RAG vs Raw LLM translations."""
        return f"""
You are an expert evaluator comparing two different AI translation approaches for Kikuyu proverbs. Your task is to assess which translation better preserves cultural meaning while providing accurate, business-relevant English translations.

**ORIGINAL KIKUYU PROVERB**: {kikuyu_proverb}

**TRANSLATION A (OG-RAG System)**: {og_rag_translation}
**TRANSLATION B (Raw LLM)**: {raw_llm_translation}

**COMPARATIVE EVALUATION TASK**:
Evaluate each translation independently, then provide a comparative analysis.

**EVALUATION DIMENSIONS**:
1. **Cultural Faithfulness** (40% weight) - Preservation of traditional wisdom and cultural context
2. **Translation Accuracy** (30% weight) - Linguistic correctness and semantic fidelity  
3. **Business Relevance** (20% weight) - Modern professional application potential
4. **Overall Fluency** (10% weight) - Natural English expression and readability

**RESPONSE FORMAT**:
Provide your evaluation as a JSON object:
{{
    "translation_a_evaluation": {{
        "cultural_faithfulness": <score 1-5>,
        "translation_accuracy": <score 1-5>,
        "business_relevance": <score 1-5>,
        "overall_fluency": <score 1-5>,
        "detailed_feedback": "<specific feedback for Translation A>",
        "confidence_score": <0.0-1.0>
    }},
    "translation_b_evaluation": {{
        "cultural_faithfulness": <score 1-5>,
        "translation_accuracy": <score 1-5>,
        "business_relevance": <score 1-5>,
        "overall_fluency": <score 1-5>,
        "detailed_feedback": "<specific feedback for Translation B>",
        "confidence_score": <0.0-1.0>
    }},
    "comparative_analysis": {{
        "superior_translation": "<A or B>",
        "key_differences": "<main differences between translations>",
        "cultural_preservation_winner": "<A or B>",
        "business_applicability_winner": "<A or B>",
        "overall_recommendation": "<detailed recommendation and reasoning>"
    }}
}}

**EVALUATION PRINCIPLES**:
- Consider both linguistic accuracy and cultural authenticity
- Assess business relevance without compromising cultural integrity
- Evaluate which approach better serves cross-cultural understanding
- Consider the target audience: business professionals seeking cultural wisdom

Focus on which translation approach better achieves the goal of culturally faithful, professionally relevant proverb translation.
"""

class LLMProvider_Client:
    """Base class for LLM provider clients."""
    
    def __init__(self, config: LLMModelConfig):
        self.config = config
        
    async def generate_response(self, prompt: str) -> str:
        """Generate response from the LLM. To be implemented by subclasses."""
        raise NotImplementedError

class CohereClient(LLMProvider_Client):
    """Cohere API client for LLM as a Judge evaluation."""
    
    def __init__(self, config: LLMModelConfig):
        super().__init__(config)
        try:
            import cohere
            self.client = cohere.Client(api_key=config.api_key)
        except ImportError:
            logger.error("Cohere library not installed. Install with: pip install cohere")
            raise
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response from Cohere model."""
        try:
            response = self.client.chat(
                model=self.config.model_name,
                message=prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.text
        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            raise

class OpenAIClient(LLMProvider_Client):
    """OpenAI API client for LLM as a Judge evaluation."""
    
    def __init__(self, config: LLMModelConfig):
        super().__init__(config)
        try:
            import openai
            self.client = openai.OpenAI(api_key=config.api_key)
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response from OpenAI model."""
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

class AnthropicClient(LLMProvider_Client):
    """Anthropic API client for LLM as a Judge evaluation."""
    
    def __init__(self, config: LLMModelConfig):
        super().__init__(config)
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=config.api_key)
        except ImportError:
            logger.error("Anthropic library not installed. Install with: pip install anthropic")
            raise
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response from Anthropic model."""
        try:
            response = self.client.messages.create(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

class GoogleClient(LLMProvider_Client):
    """Google Gemini API client for LLM as a Judge evaluation."""
    
    def __init__(self, config: LLMModelConfig):
        super().__init__(config)
        try:
            import google.generativeai as genai
            genai.configure(api_key=config.api_key)
            self.model = genai.GenerativeModel(config.model_name)
        except ImportError:
            logger.error("Google Generative AI library not installed. Install with: pip install google-generativeai")
            raise
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response from Google Gemini model."""
        import asyncio
        import time
        
        max_retries = 3
        retry_delay = 15  # seconds, to respect rate limits
        
        for attempt in range(max_retries):
            try:
                # Gemini API is synchronous, so we run it in executor
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.model.generate_content(
                        prompt,
                        generation_config={
                            'temperature': self.config.temperature,
                            'max_output_tokens': self.config.max_tokens,
                        }
                    )
                )
                return response.text
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'quota' in error_msg.lower():
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limit hit, waiting {retry_delay}s before retry {attempt + 1}/{max_retries}")
                        await asyncio.sleep(retry_delay)
                        continue
                logger.error(f"Google Gemini API error: {e}")
                raise

class LLMJudgeEvaluator:
    """Main LLM as a Judge evaluation framework."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize evaluator with dynamic configuration."""
        self.configurator = DynamicLLMConfigurator(config_file)
        self.clients: Dict[LLMProvider, LLMProvider_Client] = {}
        self._setup_clients()
        
        # Evaluation settings
        self.evaluation_weights = {
            'cultural_faithfulness': self.configurator.evaluation_config.cultural_weight,
            'translation_accuracy': self.configurator.evaluation_config.translation_weight,
            'business_relevance': self.configurator.evaluation_config.business_weight,
            'overall_fluency': self.configurator.evaluation_config.fluency_weight
        }
        
    def _setup_clients(self):
        """Setup LLM provider clients."""
        for provider, config in self.configurator.available_models.items():
            try:
                if provider == LLMProvider.COHERE:
                    self.clients[provider] = CohereClient(config)
                elif provider == LLMProvider.OPENAI:
                    self.clients[provider] = OpenAIClient(config)
                elif provider == LLMProvider.ANTHROPIC:
                    self.clients[provider] = AnthropicClient(config)
                elif provider == LLMProvider.GOOGLE:
                    self.clients[provider] = GoogleClient(config)
                
                logger.info(f"Initialized {provider.value} client")
            except Exception as e:
                logger.warning(f"Failed to initialize {provider.value} client: {e}")
                
    async def evaluate_single_translation(self, 
                                        kikuyu_proverb: str,
                                        english_translation: str,
                                        system_type: str,
                                        proverb_id: str = None,
                                        model_config: LLMModelConfig = None) -> TranslationEvaluation:
        """Evaluate a single translation using LLM as a Judge."""
        
        if model_config is None:
            model_config = self.configurator.get_primary_model()
            
        if not model_config or model_config.provider not in self.clients:
            raise ValueError(f"No available client for provider: {model_config.provider if model_config else 'None'}")
            
        client = self.clients[model_config.provider]
        
        # Generate evaluation prompt
        prompt = CulturalEvaluationPrompts.get_cultural_assessment_prompt(
            kikuyu_proverb, english_translation
        )
        
        try:
            # Get LLM evaluation
            response = await client.generate_response(prompt)
            
            # Parse JSON response
            evaluation_data = self._parse_evaluation_response(response)
            
            # Create evaluation criteria object
            criteria = EvaluationCriteria(
                cultural_faithfulness=evaluation_data.get('cultural_faithfulness', 0),
                translation_accuracy=evaluation_data.get('translation_accuracy', 0),
                business_relevance=evaluation_data.get('business_relevance', 0),
                overall_fluency=evaluation_data.get('overall_fluency', 0),
                detailed_feedback=evaluation_data.get('detailed_feedback', ''),
                confidence_score=evaluation_data.get('confidence_score', 0.0)
            )
            
            # Calculate weighted score
            weighted_score = self._calculate_weighted_score(criteria)
            
            # Create evaluation result
            evaluation = TranslationEvaluation(
                proverb_id=proverb_id or f"eval_{int(time.time())}",
                kikuyu_original=kikuyu_proverb,
                english_translation=english_translation,
                system_type=system_type,
                evaluator_model=f"{model_config.provider.value}:{model_config.model_name}",
                evaluation_criteria=criteria,
                weighted_score=weighted_score,
                evaluation_timestamp=datetime.now(),
                evaluation_metadata={
                    'provider': model_config.provider.value,
                    'model': model_config.model_name,
                    'temperature': model_config.temperature,
                    'max_tokens': model_config.max_tokens
                }
            )
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Evaluation failed for {model_config.provider.value}: {e}")
            raise
            
    def _parse_evaluation_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM evaluation."""
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in response, returning empty evaluation")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {response}")
            return {}
            
    def _calculate_weighted_score(self, criteria: EvaluationCriteria) -> float:
        """Calculate weighted score based on evaluation criteria."""
        score = (
            criteria.cultural_faithfulness * self.evaluation_weights['cultural_faithfulness'] +
            criteria.translation_accuracy * self.evaluation_weights['translation_accuracy'] +
            criteria.business_relevance * self.evaluation_weights['business_relevance'] +
            criteria.overall_fluency * self.evaluation_weights['overall_fluency']
        )
        return round(score, 2)
        
    async def evaluate_comparative_translations(self,
                                              kikuyu_proverb: str,
                                              og_rag_translation: str,
                                              raw_llm_translation: str,
                                              proverb_id: str = None) -> Dict[str, TranslationEvaluation]:
        """Evaluate OG-RAG vs Raw LLM translations comparatively."""
        
        primary_model = self.configurator.get_primary_model()
        if not primary_model or primary_model.provider not in self.clients:
            raise ValueError("No primary model available for comparative evaluation")
            
        client = self.clients[primary_model.provider]
        
        # Generate comparative evaluation prompt
        prompt = CulturalEvaluationPrompts.get_comparative_assessment_prompt(
            kikuyu_proverb, og_rag_translation, raw_llm_translation
        )
        
        try:
            response = await client.generate_response(prompt)
            comparative_data = self._parse_evaluation_response(response)
            
            # Extract individual evaluations
            og_rag_eval = self._create_evaluation_from_comparative_data(
                comparative_data.get('translation_a_evaluation', {}),
                proverb_id, kikuyu_proverb, og_rag_translation, 'og_rag', primary_model
            )
            
            raw_llm_eval = self._create_evaluation_from_comparative_data(
                comparative_data.get('translation_b_evaluation', {}),
                proverb_id, kikuyu_proverb, raw_llm_translation, 'raw_llm', primary_model
            )
            
            return {
                'og_rag': og_rag_eval,
                'raw_llm': raw_llm_eval,
                'comparative_analysis': comparative_data.get('comparative_analysis', {})
            }
            
        except Exception as e:
            logger.error(f"Comparative evaluation failed: {e}")
            raise
            
    def _create_evaluation_from_comparative_data(self,
                                               eval_data: Dict[str, Any],
                                               proverb_id: str,
                                               kikuyu_proverb: str,
                                               translation: str,
                                               system_type: str,
                                               model_config: LLMModelConfig) -> TranslationEvaluation:
        """Create TranslationEvaluation from comparative evaluation data."""
        
        criteria = EvaluationCriteria(
            cultural_faithfulness=eval_data.get('cultural_faithfulness', 0),
            translation_accuracy=eval_data.get('translation_accuracy', 0),
            business_relevance=eval_data.get('business_relevance', 0),
            overall_fluency=eval_data.get('overall_fluency', 0),
            detailed_feedback=eval_data.get('detailed_feedback', ''),
            confidence_score=eval_data.get('confidence_score', 0.0)
        )
        
        weighted_score = self._calculate_weighted_score(criteria)
        
        return TranslationEvaluation(
            proverb_id=proverb_id or f"comp_eval_{int(time.time())}",
            kikuyu_original=kikuyu_proverb,
            english_translation=translation,
            system_type=system_type,
            evaluator_model=f"{model_config.provider.value}:{model_config.model_name}",
            evaluation_criteria=criteria,
            weighted_score=weighted_score,
            evaluation_timestamp=datetime.now(),
            evaluation_metadata={
                'evaluation_type': 'comparative',
                'provider': model_config.provider.value,
                'model': model_config.model_name
            }
        )
        
    async def ensemble_evaluation(self,
                                kikuyu_proverb: str,
                                english_translation: str,
                                system_type: str,
                                proverb_id: str = None) -> Dict[str, Any]:
        """Perform ensemble evaluation using multiple models."""
        
        if not self.configurator.evaluation_config.enable_ensemble:
            logger.info("Ensemble evaluation disabled, using single model")
            single_eval = await self.evaluate_single_translation(
                kikuyu_proverb, english_translation, system_type, proverb_id
            )
            return {'single_evaluation': single_eval, 'ensemble_summary': None}
            
        ensemble_models = self.configurator.get_ensemble_models()
        if len(ensemble_models) < 2:
            logger.warning("Insufficient models for ensemble evaluation")
            return await self.ensemble_evaluation(kikuyu_proverb, english_translation, system_type, proverb_id)
            
        # Perform evaluations with multiple models
        evaluations = []
        tasks = []
        
        for model_config in ensemble_models:
            if model_config.provider in self.clients:
                task = self.evaluate_single_translation(
                    kikuyu_proverb, english_translation, system_type, proverb_id, model_config
                )
                tasks.append(task)
                
        # Execute evaluations concurrently
        try:
            evaluations = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter successful evaluations
            valid_evaluations = [
                eval_result for eval_result in evaluations 
                if isinstance(eval_result, TranslationEvaluation)
            ]
            
            if not valid_evaluations:
                raise ValueError("No successful evaluations in ensemble")
                
            # Calculate ensemble statistics
            ensemble_summary = self._calculate_ensemble_summary(valid_evaluations)
            
            return {
                'individual_evaluations': valid_evaluations,
                'ensemble_summary': ensemble_summary
            }
            
        except Exception as e:
            logger.error(f"Ensemble evaluation failed: {e}")
            raise
            
    def _calculate_ensemble_summary(self, evaluations: List[TranslationEvaluation]) -> Dict[str, Any]:
        """Calculate ensemble summary statistics."""
        if not evaluations:
            return {}
            
        # Extract scores
        cultural_scores = [eval.evaluation_criteria.cultural_faithfulness for eval in evaluations]
        accuracy_scores = [eval.evaluation_criteria.translation_accuracy for eval in evaluations]
        business_scores = [eval.evaluation_criteria.business_relevance for eval in evaluations]
        fluency_scores = [eval.evaluation_criteria.overall_fluency for eval in evaluations]
        weighted_scores = [eval.weighted_score for eval in evaluations]
        confidence_scores = [eval.evaluation_criteria.confidence_score for eval in evaluations]
        
        return {
            'num_evaluators': len(evaluations),
            'mean_scores': {
                'cultural_faithfulness': round(np.mean(cultural_scores), 2),
                'translation_accuracy': round(np.mean(accuracy_scores), 2),
                'business_relevance': round(np.mean(business_scores), 2),
                'overall_fluency': round(np.mean(fluency_scores), 2),
                'weighted_score': round(np.mean(weighted_scores), 2)
            },
            'score_variance': {
                'cultural_faithfulness': round(np.var(cultural_scores), 3),
                'translation_accuracy': round(np.var(accuracy_scores), 3),
                'business_relevance': round(np.var(business_scores), 3),
                'overall_fluency': round(np.var(fluency_scores), 3),
                'weighted_score': round(np.var(weighted_scores), 3)
            },
            'evaluator_agreement': {
                'mean_confidence': round(np.mean(confidence_scores), 2),
                'confidence_variance': round(np.var(confidence_scores), 3)
            },
            'evaluators': [
                eval.evaluator_model for eval in evaluations
            ]
        }
        
    def save_evaluations(self, evaluations: List[TranslationEvaluation], output_file: str):
        """Save evaluation results to file."""
        # Convert evaluations to serializable format
        evaluation_data = []
        for eval in evaluations:
            eval_dict = asdict(eval)
            eval_dict['evaluation_timestamp'] = eval.evaluation_timestamp.isoformat()
            evaluation_data.append(eval_dict)
            
        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(evaluation_data, f, indent=2)
            
        logger.info(f"Saved {len(evaluations)} evaluations to {output_file}")
        
    def export_to_dataframe(self, evaluations: List[TranslationEvaluation]) -> pd.DataFrame:
        """Export evaluation results to pandas DataFrame."""
        data = []
        for eval in evaluations:
            row = {
                'proverb_id': eval.proverb_id,
                'kikuyu_original': eval.kikuyu_original,
                'english_translation': eval.english_translation,
                'system_type': eval.system_type,
                'evaluator_model': eval.evaluator_model,
                'cultural_faithfulness': eval.evaluation_criteria.cultural_faithfulness,
                'translation_accuracy': eval.evaluation_criteria.translation_accuracy,
                'business_relevance': eval.evaluation_criteria.business_relevance,
                'overall_fluency': eval.evaluation_criteria.overall_fluency,
                'confidence_score': eval.evaluation_criteria.confidence_score,
                'weighted_score': eval.weighted_score,
                'evaluation_timestamp': eval.evaluation_timestamp,
                'detailed_feedback': eval.evaluation_criteria.detailed_feedback
            }
            data.append(row)
            
        return pd.DataFrame(data)

# Test function
async def main():
    """Test the LLM as a Judge evaluation framework."""
    
    # Test example
    kikuyu_proverb = "Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ"
    og_rag_translation = "A visitor is like a vessel that should be filled with water (hospitality)"
    raw_llm_translation = "A stranger is a container that should be filled with water"
    
    try:
        evaluator = LLMJudgeEvaluator()
        
        print("=== Testing Single Translation Evaluation ===")
        evaluation = await evaluator.evaluate_single_translation(
            kikuyu_proverb, og_rag_translation, "og_rag", "test_001"
        )
        
        print(f"Weighted Score: {evaluation.weighted_score}")
        print(f"Cultural Faithfulness: {evaluation.evaluation_criteria.cultural_faithfulness}")
        print(f"Translation Accuracy: {evaluation.evaluation_criteria.translation_accuracy}")
        print(f"Feedback: {evaluation.evaluation_criteria.detailed_feedback[:200]}...")
        
        print("\n=== Testing Ensemble Evaluation ===")
        ensemble_result = await evaluator.ensemble_evaluation(
            kikuyu_proverb, og_rag_translation, "og_rag", "test_002"
        )
        
        if ensemble_result.get('ensemble_summary'):
            summary = ensemble_result['ensemble_summary']
            print(f"Ensemble Mean Score: {summary['mean_scores']['weighted_score']}")
            print(f"Number of Evaluators: {summary['num_evaluators']}")
            print(f"Score Variance: {summary['score_variance']['weighted_score']}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())