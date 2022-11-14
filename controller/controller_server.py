import math
from typing import Dict

import sys

# setting path
sys.path.append("../")

from base_types.account_type import Account
from base_types.stock_type import Stock

from fill_server.fill_server import StockTicker


class ControllerServer:
    accounts: Dict[str, Account] = {}
    stocks: Dict[str, Stock] = {}

    def __init__(self) -> None:
        print("Controller init")

    def recv_trade_fills(self) -> None:
        pass

    def calculate_fills(self, stock_ticker: StockTicker) -> Dict[str, Account]:
        if stock_ticker.name in self.stocks:
            self.stocks[stock_ticker.name].add_stock_ticker(stock_ticker)
        else:
            self.stocks[stock_ticker.name] = Stock(stock_ticker)

        overallsum = self.stocks[stock_ticker.name].quantity
        print(f"Overall stock quantity sum {overallsum}")
        free_stocks = stock_ticker.quantity
        stock_name = stock_ticker.name

        deficiency = {}  # the ammount of stocks is less then expected
        excess = {}  # the amount of stocks is more then expected
        match = {}  # the ammount of stocks match the expectations

        min_deficiency = 100  # begin with 100%
        sum_of_needs = 0
        for name, account in self.accounts.items():
            quantity = 0
            if stock_name in account.stocks:
                quantity = account.stocks[stock_name]
                print(f"Current quantity for {name} is {quantity}")
            current_percentage = quantity * 100 / overallsum
            quantity_difference = account.split * overallsum / 100 - quantity
            print(
                f"For {name} the current % is {current_percentage} expected {account.split} / {quantity_difference} stocks"
            )

            difference_p = account.split - current_percentage
            if current_percentage < account.split:
                sum_of_needs += quantity_difference
                min_deficiency = min(min_deficiency, difference_p)
                # print(f"min_deficiency: {min_deficiency}")
                deficiency[account.name] = {
                    "current_p": current_percentage,
                    "quantity": quantity,
                    "difference_p": difference_p,
                    "difference_q": quantity_difference,
                    "split": account.split
                }
            elif current_percentage > account.split:
                excess[account.name] = {
                    "current_p": current_percentage,
                    "quantity": quantity,
                    "difference_p": difference_p,
                    "difference_q": quantity_difference,
                    "split": account.split
                }
            else:
                match[account.name] = {
                    "current_p": current_percentage,
                    "quantity": quantity,
                    "difference_p": difference_p,
                    "difference_q": quantity_difference,
                    "split": account.split
                }

        print(f"Sum of needs for all: {sum_of_needs} , under available: {free_stocks}")
        # try to satisfy deficiency
        #min_deficienty_q = math.floor(min_deficiency * overallsum / 100)
        #print(f"Fill deficiency, min val is {min_deficienty_q}")
        wskaznik = free_stocks / sum_of_needs
        keys_to_remove = []
        for name, data in deficiency.items():
            share = math.floor(wskaznik*data["difference_q"])
            print(f"Add {share} to account {name}")
            deficiency[name]["quantity"] += share
            if not stock_name in self.accounts[name].stocks:
                self.accounts[name].stocks[stock_name]  = 0
            self.accounts[name].stocks[stock_name] += share
            if share >= data["difference_q"]:
                print(f"The requested shares where provided for account {name}")
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
            raise Exception(f"Algorithm error, not all stock assigned, free_stocks={free_stocks}")
        return self.accounts



    def update_accounts_quantity(self, aum_splits: Dict[str, int]):
        for account_name, percentage in aum_splits.items():
            if account_name in self.accounts:
                self.accounts[account_name].split = percentage
            else:
                self.accounts[account_name] = Account(
                    name=account_name, split=percentage
                )
