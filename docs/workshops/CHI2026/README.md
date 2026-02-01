# CHI 2026 Workshop Paper Compilation Instructions

## Files in this Directory

- `chi2026-workshop-paper.tex` - Main LaTeX source file
- `references.bib` - Bibliography file with all citations
- `CALL_FOR_PARTICIPATION.md` - Workshop call for papers/participation
- `THESIS_ALIGNMENT_ANALYSIS.md` - Analysis of alignment between paper and thesis
- `CHI2026_Workshop_Paper_Watson_Ndethi.docx` - Original Word document (if converting)
- `README.md` - This file

## Prerequisites

To compile the LaTeX paper, you need:

1. **LaTeX Distribution:**
   - macOS: MacTeX (`brew install --cask mactex`)
   - Linux: TeX Live (`sudo apt-get install texlive-full`)
   - Windows: MiKTeX or TeX Live

2. **ACM LaTeX Class:**
   - The `acmart` document class (usually included in modern TeX distributions)
   - If missing: `tlmgr install acmart`

## Compilation Methods

### Method 1: Command Line (Recommended)

```bash
# Navigate to CHI2026 directory
cd /Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/docs/workshops/CHI2026

# Compile (run multiple times for references)
pdflatex chi2026-workshop-paper.tex
bibtex chi2026-workshop-paper
pdflatex chi2026-workshop-paper.tex
pdflatex chi2026-workshop-paper.tex

# Or use latexmk for automatic compilation
latexmk -pdf chi2026-workshop-paper.tex
```

### Method 2: Using Make (if Makefile provided)

```bash
make chi2026-workshop-paper.pdf
```

### Method 3: VS Code LaTeX Workshop Extension

1. Install "LaTeX Workshop" extension in VS Code
2. Open `chi2026-workshop-paper.tex`
3. Save the file (Cmd+S / Ctrl+S)
4. The extension will auto-compile
5. View PDF: Click "View LaTeX PDF" button or Cmd+Option+V

### Method 4: Overleaf (Online)

1. Go to https://www.overleaf.com/
2. Create new project → Upload Project
3. Upload `chi2026-workshop-paper.tex` and `references.bib`
4. Click "Recompile" to generate PDF

## Expected Output

After successful compilation, you should have:
- `chi2026-workshop-paper.pdf` - The compiled workshop paper
- `chi2026-workshop-paper.aux` - Auxiliary file
- `chi2026-workshop-paper.bbl` - Bibliography file
- `chi2026-workshop-paper.blg` - Bibliography log
- `chi2026-workshop-paper.log` - Compilation log

## Troubleshooting

### Common Issues

**1. Missing ACM Class:**
```bash
tlmgr install acmart
```

**2. Bibliography Not Showing:**
- Run `bibtex chi2026-workshop-paper` after first `pdflatex` run
- Then run `pdflatex` twice more

**3. Figure Missing Error:**
- The template includes `\ref{fig:ontology-structure}` but no figure is provided
- Either add the figure or remove the reference

**4. Compilation Errors:**
- Check the `.log` file for detailed error messages
- Ensure all required packages are installed

### Clean Build

To clean auxiliary files and rebuild:
```bash
# Remove auxiliary files
rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot

# Recompile
pdflatex chi2026-workshop-paper.tex
bibtex chi2026-workshop-paper
pdflatex chi2026-workshop-paper.tex
pdflatex chi2026-workshop-paper.tex
```

## Next Steps

### Before Submission

1. **Review Content:**
   - [ ] Check all proverb examples match thesis dataset (MW_001 to MW_100)
   - [ ] Verify statistical results match Chapter 5 of thesis
   - [ ] Ensure cultural explanations are accurate
   - [ ] Add author affiliations and contact info

2. **Add Figures:**
   - [ ] Ontology structure diagram (Fig 1)
   - [ ] System architecture diagram (optional)
   - [ ] Results visualization (optional)

3. **Format Check:**
   - [ ] Confirm ACM CHI 2026 workshop format requirements
   - [ ] Check page limits (typically 4-6 pages for workshop papers)
   - [ ] Verify citation format

4. **Proofreading:**
   - [ ] Grammar and spelling check
   - [ ] Consistent terminology
   - [ ] Clear and concise writing

### Alignment Verification

Use `THESIS_ALIGNMENT_ANALYSIS.md` to verify:
- Proverb examples match thesis evaluation dataset
- Statistical values are exactly as reported in thesis Chapter 5
- Limitations are properly acknowledged
- Community validation is proposed for future work

## Workshop Submission

The "AI Across Cultures @ CHI 2026" workshop is scheduled for **April 2026 in Barcelona, Spain**.

**Contact for workshop:** aiacrosscultures@gmail.com

Check the call for participation for:
- Submission deadline
- Page limits
- Format requirements
- Review process

## Additional Resources

- **Thesis Reference:** `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/docs/thesis/main.tex`
- **Evaluation Results:** `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/data/results/ograg_translations/`
- **Proverb Dataset:** `/Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo/data/results/ograg_evaluation_100proverbs_checkpoint_100.csv`

## Questions or Issues?

If you encounter any compilation issues or need to make changes to the paper:

1. Check the `.log` file for detailed error messages
2. Verify all citations are in `references.bib`
3. Ensure all referenced figures/tables exist or are commented out
4. Review the thesis for accurate data to include

---

**Author:** Charles Watson Ndethi Kibaki  
**Institution:** Open Institute of Technology (OPIT)  
**Program:** MSc in Responsible AI  
**Project:** thiLLMo - Culturally Faithful Kikuyu Proverb Translation
