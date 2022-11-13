from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import time
from fill_server.fill_server import StockTicker

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  
        post_data = self.rfile.read(content_length) 
        logging.info(
            "POST request,\nPath: %s\n\nBody:\n%s\n",
            str(self.path),
            post_data.decode("utf-8"),
        )

        self._set_response()
        self.post_router(post_data)

    def post_router(self, post_data) -> None:
        if self.path == "/fill":
            fill_data = StockTicker(json.loads(post_data))
            print(fill_data)
        else:
            logging.WARNING(f"Unknown path: {self.path}")


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
