TIME = /usr/bin/time -p
WC = /usr/bin/wc
PYTHON = /usr/local/bin/python3
PYPY = /usr/local/bin/pypy3

.PHONY: build \
	clean \
	run \
	fig \
	maze_qlearning \
	maze_qlearning_fig \
	maze_sarsa \
	maze_sarsa_fig \
	pendulum_qlearning \
	pendulum_qlearning_fig \
	pendulum_sarsa \
	pendulum_sarsa_fig

build: results/version.txt results/time.txt results/wc.txt

results/version.txt:
	mkdir -p results
	$(PYPY) -V > $@

results/time.txt:
	$(TIME) $(TIME) 2> $@

results/wc.txt:
	wc *.py */*.py > $@

clean:
	rm -rf results
	rm -rf __pycache__
	rm -rf agent/__pycache__
	rm -rf environment/__pycache__

run: maze_qlearning maze_sarsa pendulum_qlearning pendulum_sarsa

fig: maze_qlearning_fig maze_sarsa_fig pendulum_qlearning_fig pendulum_sarsa_fig

maze_qlearning:
	mkdir -p results/maze_qlearning
	$(TIME) $(PYPY) main.py ../_settings/maze_qlearning.env 2> results/maze_qlearning/time.txt

maze_qlearning_fig: results/maze_qlearning/route.txt results/maze_qlearning/returns.png

results/maze_qlearning/route.txt: results/maze_qlearning/history.tsv
	$(PYTHON) ../_tools/maze/visualizer/main.py $^ > $@

results/maze_qlearning/returns.png: results/maze_qlearning/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^

maze_sarsa:
	mkdir -p results/maze_sarsa
	$(TIME) $(PYPY) main.py ../_settings/maze_sarsa.env 2> results/maze_sarsa/time.txt

maze_sarsa_fig: results/maze_sarsa/route.txt results/maze_sarsa/returns.png

results/maze_sarsa/route.txt: results/maze_sarsa/history.tsv
	$(PYTHON) ../_tools/maze/visualizer/main.py $^ > $@

results/maze_sarsa/returns.png: results/maze_sarsa/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^

pendulum_qlearning:
	mkdir -p results/pendulum_qlearning
	$(TIME) $(PYPY) main.py ../_settings/pendulum_qlearning.env 2> results/pendulum_qlearning/time.txt

pendulum_qlearning_fig: results/pendulum_qlearning/animation.gif results/pendulum_qlearning/returns.png

results/pendulum_qlearning/animation.gif: results/pendulum_qlearning/history.tsv
	$(PYTHON) ../_tools/pendulum/visualizer/main.py $^

results/pendulum_qlearning/returns.png: results/pendulum_qlearning/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^

pendulum_sarsa:
	mkdir -p results/pendulum_sarsa
	$(TIME) $(PYPY) main.py ../_settings/pendulum_sarsa.env 2> results/pendulum_sarsa/time.txt

pendulum_sarsa_fig: results/pendulum_sarsa/animation.gif results/pendulum_sarsa/returns.png

results/pendulum_sarsa/animation.gif: results/pendulum_sarsa/history.tsv
	$(PYTHON) ../_tools/pendulum/visualizer/main.py $^

results/pendulum_sarsa/returns.png: results/pendulum_sarsa/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^