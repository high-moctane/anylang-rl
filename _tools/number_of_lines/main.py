import matplotlib.pyplot as plt
import numpy as np
import os.path as opath
import sys

ROOT = opath.join(opath.abspath(opath.dirname(__file__)), "..", "..")
OUTPUT_PATH = opath.join(ROOT, "_summary", "number_of_lines.png")


def languages(argv):
    return argv[1:]


def language_wc_path(lang):
    return opath.join(ROOT, lang, "results", "wc.txt")


def parse_wc(path):
    last_line = ""
    with open(path) as f:
        for line in f:
            if line:
                last_line = line
    return int(last_line.split()[0])


def draw(langs):
    left = np.arange(1, len(langs)+1)
    paths = list(map(language_wc_path, langs))
    values = list(map(parse_wc, paths))
    plt.bar(left, values, tick_label=langs, align="center")


def save():
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    langs = languages(sys.argv)
    draw(langs)
    save()
