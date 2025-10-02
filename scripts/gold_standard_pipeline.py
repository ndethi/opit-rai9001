#!/usr/bin/env python3
"""
Complete Pipeline for Expert Proverb Gold Standard Creation

Generic framework orchestrating the complete pipeline from PDF extraction
to evaluation-ready gold standard dataset creation.

Pipeline Steps:
1. Extract proverbs from expert PDF collection
2. Validate extraction quality
3. Convert to gold standard evaluation format
4. Generate metadata and documentation
5. Prepare for evaluation framework integration

Default source: Margaret Wambere Ireri's Kikuyu proverbs (2014)

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

# Import configuration and modules
from config import get_source_config, get_output_path, list_available_sources
from extract_expert_proverbs import ExpertProverbExtractor
from convert_to_gold_standard import GoldStandardConverter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GoldStandardPipeline:
    """Complete pipeline for creating gold standard datasets."""
    
    def __init__(
        self,
        pdf_path: str,
        source_name: str = 'ireri',
        force_reextract: bool = False
    ):
        """
        Initialize pipeline with configuration.
        
        Args:
            pdf_path: Path to expert proverb collection PDF
            source_name: Expert source identifier (default: 'ireri')
            force_reextract: Force re-extraction even if files exist
        """
        self.pdf_path = Path(pdf_path)
        self.source_name = source_name
        self.source_config = get_source_config(source_name)
        self.force_reextract = force_reextract
        
        # Get output paths from configuration
        self.raw_output = get_output_path(source_name, 'raw_csv')
        self.gold_standard_output = get_output_path(source_name, 'gold_standard_csv')
        self.metadata_output = get_output_path(source_name, 'metadata_json')
        self.report_output = get_output_path(source_name, 'report_md')
        
        # Initialize components
        self.extractor = ExpertProverbExtractor(str(self.pdf_path), source_name=source_name)
        self.converter = GoldStandardConverter(source_name=source_name)
        
        # Pipeline state
        self.pipeline_start_time = None
        self.extraction_time = None
        self.conversion_time = None
        self.raw_proverbs_count = 0
        self.gold_standard_count = 0
    
    def run(self) -> bool:
        """
        Execute the complete pipeline.
        
        Returns:
            True if pipeline completed successfully, False otherwise
        """
        self.pipeline_start_time = datetime.now()
        author = self.source_config.get('author', 'Unknown')
        
        logger.info("="*80)
        logger.info(f"EXPERT PROVERB GOLD STANDARD PIPELINE - {self.source_name.upper()}")
        logger.info("="*80)
        logger.info(f"Source: {author}")
        logger.info(f"PDF: {self.pdf_path}")
        logger.info(f"Started: {self.pipeline_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*80)
        
        try:
            # Stage 1: Extract proverbs from PDF
            if not self._stage_1_extract():
                return False
            
            # Stage 2: Validate extraction
            if not self._stage_2_validate():
                return False
            
            # Stage 3: Convert to gold standard
            if not self._stage_3_convert():
                return False
            
            # Stage 4: Final quality checks
            if not self._stage_4_quality_check():
                return False
            
            # Stage 5: Generate summary report
            self._stage_5_generate_report()
            
            # Pipeline complete
            elapsed_time = (datetime.now() - self.pipeline_start_time).total_seconds()
            logger.info("="*80)
            logger.info(f"✅ PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"Total time: {elapsed_time:.1f}s")
            logger.info("="*80)
            
            self._print_final_summary()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}", exc_info=True)
            return False
    
    def _stage_1_extract(self) -> bool:
        """Stage 1: Extract proverbs from PDF."""
        logger.info("\n[STAGE 1/5] Extracting proverbs from PDF...")
        
        if self.raw_output.exists() and not self.force_reextract:
            logger.info(f"Raw extraction already exists: {self.raw_output}")
            logger.info("Skipping extraction (use --force to re-extract)")
            
            # Load existing data
            df = pd.read_csv(self.raw_output)
            self.raw_proverbs_count = len(df)
            logger.info(f"Loaded {self.raw_proverbs_count} proverbs from existing file")
            return True
        
        try:
            start_time = datetime.now()
            
            # Extract all proverbs
            proverbs = self.extractor.extract_all_proverbs()
            self.raw_proverbs_count = len(proverbs)
            
            # Save to CSV
            self.extractor.save_to_csv(str(self.raw_output))
            
            self.extraction_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Stage 1 complete ({self.extraction_time:.1f}s)")
            logger.info(f"Extracted {self.raw_proverbs_count} proverbs")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Stage 1 failed: {e}")
            return False
    
    def _stage_2_validate(self) -> bool:
        """Stage 2: Validate extraction quality."""
        logger.info("\n[STAGE 2/5] Validating extraction quality...")
        
        try:
            # Load raw data
            df = pd.read_csv(self.raw_output)
            
            # Get quality thresholds from configuration
            quality_config = self.source_config.get('quality', {})
            min_proverbs = quality_config.get('min_proverbs', 90)
            max_empty = quality_config.get('max_empty_texts', 10)
            
            # Quality checks
            checks_passed = []
            checks_failed = []
            
            # Check 1: Minimum proverb count
            if len(df) >= min_proverbs:
                checks_passed.append(f"✅ Proverb count: {len(df)} >= {min_proverbs}")
            else:
                checks_failed.append(f"❌ Proverb count: {len(df)} < {min_proverbs}")
            
            # Check 2: Kikuyu text completeness
            empty_kikuyu = df['kikuyu_proverb'].isna().sum()
            if empty_kikuyu <= max_empty:
                checks_passed.append(f"✅ Empty Kikuyu texts: {empty_kikuyu} <= {max_empty}")
            else:
                checks_failed.append(f"❌ Empty Kikuyu texts: {empty_kikuyu} > {max_empty}")
            
            # Check 3: English translation completeness
            empty_english = df['english_translation'].isna().sum()
            english_pct = ((len(df) - empty_english) / len(df)) * 100
            checks_passed.append(f"✅ English translations: {english_pct:.1f}%")
            
            # Print validation results
            logger.info("Quality validation results:")
            for check in checks_passed:
                logger.info(f"  {check}")
            for check in checks_failed:
                logger.warning(f"  {check}")
            
            if checks_failed:
                logger.error("❌ Stage 2 validation failed")
                return False
            
            logger.info("✅ Stage 2 complete - All quality checks passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Stage 2 failed: {e}")
            return False
    
    def _stage_3_convert(self) -> bool:
        """Stage 3: Convert to gold standard format."""
        logger.info("\n[STAGE 3/5] Converting to gold standard format...")
        
        try:
            start_time = datetime.now()
            
            # Convert to gold standard
            gold_df = self.converter.prepare_gold_standard(
                source_csv_path=str(self.raw_output),
                output_path=str(self.gold_standard_output),
                metadata_path=str(self.metadata_output)
            )
            
            self.gold_standard_count = len(gold_df)
            self.conversion_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"✅ Stage 3 complete ({self.conversion_time:.1f}s)")
            logger.info(f"Created {self.gold_standard_count} gold standard entries")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Stage 3 failed: {e}")
            return False
    
    def _stage_4_quality_check(self) -> bool:
        """Stage 4: Final quality checks on gold standard."""
        logger.info("\n[STAGE 4/5] Final quality checks...")
        
        try:
            # Load gold standard
            gold_df = pd.read_csv(self.gold_standard_output)
            
            # Calculate completeness metrics
            total = len(gold_df)
            metrics = {
                'Kikuyu texts': (gold_df['kikuyu_text'].notna().sum() / total) * 100,
                'Expert translations': (gold_df['expert_translation'].notna().sum() / total) * 100,
                'Cultural meanings': (gold_df['expert_cultural_meaning'].notna().sum() / total) * 100,
                'Business contexts': (gold_df['expert_business_relevance'].notna().sum() / total) * 100,
            }
            
            logger.info("Completeness metrics:")
            for metric, value in metrics.items():
                logger.info(f"  - {metric}: {value:.1f}%")
            
            # Check cultural authenticity
            avg_authenticity = gold_df['cultural_authenticity'].mean()
            logger.info(f"  - Average cultural authenticity: {avg_authenticity:.1f}/5.0")
            
            logger.info("✅ Stage 4 complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Stage 4 failed: {e}")
            return False
    
    def _stage_5_generate_report(self):
        """Stage 5: Generate summary report."""
        logger.info("\n[STAGE 5/5] Generating summary report...")
        
        try:
            # Load data
            gold_df = pd.read_csv(self.gold_standard_output)
            
            # Get metadata
            import json
            with open(self.metadata_output, 'r') as f:
                metadata = json.load(f)
            
            author = self.source_config['author']
            title = self.source_config['title']
            year = self.source_config['year']
            
            # Generate markdown report
            report = f"""# Expert Proverb Gold Standard Report

**Source**: {self.source_name.upper()}  
**Generation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Source Information

- **Author**: {author}
- **Title**: {title}
- **Year**: {year}
- **Language**: {self.source_config['language'].title()} ({self.source_config['language_code']})
- **Domain**: {self.source_config['domain'].replace('_', ' ').title()}

## Extraction Summary

- **Source PDF**: `{self.pdf_path.name}`
- **Extraction time**: {self.extraction_time:.1f}s
- **Proverbs extracted**: {self.raw_proverbs_count}
- **Output file**: `{self.raw_output.name}`

## Gold Standard Conversion

- **Conversion time**: {self.conversion_time:.1f}s
- **Gold standard entries**: {len(gold_df)}
- **Unique proverb IDs**: {gold_df['proverb_id'].nunique()}
- **Validation status**: Expert validated by {author}

## Quality Metrics

- **Kikuyu texts**: {(gold_df['kikuyu_text'].notna().sum() / len(gold_df) * 100):.1f}%
- **Expert translations**: {(gold_df['expert_translation'].notna().sum() / len(gold_df) * 100):.1f}%
- **Cultural meanings**: {(gold_df['expert_cultural_meaning'].notna().sum() / len(gold_df) * 100):.1f}%
- **Business contexts**: {(gold_df['expert_business_relevance'].notna().sum() / len(gold_df) * 100):.1f}%
- **Average cultural authenticity**: {gold_df['cultural_authenticity'].mean():.1f}/5.0

## Thematic Distribution

"""
            for theme, count in gold_df['thematic_category'].value_counts().items():
                report += f"- **{theme.replace('_', ' ').title()}**: {count}\n"
            
            report += f"""

## Output Files

1. **Raw Extraction**: `{self.raw_output}`
   - {self.raw_proverbs_count} proverbs with full context
   - Source: PDF pages {self.source_config['extraction']['start_page']}-{self.source_config['extraction']['end_page']}

2. **Gold Standard**: `{self.gold_standard_output}`
   - {len(gold_df)} evaluation-ready entries
   - Standardized 16-column format
   - Expert translations as baseline

3. **Metadata**: `{self.metadata_output}`
   - Dataset statistics and provenance
   - Quality metrics and citation

## Usage Instructions

### For Evaluation

```python
import pandas as pd

# Load gold standard
gold_standard = pd.read_csv('{self.gold_standard_output}')

# Each entry contains:
# - kikuyu_text: Original proverb
# - expert_translation: Human expert baseline
# - expert_cultural_meaning: Cultural context
# - thematic_category: Classification
```

### For Translation Comparison

1. Generate translations using your system (OG-RAG, Raw LLM, etc.)
2. Compare against `expert_translation` column
3. Evaluate cultural faithfulness using `expert_cultural_meaning`
4. Assess business relevance against `expert_business_relevance`

## Citation

{self.source_config.get('citation', {}).get('text', 'See metadata for citation information')}

## Next Steps

- [ ] Review gold standard entries for completeness
- [ ] Generate OG-RAG translations
- [ ] Generate Raw LLM translations
- [ ] Run comparative evaluation
- [ ] Analyze cultural faithfulness metrics

---

*Generated by Expert Proverb Gold Standard Pipeline v2.0*
"""
            
            # Save report
            self.report_output.parent.mkdir(parents=True, exist_ok=True)
            with open(self.report_output, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"✅ Stage 5 complete")
            logger.info(f"Report saved to: {self.report_output}")
            
        except Exception as e:
            logger.warning(f"⚠️  Report generation failed: {e}")
    
    def _print_final_summary(self):
        """Print final pipeline summary."""
        print("\n" + "="*80)
        print("PIPELINE SUMMARY")
        print("="*80)
        print(f"Source: {self.source_config['author']}")
        print(f"Total proverbs: {self.gold_standard_count}")
        print(f"\nOutput files:")
        print(f"  1. Raw extraction: {self.raw_output}")
        print(f"  2. Gold standard: {self.gold_standard_output}")
        print(f"  3. Metadata: {self.metadata_output}")
        print(f"  4. Report: {self.report_output}")
        print(f"\nNext steps:")
        print(f"   - Review gold standard quality")
        print(f"   - Use {self.gold_standard_output.name} as evaluation baseline")
        print(f"   - Generate translations with your systems")
        print(f"   - Run comparative evaluation")
        print("="*80)


def main():
    """Main execution function."""
    import argparse
    
    available_sources = list_available_sources()
    
    parser = argparse.ArgumentParser(
        description="Complete pipeline for expert proverb gold standard creation"
    )
    parser.add_argument(
        '--pdf',
        default='data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf',
        help='Path to expert proverb PDF'
    )
    parser.add_argument(
        '--source',
        default='ireri',
        choices=available_sources,
        help=f'Expert source identifier (available: {", ".join(available_sources)})'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-extraction even if files exist'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize and run pipeline
        pipeline = GoldStandardPipeline(
            pdf_path=args.pdf,
            source_name=args.source,
            force_reextract=args.force
        )
        
        success = pipeline.run()
        
        return 0 if success else 1
        
    except Exception as e:
        logger.error(f"❌ Pipeline execution failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())
