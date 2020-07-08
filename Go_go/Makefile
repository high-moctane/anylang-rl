MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

GO := /usr/local/go/bin/go

SRCS := $(wildcard *.go)
PROG := main

.PHONY: build \
		clean \
		run \
		$(foreach task,$(TASKS),run_$(task)) \
		fig \
		$(foreach task,$(TASKS),fig_$(task))

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

run: $(foreach task,$(TASKS),run_$(task)) ;


define RUN_TEMPLATE
run_$(1):
	@mkdir -p results/$(1)
	$(TIME) ./$(PROG) ../_config/$(1).env 2> results/$(1)/run_time.txt
endef

$(foreach task,$(TASKS),$(eval $(call RUN_TEMPLATE,$(task))))
