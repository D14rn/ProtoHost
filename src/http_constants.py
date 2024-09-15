from enum import Enum


HTTP_VERSIONS = ("HTTP/1.0", "HTTP/1.1", "HTTP/2.0")

class HttpStatusCode(Enum):
    OK = "200 OK"
    CREATED = "201 Created"
    BAD_REQUEST = "400 Bad Request"
    UNAUTHORIZED = "401 Unauthorized"
    FORBIDDEN = "403 Forbidden"
    NOT_FOUND = "404 Not Found"
    LENGTH_REQUIRED = "411 Length Required"
    TEAPOT = "418 I'm a teapot"
    INTERNAL_ERROR = "500 Internal Server Error"
    METHOD_NOT_IMPLEMENTED = "501 Not Implemented"
    VERSION_NOT_SUPPORTED = "505 HTTP Version Not Supported"