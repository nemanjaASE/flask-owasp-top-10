class ResetTokenException(Exception):
    def __init__(self, message="The token has already been used."):
        self.message = message
        super().__init__(self.message)