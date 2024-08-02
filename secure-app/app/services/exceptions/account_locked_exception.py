class AccountLockedException(Exception):
    def __init__(self, message="Account is locked. Try again later."):
        self.message = message
        super().__init__(self.message)