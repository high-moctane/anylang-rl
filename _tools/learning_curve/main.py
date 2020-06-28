import matplotlib.pyplot as plt
import os.path as opath
import sys
import numpy as np

USAGE = "Usage: python main.py path/to/returns.txt description"
OUTPUT_FNAME = "returns.png"
TITLE = "Learning Curve"


def run(argv):
    returns_file = parse_args(argv)
    returns = read_returns(returns_file)
    plot(returns)
    save(output_path(returns_file))


def parse_args(args):
    return args[1]


def read_returns(path):
    res = []
    with open(path) as f:
        for line in f:
            res.append(float(line))
    return res


def plot(data):
    draw(data)
    draw(convolve(data, len(data)//100))
    plt.xlabel("Episodes")
    plt.ylabel("Returns")
    plt.title(TITLE)


def draw(data):
    x = np.arange(1, len(data)+1)
    plt.plot(x, data)


def convolve(data, width):
    return np.convolve(data, np.ones(width)/width, mode="same")[width+1:-width]


def output_path(input_path):
    dirname = opath.dirname(input_path)
    abspath = opath.abspath(dirname)
    return opath.join(abspath, OUTPUT_FNAME)


def save(fname):
    plt.savefig(fname)


if __name__ == "__main__":
    run(sys.argv)
