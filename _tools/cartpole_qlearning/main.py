import matplotlib.pyplot as plt
import numpy as np
import os.path as opath
import sys

ROOT = opath.join(opath.abspath(opath.dirname(__file__)), "..", "..")
OUTPUT_PATH = opath.join(ROOT, "_summary", "cartpole_qlearning.png")


def languages(argv):
    return argv[1:]


def language_cartpole_qlearning_path(lang):
    return opath.join(ROOT, lang, "results", "cartpole_qlearning", "time.txt")


def parse_time(path):
    last_line = ""
    with open(path) as f:
        for line in f:
            return float(line.split()[1])


def draw(langs):
    left = np.arange(1, len(langs)+1)
    paths = list(map(language_cartpole_qlearning_path, langs))
    values = list(map(parse_time, paths))
    plt.bar(left, values, tick_label=langs, align="center")
    plt.title("Benchmark of Cartpole (Q-learning)")


def save():
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    langs = languages(sys.argv)
    draw(langs)
    save()
