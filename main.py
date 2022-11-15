from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from controller.controller_server import StockController
from base_types.stock_ticker import StockTicker

hostName = "localhost"
serverPort = 8080

logging.basicConfig(level=logging.DEBUG)

STOCK_CONTROLLER = StockController()

class ControllerRestServer(BaseHTTPRequestHandler):

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
            logging.debug(fill_data)
            STOCK_CONTROLLER.calculate_fills(fill_data)
        elif self.path == "/aum_tick":
            logging.debug(post_data)
            STOCK_CONTROLLER.update_accounts_quantity(dict_data)
        else:
            logging.warning(f"Unknown path: {self.path}")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), ControllerRestServer)
    logging.info("Server started http://%s:%s" % (hostName, serverPort))
    
    logging.info('Starting background task...')
    daemon = Thread(target=STOCK_CONTROLLER.send_shares_to_position_server, args=(), daemon=True, name='Background')
    daemon.start()

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logging.info("Controller server stopped.")
