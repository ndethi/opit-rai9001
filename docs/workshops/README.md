# Workshop Submissions

This directory contains papers and submissions to various workshops and conferences related to the Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation project.

## Structure

Each workshop/conference has its own subdirectory containing:
- LaTeX source files (.tex)
- Generated PDF files (when available)
- Supporting materials (figures, additional documentation)

## Current Submissions

### AfriLang AI 2025
- **Venue**: AI for African Languages Conference 2025: Low Resource Language Workshop
- **Date**: October 10, 2025
- **Location**: Kampala, Uganda
- **Paper**: "Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation"
- **Status**: Prepared for submission

## Building Papers

To compile the LaTeX papers to PDF, ensure you have the required LaTeX packages installed:

```bash
# For the CEUR-WS template (AfriLang AI 2025)
pdflatex kikuyu-proverb-og-rag.tex
bibtex kikuyu-proverb-og-rag
pdflatex kikuyu-proverb-og-rag.tex
pdflatex kikuyu-proverb-og-rag.tex
```

## Dependencies

Papers may require specific LaTeX document classes and packages:
- CEUR-WS template (`ceurart.cls`) for AfriLang AI 2025
- Standard packages: `listings`, etc.

## Notes

- Keep the workshop submission deadlines in mind
- Ensure all papers follow the venue-specific formatting guidelines
- Include proper acknowledgments and ethical considerations as required
