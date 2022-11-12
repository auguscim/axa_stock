from abc import abstractmethod
import json
import random
from typing import List, NamedTuple


class StockTicker(NamedTuple):
    name: str
    price: float = 0
    quantity: int = 0

    def serialize(self) -> str:
        return json.dumps(self._asdict())


class StockTickerGenerator:
    @abstractmethod
    def generate_stock_attributes(
        name, max_quantity: int = 100, max_price: float = 100
    ) -> StockTicker:
        if not name:
            raise Exception("Cannot generate stock with an empty name")
        price = random.uniform(0, max_price)
        quantity = random.randint(0, max_quantity)
        return StockTicker(name=name, price=price, quantity=quantity)


class FillServer:
    # api_handler: ControllerAPI

    def __init__(self) -> None:

        pass

    def create_payload(self) -> List[StockTicker]:
        return []
