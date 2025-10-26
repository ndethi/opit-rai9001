#!/usr/bin/env python3
"""
Improved extraction script for Gbarra 1000 Proverb Corpus
Handles WordPress blog post format from PDF
"""

import pdfplumber
import pandas as pd
import re
from typing import List, Dict, Tuple
from datetime import datetime

def extract_proverbs_from_gbarra_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract proverbs from Gbarra PDF (WordPress blog format)
    
    Expected format:
    123. Kikuyu text
    English translation
    Optional: Additional explanation or English equivalent
    """
    
    proverbs = []
    
    print(f"📖 Opening PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        print(f"   Total pages: {len(pdf.pages)}")
        
        current_proverb = None
        
        for page_num, page in enumerate(pdf.pages, 1):
            if page_num % 10 == 0:
                print(f"   Processing page {page_num}/{len(pdf.pages)}...")
            
            text = page.extract_text()
            if not text:
                continue
            
            # Split into lines and process
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Skip header/footer lines
                if 'african manners' in line.lower() or 'gikuyu proverbs' in line.lower():
                    continue
                if line.startswith('10/20/25') or line.startswith('https://'):
                    continue
                if not line or len(line) < 3:
                    continue
                
                # Look for numbered proverbs (e.g., "123. Kikuyu text")
                proverb_match = re.match(r'^(\d+)\.\s+(.+)$', line)
                
                if proverb_match:
                    # Save previous proverb if exists
                    if current_proverb and current_proverb['kikuyu_text']:
                        proverbs.append(current_proverb)
                    
                    # Start new proverb
                    proverb_num = proverb_match.group(1)
                    kikuyu_text = proverb_match.group(2).strip()
                    
                    current_proverb = {
                        'proverb_id': f"GBARRA_{proverb_num.zfill(4)}",
                        'proverb_number': int(proverb_num),
                        'kikuyu_text': kikuyu_text,
                        'english_translation': '',
                        'cultural_meaning': '',
                        'english_equivalent': '',
                        'source': 'Gbarra G. 1939',
                        'page_number': page_num,
                        'extraction_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                elif current_proverb is not None:
                    # This is a continuation line (translation or meaning)
                    # First non-Kikuyu line after proverb is usually English translation
                    if not current_proverb['english_translation']:
                        current_proverb['english_translation'] = line
                    else:
                        # Additional lines are cultural meaning or equivalents
                        if line.lower().startswith('english equivalent:'):
                            current_proverb['english_equivalent'] = line.replace('English equivalent:', '').strip()
                        elif line.lower().startswith('contextual note:'):
                            current_proverb['cultural_meaning'] = line.replace('Contextual note:', '').strip()
                        elif line.lower().startswith('literal translation:'):
                            # Sometimes literal translation comes after initial line
                            if current_proverb['english_translation'] and len(current_proverb['english_translation']) < 50:
                                current_proverb['english_translation'] = line.replace('Literal translation:', '').strip()
                        else:
                            # Append to cultural meaning
                            if current_proverb['cultural_meaning']:
                                current_proverb['cultural_meaning'] += ' ' + line
                            else:
                                # If no cultural meaning yet, this might be continuation of translation
                                if len(current_proverb['english_translation']) < 100:
                                    current_proverb['english_translation'] += ' ' + line
                                else:
                                    current_proverb['cultural_meaning'] = line
        
        # Don't forget the last proverb
        if current_proverb and current_proverb['kikuyu_text']:
            proverbs.append(current_proverb)
    
    print(f"\n✅ Extraction Complete!")
    print(f"   Total proverbs extracted: {len(proverbs)}")
    
    return proverbs


def clean_and_validate_proverbs(proverbs: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Clean extracted proverbs and generate statistics
    """
    print(f"\n🧹 Cleaning and validating {len(proverbs)} proverbs...")
    
    cleaned = []
    stats = {
        'total': len(proverbs),
        'with_kikuyu': 0,
        'with_english': 0,
        'with_meaning': 0,
        'with_equivalent': 0,
        'avg_kikuyu_length': 0,
        'avg_english_length': 0
    }
    
    kikuyu_lengths = []
    english_lengths = []
    
    for p in proverbs:
        # Basic cleaning
        p['kikuyu_text'] = p['kikuyu_text'].strip()
        p['english_translation'] = p['english_translation'].strip()
        p['cultural_meaning'] = p['cultural_meaning'].strip()
        p['english_equivalent'] = p['english_equivalent'].strip()
        
        # Validation
        if p['kikuyu_text']:
            stats['with_kikuyu'] += 1
            kikuyu_lengths.append(len(p['kikuyu_text']))
        
        if p['english_translation']:
            stats['with_english'] += 1
            english_lengths.append(len(p['english_translation']))
        
        if p['cultural_meaning']:
            stats['with_meaning'] += 1
        
        if p['english_equivalent']:
            stats['with_equivalent'] += 1
        
        cleaned.append(p)
    
    if kikuyu_lengths:
        stats['avg_kikuyu_length'] = sum(kikuyu_lengths) / len(kikuyu_lengths)
    if english_lengths:
        stats['avg_english_length'] = sum(english_lengths) / len(english_lengths)
    
    return cleaned, stats


def main():
    """Main extraction pipeline"""
    
    # Configuration
    pdf_path = "data/sources/OPIT_RAI9001_Proverbs_1000_Gikuyu_gbarra.pdf"
    output_path = "data/raw/gbarra_1000_proverbs_extracted.csv"
    log_path = "logs/gbarra_extraction_improved.log"
    
    print("=" * 70)
    print("GBARRA 1000 PROVERB CORPUS EXTRACTION (IMPROVED)")
    print("=" * 70)
    
    # Extract proverbs
    proverbs = extract_proverbs_from_gbarra_pdf(pdf_path)
    
    if not proverbs:
        print("\n❌ No proverbs extracted! Check PDF format.")
        return
    
    # Clean and validate
    cleaned_proverbs, stats = clean_and_validate_proverbs(proverbs)
    
    # Convert to DataFrame
    df = pd.DataFrame(cleaned_proverbs)
    
    # Sort by proverb number
    df = df.sort_values('proverb_number')
    
    # Save to CSV
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n💾 Output saved to: {output_path}")
    
    # Print statistics
    print(f"\n📊 Extraction Statistics:")
    print(f"   Total proverbs: {stats['total']}")
    print(f"   With Kikuyu text: {stats['with_kikuyu']}")
    print(f"   With English translation: {stats['with_english']}")
    print(f"   With cultural meaning: {stats['with_meaning']}")
    print(f"   With English equivalent: {stats['with_equivalent']}")
    print(f"   Avg Kikuyu length: {stats['avg_kikuyu_length']:.1f} chars")
    print(f"   Avg English length: {stats['avg_english_length']:.1f} chars")
    
    # Show first 5 proverbs
    print(f"\n✨ First 5 extracted proverbs:")
    print(df[['proverb_id', 'kikuyu_text', 'english_translation']].head())
    
    print("\n" + "=" * 70)
    print("✅ EXTRACTION COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
