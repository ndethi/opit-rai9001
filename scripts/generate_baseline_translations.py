#!/usr/bin/env python3
"""
Clean Baseline Translation Generation Script

Generates baseline translations for Kikuyu proverbs with SEPARATED systems:
1. OpenAI GPT-4 (General Multilingual LLM)
2. Cohere Aya-23 (African Language Optimized LLM)
3. NLLB-200 (Specialized MT with Native Kikuyu Support)
4. Google Translate (Commercial Baseline - No Kikuyu Support)

Output: ONE row per proverb (no duplicates, no confusion)

Usage:
    python generate_baseline_translations.py [--max-proverbs N] [--output filename.csv]
    
Examples:
    # Process all proverbs
    python generate_baseline_translations.py
    
    # Test with 10 proverbs
    python generate_baseline_translations.py --max-proverbs 10
    
    # Process 50 proverbs with custom output
    python generate_baseline_translations.py --max-proverbs 50 --output my_baseline.csv
"""

import sys
import os
import argparse
from pathlib import Path
import pandas as pd
import logging
import time
import json
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class CleanTranslationResult:
    """Clean structure with ONE translation per system."""
    # Proverb Info
    proverb_id: str
    kikuyu_text: str
    expert_translation: str
    expert_cultural_meaning: str
    
    # OpenAI GPT-4
    openai_translation: str
    openai_reasoning: str
    openai_confidence: float
    openai_time: float
    
    # Cohere Aya-23
    cohere_translation: str
    cohere_reasoning: str
    cohere_confidence: float
    cohere_time: float
    
    # NLLB-200
    nllb_translation: str
    nllb_confidence: float
    nllb_time: float
    
    # Google Translate
    google_translation: str
    google_time: float
    
    # Metadata
    timestamp: str


class CleanBaselineGenerator:
    """Generates clean, deduplicated baseline translations."""
    
    def __init__(self):
        """Initialize with separated LLM clients."""
        from dotenv import load_dotenv
        load_dotenv()
        
        # Initialize OpenAI
        self.openai_client = self._setup_openai()
        
        # Initialize Cohere
        self.cohere_client = self._setup_cohere()
        
        # NLLB API available (no auth needed)
        self.nllb_available = self._check_nllb()
        
        # Google Translate available
        self.google_available = self._check_google()
        
        logger.info("\n" + "="*80)
        logger.info("CLEAN BASELINE TRANSLATION SYSTEM INITIALIZED")
        logger.info("="*80)
        logger.info(f"✅ OpenAI GPT-4 available: {self.openai_client is not None}")
        logger.info(f"✅ Cohere Aya-23 available: {self.cohere_client is not None}")
        logger.info(f"✅ NLLB-200 API available: {self.nllb_available}")
        logger.info(f"✅ Google Translate available: {self.google_available}")
        logger.info("="*80 + "\n")
    
    def _setup_openai(self):
        """Setup OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("⚠️  OPENAI_API_KEY not set")
            return None
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            return client
        except Exception as e:
            logger.error(f"OpenAI setup failed: {e}")
            return None
    
    def _setup_cohere(self):
        """Setup Cohere client."""
        api_key = os.getenv('COHERE_API_KEY')
        if not api_key:
            logger.warning("⚠️  COHERE_API_KEY not set")
            return None
        try:
            import cohere
            client = cohere.Client(api_key)
            return client
        except Exception as e:
            logger.error(f"Cohere setup failed: {e}")
            return None
    
    def _check_nllb(self):
        """Check if NLLB API is available."""
        try:
            import requests
            return True
        except ImportError:
            return False
    
    def _check_google(self):
        """Check if Google Translate is available."""
        try:
            from deep_translator import GoogleTranslator
            return True
        except ImportError:
            return False
    
    def translate_openai(self, kikuyu_text: str) -> Dict:
        """Translate using OpenAI GPT-4."""
        if not self.openai_client:
            return {"translation": "[OpenAI unavailable]", "reasoning": "", "confidence": 0.0, "time": 0.0}
        
        start_time = time.time()
        
        prompt = f"""Translate this Kikuyu proverb to English:

Kikuyu: {kikuyu_text}

Provide:
1. Your best English translation
2. Your reasoning for this translation
3. Your confidence level (0.0-1.0)

Format as JSON:
{{
    "translation": "English translation",
    "reasoning": "Why you translated it this way",
    "confidence": 0.0-1.0
}}"""
        
        try:
            model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON
            try:
                result_data = json.loads(result_text)
            except:
                # Try extracting from markdown
                import re
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                if json_match:
                    result_data = json.loads(json_match.group(1))
                else:
                    result_data = {"translation": result_text, "reasoning": "", "confidence": 0.7}
            
            return {
                "translation": result_data.get("translation", result_text),
                "reasoning": result_data.get("reasoning", ""),
                "confidence": result_data.get("confidence", 0.7),
                "time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"OpenAI translation failed: {e}")
            return {"translation": f"[ERROR: {str(e)}]", "reasoning": "", "confidence": 0.0, "time": time.time() - start_time}
    
    def translate_cohere(self, kikuyu_text: str) -> Dict:
        """Translate using Cohere Aya-23 (African language optimized)."""
        if not self.cohere_client:
            return {"translation": "[Cohere unavailable]", "reasoning": "", "confidence": 0.0, "time": 0.0}
        
        start_time = time.time()
        
        prompt = f"""Translate this Kikuyu proverb to English:

Kikuyu: {kikuyu_text}

Provide:
1. Your best English translation
2. Your reasoning for this translation  
3. Your confidence level (0.0-1.0)

Format as JSON:
{{
    "translation": "English translation",
    "reasoning": "Why you translated it this way",
    "confidence": 0.0-1.0
}}"""
        
        try:
            model = os.getenv('COHERE_MODEL', 'c4ai-aya-23')
            response = self.cohere_client.chat(
                model=model,
                message=prompt,
                temperature=0.3
            )
            
            result_text = response.text
            
            # Parse JSON
            try:
                result_data = json.loads(result_text)
            except:
                # Try extracting from markdown
                import re
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                if json_match:
                    result_data = json.loads(json_match.group(1))
                else:
                    result_data = {"translation": result_text, "reasoning": "", "confidence": 0.7}
            
            return {
                "translation": result_data.get("translation", result_text),
                "reasoning": result_data.get("reasoning", ""),
                "confidence": result_data.get("confidence", 0.7),
                "time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Cohere translation failed: {e}")
            return {"translation": f"[ERROR: {str(e)}]", "reasoning": "", "confidence": 0.0, "time": time.time() - start_time}
    
    def translate_nllb(self, kikuyu_text: str) -> Dict:
        """Translate using NLLB-200 API."""
        if not self.nllb_available:
            return {"translation": "[NLLB unavailable]", "confidence": 0.0, "time": 0.0}
        
        start_time = time.time()
        
        try:
            import requests
            api_url = "https://winstxnhdw-nllb-api.hf.space/api/v4/translator"
            params = {
                "text": kikuyu_text,
                "source": "kik_Latn",
                "target": "eng_Latn"
            }
            
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            translation_text = response.text.strip()
            
            # Handle JSON wrapping
            try:
                json_data = json.loads(translation_text)
                if isinstance(json_data, dict) and 'result' in json_data:
                    translation = json_data['result']
                else:
                    translation = translation_text
            except:
                translation = translation_text
            
            return {
                "translation": translation,
                "confidence": 0.85,
                "time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"NLLB translation failed: {e}")
            return {"translation": f"[ERROR: {str(e)}]", "confidence": 0.0, "time": time.time() - start_time}
    
    def translate_google(self, kikuyu_text: str) -> Dict:
        """Translate using Google Translate (no Kikuyu support - auto-detect)."""
        if not self.google_available:
            return {"translation": "[Google unavailable]", "time": 0.0}
        
        start_time = time.time()
        
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source='auto', target='en')
            translation = translator.translate(kikuyu_text)
            
            return {
                "translation": translation,
                "time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Google Translate failed: {e}")
            return {"translation": f"[ERROR: {str(e)}]", "time": time.time() - start_time}
    
    def generate_clean_baseline(self, gold_standard_file: str, max_proverbs: int = None, output_file: str = None):
        """Generate clean baseline with ONE row per proverb."""
        # Load gold standard
        gold_df = pd.read_csv(gold_standard_file)
        logger.info(f"\n📚 Loaded {len(gold_df)} proverbs from gold standard")
        
        if max_proverbs:
            gold_df = gold_df.head(max_proverbs)
            logger.info(f"🎯 Processing {max_proverbs} proverbs\n")
        
        results = []
        
        for idx, row in gold_df.iterrows():
            proverb_id = row.get('proverb_id', f'proverb_{idx}')
            kikuyu_text = row.get('kikuyu_text', '')
            expert_translation = row.get('expert_translation', '')
            expert_cultural_meaning = row.get('expert_cultural_meaning', '')
            
            if not kikuyu_text:
                logger.warning(f"⚠️  Skipping {proverb_id}: No Kikuyu text")
                continue
            
            logger.info(f"\n[{idx+1}/{len(gold_df)}] {proverb_id}: {kikuyu_text[:60]}...")
            
            # Translate with ALL systems (no mixing!)
            openai_result = self.translate_openai(kikuyu_text)
            logger.info(f"  ✓ OpenAI: {openai_result['translation'][:50]}...")
            
            cohere_result = self.translate_cohere(kikuyu_text)
            logger.info(f"  ✓ Cohere: {cohere_result['translation'][:50]}...")
            
            nllb_result = self.translate_nllb(kikuyu_text)
            logger.info(f"  ✓ NLLB: {nllb_result['translation'][:50]}...")
            
            google_result = self.translate_google(kikuyu_text)
            logger.info(f"  ✓ Google: {google_result['translation'][:50]}...")
            
            # Create ONE clean record
            clean_record = CleanTranslationResult(
                proverb_id=proverb_id,
                kikuyu_text=kikuyu_text,
                expert_translation=expert_translation,
                expert_cultural_meaning=expert_cultural_meaning,
                openai_translation=openai_result['translation'],
                openai_reasoning=openai_result['reasoning'],
                openai_confidence=openai_result['confidence'],
                openai_time=openai_result['time'],
                cohere_translation=cohere_result['translation'],
                cohere_reasoning=cohere_result['reasoning'],
                cohere_confidence=cohere_result['confidence'],
                cohere_time=cohere_result['time'],
                nllb_translation=nllb_result['translation'],
                nllb_confidence=nllb_result['confidence'],
                nllb_time=nllb_result['time'],
                google_translation=google_result['translation'],
                google_time=google_result['time'],
                timestamp=datetime.now().isoformat()
            )
            
            results.append(clean_record)
            
            # Save incrementally every 10 proverbs
            if (idx + 1) % 10 == 0:
                self._save_incremental(results)
        
        # Save final results
        return self._save_final(results, output_file)
    
    def _save_incremental(self, results):
        """Save incremental results."""
        df = pd.DataFrame([vars(r) for r in results])
        output_dir = Path("data/results/baseline_translations")
        output_dir.mkdir(parents=True, exist_ok=True)
        temp_file = output_dir / f"baseline_clean_temp_{len(results)}.csv"
        df.to_csv(temp_file, index=False)
        logger.info(f"  💾 Incremental save: {len(results)} proverbs")
    
    def _save_final(self, results, output_file=None):
        """Save final clean results."""
        df = pd.DataFrame([vars(r) for r in results])
        output_dir = Path("data/results/baseline_translations")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"baseline_translations_clean_{len(results)}proverbs_{timestamp}.csv"
        
        output_path = output_dir / output_file
        df.to_csv(output_path, index=False)
        
        logger.info("\n" + "="*80)
        logger.info("✅ CLEAN BASELINE GENERATION COMPLETE")
        logger.info("="*80)
        logger.info(f"📊 Total proverbs: {len(results)}")
        logger.info(f"📁 Output file: {output_path}")
        logger.info(f"🎯 Structure: ONE row per proverb")
        logger.info(f"🔧 Systems: OpenAI | Cohere | NLLB | Google")
        logger.info("="*80 + "\n")
        
        return output_path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate clean baseline translations with separated systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all proverbs from gold standard
  python generate_baseline_translations.py
  
  # Test with 10 proverbs
  python generate_baseline_translations.py --max-proverbs 10
  
  # Process 50 proverbs with custom output
  python generate_baseline_translations.py --max-proverbs 50 --output my_baseline.csv
  
  # Use alternative input file
  python generate_baseline_translations.py --input data/evaluation/alternative.csv

Environment Variables Required:
  OPENAI_API_KEY  - For OpenAI GPT-4 translations
  COHERE_API_KEY  - For Cohere Aya-23 translations
  (NLLB and Google Translate require no API keys)
        """
    )
    
    parser.add_argument(
        '--input',
        type=str,
        default='data/evaluation/gold_standard_ireri.csv',
        help='Path to gold standard CSV file (default: data/evaluation/gold_standard_ireri.csv)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output filename (default: auto-generated with timestamp)'
    )
    
    parser.add_argument(
        '--max-proverbs',
        type=int,
        default=None,
        help='Limit number of proverbs to process (useful for testing)'
    )
    
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()
    
    print("\n" + "="*80)
    print("CLEAN BASELINE TRANSLATION GENERATION")
    print("="*80)
    print("\nGenerating translations with SEPARATED systems:")
    print("  1. OpenAI GPT-4 (General Multilingual LLM)")
    print("  2. Cohere Aya-23 (African Language Optimized LLM)")
    print("  3. NLLB-200 (Specialized MT with Native Kikuyu)")
    print("  4. Google Translate (Commercial Baseline)")
    print("\nOutput: ONE row per proverb (no duplicates, no confusion)")
    print("="*80 + "\n")
    
    # Generate baseline
    print("Starting baseline generation...\n")
    
    generator = CleanBaselineGenerator()
    output_file = generator.generate_clean_baseline(
        gold_standard_file=args.input,
        max_proverbs=args.max_proverbs,
        output_file=args.output
    )
    
    print(f"\n✅ SUCCESS! Clean baseline saved to:\n   {output_file}\n")
    print("Next steps:")
    print("  1. Review the CSV (one row per proverb)")
    print("  2. Analyze OpenAI vs Cohere vs NLLB performance")
    print("  3. Identify cultural gaps across all systems")
    print("  4. Make foundation decision for OG-RAG development\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
