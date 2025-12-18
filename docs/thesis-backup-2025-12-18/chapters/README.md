# Thesis Chapters

This directory contains the individual chapters of the thesis on **Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation**.

## Chapter Structure

- **Chapter 1**: Introduction - `01-introduction.tex`
- **Chapter 2**: Literature Review - `02-literature-review.tex` ✅ **COMPLETED**
- **Chapter 3**: Methodology - `03-methodology.tex`
- **Chapter 4**: System Design and Implementation - `04-system-design.tex`
- **Chapter 5**: Evaluation and Results - `05-evaluation.tex`
- **Chapter 6**: Discussion - `06-discussion.tex`
- **Chapter 7**: Conclusion and Future Work - `07-conclusion.tex`

## Chapter 2: Literature Review - State of the Art

**Status**: ✅ COMPLETED (August 2025)

The literature review provides a comprehensive State-of-the-Art (SotA) analysis of Ontology-Grounded RAG systems following a three-part argument structure:

### Part I: Current State (2024-2025)
- Contemporary paradigm definition anchored around Microsoft's December 2024 breakthrough
- Technical landscape analysis covering hypergraph-based, GNN-integrated, and multimodal approaches
- Production systems and industry adoption (Microsoft GraphRAG, Neo4j, open-source ecosystem)

### Part II: Historical Evolution
- Pre-OG-RAG foundations and early limitations of traditional RAG
- Breakthrough period analysis with pivotal papers and research streams
- Convergent technologies that enabled current capabilities

### Part III: Future Directions and Critical Gaps
- Resource-intensive ontology construction challenges
- Cross-domain generalization limitations
- Cultural knowledge representation and ethical frameworks
- Emerging opportunities in automated ontology learning and multimodal preservation

### Key Features
- **35+ high-quality references** from top-tier venues (NeurIPS, ACL, EMNLP, AAAI, ICLR)
- **80% from 2024-2025 publications** (state-of-the-art timeframe)
- **Quantitative performance benchmarks** and empirical evidence
- **Critical analysis** beyond mere summarization
- **Interdisciplinary integration** covering AI, cognitive science, ethics, and cultural studies
- **Specific focus** on cultural heritage and low-resource language applications

### Word Count
Approximately **7,500 words** - comprehensive academic treatment suitable for PhD-level thesis

### Compilation
Include in main thesis via: `\input{chapters/02-literature-review}` (already configured in main.tex)

All references are properly formatted in BibLaTeX and included in `references/references.bib`.

## File Naming Convention

To maintain consistency and enable automated processing, all documentation files should follow this semantic naming pattern:

**Format:** `OPIT_[STUDENT_ID]_[AUTHOR_LASTNAME]_[DOC_TYPE]_[VERSION_OR_DATE].[ext]`

### Components:
- **OPIT** - Institution identifier (constant)
- **STUDENT_ID** - Your student ID (e.g., RAI9001)
- **AUTHOR_LASTNAME** - Primary author's last name (e.g., NDETHI)
- **DOC_TYPE** - Document category (see types below)
- **VERSION_OR_DATE** - Either version number (v1, v2) or date (YYYY-MM-DD)
- **ext** - File extension (.tex, .md, .pdf, .docx)

### Document Types:
- `Research_Proposal` - Initial research proposal
- `Progress_Report` - Weekly/monthly progress reports
- `Literature_Review` - Literature review documents
- `Methodology` - Methodology and approach documents
- `System_Design` - Technical design documents
- `Evaluation_Results` - Experimental results and analysis
- `Thesis_Draft` - Thesis chapter drafts
- `Final_Thesis` - Complete thesis document
- `Defense_Presentation` - Defense slides and materials
- `Committee_Submission` - Documents for committee review
- `Supervisor_Meeting` - Meeting notes and agendas

### Examples:
```
OPIT_RAI9001_NDETHI_Research_Proposal_v1.md
OPIT_RAI9001_NDETHI_Progress_Report_2025-01-15.md
OPIT_RAI9001_NDETHI_Thesis_Draft_v3.tex
OPIT_RAI9001_NDETHI_Defense_Presentation_2025-07-20.pdf
OPIT_RAI9001_NDETHI_Literature_Review_2025-02-01.md
```

### Benefits:
- **Automated Processing**: Scripts and AI agents can parse file metadata
- **Version Control**: Clear versioning and dating
- **Organization**: Easy sorting and categorization
- **Collaboration**: Clear authorship and document purpose
- **Archival**: Future-proof identification system

## Writing Guidelines

- Use consistent formatting and citation style
- Include proper figure and table references
- Maintain academic writing standards
- Keep chapters focused and well-structured
- Reference the OPIT template in `../template/` for institutional formatting requirements
- Follow the naming convention above for all new documents
