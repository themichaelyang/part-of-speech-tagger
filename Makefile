.PHONY: clean

SRC = $(wildcard *.md)

all : ${SRC:.md=.pdf}

%.pdf : %.md
				pandoc $*.md --latex-engine=pdflatex -o $*.pdf

clean :
				rm -f *.pdf

