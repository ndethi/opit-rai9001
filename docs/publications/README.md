# Publications & Conference Papers

This directory contains papers and submissions to conferences, workshops, and journals related to the thiLLMo project: Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation.

## Structure

Each venue has its own subdirectory containing:
- LaTeX source files (.tex)
- Generated PDF files (when available)
- Supporting materials (figures, additional documentation)
- Venue-specific guidelines and submission checklists

## Current Publications

### DoCEIS 2026 (In Progress)
- **Venue**: 17th DoCEIS - Doctoral Conference on Computing, Electrical and Industrial Systems
- **Type**: Conference (Regular Paper, 12-16 pages)
- **Date**: June 17-19, 2026
- **Location**: Lisbon, Portugal
- **Status**: Full paper in preparation (deadline: February 13, 2026)
- **Theme**: Technological Innovation to Tackle Societal Challenges
- **Publication**: Springer IFIP AICT series (indexed in Web of Science, SCOPUS, DBLP)

### CHI 2026
- **Venue**: ACM CHI Conference on Human Factors in Computing Systems
- **Type**: Conference Workshop Paper
- **Date**: 2026
- **Status**: Prepared

### AfriLang AI 2025
- **Venue**: AI for African Languages Conference 2025: Low Resource Language Workshop
- **Type**: Workshop Paper
- **Date**: October 10, 2025
- **Location**: Kampala, Uganda
- **Status**: Submitted

## Building Papers

### DoCEIS 2026
```bash
cd doceis2026
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### AfriLang AI 2025
```bash
cd afrilang-ai-2025
pdflatex kikuyu-proverb-og-rag.tex
bibtex kikuyu-proverb-og-rag
pdflatex kikuyu-proverb-og-rag.tex
pdflatex kikuyu-proverb-og-rag.tex
```

## Dependencies

Papers require specific LaTeX document classes and packages:
- **Springer LNCS** (`llncs.cls`) for DoCEIS 2026
- **CEUR-WS** template (`ceurart.cls`) for AfriLang AI 2025
- Standard packages: `graphicx`, `amsmath`, `booktabs`, `hyperref`, etc.

## Important Notes

- **Double-blind review**: DoCEIS 2026 requires anonymization (see WRITING_GUIDE.md in doceis2026/)
- **Deadlines**: Check individual venue directories for submission deadlines
- **Formatting**: Ensure all papers follow venue-specific formatting guidelines
- **Open Science**: All code, ontology, and evaluation corpus are open-source
