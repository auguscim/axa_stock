# pyre-strict
from abc import abstractmethod
import http.client
import json
import logging
import random
import time
from typing import NamedTuple

import sys


# setting path
sys.path.append("../")

from base_types.stock_ticker import StockTicker

from stock_ticker_generator import StockTickerGenerator

class FillServer:

    MAX_SLEEP_TIME: int = 5  # seconds
    MIN_SLEEP_TIME: int = 1  # seconds

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
