MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/include.mk

LANGS := C_GCC \
		Go_go \
		Python3_CPython \
		Python3_PyPy3 \
		Rust_rustc

.PHONY: build \
		run \
		$(foreach lang,$(LANGS),$(foreach task,$(TASKS),run_$(lang)_$(task))) \
		fig \
		$(foreach lang,$(LANGS),$(foreach task,$(TASKS),fig_$(lang)_$(task))) \
		summary

build:
	$(foreach lang,$(LANGS),cd $(lang) && ./docker.sh make build && cd .. &&) true

run: $(foreach lang,$(LANGS),$(foreach task,$(TASKS),run_$(lang)_$(task)))


define RUN_TEMPLATE
run_$(1)_$(2):
	cd $(1) && ./docker.sh make run_$(2)
endef

$(foreach lang,$(LANGS),$(foreach task,$(TASKS),$(eval $(call RUN_TEMPLATE,$(lang),$(task)))))

clean:
	rm -rf _summary
	$(foreach lang,$(LANGS),cd $(lang) && ./docker.sh make clean && cd .. &&) true

fig: summary \
		$(foreach lang,$(LANGS),$(foreach task,$(TASKS),fig_$(lang)_$(task)))

summary: _summary/build_time.png \
			_summary/run_time.png \
			_summary/run_memory.png \
			_summary/steps.png

_summary/build_time.png: $(foreach lang,$(LANGS),$(lang)/results/build_time.txt)
	@mkdir -p _summary
	$(PYTHON) _plotter/build_time/main.py $(LANGS)
	for lang in $(LANGS); do \
		echo $$lang >> _summary/build_time.txt; \
		cat $$lang/results/build_time.txt | $(TAIL) -n 4 >> _summary/build_time.txt; \
		echo "" >> _summary/build_time.txt; \
	done

_summary/run_memory.png:
	@mkdir -p _summary
	$(PYTHON) _plotter/run_memory/main.py $(LANGS)
	for lang in $(LANGS); do \
		echo $$lang >> _summary/run_memory.txt; \
		cat $$lang/results/cartpole_qlearning/run_time.txt | $(TAIL) -n 4 >> _summary/run_memory.txt; \
		echo "" >> _summary/run_memory.txt; \
	done

_summary/run_time.png:
	@mkdir -p _summary
	$(PYTHON) _plotter/run_time/main.py $(LANGS)
	for lang in $(LANGS); do \
		echo $$lang >> _summary/run_time.txt; \
		cat $$lang/results/cartpole_qlearning/run_time.txt | $(TAIL) -n 4 >> _summary/run_time.txt; \
		echo "" >> _summary/run_time.txt; \
	done

_summary/steps.png: $(foreach lang,$(LANGS),$(lang)/results/wc.txt)
	@mkdir -p _summary
	$(PYTHON) _plotter/steps/main.py $(LANGS)
	for lang in $(LANGS); do \
		echo $$lang >> _summary/steps.txt; \
		cat $$lang/results/wc.txt | $(TAIL) -n 4 >> _summary/steps.txt; \
		echo "" >> _summary/steps.txt; \
	done

define FIG_TEMPLATE
fig_$(1)_$(2): $(1)/results/$(2)/learning_curve.png \
	$(if $(findstring maze,$(2)),$(1)/results/$(2)/route.txt,$(1)/results/$(2)/animation.gif) ;
endef

$(foreach lang,$(LANGS),$(foreach task,$(TASKS),$(eval $(call FIG_TEMPLATE,$(lang),$(task)))))



define LEARNING_CURVE
$(1)/results/$(2)/learning_curve.png: $(1)/results/$(2)/returns.txt
	$(PYTHON) _plotter/learning_curve/main.py $(1)/results/$(2)/returns.txt
endef

$(foreach lang,$(LANGS),$(foreach task,$(TASKS),$(eval $(call LEARNING_CURVE,$(lang),$(task)))))


define MAZE_ROUTE
$(1)/results/$(2)/route.txt: $(1)/results/$(2)/history.tsv
	$(PYTHON) _plotter/maze/main.py $(1)/results/$(2)/history.tsv \
		> $(1)/results/$(2)/route.txt
endef

$(foreach lang,$(LANGS),$(foreach task,$(MAZE),$(eval $(call MAZE_ROUTE,$(lang),$(task)))))


define CARTPOLE_GIF
$(1)/results/$(2)/animation.gif: $(1)/results/$(2)/history.tsv
	$(PYTHON) _plotter/cartpole/main.py $(1)/results/$(2)/history.tsv
endef

$(foreach lang,$(LANGS),$(foreach task,$(CARTPOLE),$(eval $(call CARTPOLE_GIF,$(lang),$(task)))))
