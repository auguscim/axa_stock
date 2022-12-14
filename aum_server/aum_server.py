import http.client
import json
import logging
import random
import time
from typing import List

from urllib.error import HTTPError

from aum_split_type import AUMSplit
from aum_split_generator import AUMSplitGenerator

MIN_ACCOUNTS_NUMBER: int = 2
MAX_ACCOUNTS_NUMBER: int = 5


class AUMServer:
    aum_splits_list: List[AUMSplit] = []

    def __init__(self) -> None:
        logging.info("Starting AUM server")

    def create_payload(self) -> str:
        accounts_numb = random.randint(MIN_ACCOUNTS_NUMBER, MAX_ACCOUNTS_NUMBER)
        self.aum_splits_list = []
        for i in range(1, accounts_numb):
            self.aum_splits_list.append(
                AUMSplit(account_name=f"account{i}", percentage=0)
            )
        payload = {}
        percentage_range = 100
        splits_list_lenght = len(self.aum_splits_list)
        for key in range(splits_list_lenght):
            if key == (splits_list_lenght - 1):
                new_aum_split = AUMSplit(
                    self.aum_splits_list[key].account_name, percentage_range
                )
            else:
                new_aum_split = AUMSplitGenerator.generate_aum_split(
                    self.aum_splits_list[key].account_name, percentage_range
                )
            percentage_range = percentage_range - new_aum_split.percentage
            self.aum_splits_list[key] = new_aum_split
            payload[new_aum_split.account_name] = new_aum_split.percentage
        return json.dumps(payload)

    def processing(self) -> None:
        try:
            while True:
                self.call_controller(self.create_payload())
                time.sleep(10)
        except KeyboardInterrupt:
            pass

    def call_controller(self, payload: str) -> None:
        conn = http.client.HTTPConnection("localhost", 8080)

        headers = {"Content-type": "application/json"}

        logging.info(f"Call controller with data: {payload}")
        try:
            conn.request("POST", "/aum_tick", payload, headers)
        except HTTPError as errh:
            logging.exception("Http Error:", errh)
        except ConnectionError as errc:
            logging.exception("Error Connecting:", errc)
        except Exception as err:
            logging.exception("Exception: ", err)

        response = conn.getresponse()
        logging.info(f"Response: {response.read().decode()}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aum_server_instance = AUMServer()

    aum_server_instance.processing()
