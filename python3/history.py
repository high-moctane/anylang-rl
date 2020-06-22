import abc


class History(abc.ABC):
    """1エピソードの s, a, r の履歴を保存します。"""

    @abc.abstractmethod
    def clear(self):
        """すべてのエントリを初期化します。"""
        pass

    @abc.abstractmethod
    def save(self, path: str):
        """履歴をファイルに保存します。"""
        pass
