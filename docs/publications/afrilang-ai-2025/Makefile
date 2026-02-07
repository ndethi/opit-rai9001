# Makefile for AfriLang AI 2025 Paper
# Requires LaTeX installation

PAPER = kikuyu-proverb-og-rag
TEX_FILE = $(PAPER).tex
PDF_FILE = $(PAPER).pdf

.PHONY: all clean help

all: $(PDF_FILE)

$(PDF_FILE): $(TEX_FILE)
	@echo "Building $(PDF_FILE)..."
	@if command -v pdflatex >/dev/null 2>&1; then \
		pdflatex -interaction=nonstopmode $(TEX_FILE) && \
		pdflatex -interaction=nonstopmode $(TEX_FILE); \
	else \
		echo "Error: pdflatex not found. Install LaTeX first."; \
		echo "On macOS: brew install --cask mactex"; \
		echo "On Ubuntu/Debian: sudo apt-get install texlive-full"; \
		exit 1; \
	fi

clean:
	@echo "Cleaning auxiliary files..."
	@rm -f *.aux *.log *.out *.toc *.lot *.lof *.blg *.bbl *.fls *.fdb_latexmk

clean-all: clean
	@echo "Cleaning PDF..."
	@rm -f $(PDF_FILE)

help:
	@echo "Available targets:"
	@echo "  all       - Build the PDF (default)"
	@echo "  clean     - Remove auxiliary files"
	@echo "  clean-all - Remove auxiliary files and PDF"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - LaTeX distribution with pdflatex"
	@echo "  - CEUR-WS document class (ceurart.cls)"
