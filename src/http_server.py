import socket
from .http_constants import HttpStatusCode
from .http_response import HttpResponseHandler
from .http_parser import HttpParser
from .http_router import HttpRouter


class HttpServer:
    SUPPORTED_VERSIONS = ("HTTP/1.0", "HTTP/1.1")
    IMPLEMENTED_METHODS = ("GET", "HEAD")
    FETCH_DEST_TO_CONTENT_TYPE = {
        "document": "text/html; charset=UTF-8",
        "script": "text/javascript; charset=UTF-8",
        "style": "text/css; charset=UTF-8"
    }

    def __init__(self, router: HttpRouter) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.router = router

    def start(self) -> None:
        self.sock.bind(("localhost", 8080))
        self.sock.listen(1)

        while True:
            http_version = "HTTP/1.0"
            client_conn, _ = self.sock.accept()
            response_handler = HttpResponseHandler(client_conn, http_version)

            data = client_conn.recv(1024).decode() # Initial read

            head_end_idx = HttpParser.get_head_end(data)
            if head_end_idx is None:
                response_handler.set_status_code(HttpStatusCode.BAD_REQUEST)
                response_handler.send_response()
                continue

            head = data[:head_end_idx + 4]

            request_head = HttpParser.split_requesthead(head)
            if request_head is None:
                response_handler.set_status_code(HttpStatusCode.BAD_REQUEST)
                response_handler.send_response()
                continue

            request_line, headers = request_head
            headers_dict = HttpParser.parse_headers(headers)

            request_line_parsed = HttpParser.parse_requestline(request_line)
            if request_line_parsed is None:
                response_handler.set_status_code(HttpStatusCode.BAD_REQUEST)
                response_handler.send_response()
                continue

            method, uri, version = request_line_parsed

            if version not in self.SUPPORTED_VERSIONS:
                response_handler.set_status_code(HttpStatusCode.VERSION_NOT_SUPPORTED)
                response_handler.send_response()
                continue

            if method not in self.IMPLEMENTED_METHODS:
                response_handler.set_status_code(HttpStatusCode.METHOD_NOT_IMPLEMENTED)
                response_handler.send_response()
                continue

            if not "Sec-Fetch-Dest" in headers_dict:
                response_handler.set_status_code(HttpStatusCode.INTERNAL_ERROR)
                response_handler.send_response()
                continue

            sec_fetch_dest = headers_dict["Sec-Fetch-Dest"]
            if sec_fetch_dest not in self.FETCH_DEST_TO_CONTENT_TYPE:
                response_handler.set_status_code(HttpStatusCode.INTERNAL_ERROR)
                response_handler.send_response()
                continue

            if (sec_fetch_dest == "document"):
                if not self.router.is_route(uri):
                    response_handler.set_status_code(HttpStatusCode.NOT_FOUND)
                    response_handler.send_response()
                    continue
                else:
                    body = self.router.route_content(self.router.routes[uri])
            else:
                response_handler.headers["Content-Type"] = self.FETCH_DEST_TO_CONTENT_TYPE[sec_fetch_dest]
                body = self.router.route_content(uri)

            if body is None:
                response_handler.set_status_code(HttpStatusCode.NOT_FOUND)
                response_handler.send_response()
                continue

            response_handler.set_body(body)
            if method == "HEAD":
                response_handler.send_response_head()
                continue
            response_handler.send_response()
