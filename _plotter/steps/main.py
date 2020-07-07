import matplotlib.pyplot as plt
import numpy as np
import os.path as opath
import sys

ROOT = opath.join(opath.abspath(opath.dirname(__file__)), "..", "..")
OUTPUT_PATH = opath.join(ROOT, "_summary", "steps.png")


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


def parse_lang_name(s):
    elems = s.split("_", 2)
    return elems[0] + "\n(" + elems[1] + ")"


def draw(langs):
    left = np.arange(1, len(langs)+1)
    paths = list(map(language_wc_path, langs))
    values = list(map(parse_wc, paths))
    plt.bar(left, values, tick_label=list(
        map(parse_lang_name, langs)), align="center")
    plt.title("Total Number of Steps")
    plt.ylabel("Steps")


def save():
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    langs = languages(sys.argv)
    draw(langs)
    save()
