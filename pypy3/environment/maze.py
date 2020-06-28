import environment.abs_environment as abs_env
import config
import history
from typing import List, Tuple


class Maze(abs_env.Environment):
    """Maze task."""

    def __init__(self, config: "config.Config"):
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
        """Parse maze string into a double list."""
        res = [[None] * self._w for _ in range(self._h)]
        for h in range(self._h):
            for w in range(self._w):
                pos = (h, w)
                s = self._pos_to_s(pos)
                res[h][w] = maze[s]
        return res

    def s_space(self) -> int:
        """Returns the range of states."""
        return self._h * self._w

    def a_space(self) -> int:
        """Returns the range of actions."""
        return 4

    def s(self) -> int:
        """Returns a state index."""
        return self._pos_to_s(self._pos)

    def _pos_to_s(self, pos: Tuple[int, int]) -> int:
        """Convert a position into a state index."""
        return pos[0] * self._w + pos[1]

    def r(self) -> float:
        """Returns a reward."""
        pos = self._pos

        if self._is_goal(pos):
            return self._goal_reward
        elif not self._is_in_maze(pos) or self._is_in_wall(pos):
            return self._dead_reawrd
        return self._default_reward

    def _is_goal(self, pos: Tuple[int, int]) -> bool:
        """Returns whether the pos is at the goal."""
        return pos == self._goal

    def _is_in_maze(self, pos: Tuple[int, int]) -> bool:
        """Returns whether the pos is in the maze."""
        return 0 <= pos[0] < self._h and 0 <= pos[1] < self._w

    def _is_in_wall(self, pos: Tuple[int, int]) -> bool:
        """Returns whether the pos is in the wall."""
        return self._maze[pos[0]][pos[1]] == "#"

    def _s_to_pos(self, s: int) -> Tuple[int, int]:
        """Converts a state index into a position."""
        return (s // self._w, s % self._w)

    def info(self):
        """Return the current position as a commma separeted string."""
        return "{},{}".format(self._pos[0], self._pos[1])

    def reset(self):
        """Reset the environment."""
        self._pos = self._start

    def run_step(self, a: int):
        """Update the internal state."""
        if a == 0:
            self._pos = (self._pos[0]-1, self._pos[1])
        elif a == 1:
            self._pos = (self._pos[0]+1, self._pos[1])
        elif a == 2:
            self._pos = (self._pos[0], self._pos[1]-1)
        else:
            self._pos = (self._pos[0], self._pos[1]+1)

    def is_done(self) -> bool:
        """Return whether the task is done."""
        return self._is_goal(self._pos) or \
            not self._is_in_maze(self._pos) or \
            self._is_in_wall(self._pos)

    def is_success(self) -> bool:
        """Return whether the task was successful."""
        return self._is_goal(self._pos)
