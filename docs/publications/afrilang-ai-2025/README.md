# AfriLang AI 2025 Workshop Submission

## Conference Details
- **Full Name**: AI for African Languages Conference 2025: Low Resource Language Workshop
- **Date**: October 10, 2025
- **Location**: Kampala, Uganda
- **Paper Title**: "Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation"

## Files in this Directory
- `kikuyu-proverb-og-rag.tex` - Main LaTeX source file (well-formatted and ready for submission)
- `README.md` - This documentation file
- `Makefile` - Build automation for when LaTeX is available
- `build.sh` - Shell script for building PDF when LaTeX is available

## Paper Abstract
Proverb translation for low-resource languages like Kikuyu presents unique challenges that extend beyond conventional machine translation approaches, requiring deep cultural understanding and contextual preservation. This work presents an ongoing research project developing an Ontology-Grounded Retrieval Augmented Generation (OG-RAG) system for culturally faithful Kikuyu-to-English proverb translation.

## Key Contributions
1. Novel application of Ontology-Grounded RAG to cultural preservation
2. Community-centered development methodology for AI systems
3. Ethical framework for cultural knowledge representation
4. Proof-of-concept system for Kikuyu proverb translation

## Building the Paper

The LaTeX source file is well-formatted and ready for compilation when LaTeX becomes available.

### Prerequisites
- LaTeX distribution with `pdflatex`
- CEUR-WS document class (`ceurart.cls`)
- Required packages: `listings`

### Compilation Options

**Using Makefile:**
```bash
make          # Build PDF
make clean    # Remove auxiliary files
make help     # Show available targets
```

**Using build script:**
```bash
./build.sh
```

**Manual compilation:**
```bash
pdflatex kikuyu-proverb-og-rag.tex
pdflatex kikuyu-proverb-og-rag.tex  # Run twice for proper references
```

## Submission Status
- **Status**: Prepared for submission
- **Target Deadline**: TBD (check workshop website)
- **Submission System**: TBD

## Author Information
- **Author**: Charles Watson Ndethi Kibaki
- **Affiliation**: Open Institute of Technology (OPIT), MSc in Responsible AI Program
- **Email**: charles.kibaki@opit.example
- **GitHub**: https://github.com/charleskibaki/kikuyu-proverb-og-rag

## Workshop Website
Check the official workshop website for submission guidelines and deadlines.

## Notes
- This paper represents work in progress, with expected completion by October 2025
- Emphasizes ethical AI development and community ownership
- Includes declaration on generative AI usage as required by CEUR-WS
