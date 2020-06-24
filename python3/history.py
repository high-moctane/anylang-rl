import abc


class History(abc.ABC):
    """1エピソードの a, s, r, info の履歴を保存します。"""

    def __init__(self):
        self.a = []
        self.s = []
        self.r = []
        self.info = []

    def append(self, a: int, s: int, r: float, info: str):
        """a して s (info) になって r 受け取ったことを保存します。"""
        self.a.append(a)
        self.s.append(s)
        self.r.append(r)
        self.info.append(info)

    def save(self, path: str):
        """履歴をファイルに保存します。"""
        with open(path, mode="w") as f:
            for a, s, r, info in zip(self.a, self.s, self.r, self.info):
                f.write("{}\t{}\t{:.15f}\t{}\n".format(a, s, r, info))
