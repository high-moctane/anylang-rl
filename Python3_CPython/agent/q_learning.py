import config
import q_table
import random


class QLearning:
    def __init__(self, config: config.Config):
        self.alpha = float(config.items["AGENT_ALPHA"])
        self.gamma = float(config.items["AGENT_GAMMA"])
        self.eps = float(config.items["AGENT_EPSILON"])

    def action(self, q_table: q_table.QTable, s: int) -> int:
        if random.random() < self.eps:
            return random.randint(0, q_table.action_size-1)
        return self.argmax(q_table.table[s])

    def learn(self, q_table: q_table.QTable, s1: int, a1: int, r: float, s2: int, a2: int):
        alpha = self.alpha
        gamma = self.gamma

        q_table.table[s1][a1] = (1. - alpha) * q_table.table[s1][a1] + \
            alpha * (r + gamma * max(q_table.table[s2]))

    def fix(self):
        self.alpha = 0.
        self.eps = 0.

    def argmax(self, lst):
        res = 0
        for i in range(1, len(lst)):
            if lst[res] < lst[i]:
                res = i
        return res
