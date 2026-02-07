#!/usr/bin/env python3
from docx import Document

doc = Document('thiLLMo_DoCEIS2026_Conference_Paper.docx')
print('=== WORD DOCUMENT SAMPLE ===\n')

count = 0
for para in doc.paragraphs[:30]:
    text = para.text.strip()
    if text and count < 15:
        print(f'{text}\n')
        count += 1
