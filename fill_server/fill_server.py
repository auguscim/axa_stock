import argparse
import http.client
import logging
import random
import time

from urllib.error import HTTPError

import sys

# setting path
sys.path.append("../")

from base_types.stock_ticker import StockTicker

from stock_ticker_generator import StockTickerGenerator


class FillServer:

    MAX_SLEEP_TIME: int = 5  # seconds
    MIN_SLEEP_TIME: int = 1  # seconds

    stock_name: str

    def __init__(self, name: str):
        self.stock_name = name

    def processing(self) -> None:
        try:
            while True:
                time.sleep(random.randint(self.MIN_SLEEP_TIME, self.MAX_SLEEP_TIME))
                self.call_controller(
                    StockTickerGenerator.generate_stock_attributes(self.stock_name)
                )
        except KeyboardInterrupt:
            pass

    def call_controller(self, stock_ticker: StockTicker) -> None:
        data = stock_ticker.serialize()
        try:
            conn = http.client.HTTPConnection("localhost", 8080)
            headers = {"Content-type": "application/json"}

            logging.info(f"Send data: {data}")
            conn.request("POST", "/fill", data, headers)
        except HTTPError as errh:
            logging.exception("Http Error:", errh)
        except ConnectionError as errc:
            logging.exception("Error Connecting:", errc)
        except Exception as err:
            logging.exception("Exception: ", err)
        response = conn.getresponse()
        logging.info(f"Response: {response.read().decode()}")

def cmdline_args_parser():
    parser = argparse.ArgumentParser(description='Fills server')
    parser.add_argument('name', type=str,
                    help='The stocks name for this fill server', default="AXA")

    args=parser.parse_args()
    return args
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = cmdline_args_parser()
    fill_server_instance = FillServer(args.name)

    fill_server_instance.processing()
