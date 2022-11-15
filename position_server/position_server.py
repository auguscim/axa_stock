from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

hostName = "localhost"
serverPort = 8081

logging.basicConfig(level=logging.DEBUG)


class PositionServer(BaseHTTPRequestHandler):
    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self) -> None:
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self) -> None:
        content_length = int(self.headers["Content-Length"])
        post_data = str(self.rfile.read(content_length).decode("utf-8"))
        self._set_response()
        print(post_data)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), PositionServer)
    logging.info("Position server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logging.info("Position server server stopped.")
