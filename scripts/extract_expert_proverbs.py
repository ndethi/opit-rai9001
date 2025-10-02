#!/usr/bin/env python3
"""
Extract Expert-Curated Proverb Collections

Generic framework for extracting expert-curated proverb collections from PDF sources.
Supports multiple expert sources and languages through configuration.

Default source: Margaret Wambere Ireri's Kikuyu proverbs (2014)

Author: thiLLMo Research Team
Date: October 2025
"""

import logging
import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd

# Import configuration system
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_source_config, get_output_path, list_available_sources

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    raise ImportError("pdfplumber is required. Install with: pip install pdfplumber")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ExpertProverb:
    """Structure for expert-curated proverb collection."""
    proverb_number: int
    kikuyu_proverb: str
    english_translation: str
    kiswahili_translation: str
    cultural_interpretation: str
    wealth_prosperity_context: str
    biblical_parallel: str
    teaching_message: str
    references: str  # Citations like (GJW A 5, Ba 4)
    category: str  # W=Wealth, M=Money, WM=Both
    page_number: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for CSV export."""
        return asdict(self)


class ExpertProverbExtractor:
    """Extract curated proverbs from expert PDF collections."""
    
    def __init__(self, pdf_path: str, source_name: str = 'ireri'):
        """
        Initialize extractor with PDF path and source configuration.
        
        Args:
            pdf_path: Path to the expert proverb collection PDF
            source_name: Expert source identifier (default: 'ireri')
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        self.source_name = source_name
        self.source_config = get_source_config(source_name)
        
        self.proverbs: List[ExpertProverb] = []
        
        # Get extraction configuration
        extraction_config = self.source_config.get('extraction', {})
        self.start_page = extraction_config.get('start_page', 7)
        self.end_page = extraction_config.get('end_page', 150)
        self.pattern_type = extraction_config.get('pattern_type', 'numbered')
        
        # Pattern configurations (currently optimized for numbered format)
        # Future: Add custom patterns based on pattern_type
        self._setup_patterns()
        
    def _setup_patterns(self):
        """Setup regex patterns based on source configuration."""
        # Proverb number pattern - matches formats like "1.", "23.", "100."
        self.proverb_number_pattern = re.compile(r'^(\d{1,3})\.\s+(.+)')
        
        # English translation pattern
        self.english_pattern = re.compile(
            r'English:\s*(.+?)(?=Kiswahili:|$)', 
            re.IGNORECASE | re.DOTALL
        )
        
        # Kiswahili translation pattern
        self.kiswahili_pattern = re.compile(
            r'Kiswahili:\s*(.+?)(?=Meaning:|Teaching:|Bible parallel:|^\d+\.|$)', 
            re.IGNORECASE | re.DOTALL
        )
        
        # Cultural meaning/interpretation pattern
        self.meaning_pattern = re.compile(
            r'Meaning:\s*(.+?)(?=Teaching:|Bible parallel:|^\d+\.|$)', 
            re.IGNORECASE | re.DOTALL
        )
        
        # Teaching message pattern
        self.teaching_pattern = re.compile(
            r'Teaching:\s*(.+?)(?=Bible parallel:|^\d+\.|$)', 
            re.IGNORECASE | re.DOTALL
        )
        
        # Biblical parallel pattern
        self.bible_pattern = re.compile(
            r'Bible parallel:\s*(.+?)(?=^\d+\.|$)', 
            re.IGNORECASE | re.DOTALL
        )
        
        # Category markers (W=Wealth, M=Money, MW=Both)
        self.category_pattern = re.compile(r'\)\s*([WM]+)\s*$')
        
    def extract_all_proverbs(self) -> List[ExpertProverb]:
        """
        Extract all proverbs from the PDF.
        
        Returns:
            List of extracted ExpertProverb objects
        """
        author = self.source_config.get('author', 'Unknown')
        logger.info(f"Opening PDF: {self.pdf_path}")
        logger.info(f"Source: {author} ({self.source_name})")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            all_text = ""
            page_mapping = {}  # Track which proverb appears on which page
            
            # Extract text from configured page range
            for page_num in range(self.start_page - 1, min(len(pdf.pages), self.end_page)):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    # Track page numbers for proverbs
                    matches = self.proverb_number_pattern.finditer(text)
                    for match in matches:
                        proverb_num = int(match.group(1))
                        total_proverbs = self.source_config.get('total_proverbs', 100)
                        if 1 <= proverb_num <= total_proverbs:
                            page_mapping[proverb_num] = page_num + 1
                    
                    all_text += f"\n--- PAGE {page_num + 1} ---\n{text}"
        
        logger.info(f"Extracted text from {len(pdf.pages)} pages")
        
        # Parse the combined text to extract structured proverbs
        self.proverbs = self._parse_proverbs(all_text, page_mapping)
        
        logger.info(f"Successfully extracted {len(self.proverbs)} proverbs")
        return self.proverbs
    
    def _parse_proverbs(self, text: str, page_mapping: Dict[int, int]) -> List[ExpertProverb]:
        """
        Parse proverbs from the extracted text.
        
        Args:
            text: Combined text from all pages
            page_mapping: Dictionary mapping proverb number to page number
            
        Returns:
            List of parsed ExpertProverb objects
        """
        proverbs = []
        total_proverbs = self.source_config.get('total_proverbs', 100)
        
        # Split text into individual proverb blocks
        blocks = re.split(r'\n(\d{1,3})\.\s+', text)
        
        # Process blocks in pairs (number, content)
        for i in range(1, len(blocks), 2):
            if i + 1 >= len(blocks):
                break
                
            proverb_num = int(blocks[i])
            if proverb_num < 1 or proverb_num > total_proverbs:
                continue
                
            content = blocks[i + 1]
            
            try:
                proverb = self._parse_single_proverb(proverb_num, content, page_mapping)
                if proverb:
                    proverbs.append(proverb)
                    logger.debug(f"Parsed proverb {proverb_num}: {proverb.kikuyu_proverb[:50]}...")
            except Exception as e:
                logger.warning(f"Error parsing proverb {proverb_num}: {e}")
                continue
        
        # Sort by proverb number
        proverbs.sort(key=lambda p: p.proverb_number)
        
        return proverbs
    
    def _parse_single_proverb(
        self, 
        proverb_num: int, 
        content: str, 
        page_mapping: Dict[int, int]
    ) -> Optional[ExpertProverb]:
        """
        Parse a single proverb block into structured format.
        
        Args:
            proverb_num: Proverb number
            content: Text content of the proverb block
            page_mapping: Dictionary mapping proverb number to page number
            
        Returns:
            ExpertProverb object or None if parsing fails
        """
        # Extract Kikuyu text (first line before "English:")
        kikuyu_match = re.match(r'^([^\n]+?)(?=\nEnglish:)', content, re.DOTALL)
        if not kikuyu_match:
            lines = content.split('\n')
            kikuyu_text = lines[0].strip() if lines else ""
        else:
            kikuyu_text = kikuyu_match.group(1).strip()
        
        # Clean up kikuyu text
        kikuyu_text = re.sub(r'--- PAGE \d+ ---', '', kikuyu_text).strip()
        
        # Extract category
        category_match = self.category_pattern.search(kikuyu_text)
        category = category_match.group(1) if category_match else "W"
        
        # Extract references
        ref_match = re.search(r'\(([^)]+)\)', kikuyu_text)
        references = ref_match.group(1) if ref_match else ""
        
        # Clean kikuyu text
        kikuyu_text = re.sub(r'\([^)]+\)\s*[WM]*\s*$', '', kikuyu_text).strip()
        
        # Extract all other fields using patterns
        english_match = self.english_pattern.search(content)
        english_translation = self._clean_extracted_text(english_match.group(1)) if english_match else ""
        
        kiswahili_match = self.kiswahili_pattern.search(content)
        kiswahili_translation = self._clean_extracted_text(kiswahili_match.group(1)) if kiswahili_match else ""
        
        meaning_match = self.meaning_pattern.search(content)
        cultural_interpretation = self._clean_extracted_text(meaning_match.group(1)) if meaning_match else ""
        
        teaching_match = self.teaching_pattern.search(content)
        teaching_message = self._clean_extracted_text(teaching_match.group(1)) if teaching_match else ""
        
        bible_match = self.bible_pattern.search(content)
        biblical_parallel = self._clean_extracted_text(bible_match.group(1)) if bible_match else ""
        
        # Combine for wealth context
        wealth_context_parts = []
        if cultural_interpretation:
            wealth_context_parts.append(cultural_interpretation)
        if teaching_message:
            wealth_context_parts.append(f"Teaching: {teaching_message}")
        
        wealth_prosperity_context = " | ".join(wealth_context_parts)
        
        # Get page number
        page_number = page_mapping.get(proverb_num, 0)
        
        return ExpertProverb(
            proverb_number=proverb_num,
            kikuyu_proverb=kikuyu_text,
            english_translation=english_translation,
            kiswahili_translation=kiswahili_translation,
            cultural_interpretation=cultural_interpretation,
            wealth_prosperity_context=wealth_prosperity_context,
            biblical_parallel=biblical_parallel,
            teaching_message=teaching_message,
            references=references,
            category=category,
            page_number=page_number
        )
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean extracted text by removing artifacts and normalizing whitespace."""
        text = re.sub(r'--- PAGE \d+ ---', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip(' "\'')
        return text.strip()
    
    def save_to_csv(self, output_path: Optional[str] = None) -> None:
        """
        Save extracted proverbs to CSV file.
        
        Args:
            output_path: Path to save CSV file (auto-generated if None)
        """
        if not self.proverbs:
            logger.warning("No proverbs to save. Run extract_all_proverbs() first.")
            return
        
        if output_path is None:
            output_path = str(get_output_path(self.source_name, 'raw_csv'))
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to DataFrame
        df = pd.DataFrame([p.to_dict() for p in self.proverbs])
        
        # Reorder columns
        column_order = [
            'proverb_number', 'kikuyu_proverb', 'english_translation',
            'kiswahili_translation', 'cultural_interpretation',
            'wealth_prosperity_context', 'teaching_message', 'biblical_parallel',
            'references', 'category', 'page_number'
        ]
        
        df = df[column_order]
        
        # Save to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"✅ Saved {len(df)} proverbs to: {output_path}")
        
        # Print summary
        self._print_summary(df)
    
    def _print_summary(self, df: pd.DataFrame) -> None:
        """Print summary statistics of extracted proverbs."""
        author = self.source_config.get('author', 'Unknown')
        title = self.source_config.get('title', 'Collection')
        
        print("\n" + "="*80)
        print(f"EXPERT PROVERB EXTRACTION SUMMARY - {self.source_name.upper()}")
        print("="*80)
        print(f"Author: {author}")
        print(f"Collection: {title}")
        print(f"Total proverbs extracted: {len(df)}")
        print(f"Proverbs with English translation: {df['english_translation'].notna().sum()}")
        print(f"Proverbs with Kiswahili translation: {df['kiswahili_translation'].notna().sum()}")
        print(f"Proverbs with cultural interpretation: {df['cultural_interpretation'].notna().sum()}")
        print(f"Proverbs with biblical parallels: {df['biblical_parallel'].notna().sum()}")
        print(f"\nCategory distribution:")
        print(df['category'].value_counts().to_string())
        print(f"\nPage range: {df['page_number'].min()} - {df['page_number'].max()}")
        print("="*80)


def main():
    """Main execution function."""
    import argparse
    
    available_sources = list_available_sources()
    
    parser = argparse.ArgumentParser(
        description="Extract expert-curated proverb collections from PDF"
    )
    parser.add_argument(
        '--pdf',
        default='data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf',
        help='Path to the expert proverb collection PDF'
    )
    parser.add_argument(
        '--source',
        default='ireri',
        choices=available_sources,
        help=f'Expert source identifier (available: {", ".join(available_sources)})'
    )
    parser.add_argument(
        '--output',
        help='Output CSV file path (auto-generated if not specified)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = ExpertProverbExtractor(args.pdf, source_name=args.source)
        
        # Extract all proverbs
        source_config = get_source_config(args.source)
        logger.info(f"Starting extraction: {source_config.get('author', 'Unknown')}")
        proverbs = extractor.extract_all_proverbs()
        
        # Save to CSV
        extractor.save_to_csv(args.output)
        
        print(f"\n✅ SUCCESS! Extracted {len(proverbs)} proverbs")
        print(f"📁 Output saved to: {args.output or get_output_path(args.source, 'raw_csv')}")
        print("\nNext steps:")
        print("1. Review the extracted proverbs for quality")
        print("2. Run convert_to_gold_standard.py to create evaluation dataset")
        print("3. Or run gold_standard_pipeline.py for complete processing")
        
    except Exception as e:
        logger.error(f"❌ Extraction failed: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
