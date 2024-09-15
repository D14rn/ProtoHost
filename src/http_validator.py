from .http_constants import HTTP_VERSIONS, HTTP_METHODS

class HttpValidator:
    # This class will validate different values of an HTTP request
    @staticmethod
    def validate_version(version: str):
        if not version in HTTP_VERSIONS:
            return False
        return True
    
    @staticmethod
    def validate_method(method: str):
        if not method in HTTP_METHODS:
            return False
        return True
