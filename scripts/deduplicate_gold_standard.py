#!/usr/bin/env python3
"""
Script to deduplicate gold_standard_ireri.csv by merging duplicate proverb_id entries.
Each proverb_id has 2 rows - one with basic info, one with detailed cultural meaning.
We merge them into a single row per proverb.
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def deduplicate_gold_standard(input_file: str, output_file: str = None):
    """
    Deduplicate gold standard by merging rows with same proverb_id.
    Strategy: For each proverb_id, keep the row with the most complete information.
    """
    # Load source
    df = pd.read_csv(input_file)
    
    logger.info("="*80)
    logger.info("🔍 GOLD STANDARD DEDUPLICATION")
    logger.info("="*80)
    logger.info(f"📥 Input: {input_file}")
    logger.info(f"📊 Total rows: {len(df)}")
    logger.info(f"🎯 Unique proverb_ids: {df['proverb_id'].nunique()}")
    logger.info("")
    
    # Group by proverb_id and merge
    deduplicated_rows = []
    
    for proverb_id, group in df.groupby('proverb_id'):
        if len(group) == 1:
            # No duplicates, keep as is
            deduplicated_rows.append(group.iloc[0].to_dict())
        else:
            # Merge duplicates: prefer non-null values
            merged_row = {}
            for col in group.columns:
                # Get all non-null values for this column
                non_null_values = group[col].dropna().unique()
                
                if len(non_null_values) == 0:
                    merged_row[col] = None
                elif len(non_null_values) == 1:
                    merged_row[col] = non_null_values[0]
                else:
                    # Multiple non-null values - prefer the most complete one
                    # (longest string for text fields)
                    if group[col].dtype == 'object':
                        merged_row[col] = max(non_null_values, key=lambda x: len(str(x)) if pd.notna(x) else 0)
                    else:
                        # For numeric, take the first non-null
                        merged_row[col] = non_null_values[0]
            
            deduplicated_rows.append(merged_row)
    
    # Create deduplicated DataFrame
    df_dedup = pd.DataFrame(deduplicated_rows)
    
    # Sort by proverb_id for consistency
    df_dedup = df_dedup.sort_values('proverb_id').reset_index(drop=True)
    
    logger.info("✅ DEDUPLICATION COMPLETE")
    logger.info(f"📉 Rows reduced: {len(df)} → {len(df_dedup)}")
    logger.info(f"🎯 Unique proverbs: {df_dedup['proverb_id'].nunique()}")
    logger.info("")
    
    # Save deduplicated version
    if output_file is None:
        output_file = input_file.replace('.csv', '_deduplicated.csv')
    
    df_dedup.to_csv(output_file, index=False)
    logger.info(f"💾 Saved to: {output_file}")
    logger.info("="*80)
    
    return output_file, len(df_dedup)


if __name__ == "__main__":
    input_file = "data/evaluation/gold_standard_ireri.csv"
    output_file = "data/evaluation/gold_standard_ireri_deduplicated.csv"
    
    deduplicate_gold_standard(input_file, output_file)
