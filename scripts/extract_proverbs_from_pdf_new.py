#!/usr/bin/env python3
"""
PDF Proverb Extraction and Ontology Preparation Pipeline

Extracts Kikuyu proverbs from PDF documents and prepares them for 
ontology loading with cultural annotations and linguistic analysis.

Features:
- PDF text extraction with layout preservation
- Proverb pattern recognition and parsing
- Cultural domain classification
- Linguistic analysis integration
- Quality validation and expert review preparation
- Direct ontology system integration

Author: OG-RAG System Designer
Date: September 2025
"""

import logging
import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import os
import sys

# PDF processing
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF

# Text processing
try:
    import spacy
    from spacy.lang.en import English
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not available. Some linguistic analysis features will be disabled.")

# Environment and data processing
import pandas as pd
try:
    from decouple import Config
    DECOUPLE_AVAILABLE = True
except ImportError:
    DECOUPLE_AVAILABLE = False
    print("Warning: python-decouple not available. Using default configuration.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedProverb:
    """Structure for proverbs extracted from PDF."""
    
    kikuyu_text: str
    page_number: int
    position_in_page: int
    extraction_confidence: float
    raw_context: str  # Surrounding text for validation
    
    # Auto-generated fields
    id: str = ""
    literal_translation: str = ""
    cultural_meaning: str = ""
    themes: List[str] = None
    domain_relevance: str = ""
    complexity_level: str = "unknown"
    validation_status: str = "extracted"
    
    def __post_init__(self):
        """Generate ID and initialize fields."""
        if not self.id:
            text_hash = hashlib.md5(self.kikuyu_text.encode()).hexdigest()[:8]
            self.id = f"pdf_prov_{text_hash}"
        
        if self.themes is None:
            self.themes = []

class PDFProverbExtractor:
    """Extract and process Kikuyu proverbs from PDF documents."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize with configuration."""
        if DECOUPLE_AVAILABLE:
            self.config = Config()
            # Load domain terms for classification
            domain_terms_json = self.config(
                'KIKUYU_DOMAIN_TERMS', 
                default='{"wonjoria": "business", "mbeca": "money", "wira": "work"}'
            )
            self.domain_terms = json.loads(domain_terms_json)
        else:
            # Default configuration
            self.domain_terms = {"wonjoria": "business", "mbeca": "money", "wira": "work"}
        
        # Proverb patterns (common Kikuyu proverb structures)
        self.proverb_patterns = [
            r'[A-ZÀ-ž][a-zà-ž\s]+[a-zà-ž]',  # Basic capitalized phrase
            r'[A-ZÀ-ž][a-zà-ž]+\s+wa\s+[a-zà-ž]+',  # "X wa Y" pattern
            r'[A-ZÀ-ž][a-zà-ž]+\s+[a-zà-ž]+\s+nd[aeiou][a-zà-ž]*',  # Negative constructions
            r'[A-ZÀ-ž][a-zà-ž]+\s+[a-zà-ž]+\s+nĩ[a-zà-ž]*',  # "nĩ" constructions
        ]
        
        # Common Kikuyu function words that appear in proverbs
        self.kikuyu_markers = [
            'wa', 'na', 'nĩ', 'kana', 'no', 'nda', 'ndu', 'ta', 'tiga',
            'mũ', 'kĩ', 'ma', 'a', 'rĩ', 'ka', 'tu', 'ndũ', 'gĩ'
        ]
        
        self.extracted_proverbs: List[ExtractedProverb] = []
    
    def extract_text_from_pdf(self, pdf_path: str, method: str = "pdfplumber") -> List[Dict[str, Any]]:
        """Extract text from PDF with multiple fallback methods."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if method == "pdfplumber":
            return self._extract_with_pdfplumber(pdf_path)
        elif method == "pymupdf":
            return self._extract_with_pymupdf(pdf_path)
        elif method == "pypdf2":
            return self._extract_with_pypdf2(pdf_path)
        else:
            # Try all methods and return best result
            return self._extract_with_fallback(pdf_path)
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extract text using pdfplumber (best for layout preservation)."""
        pages_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        # Get text with positioning information
                        words = page.extract_words()
                        
                        pages_data.append({
                            'page_number': page_num,
                            'text': text,
                            'words': words,
                            'method': 'pdfplumber'
                        })
                        
            logger.info(f"Extracted {len(pages_data)} pages using pdfplumber")
            return pages_data
            
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            return []
    
    def _extract_with_pymupdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extract text using PyMuPDF (good for complex layouts)."""
        pages_data = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    pages_data.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'method': 'pymupdf'
                    })
            
            doc.close()
            logger.info(f"Extracted {len(pages_data)} pages using PyMuPDF")
            return pages_data
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return []
    
    def _extract_with_pypdf2(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extract text using PyPDF2 (basic extraction)."""
        pages_data = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    
                    if text.strip():
                        pages_data.append({
                            'page_number': page_num,
                            'text': text,
                            'method': 'pypdf2'
                        })
            
            logger.info(f"Extracted {len(pages_data)} pages using PyPDF2")
            return pages_data
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return []
    
    def _extract_with_fallback(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Try multiple extraction methods and return the best result."""
        methods = ["pdfplumber", "pymupdf", "pypdf2"]
        best_result = []
        best_method = None
        
        for method in methods:
            try:
                if method == "pdfplumber":
                    result = self._extract_with_pdfplumber(pdf_path)
                elif method == "pymupdf":
                    result = self._extract_with_pymupdf(pdf_path)
                elif method == "pypdf2":
                    result = self._extract_with_pypdf2(pdf_path)
                
                # Score result based on number of pages and text quality
                if result and len(result) > len(best_result):
                    total_text = sum(len(page['text']) for page in result)
                    if total_text > sum(len(page['text']) for page in best_result):
                        best_result = result
                        best_method = method
                        
            except Exception as e:
                logger.warning(f"Method {method} failed: {e}")
                continue
        
        if best_result:
            logger.info(f"Best extraction method: {best_method} with {len(best_result)} pages")
        
        return best_result
    
    def identify_proverb_candidates(self, pages_data: List[Dict[str, Any]]) -> List[ExtractedProverb]:
        """Identify potential proverbs in extracted text."""
        candidates = []
        
        for page_data in pages_data:
            page_number = page_data['page_number']
            text = page_data['text']
            
            # Split into lines and clean
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            for line_num, line in enumerate(lines):
                confidence = self._calculate_proverb_confidence(line)
                
                if confidence > 0.3:  # Threshold for potential proverbs
                    # Get surrounding context
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    candidate = ExtractedProverb(
                        kikuyu_text=line,
                        page_number=page_number,
                        position_in_page=line_num,
                        extraction_confidence=confidence,
                        raw_context=context
                    )
                    
                    candidates.append(candidate)
        
        logger.info(f"Identified {len(candidates)} proverb candidates")
        return candidates
    
    def _calculate_proverb_confidence(self, text: str) -> float:
        """Calculate confidence that text is a Kikuyu proverb."""
        confidence = 0.0
        text_lower = text.lower()
        
        # Basic checks
        if len(text) < 10 or len(text) > 200:
            return 0.0
        
        # Check for Kikuyu language markers
        kikuyu_score = 0
        for marker in self.kikuyu_markers:
            if marker in text_lower:
                kikuyu_score += 1
        
        confidence += min(kikuyu_score / len(self.kikuyu_markers), 0.4)
        
        # Check for proverb patterns
        pattern_score = 0
        for pattern in self.proverb_patterns:
            if re.search(pattern, text):
                pattern_score += 0.2
        
        confidence += min(pattern_score, 0.4)
        
        # Check for domain-relevant terms
        domain_score = 0
        for term in self.domain_terms.keys():
            if term in text_lower:
                domain_score += 0.1
        
        confidence += min(domain_score, 0.2)
        
        # Structural checks
        if self._has_proverb_structure(text):
            confidence += 0.3
        
        # Avoid non-proverb content
        if any(marker in text_lower for marker in ['page', 'chapter', 'index', 'reference']):
            confidence -= 0.2
        
        return max(0.0, min(1.0, confidence))
    
    def _has_proverb_structure(self, text: str) -> bool:
        """Check if text has typical proverb structure."""
        # Proverbs often have balanced clauses
        parts = re.split(r'[,;]', text)
        if len(parts) == 2 and abs(len(parts[0]) - len(parts[1])) < 20:
            return True
        
        # Proverbs often contain metaphorical language
        metaphor_indicators = ['ta', 'kana', 'o ta', 'tiga']
        if any(indicator in text.lower() for indicator in metaphor_indicators):
            return True
        
        return False
    
    def classify_domain_relevance(self, proverbs: List[ExtractedProverb]) -> List[ExtractedProverb]:
        """Classify proverbs by domain relevance (wealth/entrepreneurship)."""
        
        for proverb in proverbs:
            relevance_score = 0
            themes = []
            
            text_lower = proverb.kikuyu_text.lower()
            
            # Check for domain terms
            business_terms = ['wonjoria', 'kugura', 'kwendia', 'thunu']
            wealth_terms = ['utonga', 'mbeca', 'githaka', 'magetha']
            work_terms = ['wira', 'ndahi', 'kinyangĩre']
            
            if any(term in text_lower for term in business_terms):
                themes.append('business_wisdom')
                relevance_score += 0.4
            
            if any(term in text_lower for term in wealth_terms):
                themes.append('wealth_management')
                relevance_score += 0.4
            
            if any(term in text_lower for term in work_terms):
                themes.append('work_ethic')
                relevance_score += 0.3
            
            # Assign domain relevance
            if relevance_score > 0.3:
                proverb.domain_relevance = f"High relevance to wealth/entrepreneurship (score: {relevance_score:.2f})"
                proverb.themes = themes
            elif relevance_score > 0.1:
                proverb.domain_relevance = f"Medium relevance to wealth/entrepreneurship (score: {relevance_score:.2f})"
                proverb.themes = themes
            else:
                proverb.domain_relevance = "General cultural proverb - low domain relevance"
                proverb.themes = ['general_wisdom']
        
        return proverbs
    
    def enhance_with_linguistic_analysis(self, proverbs: List[ExtractedProverb]) -> List[ExtractedProverb]:
        """Add linguistic analysis to extracted proverbs."""
        
        for proverb in proverbs:
            # Generate morphological analysis (simplified)
            proverb.morphological_analysis = self._analyze_morphology(proverb.kikuyu_text)
            
            # Assess complexity
            proverb.complexity_level = self._assess_complexity(proverb.kikuyu_text)
            
            # Generate initial translations (these would need expert review)
            proverb.literal_translation = self._generate_literal_translation(proverb.kikuyu_text)
            proverb.cultural_meaning = self._generate_cultural_meaning(proverb.kikuyu_text, proverb.themes)
        
        return proverbs
    
    def _analyze_morphology(self, text: str) -> str:
        """Generate basic morphological analysis."""
        words = text.split()
        analyzed = []
        
        for word in words:
            # Basic Kikuyu morphology patterns
            if word.startswith('mũ') and len(word) > 2:
                analyzed.append(f"mũ-{word[2:]}")  # Class 1 noun
            elif word.startswith('kĩ') and len(word) > 2:
                analyzed.append(f"kĩ-{word[2:]}")  # Class 7 noun
            elif word.startswith('nda') or word.startswith('ndu'):
                analyzed.append(f"NEG-{word[3:]}")  # Negation
            else:
                analyzed.append(word)
        
        return ' '.join(analyzed)
    
    def _assess_complexity(self, text: str) -> str:
        """Assess proverb complexity level."""
        word_count = len(text.split())
        
        if word_count <= 4:
            return 'simple'
        elif word_count <= 8:
            return 'moderate'
        else:
            return 'complex'
    
    def _generate_literal_translation(self, text: str) -> str:
        """Generate basic literal translation (placeholder for expert work)."""
        # This is a placeholder - real translations need expert linguists
        return f"[NEEDS EXPERT TRANSLATION: {text}]"
    
    def _generate_cultural_meaning(self, text: str, themes: List[str]) -> str:
        """Generate cultural meaning description (placeholder)."""
        theme_context = ", ".join(themes) if themes else "general wisdom"
        return f"[NEEDS CULTURAL ANALYSIS: Proverb related to {theme_context}. Expert interpretation required for cultural meaning.]"
    
    def prepare_expert_review_materials(self, proverbs: List[ExtractedProverb], output_dir: str = "expert_review") -> Dict[str, str]:
        """Prepare materials for expert cultural validation."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create expert review spreadsheet
        review_data = []
        for proverb in proverbs:
            review_data.append({
                'ID': proverb.id,
                'Kikuyu_Text': proverb.kikuyu_text,
                'Page_Number': proverb.page_number,
                'Extraction_Confidence': f"{proverb.extraction_confidence:.2f}",
                'Domain_Relevance': proverb.domain_relevance,
                'Suggested_Themes': ', '.join(proverb.themes),
                'Context': proverb.raw_context[:100] + "..." if len(proverb.raw_context) > 100 else proverb.raw_context,
                'Expert_Translation': '',  # For expert to fill
                'Cultural_Meaning': '',   # For expert to fill
                'Usage_Context': '',      # For expert to fill
                'Accuracy_Rating': '',    # For expert to rate 1-5
                'Comments': ''            # For expert feedback
            })
        
        # Save as Excel for easy expert review
        df = pd.DataFrame(review_data)
        excel_file = output_path / "proverb_expert_review.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Create review instructions
        instructions_file = output_path / "expert_review_instructions.md"
        instructions = self._generate_expert_instructions()
        
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        # Create summary report
        summary_file = output_path / "extraction_summary.txt"
        summary = self._generate_extraction_summary(proverbs)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return {
            'review_spreadsheet': str(excel_file),
            'instructions': str(instructions_file),
            'summary': str(summary_file)
        }
    
    def _generate_expert_instructions(self) -> str:
        """Generate instructions for cultural experts."""
        return """# Kikuyu Proverb Expert Review Instructions

## Overview
Please review the extracted Kikuyu proverbs for cultural accuracy and provide translations and interpretations.

## Review Tasks

### 1. Verify Extraction Accuracy
- Check if the Kikuyu text is correctly extracted
- Rate extraction accuracy (1-5 scale)
- Note any OCR or formatting errors

### 2. Provide Translations
- **Expert_Translation**: Provide accurate English translation
- Focus on preserving cultural meaning over literal word-for-word translation

### 3. Cultural Analysis
- **Cultural_Meaning**: Explain the deeper cultural significance
- **Usage_Context**: Describe when and how this proverb is used
- Consider the wealth/entrepreneurship domain relevance

### 4. Quality Assessment
- **Accuracy_Rating**: Rate the overall proverb authenticity (1-5)
- **Comments**: Any additional notes or corrections

## Guidelines
- Prioritize cultural authenticity over literal accuracy
- Consider traditional usage contexts
- Note regional variations if applicable
- Flag any proverbs that seem inauthentic or poorly extracted

## Contact
[Your contact information for questions]
"""
    
    def _generate_extraction_summary(self, proverbs: List[ExtractedProverb]) -> str:
        """Generate summary of extraction results."""
        total = len(proverbs)
        high_confidence = len([p for p in proverbs if p.extraction_confidence > 0.7])
        domain_relevant = len([p for p in proverbs if 'High relevance' in p.domain_relevance])
        
        summary = f"""Kikuyu Proverb Extraction Summary
=====================================

Total Proverbs Extracted: {total}
High Confidence Extractions: {high_confidence} ({high_confidence/total*100:.1f}%)
Domain Relevant (Wealth/Entrepreneurship): {domain_relevant} ({domain_relevant/total*100:.1f}%)

Confidence Distribution:
- High (>0.7): {len([p for p in proverbs if p.extraction_confidence > 0.7])}
- Medium (0.4-0.7): {len([p for p in proverbs if 0.4 <= p.extraction_confidence <= 0.7])}
- Low (<0.4): {len([p for p in proverbs if p.extraction_confidence < 0.4])}

Domain Relevance:
- High domain relevance: {len([p for p in proverbs if 'High relevance' in p.domain_relevance])}
- Medium domain relevance: {len([p for p in proverbs if 'Medium relevance' in p.domain_relevance])}
- General cultural: {len([p for p in proverbs if 'General cultural' in p.domain_relevance])}

Next Steps:
1. Expert review and validation
2. Translation refinement
3. Cultural meaning enhancement
4. Integration with ontology system
"""
        return summary
    
    def save_for_ontology_loading(self, proverbs: List[ExtractedProverb], output_file: str = None) -> str:
        """Save proverbs in format compatible with ontology system."""
        if output_file is None:
            output_file = "/Users/ndethi/dev/opit/opit-rai9001/data/proverbs/extracted_proverbs.csv"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to ontology-compatible format
        ontology_data = []
        for proverb in proverbs:
            ontology_data.append({
                'id': proverb.id,
                'kikuyu_text': proverb.kikuyu_text,
                'literal_translation': proverb.literal_translation,
                'cultural_meaning': proverb.cultural_meaning,
                'themes': ','.join(proverb.themes),
                'domain_relevance': proverb.domain_relevance,
                'usage_context': 'extracted_from_pdf',
                'complexity_level': proverb.complexity_level,
                'frequency_rating': 'unknown',
                'source_type': 'pdf_extraction',
                'region_variants': 'unknown',
                'validation_status': proverb.validation_status,
                'morphological_analysis': getattr(proverb, 'morphological_analysis', ''),
                'usage_notes': f"Extracted from page {proverb.page_number}, confidence: {proverb.extraction_confidence:.2f}",
                'phonetic_transcription': '',
                'metaphorical_structure': ''
            })
        
        # Save as CSV
        df = pd.DataFrame(ontology_data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"Saved {len(ontology_data)} proverbs for ontology loading: {output_path}")
        return str(output_path)
    
    def extract_and_prepare_proverbs(self, pdf_path: str, output_dir: str = None) -> Dict[str, Any]:
        """Main pipeline: extract proverbs from PDF and prepare for ontology."""
        
        if output_dir is None:
            output_dir = "/Users/ndethi/dev/opit/opit-rai9001/data/processed"
        
        logger.info(f"Starting proverb extraction from: {pdf_path}")
        
        # Step 1: Extract text from PDF
        pages_data = self.extract_text_from_pdf(pdf_path)
        if not pages_data:
            raise Exception("Failed to extract text from PDF")
        
        # Step 2: Identify proverb candidates
        candidates = self.identify_proverb_candidates(pages_data)
        if not candidates:
            raise Exception("No proverb candidates found")
        
        # Step 3: Classify by domain relevance
        classified_proverbs = self.classify_domain_relevance(candidates)
        
        # Step 4: Add linguistic analysis
        enhanced_proverbs = self.enhance_with_linguistic_analysis(classified_proverbs)
        
        # Step 5: Prepare expert review materials
        review_files = self.prepare_expert_review_materials(enhanced_proverbs, output_dir)
        
        # Step 6: Save for ontology loading
        ontology_file = self.save_for_ontology_loading(enhanced_proverbs)
        
        # Update stored proverbs
        self.extracted_proverbs = enhanced_proverbs
        
        return {
            'total_extracted': len(enhanced_proverbs),
            'high_confidence': len([p for p in enhanced_proverbs if p.extraction_confidence > 0.7]),
            'domain_relevant': len([p for p in enhanced_proverbs if 'High relevance' in p.domain_relevance]),
            'ontology_file': ontology_file,
            'expert_review_files': review_files,
            'proverbs': enhanced_proverbs
        }

def create_installation_script():
    """Create script to install required PDF processing libraries."""
    install_script = """#!/bin/bash
# Install PDF processing dependencies for thiLLMo

echo "Installing PDF processing libraries for thiLLMo project..."

# Core PDF libraries
pip install PyPDF2 pdfplumber PyMuPDF

# Text processing
pip install pandas openpyxl

# Optional: Install spacy for advanced linguistic analysis
echo "Installing spaCy (optional for linguistic analysis)..."
pip install spacy

# Download spacy model (if needed)
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Optional: python-decouple for configuration
pip install python-decouple

echo "Installation complete!"
echo "You can now run PDF proverb extraction for thiLLMo."
"""
    
    with open('/Users/ndethi/dev/opit/opit-rai9001/scripts/install_pdf_tools.sh', 'w') as f:
        f.write(install_script)
    
    print("Created install_pdf_tools.sh - run: bash scripts/install_pdf_tools.sh")

def main():
    """Extract proverbs from thiLLMo PDF document."""
    
    # Check if required libraries are available
    try:
        import PyPDF2, pdfplumber, fitz
        print("PDF processing libraries available")
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Run: pip install PyPDF2 pdfplumber PyMuPDF pandas openpyxl")
        create_installation_script()
        return
    
    # Initialize extractor
    extractor = PDFProverbExtractor()
    
    # Use the actual PDF file from the thiLLMo project structure
    pdf_path = "/Users/ndethi/dev/opit/opit-rai9001/data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"PDF file not found: {pdf_path}")
        print("Please ensure the proverbs PDF is in the correct location:")
        print("  data/sources/OPIT_RAI9001_Proverbs_Wealth_Prosperity_v1.pdf")
        return
    
    try:
        # Run the extraction pipeline
        results = extractor.extract_and_prepare_proverbs(pdf_path)
        
        print(f"\n=== thiLLMo Proverb Extraction Results ===")
        print(f"Total proverbs extracted: {results['total_extracted']}")
        print(f"High confidence extractions: {results['high_confidence']}")
        print(f"Domain relevant (wealth/entrepreneurship): {results['domain_relevant']}")
        print(f"Ontology-ready file: {results['ontology_file']}")
        print(f"Expert review materials: {results['expert_review_files']}")
        
        # Display first few proverbs
        print(f"\n=== Sample Extracted Proverbs ===")
        for i, proverb in enumerate(results['proverbs'][:5]):
            print(f"{i+1}. {proverb.kikuyu_text}")
            print(f"   Page: {proverb.page_number}, Confidence: {proverb.extraction_confidence:.2f}")
            print(f"   Themes: {', '.join(proverb.themes)}")
            print()
        
        print(f"\nExtraction complete! Files saved to data/proverbs/ and data/processed/")
        print(f"Ready for ontology integration in the thiLLMo system.")
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
