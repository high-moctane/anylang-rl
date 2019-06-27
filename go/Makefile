include $(PWD)/../include.mk

.PHONY: build run clean images

build: description.txt lines_num.txt build_time.txt
	@:

run: build_time.txt run_time.txt
	@:

clean:
	rm -rf animation.gif
	rm -rf returns.png
	rm -rf actions.csv
	rm -rf returns.csv
	rm -rf rewards.csv
	rm -rf states.csv
	rm -rf description.txt
	rm -rf build_time.txt
	rm -rf lines_num.txt
	rm -rf run_time.txt
	rm -rf main

images: returns.png animation.gif
	@:

states.csv actions.csv rewards.csv returns.csv run_time.txt: main
	$(TIME) ./main 2> run_time.txt

description.txt:
	go version > description.txt

lines_num.txt: *.go
	wc *.go > lines_num.txt

main build_time.txt: *.go
	$(TIME) go build -o main 2> build_time.txt

animation.gif: states.csv actions.csv rewards.csv
	python3 $(PWD)/../_plotter/animation.py $(PWD)

returns.png: returns.csv description.txt
	python3 $(PWD)/../_plotter/returns_curve.py $(PWD)
