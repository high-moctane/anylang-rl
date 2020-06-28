import pickle


class QTable:
    """Q-table object."""

    @classmethod
    def load(cls, path: str):
        """Loads Q-table from path."""
        with open(path, mode="rb") as f:
            return pickle.load(f)

    def __init__(self, init_q: float, s_space: int, a_space: int):
        """
        init_q: initial q-value
        s_space: range of states' indices
        a_space: range of actions' indices
        """
        self.init_q = init_q
        self.s_space = s_space
        self.a_space = a_space

        self.table = [[init_q] * a_space for _ in range(s_space)]

    def save(self, path: str):
        """Saves Q-table into path."""
        with open(path, mode="wb") as f:
            pickle.dump(self, f)
