#!/usr/bin/env python3
"""
Complete Pipeline for Margaret Ireri's 100 Proverbs Gold Standard

This master script orchestrates the complete pipeline from PDF extraction
to evaluation-ready gold standard dataset creation.

Pipeline Steps:
1. Extract 100 proverbs from Ireri's PDF
2. Validate extraction quality
3. Convert to gold standard evaluation format
4. Generate metadata and documentation
5. Prepare for evaluation framework integration

Author: thiLLMo Research Team
Date: October 2025
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import our custom extractors
from extract_ireri_100_proverbs import IreriProverbExtractor
from convert_ireri_to_gold_standard import IreriGoldStandardConverter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IreriGoldStandardPipeline:
    """Complete pipeline for creating Ireri gold standard dataset."""
    
    def __init__(
        self,
        pdf_path: str = 'data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf',
        raw_output: str = 'data/raw/ireri_100_wealth_prosperity_proverbs.csv',
        gold_standard_output: str = 'data/evaluation/gold_standard_ireri_100.csv',
        metadata_output: str = 'data/evaluation/gold_standard_ireri_100_metadata.json'
    ):
        """
        Initialize pipeline with file paths.
        
        Args:
            pdf_path: Path to Ireri's PDF
            raw_output: Path for raw extracted proverbs
            gold_standard_output: Path for gold standard dataset
            metadata_output: Path for metadata JSON
        """
        self.pdf_path = Path(pdf_path)
        self.raw_output = Path(raw_output)
        self.gold_standard_output = Path(gold_standard_output)
        self.metadata_output = Path(metadata_output)
        
        # Ensure directories exist
        self.raw_output.parent.mkdir(parents=True, exist_ok=True)
        self.gold_standard_output.parent.mkdir(parents=True, exist_ok=True)
        
    def run_complete_pipeline(self, force_reextraction: bool = False) -> bool:
        """
        Run the complete pipeline from PDF to gold standard.
        
        Args:
            force_reextraction: Force re-extraction even if raw CSV exists
            
        Returns:
            True if successful, False otherwise
        """
        logger.info("="*80)
        logger.info("MARGARET IRERI 100 PROVERBS - GOLD STANDARD PIPELINE")
        logger.info("="*80)
        
        try:
            # Step 1: Extract proverbs from PDF
            if force_reextraction or not self.raw_output.exists():
                logger.info("\n📖 STEP 1: Extracting proverbs from PDF...")
                success = self._extract_from_pdf()
                if not success:
                    return False
            else:
                logger.info(f"\n✓ Raw extraction already exists: {self.raw_output}")
                logger.info("  Use --force to re-extract")
            
            # Step 2: Validate extraction
            logger.info("\n🔍 STEP 2: Validating extraction quality...")
            validation_result = self._validate_extraction()
            if not validation_result['valid']:
                logger.error(f"❌ Validation failed: {validation_result['error']}")
                return False
            
            # Step 3: Convert to gold standard
            logger.info("\n⭐ STEP 3: Converting to gold standard format...")
            success = self._convert_to_gold_standard()
            if not success:
                return False
            
            # Step 4: Final validation
            logger.info("\n✅ STEP 4: Final quality checks...")
            final_validation = self._validate_gold_standard()
            if not final_validation['valid']:
                logger.warning(f"⚠️  Gold standard validation warnings: {final_validation['warnings']}")
            
            # Step 5: Generate summary report
            logger.info("\n📊 STEP 5: Generating summary report...")
            self._generate_summary_report()
            
            logger.info("\n" + "="*80)
            logger.info("✅ PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("="*80)
            self._print_next_steps()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}", exc_info=True)
            return False
    
    def _extract_from_pdf(self) -> bool:
        """Extract proverbs from PDF."""
        try:
            extractor = IreriProverbExtractor(str(self.pdf_path))
            proverbs = extractor.extract_all_proverbs()
            extractor.save_to_csv(str(self.raw_output))
            
            logger.info(f"✓ Extracted {len(proverbs)} proverbs")
            return True
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return False
    
    def _validate_extraction(self) -> dict:
        """Validate the extracted proverbs."""
        try:
            df = pd.read_csv(self.raw_output)
            
            # Check basic requirements
            required_columns = [
                'proverb_number', 'kikuyu_proverb', 'english_translation'
            ]
            
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                return {
                    'valid': False,
                    'error': f"Missing required columns: {missing_cols}"
                }
            
            # Check proverb count
            if len(df) < 90:
                return {
                    'valid': False,
                    'error': f"Only {len(df)} proverbs extracted, expected ~100"
                }
            
            # Check for empty Kikuyu texts
            empty_kikuyu = df['kikuyu_proverb'].isna().sum()
            if empty_kikuyu > 10:
                return {
                    'valid': False,
                    'error': f"Too many empty Kikuyu texts: {empty_kikuyu}"
                }
            
            # Check for empty translations
            empty_english = df['english_translation'].isna().sum()
            if empty_english > 20:
                logger.warning(f"⚠️  {empty_english} proverbs missing English translations")
            
            logger.info(f"✓ Validation passed: {len(df)} proverbs")
            logger.info(f"  - Kikuyu texts: {(~df['kikuyu_proverb'].isna()).sum()}")
            logger.info(f"  - English translations: {(~df['english_translation'].isna()).sum()}")
            logger.info(f"  - Cultural interpretations: {(~df['cultural_interpretation'].isna()).sum()}")
            
            return {'valid': True}
            
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _convert_to_gold_standard(self) -> bool:
        """Convert to gold standard format."""
        try:
            converter = IreriGoldStandardConverter()
            gold_df = converter.prepare_ireri_gold_standard(
                ireri_csv_path=str(self.raw_output),
                output_path=str(self.gold_standard_output),
                metadata_path=str(self.metadata_output)
            )
            
            logger.info(f"✓ Created gold standard with {len(gold_df)} entries")
            return True
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return False
    
    def _validate_gold_standard(self) -> dict:
        """Validate the gold standard dataset."""
        try:
            df = pd.read_csv(self.gold_standard_output)
            
            warnings = []
            
            # Check completeness
            completeness = {
                'kikuyu_text': (~df['kikuyu_text'].isna()).sum() / len(df) * 100,
                'expert_translation': (~df['expert_translation'].isna()).sum() / len(df) * 100,
                'expert_cultural_meaning': (~df['expert_cultural_meaning'].isna()).sum() / len(df) * 100,
                'expert_business_relevance': (~df['expert_business_relevance'].isna()).sum() / len(df) * 100
            }
            
            for field, percentage in completeness.items():
                logger.info(f"  - {field}: {percentage:.1f}% complete")
                if percentage < 80:
                    warnings.append(f"{field} only {percentage:.1f}% complete")
            
            # Check cultural authenticity scores
            if 'cultural_authenticity' in df.columns:
                avg_auth = df['cultural_authenticity'].mean()
                logger.info(f"  - Average cultural authenticity: {avg_auth:.1f}/5.0")
            
            return {
                'valid': True,
                'warnings': warnings,
                'completeness': completeness
            }
            
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _generate_summary_report(self) -> None:
        """Generate a summary report of the pipeline execution."""
        report_path = self.gold_standard_output.parent / 'ireri_gold_standard_report.md'
        
        # Load datasets
        raw_df = pd.read_csv(self.raw_output)
        gold_df = pd.read_csv(self.gold_standard_output)
        
        report = f"""# Margaret Ireri 100 Proverbs - Gold Standard Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Source Information

- **Author**: Margaret Wambere Ireri
- **Title**: A Collection of 100 Proverbs and Wise Sayings of the Gikuyu (Kenya) About Money and Wealth
- **Publication**: August 2014, Nairobi, Kenya
- **Organization**: African Proverbs Working Group

## Extraction Summary

### Raw Extraction
- **Total proverbs extracted**: {len(raw_df)}
- **PDF source**: {self.pdf_path.name}
- **Output file**: {self.raw_output.name}

### Content Completeness
- Kikuyu texts: {(~raw_df['kikuyu_proverb'].isna()).sum()} ({(~raw_df['kikuyu_proverb'].isna()).sum()/len(raw_df)*100:.1f}%)
- English translations: {(~raw_df['english_translation'].isna()).sum()} ({(~raw_df['english_translation'].isna()).sum()/len(raw_df)*100:.1f}%)
- Kiswahili translations: {(~raw_df['kiswahili_translation'].isna()).sum()} ({(~raw_df['kiswahili_translation'].isna()).sum()/len(raw_df)*100:.1f}%)
- Cultural interpretations: {(~raw_df['cultural_interpretation'].isna()).sum()} ({(~raw_df['cultural_interpretation'].isna()).sum()/len(raw_df)*100:.1f}%)
- Teaching messages: {(~raw_df['teaching_message'].isna()).sum()} ({(~raw_df['teaching_message'].isna()).sum()/len(raw_df)*100:.1f}%)
- Biblical parallels: {(~raw_df['biblical_parallel'].isna()).sum()} ({(~raw_df['biblical_parallel'].isna()).sum()/len(raw_df)*100:.1f}%)

## Gold Standard Dataset

### Statistics
- **Total entries**: {len(gold_df)}
- **Proverb ID range**: {gold_df['proverb_id'].min()} to {gold_df['proverb_id'].max()}
- **Cultural authenticity score**: {gold_df['cultural_authenticity'].mean():.1f}/5.0
- **Validation status**: Expert validated by Margaret Wambere Ireri

### Quality Metrics
- Expert translations: {(~gold_df['expert_translation'].isna()).sum()} ({(~gold_df['expert_translation'].isna()).sum()/len(gold_df)*100:.1f}%)
- Cultural meanings: {(~gold_df['expert_cultural_meaning'].isna()).sum()} ({(~gold_df['expert_cultural_meaning'].isna()).sum()/len(gold_df)*100:.1f}%)
- Business relevance: {(~gold_df['expert_business_relevance'].isna()).sum()} ({(~gold_df['expert_business_relevance'].isna()).sum()/len(gold_df)*100:.1f}%)

### Thematic Distribution
{gold_df['thematic_category'].value_counts().to_markdown()}

## Files Generated

1. **Raw Extraction**: `{self.raw_output}`
   - Complete extraction with all PDF fields preserved
   - Suitable for reference and validation

2. **Gold Standard**: `{self.gold_standard_output}`
   - Evaluation-ready format
   - Standardized fields for comparative analysis
   - Expert-validated translations and cultural meanings

3. **Metadata**: `{self.metadata_output}`
   - Dataset documentation
   - Quality assurance information
   - Usage guidelines

## Usage Instructions

### For Evaluation Framework

```python
# Load gold standard
import pandas as pd
gold_standard = pd.read_csv('{self.gold_standard_output}')

# Use for translation evaluation
for _, proverb in gold_standard.iterrows():
    kikuyu_text = proverb['kikuyu_text']
    expert_translation = proverb['expert_translation']
    
    # Generate your translation
    your_translation = your_translation_system(kikuyu_text)
    
    # Compare against expert translation
    quality_score = evaluate_translation(
        your_translation,
        expert_translation,
        cultural_context=proverb['expert_cultural_meaning']
    )
```

### For OG-RAG vs Raw LLM Comparison

This gold standard enables:
- Baseline comparison against expert translations
- Cultural faithfulness assessment
- Business relevance evaluation
- Translation accuracy measurement

## Next Steps

1. ✅ Review gold standard for quality
2. ⏩ Generate OG-RAG translations
3. ⏩ Generate Raw LLM translations
4. ⏩ Run comparative evaluation
5. ⏩ Analyze cultural preservation effectiveness

---

*Generated by thiLLMo Gold Standard Pipeline*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"✓ Summary report saved to: {report_path}")
    
    def _print_next_steps(self) -> None:
        """Print next steps for the user."""
        print("\n📋 NEXT STEPS:")
        print(f"\n1. Review the extracted data:")
        print(f"   Raw extraction: {self.raw_output}")
        print(f"   Gold standard:  {self.gold_standard_output}")
        print(f"   Metadata:       {self.metadata_output}")
        
        print(f"\n2. Integrate with evaluation framework:")
        print(f"   - Use gold_standard_ireri_100.csv as baseline")
        print(f"   - Generate OG-RAG translations")
        print(f"   - Generate Raw LLM translations")
        print(f"   - Run comparative analysis")
        
        print(f"\n3. Example usage in Python:")
        print(f"""
   import pandas as pd
   
   # Load gold standard
   gold = pd.read_csv('{self.gold_standard_output}')
   
   # Get a proverb for translation
   proverb = gold.iloc[0]
   print(f"Kikuyu: {{proverb['kikuyu_text']}}")
   print(f"Expert: {{proverb['expert_translation']}}")
""")


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Complete pipeline for Ireri 100 proverbs gold standard creation"
    )
    parser.add_argument(
        '--pdf',
        default='data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf',
        help='Path to Ireri PDF'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-extraction even if raw CSV exists'
    )
    
    args = parser.parse_args()
    
    # Initialize and run pipeline
    pipeline = IreriGoldStandardPipeline(pdf_path=args.pdf)
    success = pipeline.run_complete_pipeline(force_reextraction=args.force)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
