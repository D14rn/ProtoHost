from .http_parser import HttpParser
from socket import socket

class HttpRequest:
    INITIAL_BUFFER_SIZE = 1024
    MAX_BYTES = 65536
    def __init__(self, conn: socket) -> None:
        self.conn = conn
        self.bytes_read = 0
    
    def receive(self, buffer_size: int):
        if (self.bytes_read + buffer_size) > self.MAX_BYTES:
            return

        data = self.conn.recv(buffer_size)
        self.bytes_read += len(data)
        return data
    
    def receive_decoded(self, buffer_size: int):
        return self.receive(buffer_size).decode()

    def read_request(self):
        data = self.receive_decoded(self.INITIAL_BUFFER_SIZE)
        print(data)
        print(repr(data))
        header_end_idx = data.find("\r\n\r\n")
        if (header_end_idx == -1):
            self.conn.close()
        requestline, raw_headers = HttpParser.split_requesthead(data[:header_end_idx])
        headers = HttpParser.parse_headers(raw_headers)
        method, uri, version = HttpParser.parse_requestline(requestline)
