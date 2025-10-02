#!/usr/bin/env python3
"""
Convert Expert Proverb Collections to Gold Standard Format

Generic framework for converting expert-curated proverb collections into 
standardized evaluation-ready datasets. Supports multiple expert sources 
and languages through configuration.

Default source: Margaret Wambere Ireri's Kikuyu proverbs (2014)

Author: thiLLMo Research Team
Date: October 2025
"""

import logging
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import configuration system
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_source_config, get_output_path, list_available_sources

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GoldStandardConverter:
    """Convert expert proverb collections to standardized evaluation format."""
    
    def __init__(self, source_name: str = 'ireri'):
        """
        Initialize converter with source configuration.
        
        Args:
            source_name: Expert source identifier (default: 'ireri')
        """
        self.source_name = source_name
        self.source_config = get_source_config(source_name)
        
        self.gold_standard_columns = [
            'proverb_id', 'kikuyu_text', 'expert_translation',
            'expert_cultural_meaning', 'expert_business_relevance',
            'expert_teaching', 'biblical_context', 'thematic_category',
            'cultural_authenticity', 'source', 'source_reference',
            'original_proverb_number', 'page_number', 'extraction_date',
            'validation_status', 'expert_notes'
        ]
        
    def prepare_gold_standard(
        self, 
        source_csv_path: str,
        output_path: Optional[str] = None,
        metadata_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Convert expert proverbs to standardized evaluation format.
        
        Args:
            source_csv_path: Path to the extracted proverbs CSV
            output_path: Path to save gold standard CSV (auto-generated if None)
            metadata_path: Path to save metadata JSON (auto-generated if None)
            
        Returns:
            DataFrame with standardized gold standard format
        """
        logger.info(f"Loading proverbs from: {source_csv_path}")
        logger.info(f"Source: {self.source_config.get('author')} ({self.source_name})")
        
        # Load source collection
        source_df = pd.read_csv(source_csv_path)
        logger.info(f"Loaded {len(source_df)} proverbs")
        
        # Convert to gold standard format
        gold_standard = []
        
        for idx, row in source_df.iterrows():
            theme = self._determine_theme(row)
            
            # Generate proverb ID based on source
            author_initials = ''.join([w[0].upper() for w in self.source_config['author'].split()[:2]])
            proverb_id = f"{author_initials}_{row['proverb_number']:03d}"
            
            # Get source citation
            author = self.source_config['author']
            year = self.source_config['year']
            source_str = f"{author.replace(' ', '_')}_{year}"
            
            proverb_entry = {
                'proverb_id': proverb_id,
                'kikuyu_text': row['kikuyu_proverb'],
                'expert_translation': row['english_translation'],
                'expert_cultural_meaning': row['cultural_interpretation'],
                'expert_business_relevance': self._extract_business_context(row),
                'expert_teaching': row['teaching_message'],
                'biblical_context': row.get('biblical_parallel', ''),
                'thematic_category': theme,
                'cultural_authenticity': self.source_config['quality'].get('expected_authenticity', 5.0),
                'source': source_str,
                'source_reference': row.get('references', ''),
                'original_proverb_number': row['proverb_number'],
                'page_number': row['page_number'],
                'extraction_date': datetime.now().strftime('%Y-%m-%d'),
                'validation_status': 'expert_validated',
                'expert_notes': f"Category: {row.get('category', 'W')}"
            }
            gold_standard.append(proverb_entry)
        
        # Create DataFrame
        gold_df = pd.DataFrame(gold_standard)
        
        # Ensure all columns exist
        for col in self.gold_standard_columns:
            if col not in gold_df.columns:
                gold_df[col] = ''
        
        gold_df = gold_df[self.gold_standard_columns]
        
        # Auto-generate paths if not provided
        if output_path is None:
            output_path = str(get_output_path(self.source_name, 'gold_standard_csv'))
        if metadata_path is None:
            metadata_path = str(get_output_path(self.source_name, 'metadata_json'))
        
        # Save files
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gold_df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"✅ Saved gold standard to: {output_path}")
        
        # Save metadata
        self._save_metadata(gold_df, source_df, metadata_path)
        
        # Print summary
        self._print_summary(gold_df)
        
        return gold_df
    
    def _determine_theme(self, row: pd.Series) -> str:
        """Determine thematic category based on proverb content."""
        text = f"{row['kikuyu_proverb']} {row['english_translation']} {row.get('cultural_interpretation', '')}".lower()
        
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
        
        theme_scores = {}
        for theme, keywords in themes.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                theme_scores[theme] = score
        
        if theme_scores:
            return max(theme_scores.items(), key=lambda x: x[1])[0]
        
        category = row.get('category', 'W')
        return 'wealth_acquisition' if category == 'M' else 'business_wisdom'
    
    def _extract_business_context(self, row: pd.Series) -> str:
        """Extract or generate business relevance context."""
        parts = []
        
        if pd.notna(row.get('wealth_prosperity_context')) and row['wealth_prosperity_context']:
            parts.append(row['wealth_prosperity_context'])
        
        category = row.get('category', 'W')
        if category == 'M':
            parts.append("Focus: Money management and financial wisdom")
        elif category == 'W':
            parts.append("Focus: Wealth creation and prosperity principles")
        elif category == 'WM':
            parts.append("Focus: Integrated wealth and money management")
        
        return " | ".join(parts) if parts else "Business wisdom from tradition"
    
    def _save_metadata(
        self, 
        gold_df: pd.DataFrame, 
        source_df: pd.DataFrame,
        metadata_path: str
    ) -> None:
        """Save metadata about the gold standard dataset."""
        metadata = {
            'dataset_name': f"{self.source_config['author']} {self.source_config['language'].title()} Proverbs - Gold Standard",
            'version': '2.0',
            'creation_date': datetime.now().isoformat(),
            'source': {
                'author': self.source_config['author'],
                'title': self.source_config['title'],
                'year': self.source_config['year'],
                'language': self.source_config['language'],
                'language_code': self.source_config['language_code'],
                'domain': self.source_config['domain']
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
                'cultural_authenticity_score': self.source_config['quality']['expected_authenticity'],
                'validation_method': f"Expert curation by {self.source_config['author']}"
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
            },
            'citation': self.source_config.get('citation', {})
        }
        
        metadata_path = Path(metadata_path)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved metadata to: {metadata_path}")
    
    def _print_summary(self, df: pd.DataFrame) -> None:
        """Print summary of gold standard dataset."""
        author = self.source_config['author']
        
        print("\n" + "="*80)
        print(f"GOLD STANDARD CONVERSION SUMMARY - {self.source_name.upper()}")
        print("="*80)
        print(f"Author: {author}")
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
        for theme, count in df['thematic_category'].value_counts().items():
            print(f"  - {theme}: {count}")
        print("="*80)


def main():
    """Main execution function."""
    import argparse
    
    available_sources = list_available_sources()
    
    parser = argparse.ArgumentParser(
        description="Convert expert proverb collections to gold standard format"
    )
    parser.add_argument(
        '--input',
        help='Path to extracted proverbs CSV (auto-detected if not specified)'
    )
    parser.add_argument(
        '--source',
        default='ireri',
        choices=available_sources,
        help=f'Expert source identifier (available: {", ".join(available_sources)})'
    )
    parser.add_argument(
        '--output',
        help='Output gold standard CSV file path (auto-generated if not specified)'
    )
    parser.add_argument(
        '--metadata',
        help='Output metadata JSON file path (auto-generated if not specified)'
    )
    
    args = parser.parse_args()
    
    try:
        # Auto-detect input if not specified
        if not args.input:
            args.input = str(get_output_path(args.source, 'raw_csv'))
        
        # Check if input exists
        input_path = Path(args.input)
        if not input_path.exists():
            logger.error(f"❌ Input file not found: {args.input}")
            logger.info(f"Run extract_expert_proverbs.py --source {args.source} first to extract the proverbs.")
            return 1
        
        # Initialize converter
        converter = GoldStandardConverter(source_name=args.source)
        
        # Prepare gold standard
        source_config = get_source_config(args.source)
        logger.info(f"Starting conversion: {source_config['author']}")
        gold_df = converter.prepare_gold_standard(
            source_csv_path=args.input,
            output_path=args.output,
            metadata_path=args.metadata
        )
        
        print(f"\n✅ SUCCESS! Created gold standard with {len(gold_df)} entries")
        print(f"📁 Gold standard saved to: {args.output or get_output_path(args.source, 'gold_standard_csv')}")
        print(f"📋 Metadata saved to: {args.metadata or get_output_path(args.source, 'metadata_json')}")
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
