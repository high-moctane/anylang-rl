import environment.abs_environment
import config
from math import sin, cos, pi
from typing import List


class Cartpole(environment.abs_environment.Environment):
    """Cartpole environment."""

    def __init__(self, cfg: config.Config):
        super().__init__()

        self._actions = (float(cfg.cfg["ENV_ACTION_LEFT"]),
                         float(cfg.cfg["ENV_ACTION_RIGHT"]))

        self._x_bounds = (
            float(cfg.cfg["ENV_X_LEFT"]), float(cfg.cfg["ENV_X_RIGHT"]))
        self._theta_bounds = (
            float(cfg.cfg["ENV_THETA_LEFT"]), float(cfg.cfg["ENV_THETA_RIGHT"]))
        self._xdot_bounds = (
            float(cfg.cfg["ENV_XDOT_LEFT"]), float(cfg.cfg["ENV_XDOT_RIGHT"]))
        self._thetadot_bounds = (
            float(cfg.cfg["ENV_THETADOT_LEFT"]), float(cfg.cfg["ENV_THETADOT_RIGHT"]))

        self._x_space = int(cfg.cfg["ENV_X_SPACE"])
        self._theta_space = int(cfg.cfg["ENV_THETA_SPACE"])
        self._xdot_space = int(cfg.cfg["ENV_XDOT_SPACE"])
        self._thetadot_space = int(cfg.cfg["ENV_THETADOT_SPACE"])

        self._g = float(cfg.cfg["ENV_G"])
        self._M = float(cfg.cfg["ENV_CART_MASS"])
        self._m = float(cfg.cfg["ENV_POLE_MASS"])
        self._l = float(cfg.cfg["ENV_POLE_LENGTH"])

        self._fps = float(cfg.cfg["ENV_FPS"])
        self._tau = 1. / self._fps

        self._ml = self._m * self._l
        self._mass = self._m + self._M

        self._init_state = (0., pi, 0., 0.)
        self._s = self._init_state  # (x, theta, xdot, thetadot)

        self.reset()

    def s_space(self) -> int:
        """Returns the range of states."""
        return self._x_space * self._theta_space * self._xdot_space * self._thetadot_space

    def a_space(self) -> int:
        """Returns the range of actions."""
        return len(self._actions)

    def s(self) -> int:
        """Return a current state."""
        x_idx = self._digitize(self._x_bounds, self._x_space, self._s[0])
        theta_idx = self._digitize(
            self._theta_bounds, self._theta_space, self._s[1])
        xdot_idx = self._digitize(
            self._xdot_bounds, self._xdot_space, self._s[2])
        thetadot_idx = self._digitize(
            self._thetadot_bounds, self._thetadot_space, self._s[3])

        return ((x_idx * self._theta_space + theta_idx) * self._xdot_space + xdot_idx) * self._thetadot_space + thetadot_idx

    def _digitize(self, bounds: List[int], num: int, val: float):
        """Returns val's index in the space separated by bounds."""
        if val < bounds[0]:
            return 0
        elif val >= bounds[1]:
            return num - 1
        width = (bounds[1] - bounds[0]) / (num - 2)
        return int((val - bounds[0]) // width) + 1

    def info(self) -> str:
        """Returns (x, theta, xdot, thetadot) comma separated string."""
        return ",".join(map(lambda v: "{:.15f}".format(v), self._s))

    def r(self) -> float:
        """Reward."""
        x = self._s[0]
        if abs(x) > 2.0:
            return -2.
        theta = self._s[1]
        return -abs(theta) + pi / 2. - .001 * abs(x)

    def reset(self):
        """Reset env."""
        self._s = self._init_state

    def run_step(self, a: int):
        """Update internal state."""
        u = self._actions[a]
        self._s = self._solve_runge_kutta(self._s, u, self._tau)

    def _solve_runge_kutta(self, s, u, dt):
        """Solves the cartpole dynamics.
        Args:
            s:  (x, theta, xdot, thetadot)
            u:  force
            dt: tic

        Returns:
            (next_x, next_theta, next_xdot, next_thetadot)
        """
        k1 = self._differential(s, u)
        s1 = self._solve_euler(s, k1, dt / 2)
        k2 = self._differential(s1, u)
        s2 = self._solve_euler(s, k2, dt / 2)
        k3 = self._differential(s2, u)
        s3 = self._solve_euler(s, k3, dt)
        k4 = self._differential(s3, u)

        snext = list(s)
        for i in range(len(s)):
            snext[i] += (k1[i] + 2. * k2[i] + 2. * k3[i] + k4[i]) * dt / 6.

        snext[1] = (snext[1] + pi) % (2. * pi) - pi
        return tuple(snext)

    def _differential(self, s, u):
        """The differential of the cartpole equation of motion.
        Args:
            s:  (x, theta, xdot, thetadot)
            u: force
        Returns:
            (xdot, thetadot, xddot, thetaddot)
        """
        x, theta, xdot, thetadot = s
        sintheta = sin(theta)
        costheta = cos(theta)

        ml = self._ml
        m = self._m
        g = self._g
        mass = self._mass
        l = self._l

        xddot = (4 * u / 3 + 4 * ml * thetadot**2 * sintheta / 3 - m *
                 g * sin(2*theta) / 2) / (4 * mass - m * costheta**2)
        thetaddot = (mass * g * sintheta - ml * thetadot**2 * sintheta *
                     costheta - u * costheta) / (4 * mass * l / 3 - ml * costheta**2)

        return (xdot, thetadot, xddot, thetaddot)

    def _solve_euler(self, s, sdot, dt):
        """Solve equation of motion by Euler method.
        Args:
            s:  (x, theta, xdot, thetadot)
            sdot: (xdot, thetadot, xddot, thetaddot)
            u: force
            dt: tic
        Returns:
            (next_x, next_theta, next_xdot, next_thetadot)
        """
        return [si + sdoti * dt for si, sdoti in zip(s, sdot)]

    def is_done(self) -> bool:
        """Return the task is done."""
        return False

    def is_success(self) -> bool:
        """Return False because the experiment lasts all the steps."""
        return False
