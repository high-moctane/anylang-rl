MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

PYPY := /usr/local/pypy3/bin/pypy3

SRCS := $(wildcard *.py)

.PHONY: build \
		clean \
		run \
		$(foreach task,$(TASKS),run_$(task))

build: results/version.txt results/wc.txt $(PROG) results/build_time.txt ;

results/version.txt:
	@mkdir -p results
	$(PYPY) -V > $@

results/wc.txt: $(SRCS)
	@mkdir -p results
	$(WC) $(SRCS) > $@

results/build_time.txt: $(SRCS)
	@mkdir -p results
	$(TIME) echo "" 2> results/build_time.txt

clean:
	rm -rf __pycache__ */__pycache__
	rm -rf results

run: $(foreach task,$(TASKS),run_$(task)) ;

define RUN_TEMPLATE
run_$(1):
	@mkdir -p results/$(1)
	$(TIME) $(PYPY) main.py ../_config/$(1).env 2> results/$(1)/run_time.txt
endef

$(foreach task,$(TASKS),$(eval $(call RUN_TEMPLATE,$(task))))
