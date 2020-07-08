MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

RUSTC := /usr/local/cargo/bin/rustc
CARGO := /usr/local/cargo/bin/cargo

SRCS := $(wildcard src/*.rs src/*/*.rs)
PROG := target/release/rust_rustc

.PHONY: build \
		clean \
		run \
		$(foreach task,$(TASKS),run_$(task))

build: results/version.txt results/wc.txt $(PROG) results/build_time.txt ;

results/version.txt:
	@mkdir -p results
	$(RUSTC) --version > $@

results/wc.txt: $(SRCS)
	@mkdir -p results
	$(WC) $(SRCS) > $@

$(PROG) results/build_time.txt: $(SRCS)
	@mkdir -p results
	$(CARGO) check
	$(TIME) $(CARGO) build --release 2> results/build_time.txt

clean:
	rm -rf results
	$(CARGO) clean

run: $(foreach task,$(TASKS),run_$(task)) ;


define RUN_TEMPLATE
run_$(1):
	@mkdir -p results/$(1)
	$(TIME) ./$(PROG) ../_config/$(1).env 2> results/$(1)/run_time.txt
endef
$(foreach task,$(TASKS),$(eval $(call RUN_TEMPLATE,$(task))))
