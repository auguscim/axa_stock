# pyre-strict
from abc import abstractmethod
import http.client
import json
import logging
import random
import time
from typing import List, NamedTuple


class StockTicker(NamedTuple):
    name: str
    price: float = 0
    quantity: int = 0

    def serialize(self) -> str:
        return json.dumps(self._asdict())

    def get_calculated_value(self) -> float:
        return self.price * self.quantity


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

    MAX_SLEEP_TIME: int = 5  # seconds
    MIN_SLEEP_TIME: int = 1  # seconds

    def __init__(self) -> None:

        pass

    def create_payload(self) -> List[StockTicker]:
        return []

    def processing(self) -> None:
        try:
            while True:
                time.sleep(random.randint(self.MIN_SLEEP_TIME, self.MAX_SLEEP_TIME))
                self.call_controller(
                    StockTickerGenerator.generate_stock_attributes("RandName")
                )
        except KeyboardInterrupt:
            pass

    def call_controller(self, stock_ticker: StockTicker) -> None:
        conn = http.client.HTTPConnection("localhost", 8080)

        headers = {"Content-type": "application/json"}

        data = stock_ticker.serialize()
        logging.info(f"Send data: {data}")
        conn.request("POST", "/fill", data, headers)

        response = conn.getresponse()
        logging.info(f"Response: {response.read().decode()}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fill_server_instance = FillServer()

    fill_server_instance.processing()
