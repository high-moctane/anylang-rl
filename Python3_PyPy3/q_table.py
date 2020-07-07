from typing import List


class QTable:
    def __init__(self, state_size: int, action_size: int, init_qvalue: float):
        self.state_size = state_size
        self.action_size = action_size
        self.init_qvalue = init_qvalue
        self.table = [[init_qvalue] * action_size for _ in range(state_size)]
