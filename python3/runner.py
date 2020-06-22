import config
import experiment
import environment.maze as maze
import agent.q_learning as q_learning
import q_table
from typing import List


class InvalidArgsException(Exception):
    """Args が不正だったときに投げるエラーです。"""


class Runner:
    """プログラムを走らせます。"""

    def __init__(self, args: List[str]):
        self._parse_args(args)

    def _parse_args(self, args: List[str]):
        if len(args) != 1:
            raise InvalidArgsException
        self.config = config.Config(args[0])

    def run(self):
        """実行します。"""
        if self.config.cfg["ENV_NAME"] == "maze":
            env = maze.Maze(self.config)
        else:
            raise Exception

        if self.config.cfg["AGENT_NAME"] == "Q-learning":
            agent = q_learning.QLearning(self.config)
        else:
            raise Exception

        exp = experiment.Experiment(self.config, agent, env)

        exp.run()
        exp.save_returns(self.config.cfg["RETURNS_PATH"])
        exp.test_and_save(self.config.cfg["HISTORY_PATH"])
        exp.q_table.save(self.config.cfg["QTABLE_PATH"])
