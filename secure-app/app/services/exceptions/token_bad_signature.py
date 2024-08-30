class TokenBadSignatureException(Exception):
    def __init__(self, message="Token bad signature."):
        super().__init__(self.message)