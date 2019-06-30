include $(PWD)/../include.mk

.PHONY: all build run clean images

all:
	make description.txt
	make lines_num.txt
	make build_time.txt

build:
	@:

run: returns.csv
	@:

clean:
	rm -f animation.gif
	rm -f returns.png
	rm -f actions.csv
	rm -f returns.csv
	rm -f rewards.csv
	rm -f states.csv
	rm -f description.txt
	rm -f build_time.txt
	rm -f lines_num.txt
	rm -f run_time.txt

images: returns.png animation.gif
	@:

states.csv actions.csv rewards.csv returns.csv run_time.txt: *.py
	$(TIME) python3 -B main.py 2> run_time.txt

description.txt:
	python3 -V > description.txt

lines_num.txt: *.py
	wc *.py > lines_num.txt

build_time.txt:
	$(TIME) true 2> build_time.txt

animation.gif: states.csv actions.csv rewards.csv
	python3 $(PWD)/../_plotter/animation.py $(PWD)

returns.png: returns.csv description.txt
	python3 $(PWD)/../_plotter/returns_curve.py $(PWD)

