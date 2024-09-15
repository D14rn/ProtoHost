import socket


test_response1 = str.encode((
    "HTTP/1.0 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: 13\r\n"
    "\r\n"
    "Hello, World!"
))

test_response2 = str.encode((
    "HTTP/1.0 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
))

def get_test_response(num):
    html_content = f"Hello, HTTP!\nRequests made: {num}".encode()

    return str.encode((
    "HTTP/1.0 200 OK\r\n"
    "Content-Type: text/html\r\n"
    f"Content-Length: {len(html_content)}\r\n"
    "\r\n"
)) + html_content

class HttpServer:
    DEFAULT_BUFFER_SIZE = 1024
    DEFAULT_SOCKET = ('::1', 8080, 0, 0)
    MAX_CONNECTIONS = 1

    CONNECTION_COUNT = 0

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    def start(self):
        self.sock.bind(self.DEFAULT_SOCKET)
        self.sock.listen(self.MAX_CONNECTIONS)

        while True:
            client_conn, client_addr = self.sock.accept()
            self.CONNECTION_COUNT += 1
            print(client_conn)
            print(client_addr)
            print("NEW CONNECTION FROM", client_addr)
            client_conn.sendall(get_test_response(self.CONNECTION_COUNT))
            client_conn.close()
