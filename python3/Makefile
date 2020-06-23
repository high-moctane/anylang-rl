TIME = /usr/bin/time -p
PYTHON = /usr/local/bin/python3

MAZE_QLEARNING = results/maze_qlearning
MAZE_SARSA = results/maze_sarsa

.PHONY: build clean maze_qlearning maze_sarsa

build: results/version.txt

results/version.txt:
	mkdir -p results
	$(PYTHON) -V > results/version.txt

clean:
	rm -rf results
	rm -rf __pycache__
	rm -rf agent/__pycache__
	rm -rf environment/__pycache__

maze_qlearning: $(MAZE_QLEARNING)/history.tsv $(MAZE_QLEARNING)/qtable.bin $(MAZE_QLEARNING)/returns.txt $(MAZE_QLEARNING)/time.txt
	mkdir -p $(MAZE_QLEARNING)

$(MAZE_QLEARNING)/history.tsv $(MAZE_QLEARNING)/qtable.bin $(MAZE_QLEARNING)/returns.txt $(MAZE_QLEARNING)/time.txt:
	$(TIME) $(PYTHON) main.py ../_settings/maze_qlearning.env 2> $(MAZE_QLEARNING)/time.txt

maze_sarsa: $(MAZE_SARSA)/history.tsv $(MAZE_SARSA)/qtable.bin $(MAZE_SARSA)/returns.txt $(MAZE_SARSA)/time.txt
	mkdir -p $(MAZE_SARSA)

$(MAZE_SARSA)/history.tsv $(MAZE_SARSA)/qtable.bin $(MAZE_SARSA)/returns.txt $(MAZE_SARSA)/time.txt:
	$(TIME) $(PYTHON) main.py ../_settings/maze_sarsa.env 2> $(MAZE_SARSA)/time.txt
