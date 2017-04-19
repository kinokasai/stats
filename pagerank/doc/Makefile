NAME ?= report
TEMPL = ../../template.latex

all: $(NAME).pdf

$(NAME).pdf: $(NAME).md $(TEMPL)
	pandoc -s -f markdown+table_captions+definition_lists -t latex --latex-engine=pdflatex --template=$(TEMPL) $< --filter pandoc-fignos -o $@

view: $(NAME).pdf
	mupdf $^

clean:
	rm $(NAME).pdf

.PHONY: view clean
