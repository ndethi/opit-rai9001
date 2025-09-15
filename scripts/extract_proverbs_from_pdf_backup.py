#!/usr/bin/env python3
"""
Proverb Extraction Script for OPIT RAI9001 Research Project

This script extracts proverbs from PDF documents, specifically designed for
the wealth and prosperity proverbs collection. It uses multiple PDF processing
libraries to ensure robust extraction and handles various PDF formats.

Author: OPIT RAI9001 Research Team
Date: September 16, 2025
"""

import os
import re
import json
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# PDF processing libraries
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_extract
from pdfminer.layout import LAParams

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/proverb_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProverbExtractor:
    """Extract proverbs from PDF documents using multiple extraction methods."""
    
    def __init__(self, pdf_path: str, output_dir: str = "../data/proverbs"):
        """
        Initialize the proverb extractor.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted proverbs
        """
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Proverb patterns - common indicators of proverbs
        self.proverb_patterns = [
            r'^\d+\.\s*(.+)',  # Numbered lists (1. Proverb text)
            r'^[•·▪▫]\s*(.+)',  # Bullet points
            r'^[-–—]\s*(.+)',   # Dash-prefixed items
            r'"([^"]+)"',       # Quoted text
            r"'([^']+)'",       # Smart quotes
            r'Proverb:\s*(.+)', # Explicit proverb labels
            r'Saying:\s*(.+)',  # Saying labels
        ]
        
        # Keywords that often indicate proverb sections
        self.section_keywords = [
            'proverb', 'saying', 'wisdom', 'traditional', 'folk',
            'wealth', 'prosperity', 'money', 'riches', 'fortune',
            'success', 'business', 'trade', 'commerce', 'poverty'
        ]
    
    def extract_with_pypdf2(self) -> str:
        """Extract text using PyPDF2."""
        try:
            logger.info("Extracting text with PyPDF2...")
            text = ""
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            return text
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def extract_with_pdfplumber(self) -> str:
        """Extract text using pdfplumber (better layout preservation)."""
        try:
            logger.info("Extracting text with pdfplumber...")
            text = ""
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            return text
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            return ""
    
    def extract_with_pymupdf(self) -> str:
        """Extract text using PyMuPDF (fitz)."""
        try:
            logger.info("Extracting text with PyMuPDF...")
            text = ""
            pdf_document = fitz.open(self.pdf_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                page_text = page.get_text()
                text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            pdf_document.close()
            return text
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def extract_with_pdfminer(self) -> str:
        """Extract text using pdfminer."""
        try:
            logger.info("Extracting text with pdfminer...")
            laparams = LAParams(
                line_margin=0.5,
                word_margin=0.1,
                char_margin=2.0,
                boxes_flow=0.5,
                all_texts=False
            )
            text = pdfminer_extract(self.pdf_path, laparams=laparams)
            return text
        except Exception as e:
            logger.error(f"pdfminer extraction failed: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page markers
        text = re.sub(r'--- Page \d+ ---', '\n', text)
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\'".,;:!?()-]', '', text)
        return text.strip()
    
    def identify_proverb_sections(self, text: str) -> List[str]:
        """Identify sections that likely contain proverbs."""
        sections = []
        lines = text.split('\n')
        current_section = []
        in_proverb_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_section and in_proverb_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
                continue
            
            # Check if line contains proverb-related keywords
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in self.section_keywords):
                in_proverb_section = True
                current_section = [line]
            elif in_proverb_section:
                current_section.append(line)
                # End section if we hit a clear section break
                if len(line) > 50 and any(word in line_lower for word in ['chapter', 'section', 'conclusion', 'reference']):
                    sections.append('\n'.join(current_section))
                    current_section = []
                    in_proverb_section = False
        
        if current_section and in_proverb_section:
            sections.append('\n'.join(current_section))
        
        return sections
    
    def extract_proverbs_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract individual proverbs from text using patterns."""
        proverbs = []
        sections = self.identify_proverb_sections(text)
        
        for section_idx, section in enumerate(sections):
            logger.info(f"Processing section {section_idx + 1}/{len(sections)}")
            
            for pattern in self.proverb_patterns:
                matches = re.finditer(pattern, section, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    proverb_text = match.group(1) if match.groups() else match.group(0)
                    proverb_text = proverb_text.strip()
                    
                    # Filter out very short or very long matches
                    if 10 <= len(proverb_text) <= 200:
                        # Basic quality checks
                        if self.is_likely_proverb(proverb_text):
                            proverbs.append({
                                'text': proverb_text,
                                'pattern': pattern,
                                'section': section_idx + 1,
                                'length': len(proverb_text),
                                'source': self.pdf_path.name
                            })
        
        # Remove duplicates
        unique_proverbs = []
        seen_texts = set()
        for proverb in proverbs:
            normalized_text = re.sub(r'\s+', ' ', proverb['text'].lower())
            if normalized_text not in seen_texts:
                seen_texts.add(normalized_text)
                unique_proverbs.append(proverb)
        
        return unique_proverbs
    
    def is_likely_proverb(self, text: str) -> bool:
        """Basic heuristics to determine if text is likely a proverb."""
        text_lower = text.lower()
        
        # Exclude obvious non-proverbs
        exclude_patterns = [
            r'page \d+', r'chapter \d+', r'figure \d+', r'table \d+',
            r'http[s]?://', r'www\.', r'@', r'copyright',
            r'reference[s]?', r'bibliograph', r'citation'
        ]
        
        for pattern in exclude_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # Look for proverb indicators
        proverb_indicators = [
            'wealth', 'money', 'riches', 'poor', 'rich', 'fortune',
            'success', 'prosperity', 'work', 'wisdom', 'patience',
            'time', 'friend', 'family', 'god', 'life', 'death'
        ]
        
        indicator_count = sum(1 for indicator in proverb_indicators if indicator in text_lower)
        
        # At least one wealth/wisdom indicator and reasonable length
        return indicator_count >= 1 and 10 <= len(text) <= 200
    
    def save_proverbs(self, proverbs: List[Dict[str, str]], format_type: str = 'all'):
        """Save extracted proverbs in various formats."""
        base_filename = self.pdf_path.stem
        timestamp = "20250916"  # Current date
        
        if format_type in ['json', 'all']:
            json_file = self.output_dir / f"{base_filename}_proverbs_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(proverbs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(proverbs)} proverbs to {json_file}")
        
        if format_type in ['csv', 'all']:
            csv_file = self.output_dir / f"{base_filename}_proverbs_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['text', 'pattern', 'section', 'length', 'source'])
                writer.writeheader()
                writer.writerows(proverbs)
            logger.info(f"Saved {len(proverbs)} proverbs to {csv_file}")
        
        if format_type in ['txt', 'all']:
            txt_file = self.output_dir / f"{base_filename}_proverbs_{timestamp}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Extracted Proverbs from {self.pdf_path.name}\n")
                f.write(f"Extraction Date: September 16, 2025\n")
                f.write(f"Total Proverbs: {len(proverbs)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, proverb in enumerate(proverbs, 1):
                    f.write(f"{i:3d}. {proverb['text']}\n")
                    f.write(f"     (Section {proverb['section']}, {proverb['length']} chars)\n\n")
            logger.info(f"Saved {len(proverbs)} proverbs to {txt_file}")
    
    def extract_proverbs(self, method: str = 'best') -> List[Dict[str, str]]:
        """
        Main extraction method that tries different PDF libraries.
        
        Args:
            method: 'best' for best available, or specific method name
        """
        logger.info(f"Starting proverb extraction from {self.pdf_path}")
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        
        # Try different extraction methods
        extraction_methods = {
            'pdfplumber': self.extract_with_pdfplumber,
            'pymupdf': self.extract_with_pymupdf,
            'pypdf2': self.extract_with_pypdf2,
            'pdfminer': self.extract_with_pdfminer
        }
        
        extracted_text = ""
        
        if method == 'best':
            # Try methods in order of preference
            for method_name, method_func in extraction_methods.items():
                try:
                    text = method_func()
                    if text and len(text) > len(extracted_text):
                        extracted_text = text
                        logger.info(f"Best extraction so far: {method_name} ({len(text)} chars)")
                except Exception as e:
                    logger.warning(f"Method {method_name} failed: {e}")
        else:
            if method in extraction_methods:
                extracted_text = extraction_methods[method]()
            else:
                raise ValueError(f"Unknown extraction method: {method}")
        
        if not extracted_text:
            raise Exception("No text could be extracted from PDF")
        
        logger.info(f"Extracted {len(extracted_text)} characters of text")
        
        # Clean and process text
        cleaned_text = self.clean_text(extracted_text)
        
        # Extract proverbs
        proverbs = self.extract_proverbs_from_text(cleaned_text)
        
        logger.info(f"Extracted {len(proverbs)} potential proverbs")
        
        return proverbs


def main():
    """Main function to run proverb extraction."""
    parser = argparse.ArgumentParser(description='Extract proverbs from PDF documents')
    parser.add_argument('pdf_path', nargs='?', 
                       default='../data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf',
                       help='Path to PDF file')
    parser.add_argument('--output-dir', default='../data/proverbs',
                       help='Output directory for extracted proverbs')
    parser.add_argument('--method', default='best',
                       choices=['best', 'pdfplumber', 'pymupdf', 'pypdf2', 'pdfminer'],
                       help='Extraction method to use')
    parser.add_argument('--format', default='all',
                       choices=['all', 'json', 'csv', 'txt'],
                       help='Output format(s)')
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = ProverbExtractor(args.pdf_path, args.output_dir)
        
        # Extract proverbs
        proverbs = extractor.extract_proverbs(method=args.method)
        
        # Save results
        extractor.save_proverbs(proverbs, format_type=args.format)
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"PROVERB EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"Source PDF: {args.pdf_path}")
        print(f"Total proverbs extracted: {len(proverbs)}")
        print(f"Output directory: {args.output_dir}")
        print(f"Extraction method: {args.method}")
        
        if proverbs:
            print(f"\nSample proverbs:")
            for i, proverb in enumerate(proverbs[:5], 1):
                print(f"{i}. {proverb['text']}")
        
        print(f"\nFiles saved:")
        output_dir = Path(args.output_dir)
        base_name = Path(args.pdf_path).stem
        timestamp = "20250916"
        
        if args.format in ['all', 'json']:
            print(f"  - {output_dir}/{base_name}_proverbs_{timestamp}.json")
        if args.format in ['all', 'csv']:
            print(f"  - {output_dir}/{base_name}_proverbs_{timestamp}.csv")
        if args.format in ['all', 'txt']:
            print(f"  - {output_dir}/{base_name}_proverbs_{timestamp}.txt")
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
