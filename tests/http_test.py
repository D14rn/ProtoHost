import unittest
from src import HttpParser


class HttpParserTest(unittest.TestCase):
    def test_requestline(self):
        test_requestlines = {
            "GET / HTTP/1.1\r\n": ("GET", "/", "HTTP/1.1"),
            "POST /api/posts HTTP/1.1": ("POST", "/api/posts", "HTTP/1.1")
        }

        for requestline, expected in test_requestlines.items():
            res = HttpParser.parse_requestline(requestline)
            self.assertEqual(res, expected)

    def test_version(self):
        test_versions = {
            "HTTP/1.0": "1.0",
            "HTTP/1.1": "1.1"
        }

        for version, expected in test_versions.items():
            res = HttpParser.parse_version(version)
            self.assertEqual(res, expected)

    def test_headers(self):
        raw_headers = """Host: en.wikipedia.org\r\n\
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0\r\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8\r\n\
Accept-Language: en-US,en;q=0.5\r\n\
Accept-Encoding: gzip, deflate, br, zstd\r\n\
Connection: keep-alive\r\n\
Cookie: IsNoGood=naur; Burr=nah\r\n\
Upgrade-Insecure-Requests: 1\r\n\
Sec-Fetch-Dest: document\r\n\
Sec-Fetch-Mode: navigate\r\n\
Sec-Fetch-Site: none\r\n\
Sec-Fetch-User: ?1\r\n\
Priority: u=0, i\r\n"""

        expected = {
            "Host": "en.wikipedia.org",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Cookie": "IsNoGood=naur; Burr=nah",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Priority": "u=0, i"
        }

        res = HttpParser.parse_headers(raw_headers)
        self.assertEqual(res, expected)
