#!/usr/bin/env python3
"""
Prepare LLM-as-a-Judge Evaluation Input from Cultural Evaluation Results

Creates a properly formatted input file for the LLM-as-a-Judge comparative evaluation
using the 100 proverbs we've already translated with all three systems.
"""

import pandas as pd
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def prepare_llm_evaluation_input():
    """Prepare input data for LLM-as-a-Judge evaluation."""
    
    # Read cultural evaluation results
    cultural_results_file = "data/results/cultural_evaluation_100proverbs.csv"
    logger.info(f"Reading cultural evaluation results from {cultural_results_file}")
    
    df = pd.read_csv(cultural_results_file)
    logger.info(f"Loaded {len(df)} evaluation records")
    
    # Pivot to get one row per proverb with all three system translations
    logger.info("Reshaping data to proverb-centric format...")
    
    # Get unique proverbs
    proverb_ids = df['proverb_id'].unique()
    logger.info(f"Found {len(proverb_ids)} unique proverbs")
    
    # Create list to store formatted records
    llm_input_records = []
    
    for proverb_id in proverb_ids:
        proverb_data = df[df['proverb_id'] == proverb_id]
        
        # Get the Kikuyu text (same across all systems)
        kikuyu_text = proverb_data.iloc[0]['kikuyu_text']
        
        # Get expert translation if available
        expert_translation = proverb_data.iloc[0].get('expert_translation', '')
        
        # Get translations from each system
        og_rag_row = proverb_data[proverb_data['system'] == 'OG-RAG']
        traditional_rag_row = proverb_data[proverb_data['system'] == 'Traditional RAG']
        raw_gpt4_row = proverb_data[proverb_data['system'] == 'Raw GPT-4']
        
        og_rag_translation = og_rag_row.iloc[0]['translation'] if len(og_rag_row) > 0 else ''
        traditional_rag_translation = traditional_rag_row.iloc[0]['translation'] if len(traditional_rag_row) > 0 else ''
        raw_gpt4_translation = raw_gpt4_row.iloc[0]['translation'] if len(raw_gpt4_row) > 0 else ''
        
        # Create record for LLM evaluation
        llm_input_records.append({
            'proverb_id': proverb_id,
            'kikuyu_proverb': kikuyu_text,
            'og_rag_translation': og_rag_translation,
            'traditional_rag_translation': traditional_rag_translation,
            'raw_llm_translation': raw_gpt4_translation,  # Using Raw GPT-4 as "Raw LLM"
            'expert_translation': expert_translation,
            'cultural_context': '[Kikuyu proverb on wealth, entrepreneurship, and traditional wisdom]',
            'business_scenario': '[Business and entrepreneurship application]',
            'complexity_level': 'medium'
        })
    
    # Create DataFrame
    llm_input_df = pd.DataFrame(llm_input_records)
    
    # Save to CSV
    output_file = "data/evaluation/llm_judge_input_100proverbs.csv"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    llm_input_df.to_csv(output_file, index=False)
    
    logger.info(f"✅ Created LLM evaluation input file: {output_file}")
    logger.info(f"   Total proverbs: {len(llm_input_df)}")
    logger.info(f"   Systems: OG-RAG, Traditional RAG, Raw GPT-4")
    
    # Show sample
    logger.info("\nSample record:")
    print(llm_input_df.iloc[0].to_dict())
    
    return output_file

if __name__ == "__main__":
    output_file = prepare_llm_evaluation_input()
    print(f"\n✅ LLM evaluation input ready: {output_file}")
    print("\nNext step:")
    print("  python scripts/run_llm_evaluation.py --mode comparative \\")
    print(f"    --benchmark-file {output_file} \\")
    print("    --enable-ensemble")
