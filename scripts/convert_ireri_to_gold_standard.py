#!/usr/bin/env python3
"""
Convert Margaret Ireri's 100 Proverbs to Gold Standard Evaluation Format

This script converts the extracted Ireri proverb collection into a standardized
evaluation-ready dataset for assessing AI translation quality and cultural faithfulness.

The gold standard format is optimized for:
- Expert validation and benchmarking
- OG-RAG vs Raw LLM comparison
- Cultural faithfulness assessment
- Translation quality evaluation

Author: thiLLMo Research Team
Date: October 2025
"""

import logging
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IreriGoldStandardConverter:
    """Convert Ireri's proverbs to standardized evaluation format."""
    
    def __init__(self):
        """Initialize converter with format specifications."""
        self.gold_standard_columns = [
            'proverb_id',
            'kikuyu_text',
            'expert_translation',
            'expert_cultural_meaning',
            'expert_business_relevance',
            'expert_teaching',
            'biblical_context',
            'thematic_category',
            'cultural_authenticity',
            'source',
            'source_reference',
            'original_proverb_number',
            'page_number',
            'extraction_date',
            'validation_status',
            'expert_notes'
        ]
        
    def prepare_ireri_gold_standard(
        self, 
        ireri_csv_path: str,
        output_path: str = 'data/evaluation/gold_standard_ireri_100.csv',
        metadata_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Convert Ireri's 100 proverbs to standardized evaluation format.
        
        Args:
            ireri_csv_path: Path to the extracted Ireri proverbs CSV
            output_path: Path to save the gold standard CSV
            metadata_path: Optional path to save metadata JSON
            
        Returns:
            DataFrame with standardized gold standard format
        """
        logger.info(f"Loading Ireri's proverbs from: {ireri_csv_path}")
        
        # Load Ireri's collection
        ireri_df = pd.read_csv(ireri_csv_path)
        logger.info(f"Loaded {len(ireri_df)} proverbs")
        
        # Convert to gold standard format
        gold_standard = []
        
        for idx, row in ireri_df.iterrows():
            # Determine thematic category based on content analysis
            theme = self._determine_theme(row)
            
            proverb_entry = {
                'proverb_id': f"MP_{row['proverb_number']:03d}",  # Margaret Proverb 001-100
                'kikuyu_text': row['kikuyu_proverb'],
                'expert_translation': row['english_translation'],
                'expert_cultural_meaning': row['cultural_interpretation'],
                'expert_business_relevance': self._extract_business_context(row),
                'expert_teaching': row['teaching_message'],
                'biblical_context': row['biblical_parallel'],
                'thematic_category': theme,
                'cultural_authenticity': 5.0,  # Ireri's expert validation = max score
                'source': 'Margaret_Wambere_Ireri_2014',
                'source_reference': row['references'],
                'original_proverb_number': row['proverb_number'],
                'page_number': row['page_number'],
                'extraction_date': datetime.now().strftime('%Y-%m-%d'),
                'validation_status': 'expert_validated',
                'expert_notes': f"Category: {row['category']} (W=Wealth, M=Money, WM=Both)"
            }
            gold_standard.append(proverb_entry)
        
        # Create DataFrame
        gold_df = pd.DataFrame(gold_standard)
        
        # Ensure all required columns exist
        for col in self.gold_standard_columns:
            if col not in gold_df.columns:
                gold_df[col] = ''
        
        # Reorder columns
        gold_df = gold_df[self.gold_standard_columns]
        
        # Save to CSV
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gold_df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"✅ Saved gold standard to: {output_path}")
        
        # Save metadata if requested
        if metadata_path:
            self._save_metadata(gold_df, ireri_df, metadata_path)
        
        # Print summary
        self._print_summary(gold_df)
        
        return gold_df
    
    def _determine_theme(self, row: pd.Series) -> str:
        """
        Determine thematic category based on proverb content.
        
        Args:
            row: DataFrame row with proverb data
            
        Returns:
            Theme category string
        """
        # Analyze the proverb content for theme classification
        text = f"{row['kikuyu_proverb']} {row['english_translation']} {row['cultural_interpretation']}".lower()
        
        # Define theme keywords
        themes = {
            'wealth_acquisition': ['rich', 'wealth', 'money', 'acquire', 'gain', 'prosperity'],
            'wealth_management': ['save', 'manage', 'keep', 'guard', 'protect', 'maintain'],
            'poverty_hardship': ['poor', 'poverty', 'lack', 'need', 'hardship', 'struggle'],
            'business_wisdom': ['business', 'trade', 'buy', 'sell', 'market', 'exchange'],
            'work_diligence': ['work', 'labor', 'diligent', 'effort', 'toil', 'industry'],
            'generosity_sharing': ['share', 'give', 'generous', 'help', 'assist', 'charity'],
            'patience_wisdom': ['patience', 'wait', 'time', 'wise', 'wisdom', 'prudent'],
            'community_relations': ['family', 'community', 'people', 'together', 'cooperation']
        }
        
        # Count matches for each theme
        theme_scores = {}
        for theme, keywords in themes.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                theme_scores[theme] = score
        
        # Return theme with highest score, or default
        if theme_scores:
            return max(theme_scores.items(), key=lambda x: x[1])[0]
        
        # Fallback based on category
        category = row.get('category', 'W')
        if category == 'M':
            return 'wealth_acquisition'
        elif category == 'W':
            return 'business_wisdom'
        else:
            return 'wealth_management'
    
    def _extract_business_context(self, row: pd.Series) -> str:
        """
        Extract or generate business relevance context.
        
        Args:
            row: DataFrame row with proverb data
            
        Returns:
            Business relevance description
        """
        # Combine wealth context with teaching for business relevance
        parts = []
        
        if pd.notna(row['wealth_prosperity_context']) and row['wealth_prosperity_context']:
            parts.append(row['wealth_prosperity_context'])
        
        # Add category context
        category = row.get('category', 'W')
        if category == 'M':
            parts.append("Focus: Money management and financial wisdom")
        elif category == 'W':
            parts.append("Focus: Wealth creation and prosperity principles")
        elif category == 'WM':
            parts.append("Focus: Integrated wealth and money management")
        
        return " | ".join(parts) if parts else "Business wisdom from Kikuyu tradition"
    
    def _save_metadata(
        self, 
        gold_df: pd.DataFrame, 
        source_df: pd.DataFrame,
        metadata_path: str
    ) -> None:
        """
        Save metadata about the gold standard dataset.
        
        Args:
            gold_df: Gold standard DataFrame
            source_df: Source Ireri DataFrame
            metadata_path: Path to save metadata JSON
        """
        metadata = {
            'dataset_name': 'Margaret Ireri 100 Kikuyu Proverbs - Gold Standard',
            'version': '1.0',
            'creation_date': datetime.now().isoformat(),
            'source': {
                'author': 'Margaret Wambere Ireri',
                'title': 'A Collection of 100 Proverbs and Wise Sayings of the Gikuyu (Kenya) About Money and Wealth',
                'publication_date': 'August 2014',
                'location': 'Nairobi, Kenya',
                'organization': 'African Proverbs Working Group'
            },
            'statistics': {
                'total_proverbs': int(len(gold_df)),
                'proverbs_with_english': int(gold_df['expert_translation'].notna().sum()),
                'proverbs_with_cultural_meaning': int(gold_df['expert_cultural_meaning'].notna().sum()),
                'proverbs_with_business_context': int(gold_df['expert_business_relevance'].notna().sum()),
                'proverbs_with_biblical_context': int(gold_df['biblical_context'].notna().sum()),
                'theme_distribution': {k: int(v) for k, v in gold_df['thematic_category'].value_counts().to_dict().items()},
                'average_cultural_authenticity': float(gold_df['cultural_authenticity'].mean())
            },
            'quality_assurance': {
                'expert_validated': True,
                'native_speaker_authored': True,
                'cultural_authenticity_score': 5.0,
                'validation_method': 'Expert curation by Margaret Wambere Ireri'
            },
            'usage': {
                'intended_use': 'Gold standard for AI translation evaluation',
                'evaluation_dimensions': [
                    'Cultural faithfulness',
                    'Translation accuracy',
                    'Business relevance',
                    'Overall fluency'
                ],
                'comparison_baseline': 'Expert human translation'
            }
        }
        
        metadata_path = Path(metadata_path)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved metadata to: {metadata_path}")
    
    def _print_summary(self, df: pd.DataFrame) -> None:
        """Print summary of gold standard dataset."""
        print("\n" + "="*80)
        print("IRERI GOLD STANDARD - CONVERSION SUMMARY")
        print("="*80)
        print(f"Total gold standard entries: {len(df)}")
        print(f"Proverb ID range: {df['proverb_id'].min()} to {df['proverb_id'].max()}")
        print(f"\nQuality Metrics:")
        print(f"  - Expert translations: {df['expert_translation'].notna().sum()}")
        print(f"  - Cultural meanings: {df['expert_cultural_meaning'].notna().sum()}")
        print(f"  - Business relevance: {df['expert_business_relevance'].notna().sum()}")
        print(f"  - Teaching messages: {df['expert_teaching'].notna().sum()}")
        print(f"  - Biblical contexts: {df['biblical_context'].notna().sum()}")
        print(f"\nCultural Authenticity: {df['cultural_authenticity'].mean():.1f}/5.0")
        print(f"\nThematic Distribution:")
        theme_counts = df['thematic_category'].value_counts()
        for theme, count in theme_counts.items():
            print(f"  - {theme}: {count}")
        print("="*80)


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Ireri's 100 proverbs to gold standard evaluation format"
    )
    parser.add_argument(
        '--input',
        default='data/raw/ireri_100_wealth_prosperity_proverbs.csv',
        help='Path to extracted Ireri proverbs CSV'
    )
    parser.add_argument(
        '--output',
        default='data/evaluation/gold_standard_ireri_100.csv',
        help='Output gold standard CSV file path'
    )
    parser.add_argument(
        '--metadata',
        default='data/evaluation/gold_standard_ireri_100_metadata.json',
        help='Output metadata JSON file path'
    )
    
    args = parser.parse_args()
    
    try:
        # Check if input exists
        input_path = Path(args.input)
        if not input_path.exists():
            logger.error(f"❌ Input file not found: {args.input}")
            logger.info("Run extract_ireri_100_proverbs.py first to extract the proverbs.")
            return 1
        
        # Initialize converter
        converter = IreriGoldStandardConverter()
        
        # Prepare gold standard
        logger.info("Starting conversion to gold standard format...")
        gold_df = converter.prepare_ireri_gold_standard(
            ireri_csv_path=args.input,
            output_path=args.output,
            metadata_path=args.metadata
        )
        
        print(f"\n✅ SUCCESS! Created gold standard with {len(gold_df)} entries")
        print(f"📁 Gold standard saved to: {args.output}")
        print(f"📋 Metadata saved to: {args.metadata}")
        print("\nNext steps:")
        print("1. Review the gold standard for completeness")
        print("2. Use this dataset for OG-RAG vs Raw LLM evaluation")
        print("3. Generate translations using your translation systems")
        print("4. Run comparative evaluation against this gold standard")
        
    except Exception as e:
        logger.error(f"❌ Conversion failed: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
