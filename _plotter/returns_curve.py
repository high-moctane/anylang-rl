import matplotlib.pyplot as plt
import numpy as np
import os.path as path
import sys


USAGE = """Usage: python3 returns_curve.py LANG_DIR"""
DATA_FNAME = "returns.csv"
DESCRIPTION_FNAME = "description.txt"
IMAGE_FNAME = "returns.png"


def get_lang_dir():
    if len(sys.argv) != 2:
        return None
    return sys.argv[1]


def read_desc(fname):
    buf = ""
    with open(fname) as f:
        buf += f.read()
    return buf.replace("\n", " ")


def read_data(fname):
    with open(fname) as f:
        return list(map(float, f.read().split()))


def plot(data, desc):
    draw(data)
    draw(convolve(data, len(data)//1000))
    plt.xlabel("Episodes")
    plt.ylabel("Returns")
    plt.title(f"Episode-Return graph with {desc}")


def draw(data):
    x = np.arange(1, len(data)+1)
    plt.plot(x, data)


def convolve(data, num):
    return np.convolve(data, np.ones(num)/num, mode="same")[num+1:-num]


def save(fname):
    plt.savefig(fname)


if __name__ == "__main__":
    dir = get_lang_dir()
    if dir is None:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    if not path.isdir(dir):
        print(f"no such directory: {repr(dir)}", file=sys.stderr)
        sys.exit(1)

    try:
        desc = read_desc(path.join(dir, DESCRIPTION_FNAME))
    except Exception as e:
        print(f"desc read error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = read_data(path.join(dir, DATA_FNAME))
    except Exception as e:
        print(f"data read error: {e}", file=sys.stderr)
        sys.exit(1)

    plot(data, desc)
    try:
        save(path.join(dir, IMAGE_FNAME))
    except Exception as e:
        print(f"plot save error: {e}", file=sys.stderr)
        sys.exit(1)
