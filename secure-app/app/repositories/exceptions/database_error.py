from app.repositories.exceptions.base_repository_exceptions import BaseRepositoryError

class DatabaseError(BaseRepositoryError):
    def __init__(self, original_exception: Exception):
        message = f"An error occurred while accessing the database: {original_exception}"
        super().__init__(message)