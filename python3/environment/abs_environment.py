import abc


class Environment(abc.ABC):
    """環境の抽象クラスです。"""

    @abc.abstractmethod
    def s_space(self) -> int:
        """s のインデックス取りうる個数を返します。"""
        pass

    @abc.abstractmethod
    def a_space(self) -> int:
        """a のインデックスの取りうる個数を返します。"""
        pass

    @abc.abstractmethod
    def s(self) -> int:
        """s のインデックスを返します。"""
        pass

    @abc.abstractmethod
    def info(self) -> str:
        """現在の環境の状態についてわかりやすい文字列を提供します。"""
        pass

    @abc.abstractmethod
    def r(self, s1: int, a1: int, s2: int) -> float:
        """s1 で a1 したとき s2 に移った場合の報酬です。"""
        pass

    @abc.abstractmethod
    def reset(self):
        """環境を初期状態に戻します。"""
        pass

    @abc.abstractmethod
    def run_step(self, a):
        """a を受け取って内部の状態を遷移させます。"""
        pass

    @abc.abstractmethod
    def is_done(self, s) -> bool:
        """タスクが終了したかどうかを返します。"""
        pass

    @abc.abstractmethod
    def is_success(self, s) -> bool:
        """タスクが成功したかどうかを返します。"""
        pass
