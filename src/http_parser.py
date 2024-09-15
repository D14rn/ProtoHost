class HttpParsingException(Exception):
    pass

class HttpParser:
    # This class will merely 'parse/format' data for later validation
    @staticmethod
    def split_requesthead(head: str):
        res = head.split("\r\n", 1)
        if len(res) != 2:
            raise HttpParsingException("Wrong HTTP headers format")
        requestline, headers = res
        return (requestline, headers)
    
    @staticmethod
    def get_head_end(head: str):
        res = head.find("\r\n\r\n")
        if res == -1:
            return False
        return res

    @staticmethod
    def parse_requestline(requestline: str):
        if requestline.count(' ') != 2: # Verify that it contains the spaces between each part METHOD URI VERSION
            raise HttpParsingException("Wrong HTTP requestline format")

        res = requestline.strip().split()
        method, uri, version = res
        return (method, uri, version)

    @staticmethod
    def parse_version(version: str):
        res = version.split("/")

        if ((len(res) != 2) or (res[0] != "HTTP")):
            raise HttpParsingException("Wrong HTTP version format")

        version_num = res[1]
        return version_num

    @staticmethod
    def parse_headers(raw_headers: str):
        try:
            headers = raw_headers.split("\r\n") # CRLF defined in RFC2616 & RFC7230
            headers.pop() # Remove last match (there is an empty match at the end)
            header_list = [header.split(": ", 1) for header in headers] # List of (field-name, field-value) tuples
            return {header_key: header_value for header_key, header_value in header_list} # Dictionary of field-name: field-value
        except:
            raise HttpParsingException("Wrong headers format")
