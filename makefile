all:
	python src/generator.py
	pdflatex -output-directory gen src-gen/play.tex
