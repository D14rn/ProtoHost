class HttpParser:
    # This class will mostly 'parse/format' data, requiring further validation on successful parsing
    @staticmethod
    def split_requesthead(head: str):
        res = head.split("\r\n", 1)
        if len(res) != 2:
            return None
        requestline, headers = res
        return (requestline, headers)
    
    @staticmethod
    def get_head_end(head: str):
        res = head.find("\r\n\r\n")
        if res == -1:
            return None
        return res

    @staticmethod
    def parse_requestline(requestline: str):
        parts = requestline.strip().split()
        if len(parts) != 3:
            return None
        method, uri, version = parts
        return (method, uri, version)

    @staticmethod
    def parse_headers(raw_headers: str):
        # We assume that the requestline and the last two \r\n have been removed
        headers = raw_headers.split("\r\n") # CRLF defined in RFC2616 & RFC7230
        header_dict = {}
        for header in headers:
            parts = header.split(": ")
            if len(parts) != 2:
                return None
            else:
                header_name, header_value = parts
                header_dict[header_name] = header_value
        return header_dict
