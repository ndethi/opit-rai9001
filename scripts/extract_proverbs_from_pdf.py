#!/usr/bin/env python3
"""
thiLLMo PDF Proverb Extraction Pipeline

Extracts Kikuyu proverbs from PDF documents and prepares them for 
thiLLMo OG-RAG ontology loading with cultural annotations and linguistic analysis.

Features:
- PDF text extraction with layout preservation
- Kikuyu proverb pattern recognition and parsing
- Cultural domain classification for wealth/entrepreneurship
- Linguistic analysis integration with thiLLMo standards
- Quality validation and expert review preparation
- Direct integration with thiLLMo ontology system

Author: thiLLMo OG-RAG System - Watson Ndethi
Institution: OPIT RAI9001
Date: September 2025
"""

import logging
import re
import json
import csv
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Add project source path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# PDF processing
try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
except ImportError as e:
    print(f"Missing PDF processing library: {e}")
    print("Run: pip install PyPDF2 pdfplumber PyMuPDF")
    sys.exit(1)

# Text processing
try:
    import pandas as pd
    from decouple import Config, RepositoryEnv
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Run: pip install pandas python-decouple")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedKikuyuProverb:
    """Structure for Kikuyu proverbs extracted from PDF for thiLLMo system."""
    
    kikuyu_text: str
    page_number: int
    position_in_page: int
    extraction_confidence: float
    raw_context: str  # Surrounding text for validation
    
    # thiLLMo-specific fields
    id: str = ""
    literal_translation: str = ""
    cultural_meaning: str = ""
    themes: List[str] = None
    domain_relevance: str = ""
    complexity_level: str = "unknown"
    validation_status: str = "extracted"
    cultural_significance: str = ""
    morphological_analysis: str = ""
    
    def __post_init__(self):
        """Generate thiLLMo-compatible ID and initialize fields."""
        if not self.id:
            text_hash = hashlib.md5(self.kikuyu_text.encode()).hexdigest()[:8]
            self.id = f"thiLLMo_pdf_{text_hash}"
        
        if self.themes is None:
            self.themes = []

class ThiLLMoPDFProverbExtractor:
    """Extract and process Kikuyu proverbs from PDF documents for thiLLMo OG-RAG system."""
    
    def __init__(self, source_directory: Optional[str] = None):
        """Initialize with thiLLMo project configuration and source directory.
        
        Args:
            source_directory: Path to directory containing PDF files. 
                            Defaults to project's data/sources/ directory.
        """
        # Load configuration from project .env file
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            config = Config(RepositoryEnv(str(env_path)))
        else:
            config = Config()
        
        # thiLLMo project paths
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data"
        
        # Set source directory - either provided or default to data/sources/
        if source_directory:
            self.sources_dir = Path(source_directory).resolve()
            if not self.sources_dir.exists():
                raise FileNotFoundError(f"Source directory not found: {self.sources_dir}")
        else:
            self.sources_dir = self.data_dir / "sources"
        
        # Output directories
        self.proverbs_dir = self.data_dir / "proverbs"
        self.processed_dir = self.data_dir / "processed"
        
        # Ensure output directories exist
        for directory in [self.data_dir, self.proverbs_dir, self.processed_dir]:
            directory.mkdir(exist_ok=True)
        
        # Create sources directory if using default and it doesn't exist
        if not source_directory:
            self.sources_dir.mkdir(exist_ok=True)
        
        # thiLLMo domain terms for wealth/entrepreneurship classification
        self.wealth_entrepreneurship_terms = {
            # Wealth terms
            'ũtonga': 'wealth',
            'mbeca': 'money',
            'githaka': 'land/property',
            'magetha': 'harvest/profits',
            'utongi': 'riches',
            
            # Business/entrepreneurship terms
            'wonjoria': 'business',
            'kũgura': 'buying',
            'kũendia': 'selling',
            'thunu': 'profit',
            'kũrĩma': 'cultivation/development',
            
            # Work/effort terms
            'wĩra': 'work',
            'ndahi': 'effort',
            'kĩnyangĩre': 'diligence',
            'gwĩka': 'doing/action',
            'kũruta': 'production'
        }
        
        # Kikuyu proverb linguistic patterns
        self.kikuyu_proverb_patterns = [
            r'[A-ZÀ-ž][a-zà-ž\s]+[a-zà-ž]',  # Basic capitalized phrase
            r'[A-ZÀ-ž][a-zà-ž]+\s+wa\s+[a-zà-ž]+',  # "X wa Y" pattern (possessive)
            r'[A-ZÀ-ž][a-zà-ž]+\s+[a-zà-ž]+\s+nd[aeiou][a-zà-ž]*',  # Negative constructions
            r'[A-ZÀ-ž][a-zà-ž]+\s+[a-zà-ž]+\s+nĩ[a-zà-ž]*',  # "nĩ" constructions (copula)
            r'[A-ZÀ-ž][a-zà-ž]+\s+[a-zà-ž]+\s+ta\s+[a-zà-ž]+',  # Comparison patterns
            r'Mũ[a-zà-ž]+\s+[a-zà-ž]+',  # Class 1 noun constructions
        ]
        
        # Kikuyu function words and morphemes common in proverbs
        self.kikuyu_linguistic_markers = [
            # Possessive and associative
            'wa', 'na', 'ya', 'cia',
            # Copula and focus
            'nĩ', 'no', 'rĩ', 'nĩ',
            # Negation
            'nda', 'ndu', 'ndaka', 'ndũka',
            # Comparison and manner
            'ta', 'tiga', 'o ta', 'kana',
            # Class prefixes
            'mũ', 'kĩ', 'ma', 'a', 'ka', 'tu', 'ndũ', 'gĩ',
            # Tense/aspect markers
            'ka', 'kũ', 'gũ', 'tũ', 'mũ'
        ]
        
        self.extracted_proverbs: List[ExtractedKikuyuProverb] = []
        
        logger.info(f"thiLLMo PDF Proverb Extractor initialized - Source: {self.sources_dir}")
    
    def extract_text_from_pdf(self, pdf_path: str, method: str = "pdfplumber") -> List[Dict[str, Any]]:
        """Extract text from PDF with multiple fallback methods optimized for Kikuyu text."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting text from: {pdf_path.name}")
        
        if method == "pdfplumber":
            return self._extract_with_pdfplumber(pdf_path)
        elif method == "pymupdf":
            return self._extract_with_pymupdf(pdf_path)
        elif method == "pypdf2":
            return self._extract_with_pypdf2(pdf_path)
        else:
            # Try all methods and return best result for Kikuyu text
            return self._extract_with_fallback(pdf_path)
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extract text using pdfplumber (best for Kikuyu Unicode preservation)."""
        pages_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        # Get text with positioning information for context
                        words = page.extract_words()
                        
                        pages_data.append({
                            'page_number': page_num,
                            'text': text,
                            'words': words,
                            'method': 'pdfplumber',
                            'unicode_quality': self._assess_unicode_quality(text)
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
                        'method': 'pymupdf',
                        'unicode_quality': self._assess_unicode_quality(text)
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
                            'method': 'pypdf2',
                            'unicode_quality': self._assess_unicode_quality(text)
                        })
            
            logger.info(f"Extracted {len(pages_data)} pages using PyPDF2")
            return pages_data
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return []
    
    def _assess_unicode_quality(self, text: str) -> float:
        """Assess quality of Unicode extraction for Kikuyu characters."""
        kikuyu_chars = ['ũ', 'ĩ', 'ũ', 'ĩ', 'ã', 'ẽ', 'õ']
        unicode_score = 0
        
        for char in kikuyu_chars:
            if char in text:
                unicode_score += 1
        
        # Check for common extraction errors
        error_indicators = ['?', '???', 'â€™', 'â€œ', 'â€']
        error_count = sum(text.count(error) for error in error_indicators)
        
        quality = (unicode_score / len(kikuyu_chars)) - (error_count * 0.1)
        return max(0.0, min(1.0, quality))
    
    def _extract_with_fallback(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Try multiple extraction methods and return the best result for Kikuyu text."""
        methods = ["pdfplumber", "pymupdf", "pypdf2"]
        best_result = []
        best_method = None
        best_score = 0
        
        for method in methods:
            try:
                if method == "pdfplumber":
                    result = self._extract_with_pdfplumber(pdf_path)
                elif method == "pymupdf":
                    result = self._extract_with_pymupdf(pdf_path)
                elif method == "pypdf2":
                    result = self._extract_with_pypdf2(pdf_path)
                
                # Score result based on pages, text quality, and Unicode quality
                if result:
                    total_text = sum(len(page['text']) for page in result)
                    avg_unicode_quality = sum(page.get('unicode_quality', 0) for page in result) / len(result)
                    score = len(result) * total_text * (1 + avg_unicode_quality)
                    
                    if score > best_score:
                        best_result = result
                        best_method = method
                        best_score = score
                        
            except Exception as e:
                logger.warning(f"Method {method} failed: {e}")
                continue
        
        if best_result:
            logger.info(f"Best extraction: {best_method} with {len(best_result)} pages (score: {best_score:.0f})")
        
        return best_result
    
    def identify_kikuyu_proverb_candidates(self, pages_data: List[Dict[str, Any]]) -> List[ExtractedKikuyuProverb]:
        """Identify potential Kikuyu proverbs in extracted text using linguistic patterns."""
        candidates = []
        
        for page_data in pages_data:
            page_number = page_data['page_number']
            text = page_data['text']
            
            # Split into lines and clean, preserving Kikuyu characters
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            for line_num, line in enumerate(lines):
                # Skip obvious non-proverb content
                if self._is_non_proverb_content(line):
                    continue
                
                confidence = self._calculate_kikuyu_proverb_confidence(line)
                
                if confidence > 0.25:  # Lower threshold for Kikuyu due to linguistic complexity
                    # Get surrounding context for cultural validation
                    context_start = max(0, line_num - 3)
                    context_end = min(len(lines), line_num + 4)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    candidate = ExtractedKikuyuProverb(
                        kikuyu_text=line,
                        page_number=page_number,
                        position_in_page=line_num,
                        extraction_confidence=confidence,
                        raw_context=context
                    )
                    
                    candidates.append(candidate)
        
        logger.info(f"Identified {len(candidates)} Kikuyu proverb candidates")
        return candidates
    
    def _is_non_proverb_content(self, text: str) -> bool:
        """Check if text is obviously not a proverb."""
        text_lower = text.lower()
        
        # Skip headers, footers, page numbers
        non_proverb_indicators = [
            'page', 'chapter', 'index', 'reference', 'bibliography',
            'table', 'figure', 'author', 'publisher', 'isbn',
            'contents', 'preface', 'appendix', 'copyright',
            '©', '®', 'http', 'www', 'email', '@'
        ]
        
        if any(indicator in text_lower for indicator in non_proverb_indicators):
            return True
        
        # Skip very short or very long texts
        if len(text) < 8 or len(text) > 300:
            return True
        
        # Skip texts that are mostly numbers or punctuation
        alpha_ratio = sum(c.isalpha() for c in text) / len(text)
        if alpha_ratio < 0.6:
            return True
        
        return False
    
    def _calculate_kikuyu_proverb_confidence(self, text: str) -> float:
        """Calculate confidence that text is a Kikuyu proverb using linguistic analysis."""
        confidence = 0.0
        text_lower = text.lower()
        
        # Kikuyu language marker detection
        kikuyu_score = 0
        for marker in self.kikuyu_linguistic_markers:
            if marker in text_lower:
                kikuyu_score += 1
        
        # Normalize by total markers and weight
        confidence += min(kikuyu_score / len(self.kikuyu_linguistic_markers) * 2, 0.4)
        
        # Kikuyu proverb pattern matching
        pattern_score = 0
        for pattern in self.kikuyu_proverb_patterns:
            if re.search(pattern, text):
                pattern_score += 0.15
        
        confidence += min(pattern_score, 0.3)
        
        # Domain relevance (wealth/entrepreneurship)
        domain_score = 0
        for term in self.wealth_entrepreneurship_terms.keys():
            if term in text_lower:
                domain_score += 0.15
        
        confidence += min(domain_score, 0.25)
        
        # Structural proverb characteristics
        if self._has_kikuyu_proverb_structure(text):
            confidence += 0.2
        
        # Unicode quality bonus (well-preserved Kikuyu characters)
        if any(char in text for char in ['ũ', 'ĩ', 'ã', 'ẽ', 'õ']):
            confidence += 0.15
        
        # Penalize non-proverb characteristics
        if any(marker in text_lower for marker in ['http', 'www', 'page', 'chapter']):
            confidence -= 0.3
        
        return max(0.0, min(1.0, confidence))
    
    def _has_kikuyu_proverb_structure(self, text: str) -> bool:
        """Check if text has typical Kikuyu proverb structure."""
        # Kikuyu proverbs often have balanced parallel structures
        # Split by common Kikuyu conjunctions and punctuation
        parts = re.split(r'[,;:]|\s+na\s+|\s+kana\s+|\s+no\s+', text)
        
        if len(parts) == 2:
            # Check for balanced length (common in parallel proverbs)
            if abs(len(parts[0]) - len(parts[1])) < 15:
                return True
        
        # Check for metaphorical indicators common in Kikuyu proverbs
        metaphor_indicators = ['ta', 'kana', 'o ta', 'tiga', 'kĩrĩa']
        if any(indicator in text.lower() for indicator in metaphor_indicators):
            return True
        
        # Check for wisdom/teaching indicators
        wisdom_indicators = ['mũndũ', 'ũrĩa', 'rĩrĩa', 'ũrĩa']
        if any(indicator in text.lower() for indicator in wisdom_indicators):
            return True
        
        return False
    
    def classify_wealth_entrepreneurship_relevance(self, proverbs: List[ExtractedKikuyuProverb]) -> List[ExtractedKikuyuProverb]:
        """Classify proverbs by relevance to wealth/entrepreneurship domain for thiLLMo."""
        
        for proverb in proverbs:
            relevance_score = 0
            themes = []
            significance_notes = []
            
            text_lower = proverb.kikuyu_text.lower()
            
            # Wealth-related terms
            wealth_matches = []
            for term, meaning in self.wealth_entrepreneurship_terms.items():
                if term in text_lower:
                    if meaning in ['wealth', 'money', 'land/property', 'harvest/profits', 'riches']:
                        themes.append('wealth_management')
                        wealth_matches.append(f"{term} ({meaning})")
                        relevance_score += 0.3
            
            # Business/entrepreneurship terms
            business_matches = []
            for term, meaning in self.wealth_entrepreneurship_terms.items():
                if term in text_lower:
                    if meaning in ['business', 'buying', 'selling', 'profit', 'cultivation/development']:
                        themes.append('business_wisdom')
                        business_matches.append(f"{term} ({meaning})")
                        relevance_score += 0.35
            
            # Work/effort terms
            work_matches = []
            for term, meaning in self.wealth_entrepreneurship_terms.items():
                if term in text_lower:
                    if meaning in ['work', 'effort', 'diligence', 'doing/action', 'production']:
                        themes.append('work_ethic')
                        work_matches.append(f"{term} ({meaning})")
                        relevance_score += 0.25
            
            # Assign domain relevance and cultural significance
            if relevance_score > 0.4:
                proverb.domain_relevance = "wealth_entrepreneurship"
                proverb.cultural_significance = f"High relevance to wealth/entrepreneurship (score: {relevance_score:.2f})"
                significance_notes.extend([
                    f"Wealth terms: {', '.join(wealth_matches)}" if wealth_matches else "",
                    f"Business terms: {', '.join(business_matches)}" if business_matches else "",
                    f"Work terms: {', '.join(work_matches)}" if work_matches else ""
                ])
            elif relevance_score > 0.2:
                proverb.domain_relevance = "general_wisdom_some_relevance"
                proverb.cultural_significance = f"Medium relevance to wealth/entrepreneurship (score: {relevance_score:.2f})"
            else:
                proverb.domain_relevance = "general_cultural_wisdom"
                proverb.cultural_significance = "General Kikuyu cultural wisdom - low domain relevance"
                themes = ['general_wisdom']
            
            proverb.themes = list(set(themes)) if themes else ['general_wisdom']
            
            # Store detailed analysis
            if significance_notes:
                proverb.cultural_significance += f" | {' | '.join(filter(None, significance_notes))}"
        
        return proverbs
    
    def enhance_with_kikuyu_linguistic_analysis(self, proverbs: List[ExtractedKikuyuProverb]) -> List[ExtractedKikuyuProverb]:
        """Add Kikuyu linguistic analysis to extracted proverbs for thiLLMo ontology."""
        
        for proverb in proverbs:
            # Generate morphological analysis
            proverb.morphological_analysis = self._analyze_kikuyu_morphology(proverb.kikuyu_text)
            
            # Assess linguistic complexity
            proverb.complexity_level = self._assess_kikuyu_complexity(proverb.kikuyu_text)
            
            # Generate placeholder translations (require expert validation)
            proverb.literal_translation = self._generate_placeholder_translation(proverb.kikuyu_text)
            proverb.cultural_meaning = self._generate_placeholder_cultural_meaning(
                proverb.kikuyu_text, proverb.themes
            )
        
        return proverbs
    
    def _analyze_kikuyu_morphology(self, text: str) -> str:
        """Generate basic Kikuyu morphological analysis for thiLLMo ontology."""
        words = text.split()
        analyzed = []
        
        for word in words:
            analysis = word  # Default
            
            # Kikuyu noun classes
            if word.startswith('mũ') and len(word) > 2:
                analysis = f"[Class1: mũ-{word[2:]}]"  # Person class
            elif word.startswith('kĩ') and len(word) > 2:
                analysis = f"[Class7: kĩ-{word[2:]}]"  # Thing class
            elif word.startswith('ma') and len(word) > 2:
                analysis = f"[Class6: ma-{word[2:]}]"  # Liquid/plural class
            elif word.startswith('ndũ') and len(word) > 3:
                analysis = f"[Class10: ndũ-{word[3:]}]"  # Abstract concepts
            
            # Negation patterns
            elif word.startswith('nda') or word.startswith('ndu'):
                analysis = f"[NEG: {word[3:]}]"
            elif word.startswith('ndaka') or word.startswith('ndũka'):
                analysis = f"[NEG.FUT: {word[4:]}]"
            
            # Verbal patterns
            elif word.startswith('kũ') and len(word) > 2:
                analysis = f"[INF: kũ-{word[2:]}]"  # Infinitive
            elif word.startswith('gũ') and len(word) > 2:
                analysis = f"[INF.ALT: gũ-{word[2:]}]"  # Alternative infinitive
            
            analyzed.append(analysis)
        
        return ' '.join(analyzed)
    
    def _assess_kikuyu_complexity(self, text: str) -> str:
        """Assess Kikuyu proverb complexity for thiLLMo classification."""
        word_count = len(text.split())
        
        # Check for complex linguistic features
        complexity_indicators = 0
        
        # Multiple clauses
        if any(conj in text.lower() for conj in ['na', 'kana', 'no', 'nĩ']):
            complexity_indicators += 1
        
        # Metaphorical language
        if any(meta in text.lower() for meta in ['ta', 'tiga', 'o ta']):
            complexity_indicators += 1
        
        # Multiple noun classes
        classes = ['mũ', 'kĩ', 'ma', 'ndũ', 'gĩ']
        class_count = sum(1 for cls in classes if cls in text.lower())
        if class_count > 2:
            complexity_indicators += 1
        
        # Determine complexity level
        if word_count <= 4 and complexity_indicators <= 1:
            return 'simple'
        elif word_count <= 8 and complexity_indicators <= 2:
            return 'moderate'
        else:
            return 'complex'
    
    def _generate_placeholder_translation(self, text: str) -> str:
        """Generate placeholder translation requiring expert validation."""
        return f"[EXPERT TRANSLATION REQUIRED: {text}]"
    
    def _generate_placeholder_cultural_meaning(self, text: str, themes: List[str]) -> str:
        """Generate placeholder cultural meaning for expert completion."""
        theme_context = ", ".join(themes) if themes else "general wisdom"
        return f"[CULTURAL ANALYSIS REQUIRED: Kikuyu proverb related to {theme_context}. Expert interpretation needed for cultural meaning and usage context.]"
    
    def prepare_thiLLMo_expert_review(self, proverbs: List[ExtractedKikuyuProverb]) -> Dict[str, str]:
        """Prepare materials for thiLLMo expert cultural validation."""
        output_dir = self.processed_dir / "expert_review"
        output_dir.mkdir(exist_ok=True)
        
        # Create expert review spreadsheet
        review_data = []
        for proverb in proverbs:
            review_data.append({
                'thiLLMo_ID': proverb.id,
                'Kikuyu_Text': proverb.kikuyu_text,
                'Page_Number': proverb.page_number,
                'Extraction_Confidence': f"{proverb.extraction_confidence:.3f}",
                'Domain_Relevance': proverb.domain_relevance,
                'Cultural_Significance': proverb.cultural_significance,
                'Suggested_Themes': ', '.join(proverb.themes),
                'Morphological_Analysis': proverb.morphological_analysis,
                'Complexity_Level': proverb.complexity_level,
                'Context': proverb.raw_context[:150] + "..." if len(proverb.raw_context) > 150 else proverb.raw_context,
                
                # Fields for expert completion
                'Expert_Translation': '',
                'Cultural_Meaning': '',
                'Usage_Context': '',
                'Metaphorical_Structure': '',
                'Regional_Variants': '',
                'Cultural_Authenticity_Score': '',  # 1-5 scale
                'Heritage_Preservation_Notes': '',
                'Expert_Comments': ''
            })
        
        # Save as Excel for expert review
        df = pd.DataFrame(review_data)
        excel_file = output_dir / f"thiLLMo_proverb_expert_review_{datetime.now().strftime('%Y%m%d')}.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Create thiLLMo-specific review instructions
        instructions_file = output_dir / "thiLLMo_expert_review_instructions.md"
        instructions = self._generate_thiLLMo_expert_instructions()
        
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        # Create extraction summary
        summary_file = output_dir / f"thiLLMo_extraction_summary_{datetime.now().strftime('%Y%m%d')}.txt"
        summary = self._generate_thiLLMo_extraction_summary(proverbs)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info(f"Expert review materials prepared in: {output_dir}")
        
        return {
            'review_spreadsheet': str(excel_file),
            'instructions': str(instructions_file),
            'summary': str(summary_file)
        }
    
    def _generate_thiLLMo_expert_instructions(self) -> str:
        """Generate thiLLMo-specific instructions for cultural experts."""
        return """# thiLLMo Kikuyu Proverb Expert Review Instructions

## Project Context
thiLLMo (Kikuyu Proverbs + LLM) aims to create culturally faithful translations of Kikuyu proverbs 
using Ontology-Grounded Retrieval Augmented Generation (OG-RAG). Your expert validation is crucial 
for preserving cultural authenticity and heritage.

## Review Objectives
1. **Cultural Authenticity**: Verify proverbs are genuine Kikuyu expressions
2. **Translation Accuracy**: Provide culturally faithful English translations
3. **Heritage Preservation**: Ensure cultural significance is maintained
4. **Domain Relevance**: Validate wealth/entrepreneurship domain classification

## Review Tasks

### 1. Authenticity Verification
- **Cultural_Authenticity_Score**: Rate 1-5 (1=Not authentic, 5=Highly authentic)
- Verify the proverb is genuinely used in Kikuyu culture
- Note any extraction errors or OCR issues

### 2. Expert Translation
- **Expert_Translation**: Provide accurate, culturally sensitive English translation
- Preserve metaphorical meaning over literal word-for-word translation
- Consider cultural context and traditional usage

### 3. Cultural Analysis
- **Cultural_Meaning**: Explain deeper cultural significance and wisdom
- **Usage_Context**: Describe when, where, and how the proverb is traditionally used
- **Metaphorical_Structure**: Explain symbolic elements and their meanings

### 4. Heritage Documentation
- **Heritage_Preservation_Notes**: Document cultural importance and preservation needs
- **Regional_Variants**: Note any regional differences in usage or meaning
- **Expert_Comments**: Additional insights, corrections, or cultural context

## thiLLMo Domain Focus
Special attention to proverbs related to:
- **Wealth Management** (ũtonga, mbeca, githaka)
- **Business Wisdom** (wonjoria, kũgura, kũendia)
- **Work Ethic** (wĩra, ndahi, kĩnyangĩre)

## Quality Guidelines
- Prioritize cultural authenticity over academic precision
- Consider traditional contexts and modern applications
- Note generational or regional variations
- Flag any proverbs that seem inauthentic or poorly extracted

## Contact Information
thiLLMo Project - Watson Ndethi (OPIT RAI9001)
[Contact information for questions]

## Cultural Sensitivity
This work contributes to digital preservation of Kikuyu heritage. Your expertise ensures 
respectful and accurate representation of traditional wisdom.
"""
    
    def _generate_thiLLMo_extraction_summary(self, proverbs: List[ExtractedKikuyuProverb]) -> str:
        """Generate thiLLMo-specific extraction summary."""
        total = len(proverbs)
        high_confidence = len([p for p in proverbs if p.extraction_confidence > 0.6])
        domain_relevant = len([p for p in proverbs if p.domain_relevance == 'wealth_entrepreneurship'])
        
        # Theme distribution
        theme_counts = {}
        for proverb in proverbs:
            for theme in proverb.themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        summary = f"""thiLLMo Kikuyu Proverb Extraction Summary
==========================================

Project: thiLLMo OG-RAG System for Culturally Faithful Translation
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Extraction Results
Total Proverbs Extracted: {total}
High Confidence Extractions (>0.6): {high_confidence} ({high_confidence/total*100:.1f}%)
Wealth/Entrepreneurship Domain Relevant: {domain_relevant} ({domain_relevant/total*100:.1f}%)

## Confidence Distribution
- High (>0.6): {len([p for p in proverbs if p.extraction_confidence > 0.6])}
- Medium (0.4-0.6): {len([p for p in proverbs if 0.4 <= p.extraction_confidence <= 0.6])}
- Low (<0.4): {len([p for p in proverbs if p.extraction_confidence < 0.4])}

## Domain Relevance Classification
- Wealth/Entrepreneurship: {len([p for p in proverbs if p.domain_relevance == 'wealth_entrepreneurship'])}
- General with Some Relevance: {len([p for p in proverbs if p.domain_relevance == 'general_wisdom_some_relevance'])}
- General Cultural Wisdom: {len([p for p in proverbs if p.domain_relevance == 'general_cultural_wisdom'])}

## Theme Distribution
{chr(10).join([f"- {theme}: {count}" for theme, count in sorted(theme_counts.items())])}

## Complexity Analysis
- Simple: {len([p for p in proverbs if p.complexity_level == 'simple'])}
- Moderate: {len([p for p in proverbs if p.complexity_level == 'moderate'])}
- Complex: {len([p for p in proverbs if p.complexity_level == 'complex'])}

## Next Steps for thiLLMo Integration
1. Expert cultural validation and translation refinement
2. Cultural meaning enhancement and usage context documentation
3. Integration with thiLLMo OG-RAG ontology system
4. Cultural sensitivity compliance verification

## Quality Assurance
All extracted proverbs require expert validation before integration into the thiLLMo 
OG-RAG system to ensure cultural authenticity and heritage preservation.

---
thiLLMo Project - OPIT RAI9001 - Watson Ndethi
Culturally Faithful Kikuyu Proverb Translation System
"""
        return summary
    
    def save_for_thiLLMo_ontology(self, proverbs: List[ExtractedKikuyuProverb]) -> str:
        """Save proverbs in thiLLMo ontology-compatible format."""
        output_file = self.proverbs_dir / f"extracted_proverbs_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Convert to thiLLMo ontology format
        ontology_data = []
        for proverb in proverbs:
            ontology_data.append({
                'id': proverb.id,
                'kikuyu_text': proverb.kikuyu_text,
                'literal_translation': proverb.literal_translation,
                'cultural_meaning': proverb.cultural_meaning,
                'themes': ','.join(proverb.themes),
                'domain_relevance': proverb.domain_relevance,
                'usage_context': 'pdf_extracted_requires_validation',
                'complexity_level': proverb.complexity_level,
                'frequency_rating': 'unknown',
                'source_type': 'pdf_extraction',
                'region_variants': 'unknown',
                'validation_status': 'extracted_pending_expert_review',
                'morphological_analysis': proverb.morphological_analysis,
                'cultural_significance': proverb.cultural_significance,
                'usage_notes': f"Extracted from page {proverb.page_number}, confidence: {proverb.extraction_confidence:.3f}",
                'phonetic_transcription': '',
                'metaphorical_structure': '',
                'cultural_authenticity_score': '',
                'heritage_preservation_flag': 'pending_expert_validation'
            })
        
        # Save as CSV with UTF-8 encoding for Kikuyu characters
        df = pd.DataFrame(ontology_data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"Saved {len(ontology_data)} proverbs for thiLLMo ontology: {output_file}")
        return str(output_file)
    
    def extract_and_prepare_for_thiLLMo(self, pdf_path: str) -> Dict[str, Any]:
        """Main pipeline: extract Kikuyu proverbs from PDF and prepare for thiLLMo OG-RAG."""
        
        logger.info(f"Starting thiLLMo proverb extraction from: {Path(pdf_path).name}")
        
        # Step 1: Extract text from PDF
        pages_data = self.extract_text_from_pdf(pdf_path)
        if not pages_data:
            raise Exception("Failed to extract text from PDF")
        
        # Step 2: Identify Kikuyu proverb candidates
        candidates = self.identify_kikuyu_proverb_candidates(pages_data)
        if not candidates:
            raise Exception("No Kikuyu proverb candidates found")
        
        # Step 3: Classify by wealth/entrepreneurship domain relevance
        classified_proverbs = self.classify_wealth_entrepreneurship_relevance(candidates)
        
        # Step 4: Add Kikuyu linguistic analysis
        enhanced_proverbs = self.enhance_with_kikuyu_linguistic_analysis(classified_proverbs)
        
        # Step 5: Prepare expert review materials
        review_files = self.prepare_thiLLMo_expert_review(enhanced_proverbs)
        
        # Step 6: Save for thiLLMo ontology loading
        ontology_file = self.save_for_thiLLMo_ontology(enhanced_proverbs)
        
        # Update stored proverbs
        self.extracted_proverbs = enhanced_proverbs
        
        # Generate results summary
        domain_relevant = len([p for p in enhanced_proverbs if p.domain_relevance == 'wealth_entrepreneurship'])
        high_confidence = len([p for p in enhanced_proverbs if p.extraction_confidence > 0.6])
        
        logger.info(f"thiLLMo extraction complete: {len(enhanced_proverbs)} total, {domain_relevant} domain-relevant")
        
        return {
            'total_extracted': len(enhanced_proverbs),
            'high_confidence': high_confidence,
            'domain_relevant': domain_relevant,
            'ontology_file': ontology_file,
            'expert_review_files': review_files,
            'proverbs': enhanced_proverbs,
            'project_context': 'thiLLMo OG-RAG System - Culturally Faithful Kikuyu Translation'
        }

def install_thiLLMo_pdf_dependencies():
    """Create script to install thiLLMo PDF processing dependencies."""
    install_script = f"""#!/bin/bash
# Install thiLLMo PDF processing dependencies

echo "Installing thiLLMo PDF processing libraries..."

# Core PDF libraries
pip install PyPDF2 pdfplumber PyMuPDF

# Data processing (already in thiLLMo requirements)
pip install pandas openpyxl python-decouple

echo "thiLLMo PDF processing setup complete!"
echo "You can now extract Kikuyu proverbs from PDF documents."
echo ""
echo "Usage examples:"
echo "  # Use default data/sources/ directory"
echo "  python scripts/extract_proverbs_from_pdf.py"
echo ""
echo "  # Use custom source directory"
echo "  python scripts/extract_proverbs_from_pdf.py --source-dir /path/to/pdfs"
echo ""
echo "  # Process specific PDF file"
echo "  python scripts/extract_proverbs_from_pdf.py --pdf kikuyu_proverbs.pdf"
"""
    
    script_path = Path(__file__).parent / 'install_thiLLMo_pdf_tools.sh'
    with open(script_path, 'w') as f:
        f.write(install_script)
    
    script_path.chmod(0o755)  # Make executable
    print(f"Created: {script_path}")
    print("Run: ./scripts/install_thiLLMo_pdf_tools.sh")

def main():
    """Main function for thiLLMo PDF proverb extraction with command-line arguments."""
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract Kikuyu proverbs from PDF documents for thiLLMo OG-RAG system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default data/sources/ directory
  python scripts/extract_proverbs_from_pdf.py
  
  # Specify custom source directory
  python scripts/extract_proverbs_from_pdf.py --source-dir /path/to/pdfs
  
  # Process specific PDF file
  python scripts/extract_proverbs_from_pdf.py --source-dir /path/to/pdfs --pdf kikuyu_proverbs.pdf
  
Data Organization:
  data/sources/     - Raw PDF source documents (default source directory)
  data/proverbs/    - Extracted and processed proverb data
  data/processed/   - Expert review materials and intermediate files
        """
    )
    
    parser.add_argument(
        '--source-dir', '-s',
        type=str,
        default=None,
        help='Directory containing PDF files (default: data/sources/)'
    )
    
    parser.add_argument(
        '--pdf', '-p',
        type=str,
        default=None,
        help='Specific PDF file to process (default: process all PDFs in source directory)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default=None,
        help='Custom output directory (default: data/processed/expert_review/)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check dependencies
    try:
        import PyPDF2, pdfplumber, fitz, pandas
        logger.info("thiLLMo PDF processing libraries available")
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Installing dependencies...")
        install_thiLLMo_pdf_dependencies()
        return
    
    # Initialize thiLLMo extractor with custom source directory if provided
    try:
        extractor = ThiLLMoPDFProverbExtractor(source_directory=args.source_dir)
        logger.info(f"Using source directory: {extractor.sources_dir}")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure the source directory exists and contains PDF files.")
        return
    
    # Determine which PDFs to process
    if args.pdf:
        # Process specific PDF file
        pdf_path = extractor.sources_dir / args.pdf
        if not pdf_path.exists():
            print(f"❌ PDF file not found: {pdf_path}")
            return
        pdf_files = [pdf_path]
    else:
        # Process all PDFs in source directory
        pdf_files = list(extractor.sources_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in: {extractor.sources_dir}")
        print("\nPlease place your Kikuyu proverb PDF files in the source directory.")
        print(f"Source directory: {extractor.sources_dir}")
        print("\nExample usage:")
        print("  python scripts/extract_proverbs_from_pdf.py --source-dir /path/to/pdfs")
        return
    
    print(f"📚 Found {len(pdf_files)} PDF file(s) to process:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Process each PDF file
    all_results = []
    total_extracted = 0
    total_domain_relevant = 0
    
    for pdf_path in pdf_files:
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print('='*60)
        
        try:
            results = extractor.extract_and_prepare_for_thiLLMo(str(pdf_path))
            all_results.append({
                'pdf_file': pdf_path.name,
                'results': results
            })
            
            total_extracted += results['total_extracted']
            total_domain_relevant += results['domain_relevant']
            
            print(f"✅ {pdf_path.name}: {results['total_extracted']} proverbs extracted")
            print(f"   - High confidence: {results['high_confidence']}")
            print(f"   - Domain relevant: {results['domain_relevant']}")
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_path.name}: {e}")
            print(f"❌ Failed to process {pdf_path.name}: {e}")
            continue
    
    # Print overall summary
    if all_results:
        print(f"\n{'='*60}")
        print("thiLLMo PDF Extraction Summary")
        print('='*60)
        print(f"📚 Processed PDFs: {len(all_results)}")
        print(f"🔍 Total proverbs extracted: {total_extracted}")
        print(f"💰 Total domain relevant: {total_domain_relevant}")
        print(f"📁 Source directory: {extractor.sources_dir}")
        print(f"📄 Output directory: {extractor.processed_dir}")
        print(f"🎯 Project: thiLLMo OG-RAG - Culturally Faithful Kikuyu Translation")
        print("\n✨ Ready for expert cultural validation and thiLLMo OG-RAG integration!")
        print("\nNext steps:")
        print(f"1. Review expert validation materials in: {extractor.processed_dir}/expert_review/")
        print("2. Complete cultural expert review process")
        print("3. Run thiLLMo system setup: python scripts/thiLLMo_setup.py")
    else:
        print("❌ No PDFs were successfully processed.")

def parse_arguments():
    """Parse command line arguments (kept for backwards compatibility)."""
    return main()

if __name__ == "__main__":
    main()
