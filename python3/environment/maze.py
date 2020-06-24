import environment.abs_environment as abs_env
import config
import history
from typing import List, Tuple


class Maze(abs_env.Environment):
    """迷路タスクです。"""

    def __init__(self, config: "config.Config"):
        """
        maze: 迷路文字列
        """
        super().__init__()

        self._goal_reward = float(config.cfg["ENV_GOAL_REWARD"])
        self._dead_reawrd = float(config.cfg["ENV_DEAD_REWARD"])
        self._default_reward = float(config.cfg["ENV_DEFAULT_REWARD"])

        self._h = int(config.cfg["ENV_HEIGHT"])
        self._w = int(config.cfg["ENV_WIDTH"])
        self._maze = self._parse_maze(config.cfg["ENV_MAZE"])

        self._start = (1, 1)
        self._goal = (self._h - 2, self._w - 2)

        self._pos = self._start

        self.reset()

    def _parse_maze(self, maze: str) -> List[List[str]]:
        """迷路文字列を2重リストにパースします。"""
        res = [[None] * self._w for _ in range(self._h)]
        for h in range(self._h):
            for w in range(self._w):
                pos = (h, w)
                s = self._pos_to_s(pos)
                res[h][w] = maze[s]
        return res

    def s_space(self) -> int:
        """s のインデックス取りうる個数を返します。"""
        return self._h * self._w

    def a_space(self) -> int:
        """a のインデックスの取りうる個数を返します。"""
        return 4

    def s(self) -> int:
        """s のインデックスを返します。"""
        return self._pos_to_s(self._pos)

    def _pos_to_s(self, pos: Tuple[int, int]) -> int:
        """pos を s のインデックスに変換します。"""
        return pos[0] * self._w + pos[1]

    def r(self) -> float:
        """s1 で a1 したとき s2 に移った場合の報酬です。"""
        pos = self._pos

        if self._is_goal(pos):
            return self._goal_reward
        elif not self._is_in_maze(pos) or self._is_in_wall(pos):
            return self._dead_reawrd
        return self._default_reward

    def _is_goal(self, pos: Tuple[int, int]) -> bool:
        """pos がゴールであるか判別します。"""
        return pos == self._goal

    def _is_in_maze(self, pos: Tuple[int, int]) -> bool:
        """pos が迷路内にいるか判別します。"""
        return 0 <= pos[0] < self._h and 0 <= pos[1] < self._w

    def _is_in_wall(self, pos: Tuple[int, int]) -> bool:
        """pos が壁の中にいるか判別します。"""
        return self._maze[pos[0]][pos[1]] == "#"

    def _s_to_pos(self, s: int) -> Tuple[int, int]:
        """s を pos に変換します。"""
        return (s // self._w, s % self._w)

    def info(self):
        """現在の座標 (h, w) についてコンマ区切りで返します。"""
        return "{},{}".format(self._pos[0], self._pos[1])

    def reset(self):
        """環境を初期状態に戻します。"""
        self._pos = self._start
        self._step = 0

    def run_step(self, a: int):
        """a を受け取って内部の状態を遷移させます。"""
        self._step += 1
        self._move(a)

    def _move(self, a: int):
        """a して pos を更新します。"""
        if a == 0:
            self._pos = (self._pos[0]-1, self._pos[1])
        elif a == 1:
            self._pos = (self._pos[0]+1, self._pos[1])
        elif a == 2:
            self._pos = (self._pos[0], self._pos[1]-1)
        else:
            self._pos = (self._pos[0], self._pos[1]+1)

    def is_done(self, s) -> bool:
        """タスクが終了したかどうかを返します。"""
        pos = self._s_to_pos(s)
        return self._is_goal(pos) or \
            not self._is_in_maze(pos) or \
            self._is_in_wall(pos)

    def is_success(self, s) -> bool:
        """タスクが成功したかどうかを返します。"""
        pos = self._s_to_pos(s)
        return self._is_goal(pos)
