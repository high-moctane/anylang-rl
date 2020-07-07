from typing import List


class History:
    def __init__(self):
        self.actions = []
        self.rewards = []
        self.states = []
        self.info = []

    def append(self, a: int, r: float, s: int, info: str):
        self.actions.append(a)
        self.rewards.append(r)
        self.states.append(s)
        self.info.append(info)

    def save(self, path: str):
        with open(path, mode="w") as f:
            for i in range(len(self.actions)):
                f.write("{}\t{:.15f}\t{}\t{}\n".format(
                    self.actions[i],
                    self.rewards[i],
                    self.states[i],
                    self.info[i],
                ))
