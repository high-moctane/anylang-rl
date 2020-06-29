import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os.path as opath
import sys

OUTPUT_FNAME = "animation.gif"


class Visualizer:
    def __init__(self, history_path: str):
        self.history_path = history_path
        self.actions, self.states, self.rewards, self.info =\
            self.read_history(self.history_path)

        self.pole_len = 1.
        self.frames_per_sec = 50
        self.tick = 1 / self.frames_per_sec

        # 図の出力範囲
        self.xlim = [-3, 3]
        self.ylim = [-3, 3]

        self.text_time_pos = [-2.8, 2.8]
        self.text_action_pos = [-2.8, 2.6]
        self.text_x_pos = [-2.8, 2.4]
        self.text_theta_pos = [-2.8, 2.2]
        self.text_xdot_pos = [-2.8, 2.0]
        self.text_thetadot_pos = [-2.8, 1.8]
        self.text_reward_pos = [-2.8, 1.6]

        self.cart_size = (1.0, 0.5)

        self.step = 0
        self.time = 0

        self.fig, self.ax = plt.subplots()

    def read_history(self, path):
        actions, states, rewards, info = [], [], [], []
        with open(path) as f:
            for line in f:
                action, state, reward, inf = line.rstrip().split("\t")
                actions.append(int(action))
                states.append(int(state))
                rewards.append(float(reward))
                info.append(tuple(map(float, inf.split(","))))
        return actions, states, rewards, info

    def make_animation(self):
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update,
            interval=int(self.tick * 1000),
            frames=len(self.states) - 1
        )

    def save(self):
        path = self.output_abs_path()
        self.ani.save(path, writer="imagemagick")

    def output_abs_path(self):
        dirpath = opath.dirname(self.history_path)
        abspath = opath.abspath(dirpath)
        return opath.join(abspath, OUTPUT_FNAME)

    def update(self, *args):
        self.init_axes()
        a = self.actions[self.step]
        s = self.states[self.step]
        r = self.rewards[self.step]
        info = self.info[self.step]
        self.draw_cart(info)
        self.draw_pole(info)
        self.draw_action_arrow(info, a)
        self.write_info(a, s, r, info)
        self.time += self.tick
        self.step += 1

    def init_axes(self):
        self.ax.clear()
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)
        self.ax.set_aspect("equal")

    def draw_pole(self, info):
        x = info[0]
        y = 0
        theta = info[1]

        tip_x = x + math.sin(theta)
        tip_y = math.cos(theta)

        self.ax.plot([x, tip_x], [y, tip_y])

    def draw_cart(self, info):
        x = info[0]
        left = x - self.cart_size[0]/2
        right = x + self.cart_size[0]/2
        bottom = -self.cart_size[1]/2
        top = self.cart_size[1]/2

        self.ax.hlines(bottom, left, right)
        self.ax.hlines(top, left, right)
        self.ax.vlines(left, bottom, top)
        self.ax.vlines(right, bottom, top)

    def draw_action_arrow(self, info, a):
        x = info[0]
        a = float(a)
        if a == 0:
            start = [x - self.cart_size[0] / 2, 0]
            end = [start[0] - 1, 0]
        else:
            start = [x + self.cart_size[0] / 2, 0]
            end = [start[0] + 1, 0]

        self.ax.annotate("", xy=end, xytext=start,
                         arrowprops=dict(arrowstyle="-|>", facecolor="orange", edgecolor="orange"))

    def write_info(self, a, s, r, info):
        x, theta, xdot, thetadot = info
        self.ax.text(*self.text_time_pos, f"time[s] = {self.time:.3f}")
        self.ax.text(*self.text_x_pos, f"x [m] = {x: .3f}")
        self.ax.text(*self.text_theta_pos, f"theta [rad] = {theta: .3f}")
        self.ax.text(*self.text_xdot_pos, f"xdot [m/s] = {xdot: .3f}")
        self.ax.text(*self.text_thetadot_pos,
                     f"thetadot [rad/s] = {thetadot: .3f}")
        self.ax.text(*self.text_action_pos, f"a = {a}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 animation.py path/to/history.tsv", file=sys.stderr)
        sys.exit(1)

    history_path = sys.argv[1]

    visualizer = Visualizer(history_path)
    visualizer.make_animation()
    visualizer.save()
