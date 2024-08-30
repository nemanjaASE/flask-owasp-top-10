class TokenExpiredException(Exception):
    def __init__(self, message="Token expired."):
        super().__init__(self.message)