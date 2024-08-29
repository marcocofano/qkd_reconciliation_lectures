# Do not modify this file, it is common to all the LaTeX projects
# If you don't need the bibliography, you can use the \nocite{*} command

DOCNAME=main

all: report

.PHONY: clean

report:
	pdflatex $(DOCNAME).tex
	bibtex $(DOCNAME).aux
	pdflatex $(DOCNAME).tex
	pdflatex $(DOCNAME).tex

view: report
	open $(DOCNAME).pdf

clean:
	rm lectures/*.aux
	rm *.blg *.bbl *.aux *.log *.pdf *.out *.fdb_latexmk *.fls *.toc
