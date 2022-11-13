from typing import Dict, List
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import time
from base_types.account_type import Account
from base_types.stock_type import Stock
from fill_server.fill_server import StockTicker

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    accounts: Dict[str, Account] = {}
    stocks: Dict[str, Stock] = {}

    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self) -> None:
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self) -> None:
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self._set_response()
        self.post_router(post_data)

    def post_router(self, post_data: str) -> None:

        try:
            dict_data = json.loads(post_data)
        except ValueError:
            logging.exception("Incorrect payload format, cant decode")
        if self.path == "/fill":
            fill_data = StockTicker(**dict_data)
            print(fill_data)
            self.calculate_fills(fill_data)
        elif self.path == "/aum_tick":
            print(post_data)
            self.update_accounts_quantity(dict_data)
        else:
            logging.WARNING(f"Unknown path: {self.path}")

    def calculate_fills(self, stock_ticker: StockTicker):
        if stock_ticker.name in self.stocks:
            self.stocks[stock_ticker.name].add_stock_ticker(stock_ticker)
        else:
            self.stocks[stock_ticker.name] = Stock(stock_ticker)

    def update_accounts_quantity(self, aum_splits: Dict[str, str]):
        for account_name, percentage in aum_splits.items():
            if account_name in self.accounts:
                self.accounts[account_name].split = percentage
            else:
                self.accounts[account_name] = Account(
                    name=account_name, split=percentage
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
