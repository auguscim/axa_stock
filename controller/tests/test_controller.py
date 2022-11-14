import json
from typing import Dict, List, NamedTuple
import unittest
from controller_server import ControllerServer
from fill_server.fill_server import StockTicker


class TestControllerSplits(NamedTuple):
    stock_ticker: StockTicker
    aum_splits: Dict[str, int]
    expected: Dict[str, int]


test_data_controller_splits: List[TestControllerSplits] = [
    TestControllerSplits(
        stock_ticker=StockTicker("AXA", 20, 20),
        aum_splits={"Account1": 40, "Account2": 60},
        expected={"Account1": 8, "Account2": 12},
    ),
    TestControllerSplits(
        stock_ticker=StockTicker("AXA", 30, 3),
        aum_splits={"Account1": 5, "Account2": 45, "Account3": 50},
        expected={"Account1": 8, "Account2": 12, "Account3": 3},
    ),
    TestControllerSplits(
        stock_ticker=StockTicker("AXA", 30, 10),
        aum_splits={"Account1": 15, "Account2": 25, "Account3": 60},
        expected={"Account1": 8, "Account2": 12, "Account3": 13},
    ),
    TestControllerSplits(
        stock_ticker=StockTicker("WIG", 30, 100),
        aum_splits={"Account1": 20, "Account2": 10, "Account3": 20, "Account4": 50},
        expected={"Account1": 20, "Account2": 10, "Account3": 20, "Account4": 50},
    ),
    TestControllerSplits(
        stock_ticker=StockTicker("WIG", 30, 50),
        aum_splits={"Account1": 55, "Account2": 15, "Account3": 10, "Account4": 20},
        expected={"Account1": 62, "Account2": 18, "Account3": 20, "Account4": 50},
    )
]


class ControllerServerTest(unittest.TestCase):
    def test_controller_splits(self):
        server = ControllerServer()
        for (stock_ticker, aum_splits, expected) in test_data_controller_splits:
            server.update_accounts_quantity(aum_splits)
            result = server.calculate_fills(stock_ticker)
            for name, account in result.items():
                self.assertEqual(account.stocks[stock_ticker.name], expected[name])
            print("\n")


if __name__ == "__main__":
    unittest.main()
