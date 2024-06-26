from app.services.exceptions.service_error import ServiceError

class EntityNotFoundError(ServiceError):
    def __init__(self, entity_name: str, field_name: str, field_value: str):
        message = f"{entity_name} with {field_name} '{field_value}' not found"
        super().__init__(message)