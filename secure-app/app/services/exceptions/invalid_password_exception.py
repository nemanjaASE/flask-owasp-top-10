class InvalidPasswordException(Exception):
    def __init__(self, email, message="Wrong password."):
        self.email = email
        self.message = message
        super().__init__(self.message)