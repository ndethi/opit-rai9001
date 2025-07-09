# Thesis Chapter Files

This directory contains the individual chapter files for the thesis.

## Chapter Structure

- `01-introduction.tex` - Introduction and problem statement
- `02-literature-review.tex` - Comprehensive literature review
- `03-methodology.tex` - Research methodology and approach
- `04-system-design.tex` - System architecture and implementation
- `05-evaluation.tex` - Experimental setup and results
- `06-discussion.tex` - Analysis and interpretation of results
- `07-conclusion.tex` - Conclusions and future work
- `appendices.tex` - Supplementary materials

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

<!-- Test: Fixing AI model detection accuracy and commit message generation -->
