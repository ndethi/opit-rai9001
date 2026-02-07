#!/usr/bin/env python3
"""Convert PDF to clean Markdown for Google Docs."""

import pdfplumber
import re

def clean_text(text):
    """Clean up extracted text."""
    # Fix hyphenation at line breaks
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2 ', text)
    
    # Add space between words that are stuck together (common in PDF extraction)
    # This regex adds space between lowercase and uppercase letters
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common ligatures and special characters
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬂ', 'fl')
    text = text.replace('ﬀ', 'ff')
    text = text.replace('ﬃ', 'ffi')
    text = text.replace('ﬄ', 'ffl')
    text = text.replace('–', '-')
    text = text.replace('—', '--')
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('"', '"')
    text = text.replace('"', '"')
    text = text.replace('¡', '<')
    
    # Clean up repeated spaces
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

def extract_pdf_to_markdown(pdf_path, output_path):
    """Extract text from PDF and format as Markdown."""
    
    with pdfplumber.open(pdf_path) as pdf:
        markdown_lines = []
        markdown_lines.append("# thiLLMo: Ontology-Grounded RAG for Culturally Faithful Kikuyu-English Proverb Translation\n\n")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}...")
            text = page.extract_text()
            
            if text:
                # Clean the text
                text = clean_text(text)
                
                # Skip page numbers and headers
                lines = text.split('\n')
                filtered_lines = []
                
                for line in lines:
                    line = line.strip()
                    # Skip page numbers, headers, footers
                    if line and not re.match(r'^\d+$', line):
                        filtered_lines.append(line)
                
                # Join and add to markdown
                page_text = '\n\n'.join(filtered_lines)
                markdown_lines.append(page_text)
                markdown_lines.append('\n\n')
    
    # Combine all text
    full_text = ''.join(markdown_lines)
    
    # Post-process to add markdown formatting
    # Identify and format section headings (numbered sections)
    full_text = re.sub(r'\n(\d+\.?\s+[A-Z][^\n]+)\n', r'\n## \1\n\n', full_text)
    
    # Identify subsections
    full_text = re.sub(r'\n(\d+\.\d+\.?\s+[A-Z][^\n]+)\n', r'\n### \1\n\n', full_text)
    
    # Format Abstract
    full_text = re.sub(r'\nAbstract\s*\n', r'\n## Abstract\n\n', full_text)
    
    # Format References
    full_text = re.sub(r'\nReferences\s*\n', r'\n## References\n\n', full_text)
    
    # Clean up excessive newlines
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"\n✓ Markdown created: {output_path}")
    print(f"  Ready to copy into Google Docs!")
    
    return output_path

if __name__ == '__main__':
    extract_pdf_to_markdown('main.pdf', 'thiLLMo_DoCEIS2026_Conference_Paper.md')
