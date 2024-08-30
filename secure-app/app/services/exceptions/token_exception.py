class TokenException(Exception):
    def __init__(self, user_id, message="The token has already been used."):
        self.message = message
        self.user_id = user_id
        super().__init__(self.message)