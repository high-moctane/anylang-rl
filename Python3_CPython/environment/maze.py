import config
from typing import List, Tuple

Pos = Tuple[int, int]


class ActionIndexOutOfRange(Exception):
    pass


class Maze:
    def __init__(self, config: config.Config):
        self.maze = self.open_maze(config.items["ENV_MAZE_PATH"])
        self.height = len(self.maze)
        self.width = len(self.maze[0])

        self.default_reward = float(config.items["ENV_DEFAULT_REWARD"])
        self.goal_reward = float(config.items["ENV_GOAL_REWARD"])
        self.wall_reward = float(config.items["ENV_WALL_REWARD"])

        self.init_pos = (1, 1)
        self.goal_pos = (self.height - 2, self.width - 2)
        self.pos = self.init_pos

    def open_maze(self, path: str) -> List[List[str]]:
        with open(path) as f:
            return [list(line.rstrip()) for line in f]

    def pos_to_s(self, pos: Pos) -> int:
        return pos[0] * self.width + pos[1]

    def is_goal(self) -> bool:
        return self.pos == self.goal_pos

    def is_wall(self) -> bool:
        return self.maze[self.pos[0]][self.pos[1]] == "#"

    def state_size(self) -> int:
        return self.height * self.width

    def action_size(self) -> int:
        return 4

    def state(self) -> int:
        return self.pos_to_s(self.pos)

    def reward(self) -> int:
        if self.is_wall():
            return self.wall_reward
        if self.is_goal():
            return self.goal_reward
        return self.default_reward

    def info(self) -> str:
        return "{},{}".format(*self.pos)

    def run_step(self, a: int):
        if a == 0:
            self.pos = (self.pos[0]-1, self.pos[1])
        elif a == 1:
            self.pos = (self.pos[0]+1, self.pos[1])
        elif a == 2:
            self.pos = (self.pos[0], self.pos[1]-1)
        elif a == 3:
            self.pos = (self.pos[0], self.pos[1]+1)
        else:
            raise ActionIndexOutOfRange(a)

    def reset(self):
        self.pos = self.init_pos

    def is_finish(self) -> bool:
        return self.is_goal() or self.is_wall()
