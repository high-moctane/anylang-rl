include $(PWD)/../include.mk

.PHONY: build run clean images sfmt

build: description.txt lines_num.txt build_time.txt main
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
	clang -v 2> description.txt

lines_num.txt: agent.c agent.h env.c env.h experiment.c experiment.h main.c main.h utils.c utils.h
	wc $^ > lines_num.txt

main build_time.txt: *.h *.c
	$(TIME) clang -o main -msse2 -fast -DSFMT_MEXP=19937 *.c 2> build_time.txt

animation.gif: states.csv actions.csv rewards.csv
	python3 $(PWD)/../_plotter/animation.py $(PWD)

returns.png: returns.csv description.txt
	python3 $(PWD)/../_plotter/returns_curve.py $(PWD)

SFMT-src-1.5.1.tar.gz:
	curl http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/SFMT/SFMT-src-1.5.1.tar.gz -o $@

SFMT-src-1.5.1: SFMT-src-1.5.1.tar.gz
	tar -zxvf SFMT-src-1.5.1.tar.gz

sfmt: SFMT-src-1.5.1
	cp SFMT-src-1.5.1/*.h .
	cp SFMT-src-1.5.1/*.c .
	rm test.c