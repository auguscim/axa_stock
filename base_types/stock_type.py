
from typing import Dict 

from base_types.stock_ticker import StockTicker


class Stock:
    name: str
    quantity: int
    current_price: float
    sum_value: float

    def __init__(self, name: str, quantity: int) -> None:
        self.name = name
        self.quantity = quantity
    def __init__(self, stock_ticker: StockTicker) -> None:
        self.name = stock_ticker.name
        self.quantity = stock_ticker.quantity
        self.price = stock_ticker.price
        self.sum_value = stock_ticker.get_calculated_value()

    def add_stock_ticker(self, stock_ticker: StockTicker) -> None:
        self.quantity += stock_ticker.quantity
        self.current_price = stock_ticker.price
        self.sum_value += stock_ticker.get_calculated_value()