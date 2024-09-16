from pathlib import Path

class HttpRouter:
    def __init__(self, public_folder: str) -> None:
        self.routes: dict[str, str] = {}
        self.public_folder = Path(public_folder)

    def add_route(self, route: str, filepath: str) -> None:
        self.routes[route] = filepath

    def is_route(self, route: str) -> str | None:
        if route not in self.routes:
            return False
        return True
    
    def route_content(self, uri: str) -> bytes | None:
        if uri.startswith('/'):
            uri = uri[1:]
        target_file = self.public_folder / uri
        if not target_file.exists():
            return None
    
        with open(target_file, "rb") as f:
            return f.read()
