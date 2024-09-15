from .http_constants import HttpStatusCode, HTTP_VERSIONS


def headers_to_str(headers: dict[str, str]):
    return "".join(f"{name}: {value}\r\n" for name, value in headers.items())

def create_response_head(http_version: str, status_code: HttpStatusCode, headers: dict[str, str]) -> bytes:
    return ((
        f"{http_version} {status_code.value}\r\n"
        f"{headers_to_str(headers)}"
        "\r\n"
    )).encode()

def create_http_version_not_supported_response(http_version: str, headers: dict[str, str]):
    return create_response_head(http_version, HttpStatusCode.VERSION_NOT_SUPPORTED, headers)

def create_http_method_not_implemented_response(http_version: str, headers: dict[str, str]):
    return create_response_head(http_version, HttpStatusCode.METHOD_NOT_IMPLEMENTED, headers)

def create_bad_request_response(http_version: str, headers: dict[str, str]):
    return create_response_head(http_version, HttpStatusCode.BAD_REQUEST, headers)

def create_not_found_response(http_version: str, headers: dict[str, str]):
    return create_response_head(http_version, HttpStatusCode.NOT_FOUND, headers)

class HttpResponseLine:
    def __init__(self, http_version: str, status_code: HttpStatusCode) -> None:
        if not isinstance(http_version, str):
            raise TypeError("http_version must be of type str")
        if http_version not in HTTP_VERSIONS:
            raise ValueError("http_version must have value in HTTP_VERSIONS")
        if not isinstance(status_code, HttpStatusCode):
            raise TypeError("status_code must be type HttpStatusCode")

        self.http_version = http_version
        self.status_code = status_code

    def __str__(self):
        return f"{self.http_version} {self.status_code.value}\r\n"

class HttpHeaders:
    def __init__(self, headers: dict[str, str]) -> None:
        self.headers = headers
    
    def __str__(self):
        return "".join(f"{name}: {value}\r\n" for name, value in self.headers.items())

class ResponseHead:
    def __init__(self, response_line: HttpResponseLine, headers: HttpHeaders) -> None:
        self.response_line = response_line
        self.headers = headers
    
    def __str__(self):
        return self.response_line + self.headers

# class HttpResponse:
#     def __init__(self, conn: socket):
#         self.conn = conn

#     @staticmethod
#     def bad_request():
#         return str.encode((
#             "HTTP/1.0 400 Bad request\r\n"
#             "Content-Length: 0\r\n"
#             "\r\n"
#         ))


if __name__ == "__main__":
    test_status_code = HttpStatusCode.NOT_FOUND
    print(test_status_code.name, test_status_code.value)
    print(test_status_code in HttpStatusCode)
    print(type(test_status_code) is HttpStatusCode)
    print(test_status_code is HttpStatusCode.NOT_FOUND)
    print("404 Not Found" in HttpStatusCode._value2member_map_)

    # test_headers = {
    #     "Host": "localhost",
    #     "Content-Length": "102"
    # }
    # test_http_headers = HttpHeaders(test_headers)
    # print(str(test_http_headers).encode())

# test_response1 = str.encode((
#     "HTTP/1.0 200 OK\r\n"
#     "Content-Type: text/html\r\n"
#     "Content-Length: 13\r\n"
#     "\r\n"
#     "Hello, World!"
# ))

# test_response2 = str.encode((
#     "HTTP/1.0 200 OK\r\n"
#     "Content-Type: text/html\r\n"
#     "Content-Length: 0\r\n"
#     "\r\n"
# ))

# def get_test_response(num):
#     html_content = f"Hello, HTTP!\nRequests made: {num}".encode()

#     return str.encode((
#     "HTTP/1.0 200 OK\r\n"
#     "Content-Type: text/html\r\n"
#     f"Content-Length: {len(html_content)}\r\n"
#     "\r\n"
# )) + html_content

# def get_http_response(body: str):
#     return str.encode((
#         "HTTP/1.0 200 OK\r\n"
#         "Content-Type: text/html\r\n"
#         f"Content-Length: {len(body)}\r\n"
#         "\r\n"
#     )) + body.encode()

# def get_error_response():
#     return str.encode((
#         "HTTP/1.0 400 Bad request\r\n"
#         "Content-Length: 0\r\n"
#         "\r\n"
#     ))