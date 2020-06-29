LANGS = pypy3 python3 rust
PYTHON = /usr/local/bin/python3

.PHONY: build clean

build: _summary/build_time.png \
	_summary/build_time.txt \
	_summary/number_of_lines.png \
	_summary/number_of_lines.txt \
	_summary/cartpole_qlearning.png \
	_summary/cartpole_qlearning.txt

_summary/build_time.png:
	mkdir -p _summary
	$(PYTHON) _tools/build_time/main.py $(LANGS)

_summary/build_time.txt:
	mkdir -p _summary
	@echo "generating $@"
	@for lang in $(LANGS); do \
		echo $$lang >> $@ && \
		cat $$lang/results/time.txt >> $@ && \
		echo "" >> $@; \
	done

_summary/number_of_lines.png:
	mkdir -p _summary
	$(PYTHON) _tools/number_of_lines/main.py $(LANGS)

_summary/number_of_lines.txt:
	mkdir -p _summary
	@echo "generating $@"
	@for lang in $(LANGS); do \
		echo $$lang >> $@ && \
		cat $$lang/results/wc.txt >> $@ && \
		echo "" >> $@; \
	done

_summary/cartpole_qlearning.png:
	mkdir -p _summary
	$(PYTHON) _tools/cartpole_qlearning/main.py $(LANGS)

_summary/cartpole_qlearning.txt:
	mkdir -p _summary
	@echo "generating $@"
	@for lang in $(LANGS); do \
		echo $$lang >> $@ && \
		cat $$lang/results/cartpole_qlearning/time.txt >> $@ && \
		echo "" >> $@; \
	done

clean:
	rm -rf _summary
