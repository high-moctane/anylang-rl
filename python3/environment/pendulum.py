import abc
import config
from math import sin, cos, pi
from typing import List, Tuple


class Pendulum():
    """倒立振子の実験環境です。"""

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
        """s のインデックス取りうる個数を返します。"""
        return self._theta_space * self._thetadot_space

    def a_space(self) -> int:
        """a のインデックスの取りうる個数を返します。"""
        return len(self._actions)

    def s(self) -> int:
        """s のインデックスを返します。"""
        theta_idx = self._digitize(
            self._theta_bounds, self._theta_space, self._s[0])
        thetadot_idx = self._digitize(
            self._thetadot_bounds, self._thetadot_space, self._s[1])

        return theta_idx * self._thetadot_space + thetadot_idx

    def _digitize(self, bounds: List[int], num: int, val: float) -> int:
        """[bounds[0], bounds[1]] を境界として num 個のスペースに区切った場合の
        val の番号を返します。"""
        if val < bounds[0]:
            return 0
        elif val >= bounds[1]:
            return num - 1
        width = (bounds[1] - bounds[0]) / (num - 2)
        return int((val - bounds[0]) // width) + 1

    def info(self) -> str:
        """現在の環境の状態についてわかりやすい文字列を提供します。"""
        return ",".join(map(lambda v: "{:.15f}".format(v), self._s))

    def r(self) -> float:
        """s1 で a1 したとき s2 に移った場合の報酬です。"""
        theta = self._s[0]
        return -abs(theta) + pi / 2.

    def reset(self):
        """環境を初期状態に戻します。"""
        self._s = self._init_state

    def run_step(self, a):
        """a を受け取って内部の状態を遷移させます。"""
        u = self._actions[a]

        self._s = self._solve_runge_kutta(self._s, u, self._tau)

    def _solve_runge_kutta(self, s: Tuple[float, float], u: float, dt: float) -> Tuple[float, float]:
        """s で u を入力したときの dt 時間後の s をルンゲクッタで求めます。"""
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
        """s で u を加えたときの微分。"""
        theta, thetadot = self._s

        l = self._l
        g = self._g
        m = self._m

        thetaddot = g / l * sin(theta) + u / (m * l**2)
        return (thetadot + thetaddot * self._tau, thetaddot)

    def _solve_euler(self, s: Tuple[float, float], sdot: Tuple[float, float], dt: float) -> Tuple[float, float]:
        """s と sdot より dt 後の s をオイラー法で求める。"""
        return (si + sdoti * dt for si, sdoti in zip(s, sdot))

    def _normalize_s(self, s: Tuple[float, float]) -> Tuple[float, float]:
        return ((s[0] + pi) % (2. * pi) - pi, s[1])

    def is_done(self) -> bool:
        """タスクが終了したかどうかを返します。"""
        return False

    def is_success(self) -> bool:
        """タスクが成功したかどうかを返します。"""
        return False
