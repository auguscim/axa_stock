from abc import abstractmethod
import http.client
import json
import logging
import random
import time
from typing import List, NamedTuple


class AUMSplit(NamedTuple):
    account_name: str
    percentage: int


class AUMSplitGenerator:
    @abstractmethod
    def generate_aum_split(account_name, max_percentage: int = 100) -> AUMSplit:
        if not account_name:
            raise Exception("Cannot generate stock with an empty name")
        percentage = random.randint(0, max_percentage)
        return AUMSplit(account_name=account_name, percentage=percentage)


class AUMServer:
    aum_splits_list: List[AUMSplit] = []

    def __init__(self) -> None:
        logging.info("Starting AUM server")

        self.aum_splits_list.append(AUMSplit(account_name="account1", percentage=30))
        self.aum_splits_list.append(AUMSplit(account_name="account2", percentage=35))
        self.aum_splits_list.append(AUMSplit(account_name="account3", percentage=35))

    def create_payload(self) -> str:
        payload = {}
        percentage_range = 100
        splits_list_lenght = len(self.aum_splits_list)
        for key in range(splits_list_lenght):
            if key == (splits_list_lenght-1):
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
        conn.request("POST", "/aum_tick", payload, headers)

        response = conn.getresponse()
        logging.info(f"Response: {response.read().decode()}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aum_server_instance = AUMServer()

    aum_server_instance.processing()
