.PHONY: build run clean images

build: description.txt
	@:

run:
	gtime julia main.jl

clean:
	rm -rf animation.gif
	rm -rf returns.png
	rm -rf actions.csv
	rm -rf returns.csv
	rm -rf rewards.csv
	rm -rf states.csv
	rm -rf description.txt

images: returns.png animation.gif
	@:

states.csv actions.csv rewards.csv returns.csv: main.jl cartpoleenv.jl agent.jl experiment.jl
	make run

description.txt:
	julia -v > description.txt

animation.gif: states.csv actions.csv rewards.csv
	python3 $(PWD)/../_plotter/animation.py $(PWD)

returns.png: returns.csv description.txt
	python3 $(PWD)/../_plotter/returns_curve.py $(PWD)

