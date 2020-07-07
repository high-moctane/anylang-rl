MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(MAKEFILE_DIR)/include.mk

LANGS := Go_go \
		Python3_CPython \
		Python3_PyPy3 \
		Rust_rustc

JOBS=1

.PHONY: build \
		run \
		fig \
		$(foreach lang,$(LANGS),$(foreach task,$(TASKS),fig_$(lang)_$(task)))

define DOCKER_SH
	cd $(1) && ./docker.sh make $(2) -j$(JOBS)

endef

build:
	$(foreach lang,$(LANGS),$(call DOCKER_SH,$(lang),build))

run:
	$(foreach lang,$(LANGS),$(call DOCKER_SH,$(lang),run))

clean:
	$(foreach lang,$(LANGS),$(call DOCKER_SH,$(lang),clean))

fig: $(foreach lang,$(LANGS),$(foreach task,$(TASKS),fig_$(lang)_$(task))) ;


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
