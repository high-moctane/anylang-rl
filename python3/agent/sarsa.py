import agent.abs_agent as abs_agent
import random
import config
from typing import List
import q_table


class Sarsa(abs_agent.Agent):
    """Sarsa をします。"""

    def __init__(self, config: "config.Config"):
        super().__init__()
        self.alpha = float(config.cfg["AGENT_ALPHA"])
        self.gamma = float(config.cfg["AGENT_GAMMA"])
        self.eps = float(config.cfg["AGENT_EPSILON"])

    def a(self, q_table_: "q_table.QTable", s: int) -> int:
        """eps-greedy を実装します。"""

        if random.random() < self.eps:
            return random.randint(0, q_table_.a_space - 1)
        return self.argmax(q_table_.table[s])

    def learn(self, q_table_: "q_table.QTable", s1: int, a1: int, r: float, s2: int, a2: int):
        """学習します。"""
        q_table_.table[s1][a1] = (1. - self.alpha) * q_table_.table[s1][a1] + \
            self.alpha * (r + self.gamma * q_table_.table[s2][a2])

    def fix(self):
        self.alpha = 0.
        self.eps = 0.

    def argmax(self, list_: List[int]):
        """argmax をとります。"""
        res = 0
        for i, q in enumerate(list_):
            if q > list_[res]:
                res = i
        return res
