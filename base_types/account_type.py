from typing import Dict


class Account:
    name: str
    split: int
    stocks: Dict[str, int]

    def __init__(self, name: str, split: int) -> None:
        self.name = name
        self.split = split
        self.stocks = {}
