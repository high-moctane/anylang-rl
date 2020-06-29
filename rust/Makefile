MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

CARGO := $(HOME)/.cargo/bin/cargo
RUSTC := $(HOME)/.cargo/bin/rustc
PROG := target/release/rust
SRCS := $(wildcard src/*.rs) $(wildcard src/*/*.rs)

.PHONY: build \
	clean \
	run \
	fig \
	maze_qlearning \
	maze_qlearning_fig \
	maze_sarsa \
	maze_sarsa_fig \
	cartpole_qlearning \
	cartpole_qlearning_fig \
	cartpole_sarsa \
	cartpole_sarsa_fig

build: results/version.txt results/time.txt results/wc.txt

results/version.txt:
	mkdir -p results
	$(RUSTC) --version > $@

results/time.txt: $(SRCS)
	$(TIME) $(CARGO) build
	$(shell $(TIME) $(CARGO) build --release 2>&1 > $(NULL) | $(TAIL) -n 3 > $@)

results/wc.txt:
	wc  src/*.rs src/*/*.rs > $@

clean:
	rm -rf results
	rm -rf __pycache__
	rm -rf agent/__pycache__
	rm -rf environment/__pycache__
	cargo clean

run: maze_qlearning maze_sarsa cartpole_qlearning cartpole_sarsa

fig: maze_qlearning_fig maze_sarsa_fig cartpole_qlearning_fig cartpole_sarsa_fig

maze_qlearning:
	mkdir -p results/maze_qlearning
	$(TIME) $(PROG) ../_settings/maze_qlearning.env 2> results/maze_qlearning/time.txt

maze_qlearning_fig: results/maze_qlearning/route.txt results/maze_qlearning/returns.png

results/maze_qlearning/route.txt: results/maze_qlearning/history.tsv
	$(PYTHON) ../_tools/maze/visualizer/main.py $^ > $@

results/maze_qlearning/returns.png: results/maze_qlearning/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^

maze_sarsa:
	mkdir -p results/maze_sarsa
	$(TIME) $(PROG) ../_settings/maze_sarsa.env 2> results/maze_sarsa/time.txt

maze_sarsa_fig: results/maze_sarsa/route.txt results/maze_sarsa/returns.png

results/maze_sarsa/route.txt: results/maze_sarsa/history.tsv
	$(PYTHON) ../_tools/maze/visualizer/main.py $^ > $@

results/maze_sarsa/returns.png: results/maze_sarsa/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^

cartpole_qlearning:
	mkdir -p results/cartpole_qlearning
	$(TIME) $(PROG) ../_settings/cartpole_qlearning.env 2> results/cartpole_qlearning/time.txt

cartpole_qlearning_fig: results/cartpole_qlearning/animation.gif results/cartpole_qlearning/returns.png

results/cartpole_qlearning/animation.gif: results/cartpole_qlearning/history.tsv
	$(PYTHON) ../_tools/cartpole/visualizer/main.py $^

results/cartpole_qlearning/returns.png: results/cartpole_qlearning/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^

cartpole_sarsa:
	mkdir -p results/cartpole_sarsa
	$(TIME) $(PROG) ../_settings/cartpole_sarsa.env 2> results/cartpole_sarsa/time.txt

cartpole_sarsa_fig: results/cartpole_sarsa/animation.gif results/cartpole_sarsa/returns.png

results/cartpole_sarsa/animation.gif: results/cartpole_sarsa/history.tsv
	$(PYTHON) ../_tools/cartpole/visualizer/main.py $^

results/cartpole_sarsa/returns.png: results/cartpole_sarsa/returns.txt
	$(PYTHON) ../_tools/learning_curve/main.py $^