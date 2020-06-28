import config
import experiment
import environment.maze as maze
import environment.pendulum as pendulum
import agent.q_learning as q_learning
import agent.sarsa as sarsa
import q_table
from typing import List


class InvalidArgsException(Exception):
    """The exception about the arguments."""
    pass


class InvalidAgentName(Exception):
    """The exception about the agent name."""
    pass


class InvalidEnvironmentName(Exception):
    """The exception about the environment name."""
    pass


class Runner:
    """Runs the program."""

    def __init__(self, args: List[str]):
        self._parse_args(args)

    def _parse_args(self, args: List[str]):
        """Parse args"""
        if len(args) != 1:
            raise InvalidArgsException(args)
        self.config = config.Config(args[0])

    def run(self):
        """Runs the program."""
        agent = self._choose_agent()
        env = self._choose_environment()
        exp = experiment.Experiment(self.config, agent, env)

        exp.run()
        exp.save_returns()
        exp.test_and_save()

    def _choose_agent(self):
        """Chooses the agent."""
        agent_name = self.config.cfg["AGENT_NAME"]
        if agent_name == "Q-learning":
            return q_learning.QLearning(self.config)
        elif agent_name == "Sarsa":
            return sarsa.Sarsa(self.config)
        else:
            raise InvalidAgentName(agent_name)

    def _choose_environment(self):
        """Choose the environment."""
        env_name = self.config.cfg["ENV_NAME"]
        if env_name == "Maze":
            return maze.Maze(self.config)
        elif env_name == "Pendulum":
            return pendulum.Pendulum(self.config)
        else:
            raise InvalidEnvironmentName(env_name)
