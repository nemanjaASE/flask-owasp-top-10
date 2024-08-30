class EmailAlreadyExistsException(Exception):
    def __init__(self, email, message="Email already exists."):
        self.email = email
        self.message = message
        super().__init__(self.message)


class UsernameAlreadyExistsException(Exception):
    def __init__(self, username, message="Username already exists."):
        self.username = username
        self.message = message
        super().__init__(self.message)