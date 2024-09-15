import socket
from pathlib import Path
from .http_parser import HttpParser
from .http_request import HttpRequest
from .http_response import *
from .http_constants import HttpStatusCode


routes = {
    "/": "/index.html",
}

supported_versions = ("HTTP/1.0", "HTTP/1.1")
supported_methods = ("GET", "HEAD")

class HttpServer:
    DEFAULT_BUFFER_SIZE = 1024
    DEFAULT_SOCKET = ('127.0.0.1', 8080)
    MAX_CONNECTIONS = 1

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.bind(self.DEFAULT_SOCKET)
        self.sock.listen(self.MAX_CONNECTIONS)

        while True:
            default_headers = {
                "Content-Length": "0"
            }

            client_conn, client_addr = self.sock.accept()
            print("NEW CONNECTION FROM", client_addr)

            data = client_conn.recv(1024).decode('utf-8')
            print(data)
            print(repr(data))
            header_end_idx = data.find("\r\n\r\n")
            if (header_end_idx == -1):
                client_conn.sendall(create_bad_request_response("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            try:
                requestline, raw_headers = HttpParser.split_requesthead(data[:header_end_idx])
                headers = HttpParser.parse_headers(raw_headers)
                method, uri, version = HttpParser.parse_requestline(requestline)
            except:
                client_conn.sendall(create_bad_request_response("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            if not version in supported_versions:
                client_conn.sendall(create_http_version_not_supported_response("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            if not method in supported_methods:
                client_conn.sendall(create_http_method_not_implemented_response("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            print(uri)
            print(routes[uri])
            x = Path(__file__).parent.parent.resolve()
            print(x)
            y = x / f"public{routes[uri]}"
            print(y)
            if (y).exists():
                print("route match")
                with open(y, "rb") as f:
                    temp_data = f.read()
            else:
                create_not_found_response("HTTP/1.0", default_headers)

            html = temp_data

            # client_conn.sendall(get_error_response())
            # html = f"<p>Headers</p><p>{headers}</p><p>Method: {method}</p><p>URI: {uri}</p><p>Version: {version}</p>".encode()
            default_headers["Content-Length"] = str(len(html))
            head = create_response_head("HTTP/1.0", HttpStatusCode.OK, default_headers)
            if method == "HEAD":
                client_conn.sendall(head)
            else:
                temp = head + html
                client_conn.sendall(temp)
            client_conn.close()
