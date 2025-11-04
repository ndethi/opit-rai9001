#!/usr/bin/env python3
"""
OG-RAG Evaluation Script
========================

Runs comprehensive evaluation comparing three translation approaches:
1. Raw GPT-4 (baseline - zero-shot)
2. Traditional RAG (GPT-4 + example proverbs)
3. OG-RAG (GPT-4 + ontology-grounded cultural context)

Processes 100 proverbs and stores results in:
- CSV: data/results/ograg_translations/ograg_evaluation_100proverbs.csv
- Neo4j: Updates Proverb nodes with translation properties

Author: Research Team
Date: November 4, 2025
"""

import os
import sys
import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import time
import json
from neo4j import GraphDatabase
from decouple import config

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from og_rag_system import OGRAGTranslator, TranslationResult

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OGRAGEvaluator:
    """
    Comprehensive evaluation system for OG-RAG translations.
    
    Runs all 3 translation methods, tracks progress, handles errors,
    and stores results in both CSV and Neo4j.
    """
    
    def __init__(
        self,
        output_dir: str = "data/results/ograg_translations",
        batch_size: int = 10,
        save_interval: int = 10
    ):
        """
        Initialize evaluator.
        
        Args:
            output_dir: Directory to save CSV results
            batch_size: Number of proverbs to process before showing progress
            save_interval: Save CSV every N proverbs (for crash recovery)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.batch_size = batch_size
        self.save_interval = save_interval
        
        # Initialize translator
        logger.info("Initializing OG-RAG Translator...")
        self.translator = OGRAGTranslator(model="gpt-4", temperature=0.3)
        
        # Initialize Neo4j connection
        logger.info("Connecting to Neo4j...")
        self.neo4j_driver = GraphDatabase.driver(
            config('NEO4J_URI'),
            auth=(config('NEO4J_USER'), config('NEO4J_PASSWORD'))
        )
        
        # Results storage
        self.results: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        
        # Statistics
        self.total_tokens = 0
        self.total_cost = 0.0
        self.start_time = None
        
        logger.info("✅ OGRAGEvaluator initialized successfully")
    
    def load_proverbs_from_neo4j(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Load proverbs from Neo4j database.
        
        Args:
            limit: Maximum number of proverbs to load (None = all)
            
        Returns:
            List of proverb dictionaries
        """
        logger.info(f"Loading proverbs from Neo4j (limit={limit or 'all'})...")
        
        query = """
        MATCH (p:Proverb)
        RETURN p.proverb_id as proverb_id,
               p.kikuyu_text as kikuyu_text,
               p.expert_translation as expert_translation,
               p.expert_cultural_meaning as expert_cultural_meaning
        ORDER BY p.proverb_id
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        with self.neo4j_driver.session() as session:
            result = session.run(query)
            proverbs = [dict(record) for record in result]
        
        logger.info(f"✅ Loaded {len(proverbs)} proverbs from Neo4j")
        return proverbs
    
    def translate_proverb(
        self,
        proverb: Dict[str, str],
        index: int,
        total: int
    ) -> Dict[str, Any]:
        """
        Translate a single proverb using all 3 methods.
        
        Args:
            proverb: Proverb dictionary with kikuyu_text, proverb_id, etc.
            index: Current index (for progress)
            total: Total number of proverbs
            
        Returns:
            Dictionary with all translation results
        """
        proverb_id = proverb['proverb_id']
        kikuyu_text = proverb['kikuyu_text']
        
        logger.info(f"\n{'='*70}")
        logger.info(f"[{index}/{total}] Processing: {proverb_id}")
        logger.info(f"Kikuyu: {kikuyu_text}")
        logger.info(f"{'='*70}")
        
        result_dict = {
            'proverb_id': proverb_id,
            'kikuyu_text': kikuyu_text,
            'expert_translation': proverb.get('expert_translation', ''),
            'expert_cultural_meaning': proverb.get('expert_cultural_meaning', ''),
        }
        
        # Translate with all 3 methods
        try:
            translations = self.translator.translate_all_methods(
                kikuyu_text=kikuyu_text,
                proverb_id=proverb_id,
                k=5  # Retrieve top 5 similar proverbs
            )
            
            # Raw GPT-4 results
            raw = translations['raw']
            result_dict.update({
                'raw_translation': raw.translation,
                'raw_tokens_prompt': raw.prompt_tokens,
                'raw_tokens_completion': raw.completion_tokens,
                'raw_tokens_total': raw.total_tokens,
                'raw_prompt_length': raw.prompt_length,
                'raw_error': raw.error or '',
            })
            
            # Traditional RAG results
            trad = translations['traditional_rag']
            result_dict.update({
                'trad_rag_translation': trad.translation,
                'trad_rag_tokens_prompt': trad.prompt_tokens,
                'trad_rag_tokens_completion': trad.completion_tokens,
                'trad_rag_tokens_total': trad.total_tokens,
                'trad_rag_prompt_length': trad.prompt_length,
                'trad_rag_retrieved_count': len(trad.retrieved_proverbs) if trad.retrieved_proverbs else 0,
                'trad_rag_retrieved_ids': ','.join([p.proverb_id for p in trad.retrieved_proverbs]) if trad.retrieved_proverbs else '',
                'trad_rag_error': trad.error or '',
            })
            
            # OG-RAG results
            ograg = translations['ograg']
            result_dict.update({
                'ograg_translation': ograg.translation,
                'ograg_explanation': ograg.explanation or '',
                'ograg_tokens_prompt': ograg.prompt_tokens,
                'ograg_tokens_completion': ograg.completion_tokens,
                'ograg_tokens_total': ograg.total_tokens,
                'ograg_prompt_length': ograg.prompt_length,
                'ograg_retrieved_count': len(ograg.retrieved_proverbs) if ograg.retrieved_proverbs else 0,
                'ograg_retrieved_ids': ','.join([p.proverb_id for p in ograg.retrieved_proverbs]) if ograg.retrieved_proverbs else '',
                'ograg_concepts': ','.join(ograg.concepts_used) if ograg.concepts_used else '',
                'ograg_error': ograg.error or '',
            })
            
            # Calculate total tokens and cost
            total_tokens = raw.total_tokens + trad.total_tokens + ograg.total_tokens
            cost = (total_tokens / 1000) * 0.04  # Rough estimate: $0.04 per 1K tokens
            
            result_dict.update({
                'total_tokens': total_tokens,
                'estimated_cost': cost,
                'timestamp': datetime.now().isoformat(),
            })
            
            self.total_tokens += total_tokens
            self.total_cost += cost
            
            # Log summary
            logger.info(f"✅ Raw:      {raw.translation[:60]}...")
            logger.info(f"✅ Trad RAG: {trad.translation[:60]}...")
            logger.info(f"✅ OG-RAG:   {ograg.translation[:60]}...")
            logger.info(f"📊 Tokens: {total_tokens} | Cost: ${cost:.4f}")
            
        except Exception as e:
            logger.error(f"❌ Error translating {proverb_id}: {e}")
            result_dict['error'] = str(e)
            self.errors.append({
                'proverb_id': proverb_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        return result_dict
    
    def save_to_csv(self, results: List[Dict[str, Any]], suffix: str = "") -> Path:
        """
        Save results to CSV file.
        
        Args:
            results: List of result dictionaries
            suffix: Optional suffix for filename (e.g., "_checkpoint")
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ograg_evaluation_100proverbs{suffix}.csv"
        filepath = self.output_dir / filename
        
        if not results:
            logger.warning("No results to save")
            return filepath
        
        # Write CSV using csv module (faster than pandas)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        logger.info(f"💾 Saved {len(results)} results to: {filepath}")
        return filepath
    
    def save_to_neo4j(self, result: Dict[str, Any]) -> None:
        """
        Update Neo4j with translation results.
        
        Args:
            result: Result dictionary for one proverb
        """
        query = """
        MATCH (p:Proverb {proverb_id: $proverb_id})
        SET p.raw_translation = $raw_translation,
            p.trad_rag_translation = $trad_rag_translation,
            p.ograg_translation = $ograg_translation,
            p.ograg_explanation = $ograg_explanation,
            p.ograg_concepts = $ograg_concepts,
            p.evaluation_timestamp = $timestamp
        RETURN p.proverb_id as proverb_id
        """
        
        params = {
            'proverb_id': result['proverb_id'],
            'raw_translation': result.get('raw_translation', ''),
            'trad_rag_translation': result.get('trad_rag_translation', ''),
            'ograg_translation': result.get('ograg_translation', ''),
            'ograg_explanation': result.get('ograg_explanation', ''),
            'ograg_concepts': result.get('ograg_concepts', ''),
            'timestamp': result.get('timestamp', ''),
        }
        
        try:
            with self.neo4j_driver.session() as session:
                session.run(query, params)
            logger.debug(f"✅ Updated Neo4j for {result['proverb_id']}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to update Neo4j for {result['proverb_id']}: {e}")
    
    def show_progress(self, current: int, total: int, elapsed_time: float) -> None:
        """
        Display progress statistics.
        
        Args:
            current: Current proverb count
            total: Total proverbs
            elapsed_time: Time elapsed in seconds
        """
        percent = (current / total) * 100
        avg_time_per_proverb = elapsed_time / current if current > 0 else 0
        remaining = total - current
        estimated_remaining_time = remaining * avg_time_per_proverb
        
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 PROGRESS: {current}/{total} ({percent:.1f}%)")
        logger.info(f"⏱️  Elapsed: {elapsed_time/60:.1f} minutes")
        logger.info(f"⏱️  Estimated remaining: {estimated_remaining_time/60:.1f} minutes")
        logger.info(f"💰 Total cost so far: ${self.total_cost:.2f}")
        logger.info(f"🎯 Total tokens so far: {self.total_tokens:,}")
        logger.info(f"{'='*70}\n")
    
    def run_evaluation(self, limit: Optional[int] = None) -> Path:
        """
        Run full evaluation on proverbs.
        
        Args:
            limit: Number of proverbs to process (None = all)
            
        Returns:
            Path to final CSV file
        """
        self.start_time = time.time()
        
        # Load proverbs
        proverbs = self.load_proverbs_from_neo4j(limit=limit)
        total = len(proverbs)
        
        if total == 0:
            logger.error("❌ No proverbs found in Neo4j!")
            return None
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🚀 STARTING EVALUATION")
        logger.info(f"{'='*70}")
        logger.info(f"Total proverbs: {total}")
        logger.info(f"Batch size: {self.batch_size}")
        logger.info(f"Save interval: {self.save_interval}")
        logger.info(f"Estimated time: {(total * 0.15):.1f} - {(total * 0.2):.1f} minutes")
        logger.info(f"Estimated cost: ${(total * 0.0333):.2f}")
        logger.info(f"{'='*70}\n")
        
        # Process each proverb
        for i, proverb in enumerate(proverbs, 1):
            result = self.translate_proverb(proverb, i, total)
            self.results.append(result)
            
            # Update Neo4j
            self.save_to_neo4j(result)
            
            # Save checkpoint
            if i % self.save_interval == 0:
                self.save_to_csv(self.results, suffix=f"_checkpoint_{i}")
            
            # Show progress
            if i % self.batch_size == 0 or i == total:
                elapsed = time.time() - self.start_time
                self.show_progress(i, total, elapsed)
        
        # Final save
        logger.info(f"\n{'='*70}")
        logger.info(f"✅ EVALUATION COMPLETE")
        logger.info(f"{'='*70}")
        
        elapsed = time.time() - self.start_time
        logger.info(f"⏱️  Total time: {elapsed/60:.1f} minutes")
        logger.info(f"💰 Total cost: ${self.total_cost:.2f}")
        logger.info(f"🎯 Total tokens: {self.total_tokens:,}")
        logger.info(f"📊 Successful: {len(self.results)}/{total}")
        logger.info(f"❌ Errors: {len(self.errors)}")
        
        # Save final results
        final_path = self.save_to_csv(self.results)
        
        # Save error log if any
        if self.errors:
            error_path = self.output_dir / "errors.json"
            with open(error_path, 'w') as f:
                json.dump(self.errors, f, indent=2)
            logger.warning(f"⚠️ Saved {len(self.errors)} errors to: {error_path}")
        
        logger.info(f"{'='*70}\n")
        
        return final_path
    
    def close(self):
        """Clean up resources."""
        if self.neo4j_driver:
            self.neo4j_driver.close()
        logger.info("✅ Resources cleaned up")


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run OG-RAG evaluation on proverbs')
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of proverbs (default: all)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Batch size for progress updates (default: 10)'
    )
    parser.add_argument(
        '--save-interval',
        type=int,
        default=10,
        help='Save checkpoint every N proverbs (default: 10)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize evaluator
        evaluator = OGRAGEvaluator(
            batch_size=args.batch_size,
            save_interval=args.save_interval
        )
        
        # Run evaluation
        output_file = evaluator.run_evaluation(limit=args.limit)
        
        if output_file:
            print(f"\n{'='*70}")
            print(f"✅ SUCCESS!")
            print(f"{'='*70}")
            print(f"Results saved to: {output_file}")
            print(f"Total cost: ${evaluator.total_cost:.2f}")
            print(f"Total tokens: {evaluator.total_tokens:,}")
            print(f"{'='*70}\n")
        
        # Cleanup
        evaluator.close()
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Evaluation interrupted by user")
        print("\nCheckpoint files saved. You can resume later.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
