import abc


class History(abc.ABC):
    """Stores actions, states, rewards, and info about the env."""

    def __init__(self):
        self.a = []
        self.s = []
        self.r = []
        self.info = []

    def append(self, a: int, s: int, r: float, info: str):
        """Appends a, s, r and info."""
        self.a.append(a)
        self.s.append(s)
        self.r.append(r)
        self.info.append(info)

    def save(self, path: str):
        """Saves history into path."""
        with open(path, mode="w") as f:
            for a, s, r, info in zip(self.a, self.s, self.r, self.info):
                f.write("{}\t{}\t{:.15f}\t{}\n".format(a, s, r, info))
