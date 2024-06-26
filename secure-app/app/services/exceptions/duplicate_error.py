class DuplicateEmailException(Exception):
    def __init__(self, message="Email already exists."):
        self.message = message
        super().__init__(self.message)


class DuplicateUsernameException(Exception):
    def __init__(self, message="Username already exists."):
        self.message = message
        super().__init__(self.message)