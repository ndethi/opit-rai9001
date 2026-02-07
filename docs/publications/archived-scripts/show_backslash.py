#!/usr/bin/env python3
from docx import Document

doc = Document('thiLLMo_DoCEIS2026_Conference_Paper.docx')
for i, para in enumerate(doc.paragraphs[:20]):
    text = para.text.strip()
    if '\\' in text:
        print(f'Paragraph {i+1}:')
        # Find position of backslash
        idx = text.find('\\')
        start = max(0, idx-20)
        end = min(len(text), idx+30)
        print(f'  ...{text[start:end]}...')
        print()
