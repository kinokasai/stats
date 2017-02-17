NAME ?= rapport

all: $(NAME).pdf

$(NAME).pdf: $(NAME).md
	pandoc -f markdown+table_captions -t latex $^ -o $@

view: $(NAME).pdf
	mupdf $^

clean:
	rm $(NAME).pdf

.PHONY: view clean
