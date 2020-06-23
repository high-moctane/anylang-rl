import config
import experiment
import environment.maze as maze
import agent.q_learning as q_learning
import agent.sarsa as sarsa
import q_table
from typing import List


class InvalidArgsException(Exception):
    """Args が不正だったときに投げるエラーです。"""
    pass


class InvalidAgentName(Exception):
    """エージェントの名前が変だったときに投げるエラーです。"""
    pass


class InvalidEnvironmentName(Exception):
    """環境の名前が変だったときに投げるエラーです。"""
    pass


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
        agent = self._choose_agent()
        env = self._choose_environment()
        exp = experiment.Experiment(self.config, agent, env)

        exp.run()
        exp.save_returns(self.config.cfg["RETURNS_PATH"])
        exp.test_and_save(self.config.cfg["HISTORY_PATH"])
        exp.q_table.save(self.config.cfg["QTABLE_PATH"])

    def _choose_agent(self):
        agent_name = self.config.cfg["AGENT_NAME"]
        if agent_name == "Q-learning":
            return q_learning.QLearning(self.config)
        elif agent_name == "Sarsa":
            return sarsa.Sarsa(self.config)
        else:
            raise InvalidAgentName

    def _choose_environment(self):
        env_name = self.config.cfg["ENV_NAME"]
        if env_name == "Maze":
            return maze.Maze(self.config)
        else:
            raise InvalidEnvironmentName
