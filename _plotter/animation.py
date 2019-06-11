import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os.path as path
import sys


DATA_FNAME = "states.csv"
GIF_FNAME = "animation.gif"


class Visualizer:
    def __init__(self, data_fname):
        self.data_fname = data_fname

        self.cart_size = [1.0, 0.5]
        self.pole_len = 0.5
        self.frames_per_sec = 50
        self.tick = 1 / self.frames_per_sec

        # 図の出力範囲
        self.xlim = [-3, 3]
        self.ylim = [-3, 3]

        self.text_time_pos = [-2.8, 2.8]
        self.text_x_pos = [-2.8, 2.6]
        self.text_xdot_pos = [-2.8, 2.4]
        self.text_theta_pos = [-2.8, 2.2]
        self.text_thetadot_pos = [-2.8, 2.0]

        self.time = 0.0

        self.fig, self.ax = plt.subplots()

    def make_animation(self):
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update,
            interval=int(self.tick * 1000)
        )

    def save(self, fname):
        self.ani.save(fname, writer="imagemagick")

    def update(self, *args):
        self.init_axes()
        s = self.line_to_state(self.readline())
        self.draw_cart(s)
        self.draw_pole(s)
        self.write_info(s)
        self.time += self.tick

    def init_axes(self):
        self.ax.clear()
        self.ax.xlim(*self.xlim)
        self.ax.ylim(*self.ylim)

    def readline(self):
        with open(self.data_fname) as f:
            yield f.read()

    def line_to_state(self, line):
        # s = [x, xdot, theta, thetadot]
        return list(map(float, line.strip().split(",")))

    def draw_cart(self, s):
        left = s[0] - self.cart_size[0]/2
        right = s[0] + self.cart_size[0]/2
        bottom = -self.cart_size[1]/2
        top = self.cart_size[1]/2

        self.ax.hlines(bottom, left, right)
        self.ax.hlines(top, left, right)
        self.ax.vlines(left, bottom, top)
        self.ax.vlines(right, bottom, top)

    def draw_pole(self, s):
        x, theta = s[0], s[2]

        axis_x = x
        axis_y = 0
        tip_x = axis_x + math.sin(theta)
        tip_y = math.cos(theta)

        self.ax.plot([axis_x, tip_x], [axis_y, tip_y])

    def write_info(self, s):
        x, xdot, theta, thetadot = s
        self.ax.text(*self.text_time_pos, f"time[s] = {self.time}")
        self.ax.text(*self.text_x_pos, f"x[m] ={x}")
        self.ax.text(*self.text_xdot_pos, f"xdot[m/s] ={xdot}")
        self.ax.text(*self.text_theta_pos, f"theta[rad] = {theta}")
        self.ax.text(*self.text_thetadot_pos, f"thetadot[rad/s] = {thetadot}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 animation.py LANG_DIR", file=sys.stderr)
        sys.exit(1)

    lang_dir = sys.argv[1]

    if not path.isdir(lang_dir):
        print(f"No such directory: {lang_dir}", file=sys.stderr)
        sys.exit(1)

    visualizer = Visualizer(path.join(lang_dir, DATA_FNAME))
    visualizer.make_animation()
    visualizer.save(path.join(lang_dir, GIF_FNAME))
