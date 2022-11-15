import json
from typing import NamedTuple


class StockTicker(NamedTuple):
    name: str
    price: float = 0
    quantity: int = 0

    def serialize(self) -> str:
        return json.dumps(self._asdict())

    def get_calculated_value(self) -> float:
        return self.price * self.quantity

