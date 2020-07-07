import matplotlib.pyplot as plt
import numpy as np
import os.path as opath
import sys

ROOT = opath.join(opath.abspath(opath.dirname(__file__)), "..", "..")
OUTPUT_PATH = opath.join(ROOT, "_summary", "run_memory.png")


def languages(argv):
    return argv[1:]


def language_run_memory_path(lang):
    return opath.join(ROOT, lang, "results", "cartpole_qlearning", "run_time.txt")


def parse_run_memory(path):
    with open(path) as f:
        lines = [line.rstrip() for line in f]
    return int(lines[-1].split()[1]) // 1000


def parse_lang_name(s):
    elems = s.split("_", 2)
    return elems[0] + "\n(" + elems[1] + ")"


def draw(langs):
    left = np.arange(1, len(langs)+1)
    paths = list(map(language_run_memory_path, langs))
    values = list(map(parse_run_memory, paths))
    plt.bar(left, values, tick_label=list(
        map(parse_lang_name, langs)), align="center")
    plt.ylabel("Memory [MB]")
    plt.title("Run Memory")


def save():
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    langs = languages(sys.argv)
    draw(langs)
    save()
