from .http_server import HttpServer
from .http_router import HttpRouter

if __name__ == "__main__":
    router = HttpRouter(r"path/to/public/folder")
    router.add_route("/", "index.html")
    router.add_route("/index.html", "index.html")

    server = HttpServer(router)
    server.start()
