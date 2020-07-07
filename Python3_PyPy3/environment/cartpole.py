from typing import Tuple
import config
import math

State = Tuple[float, float, float, float]


class Cartpole:
    def __init__(self, config: config.Config):
        self.actions = [
            float(config.items["ENV_ACTION_LEFT"]),
            float(config.items["ENV_ACTION_RIGHT"]),
        ]

        self.x_bounds = (
            float(config.items["ENV_X_LEFT"]),
            float(config.items["ENV_X_RIGHT"]),
        )
        self.theta_bounds = (
            float(config.items["ENV_THETA_LEFT"]),
            float(config.items["ENV_THETA_RIGHT"]),
        )
        self.xdot_bounds = (
            float(config.items["ENV_XDOT_LEFT"]),
            float(config.items["ENV_XDOT_RIGHT"]),
        )
        self.thetadot_bounds = (
            float(config.items["ENV_THETADOT_LEFT"]),
            float(config.items["ENV_THETADOT_RIGHT"]),
        )

        self.x_size = int(config.items["ENV_X_SIZE"])
        self.theta_size = int(config.items["ENV_THETA_SIZE"])
        self.xdot_size = int(config.items["ENV_XDOT_SIZE"])
        self.thetadot_size = int(config.items["ENV_THETADOT_SIZE"])

        self.g = float(config.items["ENV_GRAVITY"])
        cartmass = float(config.items["ENV_CART_MASS"])
        self.m = float(config.items["ENV_POLE_MASS"])
        self.l = float(config.items["ENV_POLE_LENGTH"])
        self.ml = self.m * self.l
        self.mass = cartmass + self.m

        fps = int(config.items["ENV_FRAME_PER_SECOND"])
        self.tau = 1 / fps

        self.init_state = (0., math.pi, 0., 0.)
        self.s = self.init_state

    def solve_runge_kutta(self, s: State, u: float, dt: float) -> State:
        k1 = self.differential(s, u)
        s1 = self.solve_euler(s, k1, dt/2)
        k2 = self.differential(s1, u)
        s2 = self.solve_euler(s, k2, dt/2)
        k3 = self.differential(s2, u)
        s3 = self.solve_euler(s, k3, dt)
        k4 = self.differential(s3, u)

        s_next = [s[i] + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) * dt / 6
                  for i in range(len(s))]

        s_next[1] = self.normalize(s_next[1])

        return tuple(s_next)

    def differential(self, s: State, u: float) -> State:
        _, theta, xdot, thetadot = s

        sintheta = math.sin(theta)
        costheta = math.cos(theta)

        l = self.l
        g = self.g
        m = self.m
        ml = self.ml
        mass = self.mass

        xddot = (4 * u / 3 + 4 * ml * thetadot**2 * sintheta / 3 -
                 m * g * math.sin(2*theta) / 2) / (4 * mass - m * costheta**2)
        thetaddot = (mass * g * sintheta - ml * thetadot**2 * sintheta * costheta
                     - u * costheta) / (4 * mass * l / 3 - ml * costheta**2)

        return (xdot, thetadot, xddot, thetaddot)

    def solve_euler(self, s: State, sdot: State, dt: float) -> State:
        return (s[i] + sdot[i]*dt for i in range(len(s)))

    def digitize(self, bounds: Tuple[float, float], num: int, val: float) -> int:
        if val < bounds[0]:
            return 0
        if val >= bounds[1]:
            return num - 1
        width = (bounds[1] - bounds[0]) / (num - 2)
        return int((val - bounds[0]) / width) + 1

    def normalize(self, theta: float) -> float:
        return (theta + 3 * math.pi) % (2 * math.pi) - math.pi

    def state_size(self) -> int:
        return self.x_size * self.theta_size * self.xdot_size * self.thetadot_size

    def action_size(self) -> int:
        return len(self.actions)

    def state(self) -> int:
        x_idx = self.digitize(self.x_bounds, self.x_size, self.s[0])
        theta_idx = self.digitize(
            self.theta_bounds, self.theta_size, self.s[1])
        xdot_idx = self.digitize(self.xdot_bounds, self.xdot_size, self.s[2])
        thetadot_idx = self.digitize(
            self.thetadot_bounds, self.thetadot_size, self.s[3])

        return ((x_idx * self.theta_size + theta_idx) * self.xdot_size + xdot_idx) \
            * self.thetadot_size + thetadot_idx

    def info(self) -> str:
        x, theta, xdot, thetadot = self.s
        return "{:.15f},{:.15f},{:.15f},{:.15f}".format(x, theta, xdot, thetadot)

    def reward(self) -> float:
        x, theta, _, _ = self.s
        if abs(x) > 2.:
            return -2.
        return -abs(theta) + math.pi / 2 - 0.01 * abs(x)

    def reset(self):
        self.s = self.init_state

    def run_step(self, a: int):
        u = self.actions[a]
        self.s = self.solve_runge_kutta(self.s, u, self.tau)

    def is_finish(self) -> bool:
        return False
