from typing import List, Dict


class InvalidArgsException(Exception):
    pass


class EnvParseException(Exception):
    pass


class Config:
    def __init__(self, argv: List[str]):
        if len(argv) != 1:
            raise InvalidArgsException(argv)

        self.items = {}

        with open(argv[0]) as f:
            for line in f:
                elems = line.rstrip().split("=")
                if len(elems) != 2:
                    raise EnvParseException(line)
                self.items[elems[0]] = elems[1]
