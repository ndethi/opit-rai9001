#!/usr/bin/env python3
"""
Extract Gikuyu Proverbs from Gbarra 1000 Proverbs PDF

This script extracts proverbs from the "1000 Gikuyu Proverbs" PDF by Gbarra.
Each proverb follows the pattern:
  Number. Kikuyu text – English translation
  Cultural explanation/context

Author: thiLLMo Project
Date: October 2025
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path
from datetime import datetime

def extract_proverbs_from_gbarra_pdf(pdf_path, output_path):
    """
    Extract proverbs from Gbarra's 1000 Proverbs PDF
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path for output CSV file
    
    Returns:
        DataFrame with extracted proverbs
    """
    
    proverbs = []
    current_proverb = None
    
    print(f"Opening PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            if page_num % 10 == 0:
                print(f"Processing page {page_num}...")
            
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Pattern: Number. Kikuyu text – English translation
                # Look for lines starting with a number followed by period
                match = re.match(r'^(\d+)\.\s*(.+?)\s*[–—-]\s*(.+?)$', line)
                
                if match:
                    # Save previous proverb if exists
                    if current_proverb:
                        proverbs.append(current_proverb)
                    
                    # Start new proverb
                    proverb_num = match.group(1)
                    kikuyu_text = match.group(2).strip()
                    english_text = match.group(3).strip()
                    
                    current_proverb = {
                        'proverb_id': f'GBARRA_{proverb_num.zfill(4)}',
                        'proverb_number': int(proverb_num),
                        'kikuyu_text': kikuyu_text,
                        'english_translation': english_text,
                        'cultural_meaning': '',
                        'source': 'Gbarra G. 1939',
                        'page_number': page_num,
                        'extraction_date': datetime.now().strftime('%Y-%m-%d')
                    }
                
                # If we have a current proverb and this line doesn't start a new one,
                # it might be cultural context/explanation
                elif current_proverb and not re.match(r'^\d+\.', line):
                    # Add to cultural meaning if line seems substantive
                    if len(line) > 20 and not line.isupper():
                        if current_proverb['cultural_meaning']:
                            current_proverb['cultural_meaning'] += ' ' + line
                        else:
                            current_proverb['cultural_meaning'] = line
        
        # Don't forget the last proverb
        if current_proverb:
            proverbs.append(current_proverb)
    
    # Create DataFrame
    df = pd.DataFrame(proverbs)
    
    # Clean up text
    df['kikuyu_text'] = df['kikuyu_text'].str.strip()
    df['english_translation'] = df['english_translation'].str.strip()
    df['cultural_meaning'] = df['cultural_meaning'].str.strip()
    
    # Remove empty proverbs
    df = df[df['kikuyu_text'].str.len() > 0]
    
    # Save to CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n✅ Extraction Complete!")
    print(f"Total proverbs extracted: {len(df)}")
    print(f"Output saved to: {output_path}")
    
    # Quick statistics
    print(f"\nQuick Statistics:")
    print(f"- Avg Kikuyu text length: {df['kikuyu_text'].str.len().mean():.0f} characters")
    print(f"- Avg English translation length: {df['english_translation'].str.len().mean():.0f} characters")
    print(f"- Proverbs with cultural meaning: {(df['cultural_meaning'].str.len() > 0).sum()}")
    print(f"- Pages covered: {df['page_number'].min()} to {df['page_number'].max()}")
    
    return df

if __name__ == "__main__":
    import sys
    
    # Paths
    pdf_path = "data/sources/OPIT_RAI9001_Proverbs_1000_Gikuyu_gbarra.pdf"
    output_path = "data/raw/gbarra_1000_proverbs_raw.csv"
    
    # Allow command line override
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    print("="*60)
    print("Gbarra 1000 Proverbs Extraction Script")
    print("="*60)
    print(f"Input PDF: {pdf_path}")
    print(f"Output CSV: {output_path}")
    print("="*60)
    
    try:
        df = extract_proverbs_from_gbarra_pdf(pdf_path, output_path)
        
        print("\n✨ First 3 extracted proverbs:")
        print(df[['proverb_id', 'kikuyu_text', 'english_translation']].head(3).to_string())
        
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
