from .http_server import HttpServer
# from .http6_server import HttpServer

if __name__ == "__main__":
    server = HttpServer()
    server.start()
