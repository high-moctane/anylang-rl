TIME = /usr/bin/time -p
PYTHON = /usr/local/bin/python3

.PHONY: build clean run maze_qlearning maze_sarsa

build: results/version.txt

results/version.txt:
	mkdir -p results
	$(PYTHON) -V > results/version.txt

clean:
	rm -rf results
	rm -rf __pycache__
	rm -rf agent/__pycache__
	rm -rf environment/__pycache__

run: build maze_qlearning maze_sarsa

maze_qlearning:
	mkdir -p results/maze_qlearning
	$(TIME) $(PYTHON) main.py ../_settings/maze_qlearning.env 2> results/maze_qlearning/time.txt

maze_sarsa:
	mkdir -p results/maze_sarsa
	$(TIME) $(PYTHON) main.py ../_settings/maze_sarsa.env 2> results/maze_sarsa/time.txt

