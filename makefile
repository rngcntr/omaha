all:
	python src/generator.py "Makkaroni Special" "with extra cheese" "trips right" "all front" "wr1 7 in wr2 8 corner wr3 slant wr4 go"
	pdflatex -output-directory gen src-gen/play.tex
