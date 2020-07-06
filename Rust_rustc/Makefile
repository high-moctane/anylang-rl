MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

CARGO := $(HOME)/.cargo/bin/cargo
RUSTC := $(HOME)/.cargo/bin/rustc
SRCS := $(wildcard src/*.rs) $(wildcard src/*/*.rs)
PROG := target/release/rust_rustc

.PHONY: build \
		clean \
		run \
		fig \
		run_maze_qlearning \
		fig_maze_qlearning \
		run_maze_sarsa \
		fig_maze_sarsa \
		run_cartpole_qlearning \
		fig_cartpole_qlearning \
		run_cartpole_sarsa \
		fig_cartpole_sarsa

build: $(PROG) results/version.txt results/lines.txt

results/version.txt:
	@mkdir -p results
	$(RUSTC) --version > $@

results/lines.txt: $(SRCS)
	@mkdir -p results
	$(WC) src/*.rs src/*/*.rs > $@

$(PROG) results/build_time.txt: $(SRCS)
	$(shell mkdir -p results && $(CARGO) check && $(TIME) $(CARGO) build --release 2>&1 > /dev/null | $(TAIL) -n 4 > results/build_time.txt)

clean:
	rm -rf results
	cargo clean

run: run_maze_qlearning run_maze_sarsa run_cartpole_qlearning run_cartpole_sarsa

fig: fig_maze_qlearning fig_maze_sarsa fig_cartpole_qlearning fig_cartpole_sarsa

run_maze_qlearning: $(PROG)
	@mkdir -p results/maze_qlearning
	$(TIME) $(PROG) ../_config/maze_qlearning.env 2> results/maze_qlearning/run_time.txt

fig_maze_qlearning: results/maze_qlearning/route.txt results/maze_qlearning/returns.png

results/maze_qlearning/route.txt: results/maze_qlearning/history.tsv
	$(PYTHON) ../_plotter/maze/main.py $^ > $@

results/maze_qlearning/returns.png: results/maze_qlearning/returns.txt
	$(PYTHON) ../_plotter/learning_curve/main.py $^

run_maze_sarsa: $(PROG)
	@mkdir -p results/maze_sarsa
	$(TIME) $(PROG) ../_config/maze_sarsa.env 2> results/maze_sarsa/run_time.txt

fig_maze_sarsa: results/maze_sarsa/route.txt results/maze_sarsa/returns.png

results/maze_sarsa/route.txt: results/maze_sarsa/history.tsv
	$(PYTHON) ../_plotter/maze/main.py $^ > $@

results/maze_sarsa/returns.png: results/maze_sarsa/returns.txt
	$(PYTHON) ../_plotter/learning_curve/main.py $^

run_cartpole_qlearning: $(PROG)
	@mkdir -p results/cartpole_qlearning
	$(TIME) $(PROG) ../_config/cartpole_qlearning.env 2> results/cartpole_qlearning/run_time.txt

fig_cartpole_qlearning: results/cartpole_qlearning/animation.gif results/cartpole_qlearning/returns.png

results/cartpole_qlearning/animation.gif: results/cartpole_qlearning/history.tsv
	$(PYTHON) ../_plotter/cartpole/main.py $^

results/cartpole_qlearning/returns.png: results/cartpole_qlearning/returns.txt
	$(PYTHON) ../_plotter/learning_curve/main.py $^

run_cartpole_sarsa: $(PROG)
	@mkdir -p results/cartpole_sarsa
	$(TIME) $(PROG) ../_config/cartpole_sarsa.env 2> results/cartpole_sarsa/run_time.txt

fig_cartpole_sarsa: results/cartpole_sarsa/animation.gif results/cartpole_sarsa/returns.png

results/cartpole_sarsa/animation.gif: results/cartpole_sarsa/history.tsv
	$(PYTHON) ../_plotter/cartpole/main.py $^

results/cartpole_sarsa/returns.png: results/cartpole_sarsa/returns.txt
	$(PYTHON) ../_plotter/learning_curve/main.py $^
