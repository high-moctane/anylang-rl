PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

PYTHON := /usr/bin/python3
WC := /usr/bin/wc
TIME := /usr/bin/time -f "Real\t%e\nUser\t%U\nSystem\t%S\nMemory\t%M"
TAIL := /usr/bin/tail

MAZE := maze_qlearning maze_sarsa
CARTPOLE := cartpole_qlearning cartpole_sarsa
TASKS := $(MAZE) $(CARTPOLE)
