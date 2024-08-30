class AccountLockedException(Exception):
    def __init__(self, email, message="Account is locked. Try again later."):
        self.email = email
        self.message = message
        super().__init__(self.message)