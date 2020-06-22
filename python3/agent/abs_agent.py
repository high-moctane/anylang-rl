import abc
import q_table


class Agent(abc.ABC):
    """強化学習エージェントの抽象クラスです。"""

    @abc.abstractmethod
    def a(self, q_table: q_table.QTable, s: int) -> int:
        """s (index) を入力として次にとる行動を決めます。"""
        pass

    @abc.abstractmethod
    def learn(self, q_table: q_table.QTable, s1: int, a1: int, r: float, s2: int, a2: int):
        """学習します。
        s1: 前の状態 のインデックス
        a1: 前の行動 のインデックス
        r: 報酬
        s2: 次の状態 のインデックス
        a2: 次の行動 のインデックス
        """
        pass

    @abc.abstractmethod
    def fix(self):
        """学習を行わなくします。"""
        pass
