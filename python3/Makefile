.PHONY: build clean maze_sarsa maze_qlearning

build:
	mkdir -p result/maze_sarsa
	mkdir -p result/maze_qlearning

clean:
	rm -rf result

maze_sarsa:
	python3 main.py ../_settings/maze_sarsa.env

maze_qlearning:
	python3 main.py ../_settings/maze_qlearning.env

