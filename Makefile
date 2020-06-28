LANGS = pypy3 python3
PYTHON = /usr/local/bin/python3

.PHONY: build clean

build: _summary/build_time.png \
	_summary/build_time.txt \
	_summary/number_of_lines.png \
	_summary/number_of_lines.txt \
	_summary/pendulum_qlearning.png \
	_summary/pendulum_qlearning.txt

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

_summary/pendulum_qlearning.png:
	mkdir -p _summary
	$(PYTHON) _tools/pendulum_qlearning/main.py $(LANGS)

_summary/pendulum_qlearning.txt:
	mkdir -p _summary
	@echo "generating $@"
	@for lang in $(LANGS); do \
		echo $$lang >> $@ && \
		cat $$lang/results/pendulum_qlearning/time.txt >> $@ && \
		echo "" >> $@; \
	done

clean:
	rm -rf _summary
