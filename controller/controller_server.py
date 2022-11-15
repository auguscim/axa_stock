import logging
import math
import time
import http.client
from typing import Dict

import sys
from urllib.error import HTTPError

# setting path
sys.path.append("../")

from base_types.account_type import Account
from base_types.stock_type import Stock

from base_types.stock_ticker import StockTicker

POSITION_SERVER_UPDATES_INTERVAL: int = 30


class StockController:
    accounts: Dict[str, Account] = {}
    stocks: Dict[str, Stock] = {}
    serialized_accounts: str = "NO UPDATES"

    def __init__(self) -> None:
        logging.info("Stock controller init")

    def send_shares_to_position_server(self) -> None:
        while True:
            start_time = time.time()
            logging.info("-- Send data to position server")
            try:
                conn = http.client.HTTPConnection("localhost", 8081)
                headers = {"Content-type": "application/json"}
                conn.request("POST", "/", self.serialized_accounts, headers)
            except HTTPError as errh:
                logging.exception("Http Error:", errh)
            except ConnectionError as errc:
                logging.exception("Error Connecting:", errc)
            except Exception as err:
                logging.exception("Exception: ", err)

            time.sleep(POSITION_SERVER_UPDATES_INTERVAL + time.time() - start_time)

    def update_serialized_accounts(self) -> None:
        data = "STOCKS UPDATES\n"
        for name, account in self.accounts.items():
            data += f"Account name: {name}\n"
            for stock_name, quantity in account.stocks.items():
                data += f"  {stock_name} quantity {quantity}\n"
        self.serialized_accounts = data

    def calculate_fills(self, stock_ticker: StockTicker) -> Dict[str, Account]:
        if stock_ticker.name in self.stocks:
            self.stocks[stock_ticker.name].add_stock_ticker(stock_ticker)
        else:
            self.stocks[stock_ticker.name] = Stock(stock_ticker)

        overallsum = self.stocks[stock_ticker.name].quantity
        logging.debug(f"Overall stock quantity sum {overallsum}")
        free_stocks = stock_ticker.quantity
        stock_name = stock_ticker.name

        deficiency = {}  # the ammount of stocks is less then expected

        min_deficiency = 100  # begin with 100%
        sum_of_needs = 0
        for name, account in self.accounts.items():
            quantity = 0
            if stock_name in account.stocks:
                quantity = account.stocks[stock_name]
                logging.debug(f"Current quantity for {name} is {quantity}")
            current_percentage = quantity * 100 / overallsum
            quantity_difference = account.split * overallsum / 100 - quantity
            logging.debug(
                f"For {name} the current % is {current_percentage} expected {account.split} / {quantity_difference} stocks"
            )

            difference_p = account.split - current_percentage
            if current_percentage < account.split:
                sum_of_needs += quantity_difference
                min_deficiency = min(min_deficiency, difference_p)
                deficiency[account.name] = {
                    "quantity": quantity,
                    "difference_q": quantity_difference,
                }

        logging.debug(
            f"Sum of needs for all: {sum_of_needs} , under available: {free_stocks}"
        )
        # try to satisfy deficiency
        if sum_of_needs > 0:
            wskaznik = free_stocks / sum_of_needs
        else:
            sum_of_needs = 0
        keys_to_remove = []
        for name, data in deficiency.items():
            share = math.floor(wskaznik * data["difference_q"])
            logging.debug(f"Add {share} to account {name}")
            deficiency[name]["quantity"] += share
            if not stock_name in self.accounts[name].stocks:
                self.accounts[name].stocks[stock_name] = 0
            self.accounts[name].stocks[stock_name] += share
            if share >= data["difference_q"]:
                logging.debug(f"The requested shares where provided for account {name}")
                keys_to_remove.append(name)

            free_stocks -= share

        for name in keys_to_remove:
            del deficiency[name]

        while free_stocks > 0:
            for name in deficiency:
                self.accounts[name].stocks[stock_name] += 1
                free_stocks -= 1
                if not free_stocks:
                    break

        if free_stocks != 0:
            raise Exception(
                f"Algorithm error, not all stock assigned, free_stocks={free_stocks}"
            )

        self.update_serialized_accounts()
        return self.accounts

    def update_accounts_quantity(self, aum_splits: Dict[str, int]):
        for account_name, percentage in aum_splits.items():
            if account_name in self.accounts:
                self.accounts[account_name].split = percentage
            else:
                self.accounts[account_name] = Account(
                    name=account_name, split=percentage
                )
