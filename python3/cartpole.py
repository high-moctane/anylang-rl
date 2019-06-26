from copy import copy
from math import sin, cos, pi


class CartPole:
    def __init__(self):
        self.g = 9.80665  # 重力加速度
        self.M = 1.0  # カートの質量
        self.m = 0.1  # ポールの質量
        self.l = 0.5  # ポールの半分の長さ
        self.fps = 50  # frames per second
        self.tau = 1 / self.fps  # 制御周期

        # 後の計算で使う
        self.ml = self.m * self.l
        self.mass = self.M + self.m

        # ここで self.s をつくる
        # [x, theta, xdot, thetadot]
        self.reset_state()

    def step(self, a):
        self.s = self.runge_kutta_solve(self.s, a, self.tau)

    def state(self):
        return self.s

    def reward(self):
        x, theta, xdot, thetadot = self.s
        if abs(x) > 2.0:
            return -2.0
        return -abs(theta) + pi / 2

    def reset_state(self):
        self.s = [0.0, -pi, 0.0, 0.0]

    def differential(self, s, u):
        """状態 s で力 u を加えたときの微分"""
        x, theta, xdot, thetadot = s
        sintheta = sin(theta)
        costheta = cos(theta)

        xddot = (4 * u / 3 + 4 * self.ml * thetadot**2 * sintheta / 3 - self.m *
                 self.g * sin(2*theta) / 2) / (4 * self.mass - self.m * costheta**2)
        thetaddot = (self.mass * self.g * sintheta - self.ml * thetadot**2 * sintheta *
                     costheta - u * costheta) / (4 * self.mass * self.l / 3 - self.ml * costheta**2)

        return [xdot, thetadot, xddot, thetaddot]

    def euler_solve(self, s, sdot, dt):
        """オイラー法を用いて微分方程式を解く"""
        return [si + sdoti * dt for si, sdoti in zip(s, sdot)]

    def runge_kutta_solve(self, s, u, dt):
        k1 = self.differential(s, u)
        s1 = self.euler_solve(s, k1, dt / 2)
        k2 = self.differential(s1, u)
        s2 = self.euler_solve(s, k2, dt / 2)
        k3 = self.differential(s2, u)
        s3 = self.euler_solve(s, k3, dt)
        k4 = self.differential(s3, u)

        snext = copy(s)
        for i in range(len(s)):
            snext[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * dt / 6

        snext[1] = (snext[1] + pi) % (2 * pi) - pi
        return snext
