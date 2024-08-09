class AccountNotVerifiedError(Exception):
    def __init__(self, message="Your account has not been verified. Please check your email to verify your account."):
        self.message = message
        super().__init__(self.message)