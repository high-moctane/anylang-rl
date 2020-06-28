import abc
import config
from math import sin, cos, pi
from typing import List, Tuple


class Pendulum():
    """Inverted pendulum environment."""

    def __init__(self, cfg: config.Config):
        super().__init__()

        self._actions = (float(cfg.cfg["ENV_ACTION_LEFT"]),
                         float(cfg.cfg["ENV_ACTION_RIGHT"]))

        self._theta_bounds = (
            float(cfg.cfg["ENV_THETA_LEFT"]), float(cfg.cfg["ENV_THETA_RIGHT"]))
        self._thetadot_bounds = (
            float(cfg.cfg["ENV_THETADOT_LEFT"]), float(cfg.cfg["ENV_THETADOT_RIGHT"]))

        self._theta_space = int(cfg.cfg["ENV_THETA_SPACE"])
        self._thetadot_space = int(cfg.cfg["ENV_THETADOT_SPACE"])

        self._g = float(cfg.cfg["ENV_G"])
        self._l = float(cfg.cfg["ENV_LENGTH"])
        self._m = float(cfg.cfg["ENV_MASS"])

        self._fps = int(cfg.cfg["ENV_FPS"])
        self._tau = 1. / self._fps

        self._init_state = (pi, 0.)
        self._s = self._init_state  # (theta, thetadot)

        self.reset()

    def s_space(self) -> int:
        """Returns the range of states."""
        return self._theta_space * self._thetadot_space

    def a_space(self) -> int:
        """Returns the range of actions."""
        return len(self._actions)

    def s(self) -> int:
        """Returns a state index."""
        theta_idx = self._digitize(
            self._theta_bounds, self._theta_space, self._s[0])
        thetadot_idx = self._digitize(
            self._thetadot_bounds, self._thetadot_space, self._s[1])

        return theta_idx * self._thetadot_space + thetadot_idx

    def _digitize(self, bounds: List[int], num: int, val: float) -> int:
        """Returns val's index in the space separated by bounds."""
        if val < bounds[0]:
            return 0
        elif val >= bounds[1]:
            return num - 1
        width = (bounds[1] - bounds[0]) / (num - 2)
        return int((val - bounds[0]) // width) + 1

    def info(self) -> str:
        """Return a (theta, thetadot) string."""
        return ",".join(map(lambda v: "{:.15f}".format(v), self._s))

    def r(self) -> float:
        """Reward."""
        theta = self._s[0]
        return -abs(theta) + pi / 2.

    def reset(self):
        """Reset the environment."""
        self._s = self._init_state

    def run_step(self, a):
        """Update the internal state."""
        u = self._actions[a]

        self._s = self._solve_runge_kutta(self._s, u, self._tau)

    def _solve_runge_kutta(self, s: Tuple[float, float], u: float, dt: float) -> Tuple[float, float]:
        """Solve the inversed pendulum's dynamics.
        Args:
            s:  (theta, thetadot)
            u:  force
            dt: tic

        Returns:
            (next_theta, next_thetadot)
        """
        k1 = self._differential(s, u)
        s1 = self._solve_euler(s, k1, dt / 2)
        k2 = self._differential(s1, u)
        s2 = self._solve_euler(s, k2, dt / 2)
        k3 = self._differential(s2, u)
        s3 = self._solve_euler(s, k3, dt)
        k4 = self._differential(s3, u)

        snext = tuple(si + (k1i + 2.*k2i + 2.*k3i + k4i) * dt / 6.
                      for si, k1i, k2i, k3i, k4i in zip(s, k1, k2, k3, k4))

        return self._normalize_s(snext)

    def _differential(self, s: Tuple[float, float], u: float) -> Tuple[float, float]:
        """The differential of the inverted pendulum equation of motion.
        Args:
            s: (theta, thetadot)
            u: force
        Returns:
            (thetadot, theta2dot)
        """
        theta, thetadot = self._s

        l = self._l
        g = self._g
        m = self._m

        thetaddot = g / l * sin(theta) + u / (m * l**2)
        return (thetadot + thetaddot * self._tau, thetaddot)

    def _solve_euler(self, s: Tuple[float, float], sdot: Tuple[float, float], dt: float) -> Tuple[float, float]:
        """Solve equation of motion with Euler method.
        Args:
            s:    (theta, thetadot)
            sdot: (thetadot, theta2dot)
            dt:   tic
        Returns:
            (next_theta, next_thetadot)
        """
        return (si + sdoti * dt for si, sdoti in zip(s, sdot))

    def _normalize_s(self, s: Tuple[float, float]) -> Tuple[float, float]:
        """Normalize state (related to angle)."""
        return ((s[0] + pi) % (2. * pi) - pi, s[1])

    def is_done(self) -> bool:
        """Return the task is done."""
        return False

    def is_success(self) -> bool:
        """Return False because the experiment lasts all the steps."""
        return False
