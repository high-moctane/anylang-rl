PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

PYTHON := /usr/bin/python3
WC := /usr/bin/wc
TIME := /usr/bin/time -f "Real\t%e\nUser\t%U\nSystem\t%S\nMemory\t%M"
TAIL := /usr/bin/tail

MAZE := maze_qlearning maze_sarsa
CARTPOLE := cartpole_qlearning cartpole_sarsa
TARGETS := $(MAZE) $(CARTPOLE)

RUN_MAZE := $(foreach target,$(MAZE),run_$(target))
RUN_CARTPOLE := $(foreach target,$(CARTPOLE),run_$(target))
RUN := $(RUN_MAZE) $(RUN_CARTPOLE)

FIG_MAZE := $(foreach target,$(MAZE),fig_$(target))
FIG_CARTPOLE := $(foreach target,$(CARTPOLE),fig_$(target))
FIG := $(FIG_MAZE) $(FIG_CARTPOLE)
