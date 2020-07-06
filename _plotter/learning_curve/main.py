import matplotlib.pyplot as plt
import numpy as np
import os.path as opath
import sys


def read_returns(path):
    with open(path) as f:
        return [float(line.rstrip()) for line in f]


def target_path(source_path):
    return opath.join(opath.dirname(source_path), "learning_curve.png")


def plot(data):
    draw(data)
    draw(convolve(data, len(data)//100))
    plt.xlabel("Episodes")
    plt.ylabel("Returns")
    plt.title("Episodes-Returns Curve")


def draw(data):
    x = np.arange(1, len(data)+1)
    plt.plot(x, data)


def convolve(data, num):
    return np.convolve(data, np.ones(num)/num, mode="same")[num+1:-num]


def save(path):
    plt.savefig(path)


if __name__ == "__main__":
    source = sys.argv[1]
    returns = read_returns(source)
    plot(returns)
    target = target_path(source)
    save(target)
