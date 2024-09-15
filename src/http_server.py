import socket
from pathlib import Path
from .http_parser import HttpParser
from .http_response import *
from .http_constants import HttpStatusCode
from .http_validator import HttpValidator


routes = {
    "/": "index.html"
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
                "Content-type": "text/html; charset=UTF-8",
                "Content-Length": "0",
            }

            client_conn, client_addr = self.sock.accept()
            print("NEW CONNECTION FROM", client_addr)

            data = client_conn.recv(1024).decode('utf-8')
            header_end_idx = data.find("\r\n\r\n")
            if (header_end_idx == -1):
                client_conn.sendall(HttpResponseFactory.bad_request("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            split_requesthead = HttpParser.split_requesthead(data[:header_end_idx])

            if split_requesthead is None:
                client_conn.sendall(HttpResponseFactory.bad_request("HTTP/1.0", default_headers))
                client_conn.close()
                continue
            
            request_line, raw_headers = split_requesthead

            parsed_requestline = HttpParser.parse_requestline(request_line)

            if parsed_requestline is None:
                client_conn.sendall(HttpResponseFactory.bad_request("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            method, uri, version = parsed_requestline

            if uri not in routes:
                client_conn.sendall(HttpResponseFactory.not_found("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            if not HttpValidator.validate_method(method):
                client_conn.sendall(HttpResponseFactory.method_not_implemented("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            if not HttpValidator.validate_version(version):
                client_conn.sendall(HttpResponseFactory.version_not_supported("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            parsed_headers = HttpParser.parse_headers(raw_headers)

            if parsed_headers is None:
                client_conn.sendall(HttpResponseFactory.bad_request("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            public_folder = Path(__file__).parent.parent.resolve() / "public"

            target_file = public_folder / routes[uri]

            if (target_file).exists():
                with open(target_file, "rb") as f:
                    response_body = f.read()
            else:
                client_conn.sendall(HttpResponseFactory.not_found("HTTP/1.0", default_headers))
                client_conn.close()
                continue

            default_headers["Content-Length"] = str(len(response_body))

            response_head = HttpResponseFactory.create_response_head(HttpResponseLine("HTTP/1.0", HttpStatusCode.OK), HttpHeaders(default_headers))

            if method == "HEAD":
                client_conn.sendall(response_head)
            else:
                temp = response_head + response_body
                client_conn.sendall(temp)
            client_conn.close()
