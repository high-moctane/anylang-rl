import matplotlib.pyplot as plt
import numpy as np
import os.path as opath
import sys

ROOT = opath.join(opath.abspath(opath.dirname(__file__)), "..", "..")
OUTPUT_PATH = opath.join(ROOT, "_summary", "build_time.png")


def languages(argv):
    return argv[1:]


def language_build_time_path(lang):
    return opath.join(ROOT, lang, "results", "build_time.txt")


def parse_build_time(path):
    with open(path) as f:
        lines = [line.rstrip() for line in f]
    return float(lines[-4].split()[1])


def parse_lang_name(s):
    elems = s.split("_", 2)
    return elems[0] + "\n(" + elems[1] + ")"


def draw(langs):
    left = np.arange(1, len(langs)+1)
    paths = list(map(language_build_time_path, langs))
    values = list(map(parse_build_time, paths))
    plt.bar(left, values, tick_label=list(
        map(parse_lang_name, langs)), align="center")
    plt.ylabel("Seconds")
    plt.title("Build Time")


def save():
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    langs = languages(sys.argv)
    draw(langs)
    save()
