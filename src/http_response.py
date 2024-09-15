from typing import NamedTuple
from .http_constants import HttpStatusCode


class HttpResponseLine(NamedTuple):
    version: str
    status_code: HttpStatusCode

    def __str__(self):
        return f"{self.version} {self.status_code.value}\r\n"

class HttpHeaders(NamedTuple):
    headers: dict[str, str]

    def __str__(self):
        return "".join(f"{name}: {value}\r\n" for name, value in self.headers.items())

class HttpResponseHead(NamedTuple):
    response_line: HttpResponseLine
    headers: HttpHeaders

    def __str__(self):
        return str(self.response_line) + str(self.headers)

class HttpResponseBody(NamedTuple):
    body: bytes

class HttpResponse(NamedTuple):
    head: HttpResponseHead
    body: HttpResponseBody = None

    @property
    def content_length(self):
        return len(self.body)

    @content_length.setter
    def content_length(self, length: str):
        self.head.headers["Content-Length"] = length


class HttpResponseFactory:
    @staticmethod
    def create_response_head(response_line: HttpResponseLine, headers: HttpHeaders) -> bytes:
        return ((
            f"{response_line}"
            f"{headers}"
            "\r\n"
        )).encode()
    
    @staticmethod
    def create_default_headers():
        return HttpHeaders({
            "Content-Length": "0"
        })
    
    @classmethod
    def create_error_response(cls, version: str, status_code: HttpStatusCode):
        response_line = HttpResponseLine(version, status_code)
        headers = cls.create_default_headers()
        head = HttpResponseHead(response_line, headers)
        return HttpResponse(head)
    
    @classmethod
    def not_found(cls, version: str, headers: HttpHeaders):
        return cls.create_response_head(
            HttpResponseLine(version, HttpStatusCode.NOT_FOUND),
            headers
        )
    
    @classmethod
    def version_not_supported(cls, version: str, headers: HttpHeaders):
        return cls.create_response_head(
            HttpResponseLine(version, HttpStatusCode.VERSION_NOT_SUPPORTED),
            headers
        )
    
    @classmethod
    def method_not_implemented(cls, version: str, headers: HttpHeaders):
        return cls.create_response_head(
            HttpResponseLine(version, HttpStatusCode.METHOD_NOT_IMPLEMENTED),
            headers
        )
    
    @classmethod
    def bad_request(cls, version: str, headers: HttpHeaders):
        return cls.create_response_head(
            HttpResponseLine(version, HttpStatusCode.BAD_REQUEST),
            headers
        )
