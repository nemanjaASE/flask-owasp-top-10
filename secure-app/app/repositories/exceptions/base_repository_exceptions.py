class BaseRepositoryError(Exception):
    def __init__(self, message: str = "An error occurred in the repository"):
        self.message = message
        super().__init__(self.message)