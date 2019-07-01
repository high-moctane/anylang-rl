MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

.PHONY: all build run clean images

all:
	make description.txt
	make lines_num.txt
	make build_time.txt

build: main
	@:

run: main returns.csv
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
	rm -f main

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
	python3 $(MAKEFILE_DIR)/../_plotter/animation.py $(MAKEFILE_DIR)

returns.png: returns.csv description.txt
	python3 $(MAKEFILE_DIR)/../_plotter/returns_curve.py $(MAKEFILE_DIR)

