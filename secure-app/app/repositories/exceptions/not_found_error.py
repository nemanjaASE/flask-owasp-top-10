from app.repositories.exceptions.base_repository_exceptions import BaseRepositoryError

class NotFoundError(BaseRepositoryError):
    def __init__(self, entity_name: str, entity_id: str):
        message = f"{entity_name} with id {entity_id} not found"
        super().__init__(message)