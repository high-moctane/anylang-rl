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
	rm -f *.gch
	rm -f main

images: returns.png animation.gif
	@:

states.csv actions.csv rewards.csv returns.csv run_time.txt: main
	$(TIME) ./main 2> run_time.txt

description.txt:
	clang -v 2> description.txt

lines_num.txt: agent.c agent.h env.c env.h experiment.c experiment.h main.c main.h utils.c utils.h
	wc $^ > lines_num.txt

main build_time.txt: *.h *.c
	$(TIME) clang -o main -Ofast *.c 2> build_time.txt

animation.gif: states.csv actions.csv rewards.csv
	python3 $(PWD)/../_plotter/animation.py $(PWD)

returns.png: returns.csv description.txt
	python3 $(PWD)/../_plotter/returns_curve.py $(PWD)