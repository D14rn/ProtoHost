import socket
from .http_constants import HttpStatusCode

class HttpResponseHandler:
    def __init__(self, conn: socket.socket, http_version: str) -> None:
        self.conn = conn
        self.http_version = http_version
        self.status_code: str = HttpStatusCode.OK.value
        self.headers = self.create_default_headers()
        self.body: bytes = "".encode()
    
    @staticmethod
    def create_default_headers() -> dict[str, str]:
        return {
            "Content-Type": "text/html; charset=UTF-8",
            "Content-Length": "0"
        }

    def send_response(self) -> None:
        self.conn.sendall(self.create_response())
        self.conn.close()
    
    def send_response_head(self) -> None:
        self.conn.sendall(self.create_response_head())
        self.conn.close()
    
    def create_response(self) -> bytes:
        return self.create_response_head() + self.body
    
    def set_status_code(self, status_code: HttpStatusCode) -> None:
        self.status_code = status_code.value
    
    def set_body(self, body: bytes) -> None:
        self.body = body
        self.headers["Content-Length"] = len(body)

    def create_response_head(self) -> bytes:
        response_line = self.create_response_line()
        headers = self.headers_to_str()

        head = response_line + headers + "\r\n"

        return head.encode()

    def create_response_line(self) -> str:
        return f"{self.http_version} {self.status_code}\r\n"

    def headers_to_str(self) -> str:
        return "".join(f"{name}: {value}\r\n" for name, value in self.headers.items())
