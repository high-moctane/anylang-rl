MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

GO := /usr/local/go/bin/go

SRCS := $(wildcard *.go)
PROG := main

.PHONY: build \
		clean \
		run \
		$(foreach target,$(TARGETS),run_$(target)) \
		fig \
		$(foreach target,$(TARGETS),fig_$(target))

build: results/version.txt results/wc.txt $(PROG) results/build_time.txt ;

results/version.txt:
	@mkdir -p results
	$(GO) version > $@

results/wc.txt: $(SRCS)
	@mkdir -p results
	$(WC) $(SRCS) > $@

$(PROG) results/build_time.txt: $(SRCS)
	@mkdir -p results
	$(TIME) $(GO) build -o $(PROG) 2> results/build_time.txt

clean:
	rm -rf $(PROG)
	rm -rf results

run: $(RUN) ;

define RUN_TEMPLATE
run_$(1): $(PROG)
	@mkdir -p results/$(1)
	$(TIME) ./$(PROG) ../_config/$(1).env 2> results/$(1)/run_time.txt
endef
$(foreach target,$(TARGETS),$(eval $(call RUN_TEMPLATE,$(target))))

fig: $(FIG) ;

define FIG_MAZE_TEMPLATE
fig_$(1): results/$(1)/learning_curve.png results/$(1)/route.txt ;
endef
$(foreach target,$(MAZE),$(eval $(call FIG_MAZE_TEMPLATE,$(target))))

define LEARNING_CURVE
results/$(1)/learning_curve.png: results/$(1)/returns.txt
	$(PYTHON) ../_plotter/learning_curve/main.py results/$(1)/returns.txt
endef
$(foreach target,$(TARGETS),$(eval $(call LEARNING_CURVE,$(target))))

define ROUTE_TEMPLATE
results/$(1)/route.txt: results/$(1)/history.tsv
	$(PYTHON) ../_plotter/maze/main.py results/$(1)/history.tsv > results/$(1)/route.txt
endef
$(foreach target,$(TARGETS),$(eval $(call ROUTE_TEMPLATE,$(target))))

define FIG_CARTPOLE_TEMPLATE
fig_$(1): results/$(1)/learning_curve.png results/$(1)/animation.gif ;
endef
$(foreach target,$(CARTPOLE),$(eval $(call FIG_CARTPOLE_TEMPLATE,$(target))))

define ANIMATION_TEMPLATE
results/$(1)/animation.gif: results/$(1)/history.tsv
	$(PYTHON) ../_plotter/cartpole/main.py results/$(1)/history.tsv
endef
$(foreach target,$(CARTPOLE),$(eval $(call ANIMATION_TEMPLATE,$(target))))
