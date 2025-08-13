#!/bin/bash

# Build script for AfriLang AI 2025 paper
# Requires LaTeX installation with pdflatex

set -e

PAPER_NAME="kikuyu-proverb-og-rag"

echo "Building ${PAPER_NAME}.pdf..."

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex not found. Please install a LaTeX distribution (e.g., MacTeX, TeX Live)"
    echo "On macOS: brew install --cask mactex"
    echo "On Ubuntu/Debian: sudo apt-get install texlive-full"
    exit 1
fi

# Check if the source file exists
if [ ! -f "${PAPER_NAME}.tex" ]; then
    echo "Error: ${PAPER_NAME}.tex not found"
    exit 1
fi

# Compile the paper (run twice for proper cross-references)
echo "First compilation pass..."
pdflatex -interaction=nonstopmode "${PAPER_NAME}.tex"

echo "Second compilation pass..."
pdflatex -interaction=nonstopmode "${PAPER_NAME}.tex"

# Clean up auxiliary files
echo "Cleaning up auxiliary files..."
rm -f *.aux *.log *.out *.toc *.lot *.lof *.blg *.bbl

if [ -f "${PAPER_NAME}.pdf" ]; then
    echo "Successfully built ${PAPER_NAME}.pdf"
    echo "File size: $(ls -lh ${PAPER_NAME}.pdf | awk '{print $5}')"
else
    echo "Error: PDF was not generated"
    exit 1
fi
