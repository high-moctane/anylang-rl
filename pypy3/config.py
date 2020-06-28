from typing import Dict


class Config:
    """実験に使う定数を読み取ります"""

    def __init__(self, path: str):
        self.cfg = self._read(path)

    def _read(self, path: str) -> Dict[str, str]:
        res = dict()
        with open(path) as f:
            for line in f:
                key, val = line.split("=")
                res[key] = val.rstrip()
        return res
