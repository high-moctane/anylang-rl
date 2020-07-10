MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/../include.mk

GCC := /usr/local/bin/gcc

SRCS := $(wildcard *.c) $(wildcard *.h)
PROG := main

SFMT_VERSION := 1.5.1

.PHONY: build \
		clean \
		run \
		$(foreach task,$(TASKS),run_$(task))

build: SFMT results/version.txt results/wc.txt $(PROG) results/build_time.txt

SFMT:
	wget http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/SFMT/SFMT-src-$(SFMT_VERSION).tar.gz
	tar -xf SFMT-src-$(SFMT_VERSION).tar.gz
	mv SFMT-src-$(SFMT_VERSION) SFMT
	rm SFMT-src-$(SFMT_VERSION).tar.gz

results/version.txt:
	@mkdir -p results
	$(GCC) -v 2> $@

results/wc.txt: $(SRCS)
	@mkdir -p results
	$(WC) $(SRCS) > $@

$(PROG) results/build_time.txt: $(SRCS)
	@mkdir -p results
	$(TIME) $(GCC) -std=c11 -Wall -Ofast -g -msse2 -DSFMT_MEXP=19937 -lm -o $(PROG) $(SRCS) SFMT/SFMT.c 2> results/build_time.txt

clean:
	rm -rf $(PROG)
	rm -rf results
	rm ./*.dSYM
	rm -rf SFMT

run: $(foreach task,$(TASKS),run_$(task))


define RUN_TEMPLATE
run_$(1):
	@mkdir -p results/$(1)
	$(TIME) ./$(PROG) ../_config/$(1).env 2> results/$(1)/run_time.txt
endef

$(foreach task,$(TASKS),$(eval $(call RUN_TEMPLATE,$(task))))
