class AccountNotVerifiedError(Exception):
    def __init__(self, email,message="Your account has not been verified. Please check your email to verify your account."):
        self.message = message
        self.email = email
        super().__init__(self.message)