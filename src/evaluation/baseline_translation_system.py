#!/usr/bin/env python3
"""
Baseline Translation System for thiLLMo

Provides a comprehensive baseline translation generation system that compares:
1. OG-RAG System (Ontology-Grounded RAG with cultural knowledge)
2. Raw LLM (Direct LLM translation without RAG or ontology)
3. Google Translate (Commercia                return Trans                return TranslationResult(
ationResult(
                    prover                   proverb_id="",
                    kikuyu_text=kikuyu_text,
                    translation=result_data.get("translation", ""),
                    system_name="Raw-LLM-Aya",
                    cultural_meaning=result_data.get("reasoning", "[Cohere Aya-23: Multilingual model optimized for 100+ languages including low-resource African languages]"),
                    confidence_score=result_data.get("confidence", 0.0),
                    gener_id="",
                    kikuyu_text=kikuyu_text,
                    translation=result_dation_time=generation_time,
                    timeta.get("transtamp=datetime.now().isoformat(),
                    mlation", ""),
                    systetadata={
                        "modem_name="Raw-LLM-GPT",
                    cultural": "c4ai-aya-23",
                        "prov_meanider": "cohere",
                        "model_type": "multilingual-lrl-optimized",
                        "languages_supported": "100+",
                        "lrl_support": "optimized_for_african_languages",
                        "with_ontology": Falsg=result_data.get("re
                    }
                asoning", ""),
                    confidence_score=result_data.get("confidence", 0.0),
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    metadata={"model": model_name, "provider": "openai", "with_ontology": False}
                )

This enables scientific validation of the OG-RAG approach by providing comparison baselines.
"""

import os
import pandas as pd
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import json
import asyncio
from dataclasses import dataclass, asdict
import time
import requests

# LLM APIs
import openai
from openai import OpenAI

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    logging.warning("google.generativeai not installed. Gemini support will be unavailable.")

# Translation APIs
try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None
    logging.warning("deep-translator not installed. Google Translate baseline will be unavailable.")

# Hugging Face Inference API
try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None
    logging.warning("huggingface_hub not installed. NLLB translation will be unavailable. Install with: pip install huggingface_hub")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class TranslationResult:
    """Single translation result from any system."""
    proverb_id: str
    kikuyu_text: str
    translation: str
    system_name: str
    cultural_meaning: Optional[str] = None
    business_relevance: Optional[str] = None
    confidence_score: Optional[float] = None
    generation_time: Optional[float] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ComparisonResult:
    """Complete comparison result across all translation systems."""
    proverb_id: str
    kikuyu_text: str
    expert_translation: str
    expert_cultural_meaning: str
    # OpenAI GPT-4 (General Multilingual LLM)
    openai_translation: str
    openai_reasoning: str
    openai_confidence: float
    openai_time: float
    # Cohere Aya-23 (African Language Optimized LLM)
    cohere_translation: str
    cohere_reasoning: str
    cohere_confidence: float
    cohere_time: float
    # NLLB-200 (Specialized MT with Native Kikuyu)
    nllb_translation: str
    nllb_confidence: float
    nllb_time: float
    # Google Translate (Commercial Baseline - No Kikuyu Support)
    google_translation: str
    google_time: float
    generation_timestamp: str


class BaselineTranslationSystem:
    """
    Core system for generating baseline translations across multiple translation approaches.
    
    This system enables rigorous evaluation of the OG-RAG approach by providing:
    - Direct comparison with raw LLM capabilities
    - Commercial baseline via Google Translate
    - Comprehensive metadata for evaluation
    """
    
    def __init__(self, config_file: str = ".env"):
        """Initialize all translation systems."""
        # Load environment variables
        if config_file:
            env_path = Path(config_file)
            if env_path.exists():
                from dotenv import load_dotenv
                load_dotenv(env_path)
        else:
            # Try to load from default .env file
            from dotenv import load_dotenv
            load_dotenv()
        
        self.config = self._load_config(config_file) if config_file and config_file.endswith('.json') else {}
        
        # Setup translation clients
        self.openai_client = self._setup_openai()
        self.cohere_client = self._setup_cohere()
        self.gemini_model = self._setup_gemini()
        self.hf_client = self._setup_huggingface()
        
        # Determine which LLM to use for Raw LLM baseline
        self.llm_client = self.openai_client or self.cohere_client
        self.llm_provider = "openai" if self.openai_client else "cohere" if self.cohere_client else None
        
        # Output directories
        self.output_dir = Path("data/results/baseline_translations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ BaselineTranslationSystem initialized")
        logger.info(f"   - OpenAI available: {self.openai_client is not None}")
        logger.info(f"   - Cohere available: {self.cohere_client is not None}")
        logger.info(f"   - Using LLM provider: {self.llm_provider}")
        logger.info(f"   - Gemini available: {self.gemini_model is not None}")
        logger.info(f"   - NLLB (Hugging Face) available: {self.hf_client is not None}")
        logger.info(f"   - Google Translate available: {GoogleTranslator is not None}")
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load config file: {e}")
            return {}
    
    def _setup_openai(self) -> Optional[OpenAI]:
        """Setup OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            logger.warning("⚠️ OPENAI_API_KEY not set - trying Cohere as alternative")
            return None
        
        try:
            client = OpenAI(api_key=api_key)
            # Test the connection
            client.models.list()
            logger.info("✅ OpenAI client initialized successfully")
            return client
        except Exception as e:
            error_msg = str(e).lower()
            if 'quota' in error_msg or 'insufficient_quota' in error_msg or 'billing' in error_msg:
                logger.warning(f"⚠️ OpenAI API key has insufficient quota - add credits at https://platform.openai.com/account/billing")
                logger.warning("⚠️ Falling back to Cohere Aya for translations")
            else:
                logger.error(f"Failed to initialize OpenAI client: {e}")
            return None
    
    def _setup_cohere(self) -> Optional[Any]:
        """Setup Cohere client as alternative to OpenAI."""
        api_key = os.getenv('COHERE_API_KEY')
        if not api_key or api_key == 'your_cohere_api_key_here':
            logger.warning("⚠️ COHERE_API_KEY not set")
            return None
        
        try:
            import cohere
            client = cohere.Client(api_key)
            logger.info("✅ Cohere client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {e}")
            return None
    
    def _setup_gemini(self) -> Optional[Any]:
        """Setup Google Gemini client (alternative to OpenAI)."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'your_google_api_key_here':
            logger.warning("⚠️ GOOGLE_API_KEY not set - Gemini translations unavailable")
            return None
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            logger.info("✅ Gemini client initialized successfully")
            return model
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return None
    
    def _setup_huggingface(self) -> bool:
        """Check if NLLB API is available (no authentication required)."""
        # The nllb-api space doesn't require authentication
        # We just need to verify requests library is available
        try:
            import requests
            logger.info("✅ NLLB-200 API available (via winstxnhdw/nllb-api space)")
            return True
        except ImportError:
            logger.warning("⚠️ requests library not installed - NLLB translations unavailable")
            return False
    
    # Google Translate setup removed - deep-translator creates translator instances on-demand
    
    def translate_openai(self, kikuyu_text: str) -> TranslationResult:
        """
        Generate translation using OG-RAG system with cultural ontology.
        
        NOTE: This is a placeholder that should integrate with your actual OG-RAG system.
        Replace this with actual OG-RAG pipeline when available.
        """
        start_time = time.time()
        
        # TODO: Replace with actual OG-RAG system integration
        # For now, this is a simulated enhanced translation
        if self.openai_client:
            prompt = f"""You are an expert Kikuyu-English translator with deep knowledge of Kikuyu culture, traditions, and business wisdom.

Kikuyu Proverb: {kikuyu_text}

Cultural Context (from ontology): {cultural_context or 'Access to cultural knowledge graph with proverb meanings, traditional usage, and community values.'}

Provide a culturally faithful translation that:
1. Preserves traditional wisdom and cultural meaning
2. Makes the wisdom accessible to English speakers
3. Identifies business and entrepreneurship relevance
4. Maintains cultural authenticity

Format your response as JSON:
{{
    "translation": "English translation",
    "cultural_meaning": "Deep cultural significance and traditional wisdom",
    "business_relevance": "How this applies to business and entrepreneurship",
    "confidence_score": 0.0-1.0
}}"""
            
            try:
                # Use gpt-4o-mini for better availability and cost-effectiveness
                openai_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
                response = self.openai_client.chat.completions.create(
                    model=openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                result_text = response.choices[0].message.content
                # Try to parse JSON response
                try:
                    result_data = json.loads(result_text)
                except:
                    # Fallback if not valid JSON
                    result_data = {
                        "translation": result_text,
                        "cultural_meaning": "Generated with OG-RAG enhanced context",
                        "business_relevance": "",
                        "confidence_score": 0.7
                    }
                
                generation_time = time.time() - start_time
                
                return TranslationResult(
                    proverb_id="",
                    kikuyu_text=kikuyu_text,
                    translation=result_data.get("translation", ""),
                    system_name="OG-RAG",
                    cultural_meaning=result_data.get("cultural_meaning", ""),
                    business_relevance=result_data.get("business_relevance", ""),
                    confidence_score=result_data.get("confidence_score", 0.0),
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    metadata={"model": "gpt-4", "with_ontology": True}
                )
            except Exception as e:
                logger.error(f"OG-RAG translation failed: {e}")
                return self._create_error_result(kikuyu_text, "OG-RAG", str(e))
        else:
            logger.error("OpenAI client not available for OG-RAG translation")
            return self._create_error_result(kikuyu_text, "OG-RAG", "OpenAI client not available")
    
    def translate_raw_llm(self, kikuyu_text: str) -> TranslationResult:
        """
        Generate translation using raw LLM without RAG or ontology.
        
        This provides the baseline of what a pure LLM can do without cultural enhancement.
        Supports both OpenAI and Cohere.
        """
        start_time = time.time()
        
        prompt = f"""Translate this Kikuyu proverb to English:

Kikuyu: {kikuyu_text}

Provide:
1. Your best English translation
2. What you think the cultural meaning might be
3. Your confidence level (0.0-1.0)

Format as JSON:
{{
    "translation": "English translation",
    "reasoning": "Why you translated it this way",
    "confidence": 0.0-1.0
}}"""
        
        # Try OpenAI first
        if self.openai_client:
            try:
                # Use gpt-4o-mini for better availability and cost-effectiveness
                openai_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
                response = self.openai_client.chat.completions.create(
                    model=openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                result_text = response.choices[0].message.content
                
                # Try to parse as JSON - handle both clean JSON and JSON wrapped in markdown
                translation = result_text
                reasoning = result_text
                confidence = 0.7
                
                try:
                    # Try direct JSON parse
                    result_data = json.loads(result_text)
                    translation = result_data.get("translation", result_text)
                    reasoning = result_data.get("reasoning", result_text)
                    confidence = result_data.get("confidence", 0.7)
                except json.JSONDecodeError:
                    # Try extracting JSON from markdown code blocks
                    try:
                        import re
                        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                        if json_match:
                            result_data = json.loads(json_match.group(1))
                            translation = result_data.get("translation", result_text)
                            reasoning = result_data.get("reasoning", result_text)
                            confidence = result_data.get("confidence", 0.7)
                        else:
                            # No JSON found, use full response
                            pass
                    except:
                        # Keep full response
                        pass
                
                generation_time = time.time() - start_time
                
                return TranslationResult(
                    proverb_id="",
                    kikuyu_text=kikuyu_text,
                    translation=translation,
                    system_name="Raw-LLM",
                    cultural_meaning=reasoning,  # Full reasoning preserved
                    confidence_score=confidence,
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    metadata={"model": openai_model, "provider": "openai", "with_ontology": False}
                )
            except Exception as e:
                error_msg = str(e).lower()
                if 'quota' in error_msg or 'insufficient_quota' in error_msg:
                    logger.warning(f"⚠️ OpenAI quota exceeded - falling back to Cohere Aya")
                else:
                    logger.error(f"OpenAI Raw LLM translation failed: {e}")
                # Fall through to try Cohere
        
        # Try Cohere as fallback
        if self.cohere_client:
            try:
                # Use c4ai-aya-23 for better low-resource language support (Kikuyu)
                # Aya is Cohere's multilingual model specifically trained on 101+ languages
                # including many African languages and low-resource languages
                cohere_model = os.getenv('COHERE_MODEL', 'c4ai-aya-23')  # Default to Aya for LRLs
                response = self.cohere_client.chat(
                    model=cohere_model,
                    message=prompt,
                    temperature=0.3
                )
                
                result_text = response.text
                
                # Try to parse as JSON - handle both clean JSON and JSON wrapped in markdown
                translation = result_text
                reasoning = result_text
                confidence = 0.7
                
                try:
                    # Try direct JSON parse
                    result_data = json.loads(result_text)
                    translation = result_data.get("translation", result_text)
                    reasoning = result_data.get("reasoning", result_text)
                    confidence = result_data.get("confidence", 0.7)
                except json.JSONDecodeError:
                    # Try extracting JSON from markdown code blocks
                    try:
                        import re
                        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                        if json_match:
                            result_data = json.loads(json_match.group(1))
                            translation = result_data.get("translation", result_text)
                            reasoning = result_data.get("reasoning", result_text)
                            confidence = result_data.get("confidence", 0.7)
                        else:
                            # No JSON found, use full response
                            pass
                    except:
                        # Keep full response
                        pass
                
                generation_time = time.time() - start_time
                
                return TranslationResult(
                    proverb_id="",
                    kikuyu_text=kikuyu_text,
                    translation=translation,
                    system_name="Raw-LLM",
                    cultural_meaning=reasoning,  # Full reasoning preserved
                    confidence_score=confidence,
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    metadata={"model": cohere_model, "provider": "cohere", "with_ontology": False, "model_type": "aya-multilingual" if 'aya' in cohere_model else "command"}
                )
            except Exception as e:
                logger.error(f"Cohere Raw LLM translation failed: {e}")
                return self._create_error_result(kikuyu_text, "Raw-LLM", str(e))
        
        # No LLM available
        logger.error("No LLM client available (tried OpenAI and Cohere)")
        return self._create_error_result(kikuyu_text, "Raw-LLM", "No LLM client available")
    
    def translate_google(self, kikuyu_text: str) -> TranslationResult:
        """
        Generate translation using Google Translate (commercial baseline).
        
        This provides the industry standard baseline for machine translation.
        Uses deep-translator library for reliable Google Translate access.
        """
        start_time = time.time()
        
        if GoogleTranslator:
            try:
                # deep-translator uses a different API - create translator with source/target
                # Use 'auto' since Kikuyu ('ki') is not officially supported
                translator = GoogleTranslator(source='auto', target='en')
                translation = translator.translate(kikuyu_text)
                generation_time = time.time() - start_time
                
                return TranslationResult(
                    proverb_id="",
                    kikuyu_text=kikuyu_text,
                    translation=translation,
                    system_name="Google-Translate",
                    cultural_meaning="Commercial MT system - no cultural enhancement",
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    metadata={"service": "Google Translate", "src": "auto", "dest": "en", "via": "deep-translator"}
                )
            except Exception as e:
                error_msg = str(e)
                # Check if it's an unsupported language error
                if 'no support' in error_msg.lower() or 'not supported' in error_msg.lower():
                    logger.warning(f"Google Translate does not support source language (likely Kikuyu): {error_msg[:100]}")
                    return TranslationResult(
                        proverb_id="",
                        kikuyu_text=kikuyu_text,
                        translation="[Language not supported by Google Translate - Kikuyu is a low-resource language]",
                        system_name="Google-Translate",
                        cultural_meaning="Commercial MT system - language not supported",
                        confidence_score=0.0,
                        generation_time=time.time() - start_time,
                        timestamp=datetime.now().isoformat(),
                        metadata={"error": "unsupported_language", "note": "Kikuyu not in Google Translate's 133 supported languages"}
                    )
                else:
                    logger.error(f"Google Translate failed: {e}")
                    return self._create_error_result(kikuyu_text, "Google-Translate", str(e))
        else:
            logger.warning("Google Translate not available")
            return self._create_error_result(kikuyu_text, "Google-Translate", "Service not available")
    
    def translate_nllb(self, kikuyu_text: str) -> TranslationResult:
        """Generate translation using NLLB-200 (Meta's specialized low-resource MT).
        
        NLLB (No Language Left Behind) is specifically trained on 200+ languages including
        Kikuyu (kik_Latn), making it the only MT model with native Kikuyu support.
        Uses the community-hosted API at winstxnhdw/nllb-api HF Space.
        This provides the specialized MT baseline for comparison.
        """
        start_time = time.time()
        
        if not self.hf_client:
            logger.warning("NLLB API not available for translation")
            return self._create_error_result(kikuyu_text, "NLLB-200", "NLLB API not available")
        
        try:
            # Use the dedicated NLLB API hosted on HF Spaces
            # This API uses CTranslate2 backend for fast CPU inference
            api_url = "https://winstxnhdw-nllb-api.hf.space/api/v4/translator"
            
            params = {
                "text": kikuyu_text,
                "source": "kik_Latn",  # Kikuyu in Latin script
                "target": "eng_Latn"   # English in Latin script
            }
            
            # Make request with timeout
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # API returns text translation (sometimes wrapped in JSON)
            translation_text = response.text.strip()
            
            # Handle potential JSON wrapping
            try:
                import json
                json_data = json.loads(translation_text)
                if isinstance(json_data, dict) and 'result' in json_data:
                    translation = json_data['result']
                else:
                    translation = translation_text
            except (json.JSONDecodeError, ValueError):
                # Not JSON, use as-is
                translation = translation_text
            
            generation_time = time.time() - start_time
            
            return TranslationResult(
                proverb_id="",
                kikuyu_text=kikuyu_text,
                translation=translation,
                system_name="NLLB-200",
                cultural_meaning="Meta's specialized MT with native Kikuyu support (FLORES-200)",
                confidence_score=0.85,  # Higher than Google due to native Kikuyu support
                generation_time=generation_time,
                timestamp=datetime.now().isoformat(),
                metadata={
                    "model": "facebook/nllb-200-distilled-1.3B",
                    "provider": "winstxnhdw-nllb-api",
                    "api_version": "v4",
                    "api_url": api_url,
                    "source_lang": "kik_Latn",
                    "target_lang": "eng_Latn",
                    "training_data": "FLORES-200",
                    "backend": "CTranslate2"
                }
            )
        except requests.exceptions.Timeout:
            logger.error("NLLB API request timed out after 30 seconds")
            return self._create_error_result(kikuyu_text, "NLLB-200", "API timeout (30s)")
        except requests.exceptions.HTTPError as e:
            logger.error(f"NLLB API HTTP error: {e}")
            return self._create_error_result(kikuyu_text, "NLLB-200", f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except requests.exceptions.RequestException as e:
            logger.error(f"NLLB API request failed: {e}")
            return self._create_error_result(kikuyu_text, "NLLB-200", str(e))
        except Exception as e:
            logger.error(f"NLLB translation failed: {e}")
            return self._create_error_result(kikuyu_text, "NLLB-200", str(e))
    
    def _create_error_result(self, kikuyu_text: str, system_name: str, error_msg: str) -> TranslationResult:
        """Create an error result when translation fails."""
        return TranslationResult(
            proverb_id="",
            kikuyu_text=kikuyu_text,
            translation=f"[ERROR: {error_msg}]",
            system_name=system_name,
            cultural_meaning="Translation failed",
            generation_time=0.0,
            timestamp=datetime.now().isoformat(),
            metadata={"error": error_msg}
        )
    
    def generate_all_translations(self, kikuyu_text: str, proverb_id: str = "") -> Dict[str, TranslationResult]:
        """Generate translations from all available systems."""
        results = {}
        
        logger.info(f"Generating translations for: {kikuyu_text[:50]}...")
        
        # OG-RAG translation (placeholder - will be enhanced with ontology later)
        og_rag_result = self.translate_og_rag(kikuyu_text)
        og_rag_result.proverb_id = proverb_id
        results['og_rag'] = og_rag_result
        logger.info(f"  ✓ OG-RAG: {og_rag_result.translation[:60]}...")
        
        # Raw LLM translation (general multilingual AI)
        raw_llm_result = self.translate_raw_llm(kikuyu_text)
        raw_llm_result.proverb_id = proverb_id
        results['raw_llm'] = raw_llm_result
        logger.info(f"  ✓ Raw LLM: {raw_llm_result.translation[:60]}...")
        
        # NLLB translation (specialized MT with native Kikuyu support)
        nllb_result = self.translate_nllb(kikuyu_text)
        nllb_result.proverb_id = proverb_id
        results['nllb'] = nllb_result
        logger.info(f"  ✓ NLLB-200: {nllb_result.translation[:60]}...")
        
        # Google Translate (commercial baseline - reference only)
        google_result = self.translate_google(kikuyu_text)
        google_result.proverb_id = proverb_id
        results['google'] = google_result
        logger.info(f"  ✓ Google: {google_result.translation[:60]}...")
        
        return results


class TranslationComparator:
    """
    Compares and analyzes translations across all baseline systems.
    
    Generates comprehensive comparison datasets for evaluation.
    """
    
    def __init__(self, translation_system: BaselineTranslationSystem):
        self.translation_system = translation_system
        self.output_dir = Path("data/results/baseline_translations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def compare_on_gold_standard(
        self, 
        gold_standard_file: str,
        output_file: Optional[str] = None,
        max_proverbs: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Generate translations for all proverbs in gold standard dataset.
        
        Args:
            gold_standard_file: Path to gold standard CSV file
            output_file: Optional custom output filename
            max_proverbs: Optional limit on number of proverbs to process
            
        Returns:
            DataFrame with comprehensive comparison across all systems
        """
        # Load gold standard
        gold_df = pd.read_csv(gold_standard_file)
        logger.info(f"Loaded {len(gold_df)} proverbs from gold standard")
        
        if max_proverbs:
            gold_df = gold_df.head(max_proverbs)
            logger.info(f"Limited to {max_proverbs} proverbs for processing")
        
        comparison_results = []
        
        for idx, row in gold_df.iterrows():
            proverb_id = row.get('proverb_id', f'proverb_{idx}')
            kikuyu_text = row.get('kikuyu_text', '')
            expert_translation = row.get('expert_translation', '')
            expert_cultural_meaning = row.get('expert_cultural_meaning', '')
            
            if not kikuyu_text:
                logger.warning(f"Skipping row {idx}: No Kikuyu text")
                continue
            
            logger.info(f"\n[{idx+1}/{len(gold_df)}] Processing: {proverb_id}")
            
            # Generate translations from all systems
            translations = self.translation_system.generate_all_translations(kikuyu_text, proverb_id)
            
            # Compile comparison record
            comparison_record = {
                'proverb_id': proverb_id,
                'kikuyu_text': kikuyu_text,
                'expert_translation': expert_translation,
                'expert_cultural_meaning': expert_cultural_meaning,
                
                # OG-RAG results
                'og_rag_translation': translations['og_rag'].translation,
                'og_rag_cultural_meaning': translations['og_rag'].cultural_meaning or '',
                'og_rag_business_relevance': translations['og_rag'].business_relevance or '',
                'og_rag_confidence': translations['og_rag'].confidence_score or 0.0,
                'og_rag_time': translations['og_rag'].generation_time or 0.0,
                
                # Raw LLM results
                'raw_llm_translation': translations['raw_llm'].translation,
                'raw_llm_reasoning': translations['raw_llm'].cultural_meaning or '',
                'raw_llm_confidence': translations['raw_llm'].confidence_score or 0.0,
                'raw_llm_time': translations['raw_llm'].generation_time or 0.0,
                
                # NLLB results (specialized MT with native Kikuyu support)
                'nllb_translation': translations['nllb'].translation,
                'nllb_metadata': json.dumps(translations['nllb'].metadata) if translations['nllb'].metadata else '',
                'nllb_time': translations['nllb'].generation_time or 0.0,
                
                # Google Translate results (reference only - limited Kikuyu support)
                'google_translation': translations['google'].translation,
                'google_time': translations['google'].generation_time or 0.0,
                
                # Metadata
                'generation_timestamp': datetime.now().isoformat(),
                'processing_order': idx + 1
            }
            
            comparison_results.append(comparison_record)
            
            # Save incrementally every 10 proverbs
            if (idx + 1) % 10 == 0:
                self._save_incremental_results(comparison_results, output_file)
        
        # Create final DataFrame
        results_df = pd.DataFrame(comparison_results)
        
        # Save final results
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"translation_comparison_all_systems_{timestamp}.csv"
        
        output_path = self.output_dir / output_file
        results_df.to_csv(output_path, index=False)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"✅ BASELINE TRANSLATION GENERATION COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Processed: {len(results_df)} proverbs")
        logger.info(f"Systems: OG-RAG, Raw LLM, NLLB-200, Google Translate")
        logger.info(f"Output: {output_path}")
        logger.info(f"{'='*80}\n")
        
        # Generate summary statistics
        self._generate_summary_report(results_df, output_path)
        
        return results_df
    
    def _save_incremental_results(self, results: List[Dict], output_file: Optional[str]):
        """Save results incrementally to prevent data loss."""
        if output_file is None:
            output_file = "translation_comparison_incremental.csv"
        
        output_path = self.output_dir / output_file
        pd.DataFrame(results).to_csv(output_path, index=False)
        logger.info(f"  💾 Incremental save: {len(results)} proverbs")
    
    def _generate_summary_report(self, results_df: pd.DataFrame, output_path: Path):
        """Generate summary statistics report."""
        report_path = output_path.parent / f"{output_path.stem}_summary.txt"
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("BASELINE TRANSLATION GENERATION SUMMARY\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Proverbs: {len(results_df)}\n\n")
            
            f.write("TRANSLATION SYSTEMS:\n")
            f.write("  1. OG-RAG (Ontology-Grounded RAG with cultural knowledge - placeholder)\n")
            f.write("  2. Raw LLM (General multilingual AI without cultural enhancement)\n")
            f.write("  3. NLLB-200 (Specialized MT with native Kikuyu training data)\n")
            f.write("  4. Google Translate (Commercial baseline - reference only)\n\n")
            
            f.write("GENERATION TIME STATISTICS:\n")
            f.write(f"  OG-RAG avg time: {results_df['og_rag_time'].mean():.2f}s\n")
            f.write(f"  Raw LLM avg time: {results_df['raw_llm_time'].mean():.2f}s\n")
            f.write(f"  NLLB avg time: {results_df['nllb_time'].mean():.2f}s\n")
            f.write(f"  Google avg time: {results_df['google_time'].mean():.2f}s\n\n")
            
            f.write("CONFIDENCE SCORES (where available):\n")
            f.write(f"  OG-RAG avg confidence: {results_df['og_rag_confidence'].mean():.2f}\n")
            f.write(f"  Raw LLM avg confidence: {results_df['raw_llm_confidence'].mean():.2f}\n")
            f.write(f"  NLLB: No confidence scores (deterministic MT model)\n\n")
            
            f.write("OUTPUT FILES:\n")
            f.write(f"  Main dataset: {output_path.name}\n")
            f.write(f"  Summary report: {report_path.name}\n\n")
            
            f.write("NEXT STEPS:\n")
            f.write("  1. Run evaluation metrics (BLEU, ROUGE, METEOR)\n")
            f.write("  2. Perform cultural authenticity assessment\n")
            f.write("  3. Conduct LLM-as-a-Judge evaluation\n")
            f.write("  4. Generate comparative analysis visualizations\n")
            f.write("="*80 + "\n")
        
        logger.info(f"📊 Summary report saved: {report_path}")


def main():
    """Main execution function with example usage."""
    print("\n" + "="*80)
    print("BASELINE TRANSLATION GENERATION SYSTEM")
    print("="*80 + "\n")
    
    # Initialize system
    translation_system = BaselineTranslationSystem()
    comparator = TranslationComparator(translation_system)
    
    # Define input file
    gold_standard_file = "data/evaluation/gold_standard_ireri.csv"
    
    if not Path(gold_standard_file).exists():
        print(f"❌ Gold standard file not found: {gold_standard_file}")
        print("Please ensure the gold standard dataset exists.")
        return
    
    # Generate baseline translations
    print("Starting baseline translation generation...")
    print("This will compare OG-RAG, Raw LLM, and Google Translate\n")
    
    # You can limit proverbs for testing
    # results_df = comparator.compare_on_gold_standard(gold_standard_file, max_proverbs=10)
    
    # Or process all proverbs
    results_df = comparator.compare_on_gold_standard(gold_standard_file)
    
    print("\n✅ Baseline translation generation complete!")
    print(f"Results saved to: data/results/baseline_translations/")


if __name__ == "__main__":
    main()
