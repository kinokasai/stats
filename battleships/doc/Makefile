NAME ?= rapport
TEMPL = ../../template.latex

all: $(NAME).pdf

$(NAME).pdf: $(NAME).md $(TEMPL)
	pandoc -s -f markdown+table_captions -t latex --latex-engine=pdflatex --template=$(TEMPL) $< -o $@

view: $(NAME).pdf
	mupdf $^

clean:
	rm $(NAME).pdf

.PHONY: view clean
