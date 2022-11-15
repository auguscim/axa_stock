from abc import abstractmethod
import random

from base_types.stock_ticker import StockTicker


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
