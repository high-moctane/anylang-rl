MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

SRCS := $(wildcard *.py)

.PHONY: build \
		clean \
		run \
		$(foreach tasks,$(TASKS),run_$(tasks)) \
		fig \
		$(foreach tasks,$(TASKS),fig_$(tasks))

build: results/version.txt results/wc.txt $(PROG) results/build_time.txt ;

results/version.txt:
	@mkdir -p results
	$(PYTHON) -V > $@

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
	$(TIME) $(PYTHON) main.py ../_config/$(1).env 2> results/$(1)/run_time.txt
endef

$(foreach tasks,$(TASKS),$(eval $(call RUN_TEMPLATE,$(tasks))))
