#!/usr/bin/env python3
"""
Extract Margaret Ireri's 100 Kikuyu Proverbs About Money and Wealth

This script specifically extracts the curated collection of 100 proverbs 
compiled by Margaret Wambere Ireri, preserving her expert translations,
cultural interpretations, and wealth/prosperity context.

Source: "A Collection of 100 Proverbs and Wise Sayings of the Gikuyu (Kenya) 
        About Money and Wealth" by Margaret Wambere Ireri (August 2014)

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
class IreriProverb:
    """Structure for Margaret Ireri's curated proverb collection."""
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


class IreriProverbExtractor:
    """Extract the 100 curated proverbs from Margaret Ireri's collection."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize extractor with PDF path.
        
        Args:
            pdf_path: Path to the Ireri proverb collection PDF
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        self.proverbs: List[IreriProverb] = []
        
        # Proverb number pattern - matches formats like "1.", "23.", "100."
        self.proverb_number_pattern = re.compile(r'^(\d{1,3})\.\s+(.+)')
        
        # English translation pattern
        self.english_pattern = re.compile(r'English:\s*(.+?)(?=Kiswahili:|$)', re.IGNORECASE | re.DOTALL)
        
        # Kiswahili translation pattern
        self.kiswahili_pattern = re.compile(r'Kiswahili:\s*(.+?)(?=Meaning:|Teaching:|Bible parallel:|^\d+\.|$)', re.IGNORECASE | re.DOTALL)
        
        # Cultural meaning/interpretation pattern
        self.meaning_pattern = re.compile(r'Meaning:\s*(.+?)(?=Teaching:|Bible parallel:|^\d+\.|$)', re.IGNORECASE | re.DOTALL)
        
        # Teaching message pattern
        self.teaching_pattern = re.compile(r'Teaching:\s*(.+?)(?=Bible parallel:|^\d+\.|$)', re.IGNORECASE | re.DOTALL)
        
        # Biblical parallel pattern
        self.bible_pattern = re.compile(r'Bible parallel:\s*(.+?)(?=^\d+\.|$)', re.IGNORECASE | re.DOTALL)
        
        # Category markers (W=Wealth, M=Money, MW=Both)
        self.category_pattern = re.compile(r'\)\s*([WM]+)\s*$')
        
    def extract_all_proverbs(self) -> List[IreriProverb]:
        """
        Extract all 100 proverbs from the PDF.
        
        Returns:
            List of extracted IreriProverb objects
        """
        logger.info(f"Opening PDF: {self.pdf_path}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            # Proverbs start from page 7 (index 6) and continue
            # We'll process pages 7-100+ to capture all 100 proverbs
            all_text = ""
            page_mapping = {}  # Track which proverb appears on which page
            
            for page_num in range(6, min(len(pdf.pages), 150)):  # Pages 7-150
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    # Track page numbers for proverbs
                    matches = self.proverb_number_pattern.finditer(text)
                    for match in matches:
                        proverb_num = int(match.group(1))
                        if 1 <= proverb_num <= 100:
                            page_mapping[proverb_num] = page_num + 1
                    
                    all_text += f"\n--- PAGE {page_num + 1} ---\n{text}"
        
        logger.info(f"Extracted text from {len(pdf.pages)} pages")
        
        # Now parse the combined text to extract structured proverbs
        self.proverbs = self._parse_proverbs(all_text, page_mapping)
        
        logger.info(f"Successfully extracted {len(self.proverbs)} proverbs")
        return self.proverbs
    
    def _parse_proverbs(self, text: str, page_mapping: Dict[int, int]) -> List[IreriProverb]:
        """
        Parse proverbs from the extracted text.
        
        Args:
            text: Combined text from all pages
            page_mapping: Dictionary mapping proverb number to page number
            
        Returns:
            List of parsed IreriProverb objects
        """
        proverbs = []
        
        # Split text into individual proverb blocks
        # Each proverb starts with a number pattern
        blocks = re.split(r'\n(\d{1,3})\.\s+', text)
        
        # Process blocks in pairs (number, content)
        for i in range(1, len(blocks), 2):
            if i + 1 >= len(blocks):
                break
                
            proverb_num = int(blocks[i])
            if proverb_num < 1 or proverb_num > 100:
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
    ) -> Optional[IreriProverb]:
        """
        Parse a single proverb block into structured format.
        
        Args:
            proverb_num: Proverb number (1-100)
            content: Text content of the proverb block
            page_mapping: Dictionary mapping proverb number to page number
            
        Returns:
            IreriProverb object or None if parsing fails
        """
        # Extract Kikuyu text (first line before "English:")
        kikuyu_match = re.match(r'^([^\n]+?)(?=\nEnglish:)', content, re.DOTALL)
        if not kikuyu_match:
            # Try alternative: text before English line
            lines = content.split('\n')
            kikuyu_text = lines[0].strip() if lines else ""
        else:
            kikuyu_text = kikuyu_match.group(1).strip()
        
        # Clean up kikuyu text - remove page markers and extra whitespace
        kikuyu_text = re.sub(r'--- PAGE \d+ ---', '', kikuyu_text).strip()
        
        # Extract category (W, M, WM) from kikuyu text
        category_match = self.category_pattern.search(kikuyu_text)
        category = category_match.group(1) if category_match else "W"
        
        # Extract references (citations in parentheses)
        ref_match = re.search(r'\(([^)]+)\)', kikuyu_text)
        references = ref_match.group(1) if ref_match else ""
        
        # Clean kikuyu text - remove references and category markers
        kikuyu_text = re.sub(r'\([^)]+\)\s*[WM]*\s*$', '', kikuyu_text).strip()
        
        # Extract English translation
        english_match = self.english_pattern.search(content)
        english_translation = english_match.group(1).strip() if english_match else ""
        english_translation = self._clean_extracted_text(english_translation)
        
        # Extract Kiswahili translation
        kiswahili_match = self.kiswahili_pattern.search(content)
        kiswahili_translation = kiswahili_match.group(1).strip() if kiswahili_match else ""
        kiswahili_translation = self._clean_extracted_text(kiswahili_translation)
        
        # Extract cultural meaning/interpretation
        meaning_match = self.meaning_pattern.search(content)
        cultural_interpretation = meaning_match.group(1).strip() if meaning_match else ""
        cultural_interpretation = self._clean_extracted_text(cultural_interpretation)
        
        # Extract teaching message
        teaching_match = self.teaching_pattern.search(content)
        teaching_message = teaching_match.group(1).strip() if teaching_match else ""
        teaching_message = self._clean_extracted_text(teaching_message)
        
        # Extract biblical parallel
        bible_match = self.bible_pattern.search(content)
        biblical_parallel = bible_match.group(1).strip() if bible_match else ""
        biblical_parallel = self._clean_extracted_text(biblical_parallel)
        
        # Combine cultural interpretation and teaching for wealth context
        wealth_context_parts = []
        if cultural_interpretation:
            wealth_context_parts.append(cultural_interpretation)
        if teaching_message:
            wealth_context_parts.append(f"Teaching: {teaching_message}")
        
        wealth_prosperity_context = " | ".join(wealth_context_parts)
        
        # Get page number
        page_number = page_mapping.get(proverb_num, 0)
        
        return IreriProverb(
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
        """
        Clean extracted text by removing page markers and normalizing whitespace.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove page markers
        text = re.sub(r'--- PAGE \d+ ---', '', text)
        
        # Remove excessive whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing quotes if present
        text = text.strip(' "\'')
        
        return text.strip()
    
    def save_to_csv(self, output_path: str) -> None:
        """
        Save extracted proverbs to CSV file.
        
        Args:
            output_path: Path to save CSV file
        """
        if not self.proverbs:
            logger.warning("No proverbs to save. Run extract_all_proverbs() first.")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to DataFrame
        df = pd.DataFrame([p.to_dict() for p in self.proverbs])
        
        # Reorder columns for better readability
        column_order = [
            'proverb_number',
            'kikuyu_proverb',
            'english_translation',
            'kiswahili_translation',
            'cultural_interpretation',
            'wealth_prosperity_context',
            'teaching_message',
            'biblical_parallel',
            'references',
            'category',
            'page_number'
        ]
        
        df = df[column_order]
        
        # Save to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"✅ Saved {len(df)} proverbs to: {output_path}")
        
        # Print summary statistics
        self._print_summary(df)
    
    def _print_summary(self, df: pd.DataFrame) -> None:
        """Print summary statistics of extracted proverbs."""
        print("\n" + "="*80)
        print("MARGARET IRERI'S 100 PROVERBS - EXTRACTION SUMMARY")
        print("="*80)
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
    
    parser = argparse.ArgumentParser(
        description="Extract Margaret Ireri's 100 Kikuyu proverbs from PDF"
    )
    parser.add_argument(
        '--pdf',
        default='data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf',
        help='Path to the Ireri proverb collection PDF'
    )
    parser.add_argument(
        '--output',
        default='data/raw/ireri_100_wealth_prosperity_proverbs.csv',
        help='Output CSV file path'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = IreriProverbExtractor(args.pdf)
        
        # Extract all proverbs
        logger.info("Starting extraction of Margaret Ireri's 100 proverbs...")
        proverbs = extractor.extract_all_proverbs()
        
        # Save to CSV
        extractor.save_to_csv(args.output)
        
        print(f"\n✅ SUCCESS! Extracted {len(proverbs)} proverbs")
        print(f"📁 Output saved to: {args.output}")
        print("\nNext steps:")
        print("1. Review the extracted proverbs for quality")
        print("2. Run the gold standard conversion pipeline")
        print("3. Use prepare_ireri_gold_standard() to create evaluation dataset")
        
    except Exception as e:
        logger.error(f"❌ Extraction failed: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
