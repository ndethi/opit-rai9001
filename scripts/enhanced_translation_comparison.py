#!/usr/bin/env python3
"""
Enhanced Translation Comparison System with LLM-as-a-Judge Integration

Integrates with the thiLLMo LLM as a Judge evaluation framework to provide
comprehensive translation comparison between OG-RAG and Raw LLM systems.
"""

import pandas as pd
from pathlib import Path
import json
import openai
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import asyncio
import sys
import os

# Add src to path for evaluation framework imports
sys.path.append(str(Path(__file__).parent.parent))

from src.evaluation import (
    LLMJudgeEvaluator, 
    ComparativeEvaluationPipeline,
    DynamicLLMConfigurator
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedTranslationComparisonSystem:
    """Comprehensive translation comparison system optimized for LLM-as-a-Judge evaluation."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize comparison system with LLM-as-a-Judge capabilities."""
        
        # Initialize LLM as a Judge evaluator
        self.llm_evaluator = LLMJudgeEvaluator(config_file)
        self.configurator = DynamicLLMConfigurator(config_file)
        
        # Initialize traditional LLM clients for translation generation
        self._setup_translation_clients()
        
        # Output directories
        self.output_dir = Path("data/evaluation/translations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced logging for LLM-as-a-Judge analysis
        self.translation_metadata = []
        self.llm_judge_prompts = self._initialize_llm_judge_prompts()
        
        logger.info("Enhanced Translation Comparison System initialized")
        logger.info(f"LLM Judge Primary Provider: {self.configurator.primary_provider}")
    
    def _setup_translation_clients(self):
        """Setup LLM clients for translation generation."""
        try:
            # OpenAI for translation generation
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key and openai_key != 'your_openai_api_key_here':
                self.openai_client = openai.OpenAI(api_key=openai_key)
                logger.info("✅ OpenAI client initialized for translation generation")
            else:
                self.openai_client = None
                logger.warning("⚠️ OpenAI client not available - check API key")
            
            # Google Gemini for additional translation options
            google_key = os.getenv('GOOGLE_API_KEY')
            if google_key and google_key != 'your_google_api_key_here':
                genai.configure(api_key=google_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("✅ Gemini client initialized for translation generation")
            else:
                self.gemini_model = None
                logger.warning("⚠️ Gemini client not available - check API key")
                
        except Exception as e:
            logger.error(f"Failed to setup translation clients: {e}")
    
    def _initialize_llm_judge_prompts(self) -> Dict[str, str]:
        """Initialize prompts optimized for LLM-as-a-Judge evaluation."""
        
        return {
            'cultural_assessment_prep': """
            You are preparing cultural context for expert LLM evaluation of Kikuyu proverb translations.
            
            KIKUYU PROVERB: {kikuyu_proverb}
            CULTURAL CONTEXT: {cultural_context}
            TRADITIONAL USAGE: {traditional_usage}
            
            Generate a comprehensive cultural analysis that an LLM judge can use to assess translation quality.
            Focus on: cultural metaphors, traditional wisdom, community values, and proper usage contexts.
            
            Provide your analysis in this format:
            CULTURAL_METAPHORS: [Key metaphors and symbolic meanings]
            TRADITIONAL_WISDOM: [Core wisdom and teachings]
            COMMUNITY_VALUES: [Kikuyu values reflected]
            USAGE_CONTEXTS: [Traditional and modern usage scenarios]
            """,
            
            'business_relevance_prep': """
            You are preparing business context for expert LLM evaluation of Kikuyu proverb translations.
            
            KIKUYU PROVERB: {kikuyu_proverb}
            CULTURAL MEANING: {cultural_meaning}
            
            Identify comprehensive business and entrepreneurship applications that an LLM judge can use to assess translation quality.
            Focus on: business principles, entrepreneurship lessons, economic wisdom, and modern applications.
            
            Provide your analysis in this format:
            BUSINESS_PRINCIPLES: [Core business wisdom]
            ENTREPRENEURSHIP_LESSONS: [Startup and business development insights]
            ECONOMIC_WISDOM: [Financial and economic principles]
            MODERN_APPLICATIONS: [Contemporary business scenarios]
            """,
            
            'og_rag_translation_prompt': """
            You are an expert Kikuyu-English translator with access to cultural ontology and business context.
            
            KIKUYU PROVERB: {kikuyu_proverb}
            CULTURAL ONTOLOGY CONTEXT: {cultural_context}
            BUSINESS RELEVANCE CONTEXT: {business_context}
            TRADITIONAL USAGE: {traditional_usage}
            
            Translate this proverb providing:
            1. TRANSLATION: [Culturally faithful English translation]
            2. CULTURAL_SIGNIFICANCE: [Deep cultural meaning and traditional wisdom]
            3. BUSINESS_APPLICATION: [Specific entrepreneurship and business relevance]
            4. USAGE_CONTEXT: [When and how this is traditionally used]
            5. MODERN_APPLICATION: [Contemporary relevance and applications]
            6. CULTURAL_METAPHORS: [Key metaphors and symbolic meanings explained]
            7. COMMUNITY_VALUES: [Kikuyu community values reflected]
            8. CONFIDENCE_SCORE: [0.0-1.0 confidence in translation quality]
            
            Ensure the translation preserves cultural authenticity while being accessible to English speakers.
            """,
            
            'raw_llm_translation_prompt': """
            You are translating a Kikuyu proverb to English without additional cultural context.
            
            KIKUYU PROVERB: {kikuyu_proverb}
            
            Provide:
            1. TRANSLATION: [Your best English translation]
            2. CULTURAL_EXPLANATION: [Your understanding of possible cultural meaning]
            3. BUSINESS_APPLICATION: [Any business relevance you can identify]
            4. REASONING: [Why you translated it this way]
            5. CONFIDENCE: [0.0-1.0 confidence in your translation]
            6. ASSUMPTIONS: [Cultural assumptions you made]
            
            Note: You are working without additional cultural context or specialized knowledge base.
            """
        }
    
    async def generate_og_rag_translations_with_metadata(self, benchmark_file: str) -> pd.DataFrame:
        """Generate OG-RAG translations with comprehensive metadata for LLM judge evaluation."""
        
        if not Path(benchmark_file).exists():
            raise FileNotFoundError(f"Benchmark file not found: {benchmark_file}")
            
        benchmark_df = pd.read_csv(benchmark_file)
        translation_results = []
        
        logger.info(f"Generating OG-RAG translations with LLM judge metadata for {len(benchmark_df)} proverbs...")
        
        for idx, row in benchmark_df.iterrows():
            proverb_id = row.get('proverb_id', f"proverb_{idx}")
            kikuyu_text = row.get('kikuyu_proverb', row.get('kikuyu_text', ''))
            
            if not kikuyu_text:
                logger.warning(f"No Kikuyu text found for row {idx}")
                continue
            
            try:
                # Generate OG-RAG translation with enhanced context
                og_rag_result = await self._translate_with_og_rag_enhanced(kikuyu_text)
                
                # Prepare cultural context for LLM judge
                cultural_analysis = await self._prepare_cultural_context_for_llm_judge(
                    kikuyu_text, 
                    og_rag_result.get('cultural_context', '')
                )
                
                # Prepare business context for LLM judge
                business_analysis = await self._prepare_business_context_for_llm_judge(
                    kikuyu_text,
                    og_rag_result.get('cultural_meaning', '')
                )
                
                # Compile comprehensive translation record
                translation_record = {
                    'proverb_id': proverb_id,
                    'kikuyu_text': kikuyu_text,
                    'expert_translation': row.get('expert_translation', ''),
                    'expert_cultural_meaning': row.get('expert_cultural_meaning', ''),
                    'expert_business_relevance': row.get('expert_business_relevance', ''),
                    
                    # OG-RAG outputs
                    'og_rag_translation': og_rag_result.get('translation', ''),
                    'og_rag_cultural_meaning': og_rag_result.get('cultural_significance', ''),
                    'og_rag_business_relevance': og_rag_result.get('business_application', ''),
                    'og_rag_usage_context': og_rag_result.get('usage_context', ''),
                    'og_rag_confidence': og_rag_result.get('confidence_score', 0.0),
                    'og_rag_cultural_metaphors': og_rag_result.get('cultural_metaphors', ''),
                    'og_rag_community_values': og_rag_result.get('community_values', ''),
                    
                    # LLM judge preparation data
                    'llm_judge_cultural_analysis': cultural_analysis,
                    'llm_judge_business_analysis': business_analysis,
                    'cultural_context_richness': len(og_rag_result.get('retrieved_context', [])),
                    
                    # Translation metadata for analysis
                    'translation_timestamp': datetime.now().isoformat(),
                    'cultural_retrieval_confidence': og_rag_result.get('cultural_confidence', 0.0),
                    'business_retrieval_confidence': og_rag_result.get('business_confidence', 0.0),
                    'system_type': 'og_rag'
                }
                
                translation_results.append(translation_record)
                logger.info(f"Enhanced OG-RAG translation generated for proverb {idx + 1}: {proverb_id}")
                
            except Exception as e:
                logger.error(f"Enhanced OG-RAG translation failed for proverb {proverb_id}: {e}")
                continue
        
        # Convert to DataFrame and save
        results_df = pd.DataFrame(translation_results)
        output_file = self.output_dir / "enhanced_og_rag_translations.csv"
        results_df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"✅ Enhanced OG-RAG translations completed!")
        logger.info(f"📊 Generated {len(results_df)} translations with LLM judge metadata")
        logger.info(f"💾 Results saved to: {output_file}")
        
        return results_df
    
    async def generate_raw_llm_translations_for_comparison(self, benchmark_file: str) -> pd.DataFrame:
        """Generate raw LLM translations for comparison study."""
        
        if not Path(benchmark_file).exists():
            raise FileNotFoundError(f"Benchmark file not found: {benchmark_file}")
            
        benchmark_df = pd.read_csv(benchmark_file)
        raw_llm_results = []
        
        logger.info(f"Generating raw LLM translations for {len(benchmark_df)} proverbs...")
        
        for idx, row in benchmark_df.iterrows():
            proverb_id = row.get('proverb_id', f"proverb_{idx}")
            kikuyu_text = row.get('kikuyu_proverb', row.get('kikuyu_text', ''))
            
            if not kikuyu_text:
                logger.warning(f"No Kikuyu text found for row {idx}")
                continue
            
            try:
                # Raw LLM translation without cultural context
                raw_result = await self._translate_with_raw_llm_enhanced(kikuyu_text)
                
                # Compile raw LLM record
                raw_record = {
                    'proverb_id': proverb_id,
                    'kikuyu_text': kikuyu_text,
                    'raw_llm_translation': raw_result.get('translation', ''),
                    'raw_llm_cultural_explanation': raw_result.get('cultural_explanation', ''),
                    'raw_llm_business_relevance': raw_result.get('business_application', ''),
                    'raw_llm_confidence': raw_result.get('confidence', 0.0),
                    'raw_llm_reasoning': raw_result.get('reasoning', ''),
                    'raw_llm_assumptions': raw_result.get('assumptions', ''),
                    'generation_timestamp': datetime.now().isoformat(),
                    'system_type': 'raw_llm'
                }
                
                raw_llm_results.append(raw_record)
                logger.info(f"Raw LLM translation generated for proverb {idx + 1}: {proverb_id}")
                
            except Exception as e:
                logger.error(f"Raw LLM translation failed for proverb {proverb_id}: {e}")
                continue
        
        # Convert to DataFrame and save
        raw_df = pd.DataFrame(raw_llm_results)
        output_file = self.output_dir / "raw_llm_translations.csv"
        raw_df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"✅ Raw LLM translations completed!")
        logger.info(f"📊 Generated {len(raw_df)} raw LLM translations")
        logger.info(f"💾 Results saved to: {output_file}")
        
        return raw_df
    
    async def create_comprehensive_comparison_dataset(self, 
                                              og_rag_file: Optional[str] = None,
                                              raw_llm_file: Optional[str] = None) -> pd.DataFrame:
        """Create comprehensive dataset optimized for LLM-as-a-Judge evaluation."""
        
        # Default file paths
        if og_rag_file is None:
            og_rag_file = self.output_dir / "enhanced_og_rag_translations.csv"
        if raw_llm_file is None:
            raw_llm_file = self.output_dir / "raw_llm_translations.csv"
        
        # Load both datasets
        og_rag_df = pd.read_csv(og_rag_file)
        raw_llm_df = pd.read_csv(raw_llm_file)
        
        # Merge datasets for comparison
        comparison_df = og_rag_df.merge(
            raw_llm_df[['proverb_id', 'raw_llm_translation', 'raw_llm_cultural_explanation', 
                       'raw_llm_business_relevance', 'raw_llm_confidence', 'raw_llm_reasoning',
                       'raw_llm_assumptions']],
            on='proverb_id',
            how='inner'
        )
        
        # Add LLM judge evaluation preparation fields
        comparison_df['llm_judge_evaluation_ready'] = True
        comparison_df['comparison_type'] = 'og_rag_vs_raw_llm_vs_expert'
        comparison_df['evaluation_priority'] = comparison_df.apply(self._calculate_evaluation_priority, axis=1)
        
        # Add evaluation metadata
        comparison_df['dataset_creation_timestamp'] = datetime.now().isoformat()
        comparison_df['llm_judge_framework_version'] = "1.0.0"
        
        # Save comprehensive comparison dataset
        output_file = self.output_dir / "comprehensive_translation_comparison.csv"
        comparison_df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"✅ Comprehensive comparison dataset created!")
        logger.info(f"📊 Dataset contains {len(comparison_df)} translation comparisons")
        logger.info(f"📋 Ready for LLM-as-a-Judge evaluation")
        logger.info(f"💾 Dataset saved to: {output_file}")
        
        return comparison_df
    
    async def run_llm_judge_evaluation(self, comparison_dataset_file: Optional[str] = None) -> Dict:
        """Run LLM as a Judge evaluation on the comparison dataset."""
        
        if comparison_dataset_file is None:
            comparison_dataset_file = self.output_dir / "comprehensive_translation_comparison.csv"
        
        logger.info("🤖 Running LLM as a Judge evaluation...")
        
        # Initialize comparative evaluation pipeline
        pipeline = ComparativeEvaluationPipeline(str(comparison_dataset_file))
        
        # Run comprehensive evaluation
        evaluation_results = await pipeline.run_comparative_evaluation(
            sample_size=None,  # Evaluate all
            enable_ensemble=self.configurator.evaluation_config.enable_ensemble
        )
        
        # Save LLM judge results
        llm_judge_output = self.output_dir / "llm_judge_evaluation_results.json"
        with open(llm_judge_output, 'w') as f:
            json.dump(evaluation_results, f, indent=2, default=str)
        
        logger.info(f"✅ LLM as a Judge evaluation completed!")
        logger.info(f"💾 Results saved to: {llm_judge_output}")
        
        return evaluation_results
    
    async def _translate_with_og_rag_enhanced(self, kikuyu_text: str) -> Dict:
        """Enhanced OG-RAG translation with LLM judge preparation."""
        
        # Simulate retrieval of cultural context from ontology
        # In real implementation, this would query your Neo4j ontology
        cultural_context = self._simulate_cultural_context_retrieval(kikuyu_text)
        business_context = self._simulate_business_context_retrieval(kikuyu_text)
        traditional_usage = self._simulate_traditional_usage_retrieval(kikuyu_text)
        
        prompt = self.llm_judge_prompts['og_rag_translation_prompt'].format(
            kikuyu_proverb=kikuyu_text,
            cultural_context=cultural_context,
            business_context=business_context,
            traditional_usage=traditional_usage
        )
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=1000
                )
                
                response_text = response.choices[0].message.content
                parsed_result = self._parse_enhanced_og_rag_response(response_text)
                
                # Add retrieval metadata
                parsed_result['retrieved_context'] = [cultural_context, business_context, traditional_usage]
                parsed_result['cultural_context'] = cultural_context
                parsed_result['cultural_confidence'] = 0.85  # Based on context richness
                parsed_result['business_confidence'] = 0.80   # Based on business relevance
                
                return parsed_result
            else:
                return {'translation': f'[OG-RAG simulation for: {kikuyu_text}]', 'error': 'OpenAI client not available'}
                
        except Exception as e:
            logger.error(f"Enhanced OG-RAG translation failed: {e}")
            return {'translation': '', 'error': str(e)}
    
    async def _translate_with_raw_llm_enhanced(self, kikuyu_text: str) -> Dict:
        """Enhanced raw LLM translation for comparison study."""
        
        prompt = self.llm_judge_prompts['raw_llm_translation_prompt'].format(
            kikuyu_proverb=kikuyu_text
        )
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=600
                )
                
                response_text = response.choices[0].message.content
                parsed_result = self._parse_raw_llm_response(response_text)
                
                return parsed_result
            else:
                return {'translation': f'[Raw LLM simulation for: {kikuyu_text}]', 'error': 'OpenAI client not available'}
                
        except Exception as e:
            logger.error(f"Raw LLM translation failed: {e}")
            return {'translation': '', 'error': str(e)}
    
    async def _prepare_cultural_context_for_llm_judge(self, kikuyu_text: str, cultural_context: str) -> str:
        """Prepare cultural context specifically for LLM judge evaluation."""
        
        prompt = self.llm_judge_prompts['cultural_assessment_prep'].format(
            kikuyu_proverb=kikuyu_text,
            cultural_context=cultural_context,
            traditional_usage="Traditional community wisdom sharing"
        )
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=500
                )
                
                return response.choices[0].message.content
            else:
                return "Cultural analysis unavailable - OpenAI client not configured"
                
        except Exception as e:
            logger.error(f"Cultural context preparation failed: {e}")
            return "Cultural analysis unavailable"
    
    async def _prepare_business_context_for_llm_judge(self, kikuyu_text: str, cultural_meaning: str) -> str:
        """Prepare business context specifically for LLM judge evaluation."""
        
        prompt = self.llm_judge_prompts['business_relevance_prep'].format(
            kikuyu_proverb=kikuyu_text,
            cultural_meaning=cultural_meaning
        )
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=500
                )
                
                return response.choices[0].message.content
            else:
                return "Business analysis unavailable - OpenAI client not configured"
                
        except Exception as e:
            logger.error(f"Business context preparation failed: {e}")
            return "Business analysis unavailable"
    
    def _simulate_cultural_context_retrieval(self, kikuyu_text: str) -> str:
        """Simulate cultural context retrieval from ontology (placeholder)."""
        return f"Cultural context for '{kikuyu_text}': Traditional Kikuyu wisdom about community values, respect, and social harmony."
    
    def _simulate_business_context_retrieval(self, kikuyu_text: str) -> str:
        """Simulate business context retrieval (placeholder)."""
        return f"Business relevance for '{kikuyu_text}': Entrepreneurship principles, teamwork, and business relationship building."
    
    def _simulate_traditional_usage_retrieval(self, kikuyu_text: str) -> str:
        """Simulate traditional usage context retrieval (placeholder)."""
        return f"Traditional usage: Used by elders to teach community values and guide social behavior."
    
    def _parse_enhanced_og_rag_response(self, response_text: str) -> Dict:
        """Parse OG-RAG translation response."""
        result = {}
        
        # Extract structured information from response
        lines = response_text.split('\\n')
        current_field = None
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1. TRANSLATION:', 'TRANSLATION:')):
                current_field = 'translation'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('2. CULTURAL_SIGNIFICANCE:', 'CULTURAL_SIGNIFICANCE:')):
                current_field = 'cultural_significance'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('3. BUSINESS_APPLICATION:', 'BUSINESS_APPLICATION:')):
                current_field = 'business_application'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('4. USAGE_CONTEXT:', 'USAGE_CONTEXT:')):
                current_field = 'usage_context'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('5. MODERN_APPLICATION:', 'MODERN_APPLICATION:')):
                current_field = 'modern_application'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('6. CULTURAL_METAPHORS:', 'CULTURAL_METAPHORS:')):
                current_field = 'cultural_metaphors'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('7. COMMUNITY_VALUES:', 'COMMUNITY_VALUES:')):
                current_field = 'community_values'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('8. CONFIDENCE_SCORE:', 'CONFIDENCE_SCORE:')):
                try:
                    result['confidence_score'] = float(line.split(':', 1)[1].strip())
                except:
                    result['confidence_score'] = 0.0
            elif current_field and line and not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                # Continue previous field
                result[current_field] = result.get(current_field, '') + ' ' + line
        
        # Set defaults for missing fields
        for field in ['translation', 'cultural_significance', 'business_application', 'usage_context']:
            if field not in result:
                result[field] = ''
        
        if 'confidence_score' not in result:
            result['confidence_score'] = 0.0
            
        return result
    
    def _parse_raw_llm_response(self, response_text: str) -> Dict:
        """Parse raw LLM translation response."""
        result = {}
        
        # Extract structured information from response
        lines = response_text.split('\\n')
        current_field = None
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1. TRANSLATION:', 'TRANSLATION:')):
                current_field = 'translation'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('2. CULTURAL_EXPLANATION:', 'CULTURAL_EXPLANATION:')):
                current_field = 'cultural_explanation'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('3. BUSINESS_APPLICATION:', 'BUSINESS_APPLICATION:')):
                current_field = 'business_application'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('4. REASONING:', 'REASONING:')):
                current_field = 'reasoning'
                result[current_field] = line.split(':', 1)[1].strip()
            elif line.startswith(('5. CONFIDENCE:', 'CONFIDENCE:')):
                try:
                    result['confidence'] = float(line.split(':', 1)[1].strip())
                except:
                    result['confidence'] = 0.0
            elif line.startswith(('6. ASSUMPTIONS:', 'ASSUMPTIONS:')):
                current_field = 'assumptions'
                result[current_field] = line.split(':', 1)[1].strip()
            elif current_field and line and not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.')):
                # Continue previous field
                result[current_field] = result.get(current_field, '') + ' ' + line
        
        # Set defaults for missing fields
        for field in ['translation', 'cultural_explanation', 'business_application', 'reasoning', 'assumptions']:
            if field not in result:
                result[field] = ''
        
        if 'confidence' not in result:
            result['confidence'] = 0.0
            
        return result
    
    def _calculate_evaluation_priority(self, row) -> str:
        """Calculate evaluation priority for LLM judge processing."""
        
        # High priority: High confidence differences or cultural complexity
        og_rag_conf = row.get('og_rag_confidence', 0)
        raw_llm_conf = row.get('raw_llm_confidence', 0)
        
        confidence_difference = abs(og_rag_conf - raw_llm_conf)
        cultural_richness = row.get('cultural_context_richness', 0)
        
        if confidence_difference > 0.3 or cultural_richness > 5:
            return "high"
        elif confidence_difference > 0.1 or cultural_richness > 3:
            return "medium"
        else:
            return "low"
    
    async def run_complete_comparison_pipeline(self, benchmark_file: str) -> Dict:
        """Run the complete translation comparison pipeline."""
        
        logger.info("🚀 Starting complete translation comparison pipeline...")
        
        # Step 1: Generate OG-RAG translations
        logger.info("Step 1: Generating enhanced OG-RAG translations...")
        og_rag_df = await self.generate_og_rag_translations_with_metadata(benchmark_file)
        
        # Step 2: Generate Raw LLM translations
        logger.info("Step 2: Generating raw LLM translations...")
        raw_llm_df = await self.generate_raw_llm_translations_for_comparison(benchmark_file)
        
        # Step 3: Create comprehensive comparison dataset
        logger.info("Step 3: Creating comprehensive comparison dataset...")
        comparison_df = await self.create_comprehensive_comparison_dataset()
        
        # Step 4: Run LLM as a Judge evaluation
        logger.info("Step 4: Running LLM as a Judge evaluation...")
        llm_judge_results = await self.run_llm_judge_evaluation()
        
        # Step 5: Generate summary report
        summary_report = self._generate_pipeline_summary(
            og_rag_df, raw_llm_df, comparison_df, llm_judge_results
        )
        
        logger.info("✅ Complete translation comparison pipeline finished!")
        return summary_report
    
    def _generate_pipeline_summary(self, og_rag_df: pd.DataFrame, 
                                 raw_llm_df: pd.DataFrame, 
                                 comparison_df: pd.DataFrame, 
                                 llm_judge_results: Dict) -> Dict:
        """Generate comprehensive pipeline summary."""
        
        summary = {
            "pipeline_metadata": {
                "completion_timestamp": datetime.now().isoformat(),
                "total_proverbs_processed": len(comparison_df),
                "llm_judge_framework_version": "1.0.0",
                "primary_llm_provider": self.configurator.primary_provider.value if self.configurator.primary_provider else None
            },
            "translation_statistics": {
                "og_rag_translations": len(og_rag_df),
                "raw_llm_translations": len(raw_llm_df),
                "successful_comparisons": len(comparison_df),
                "high_priority_evaluations": len(comparison_df[comparison_df['evaluation_priority'] == 'high']),
                "medium_priority_evaluations": len(comparison_df[comparison_df['evaluation_priority'] == 'medium']),
                "low_priority_evaluations": len(comparison_df[comparison_df['evaluation_priority'] == 'low'])
            },
            "llm_judge_evaluation": llm_judge_results.get('statistical_analysis', {}),
            "key_findings": llm_judge_results.get('key_findings', []),
            "recommendations": llm_judge_results.get('recommendations', []),
            "output_files": {
                "og_rag_translations": str(self.output_dir / "enhanced_og_rag_translations.csv"),
                "raw_llm_translations": str(self.output_dir / "raw_llm_translations.csv"),
                "comparison_dataset": str(self.output_dir / "comprehensive_translation_comparison.csv"),
                "llm_judge_results": str(self.output_dir / "llm_judge_evaluation_results.json")
            }
        }
        
        # Save summary report
        summary_file = self.output_dir / f"pipeline_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        return summary

async def main():
    """Run enhanced translation comparison system with LLM as a Judge integration."""
    
    # Initialize comparison system
    comparison_system = EnhancedTranslationComparisonSystem()
    
    # Check for benchmark file
    benchmark_file = "data/evaluation/benchmark/translation_evaluation_benchmark.csv"
    
    if not Path(benchmark_file).exists():
        logger.error(f"Benchmark file not found: {benchmark_file}")
        logger.info("Please run the evaluation benchmark creation script first:")
        logger.info("python scripts/create_evaluation_benchmark.py")
        return
    
    try:
        # Run complete pipeline
        summary_report = await comparison_system.run_complete_comparison_pipeline(benchmark_file)
        
        # Display results
        print("\\n🎯 Enhanced Translation Comparison with LLM-as-a-Judge Summary:")
        print(f"📊 Total comparisons: {summary_report['translation_statistics']['successful_comparisons']}")
        print(f"🎯 High priority evaluations: {summary_report['translation_statistics']['high_priority_evaluations']}")
        print(f"🔍 LLM Judge evaluations completed: ✅")
        print(f"🤖 Primary LLM Provider: {summary_report['pipeline_metadata']['primary_llm_provider']}")
        
        if summary_report.get('key_findings'):
            print("\\n📈 Key Findings:")
            for finding in summary_report['key_findings'][:3]:
                print(f"  • {finding}")
        
        if summary_report.get('recommendations'):
            print("\\n💡 Recommendations:")
            for rec in summary_report['recommendations'][:3]:
                print(f"  • {rec}")
        
        print(f"\\n💾 Complete results available in: {comparison_system.output_dir}")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())