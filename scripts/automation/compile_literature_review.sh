#!/bin/bash
cd /Users/ndethi/dev/opit/opit-rai9001/docs/thesis/chapters
echo "Compiling LaTeX document..."
pdflatex -interaction=nonstopmode 02-literature-review-simple.tex
echo "Compilation finished."
ls -la *.pdf
