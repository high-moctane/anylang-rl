import pickle


class QTable:
    """Q テーブルです。"""

    @classmethod
    def load(cls, path: str):
        with open(path, mode="rb") as f:
            return pickle.load(f)

    def __init__(self, init_q: float, s_space: int, a_space: int):
        """
        init_q: テーブルの初期値
        s_space: 状態空間の大きさ
        a_space: 行動空間の大きさ
        """
        self.init_q = init_q
        self.s_space = s_space
        self.a_space = a_space

        self.table = [[init_q] * a_space for _ in range(s_space)]

    def save(self, path: str):
        """Q テーブルを path に保存します"""
        with open(path, mode="wb") as f:
            pickle.dump(self, f)
