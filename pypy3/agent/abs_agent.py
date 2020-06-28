import abc
import q_table


class Agent(abc.ABC):
    """Abstract reinforcement learning class."""

    @abc.abstractmethod
    def a(self, q_table: q_table.QTable, s: int) -> int:
        """Choose an action from a state."""
        pass

    @abc.abstractmethod
    def learn(self, q_table: q_table.QTable, s1: int, a1: int, r: float, s2: int, a2: int):
        """Do learning.
        s1: previous state
        a1: previous action
        r:  reward
        s2: next state
        a2: next action
        """
        pass

    @abc.abstractmethod
    def fix(self):
        """Change learning parameters which prevent from learning."""
        pass
