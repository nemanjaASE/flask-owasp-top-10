from app.services.exceptions.service_error import ServiceError

class DatabaseServiceError(ServiceError):
    def __init__(self, original_exception: Exception):
        message = f"An error occurred while accessing the database: {original_exception}"
        super().__init__(message)