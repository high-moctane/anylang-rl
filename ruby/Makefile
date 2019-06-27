include $(PWD)/../include.mk

RUBY = /usr/local/opt/ruby/bin/ruby

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

images: returns.png animation.gif
	@:

states.csv actions.csv rewards.csv returns.csv run_time.txt: *.rb
	$(TIME) $(RUBY) main.rb 2> run_time.txt

description.txt:
	$(RUBY) -v > description.txt

lines_num.txt: *.rb
	wc *.rb > lines_num.txt

build_time.txt:
	$(TIME) true 2> build_time.txt

animation.gif: states.csv actions.csv rewards.csv
	python3 $(PWD)/../_plotter/animation.py $(PWD)

returns.png: returns.csv description.txt
	python3 $(PWD)/../_plotter/returns_curve.py $(PWD)

