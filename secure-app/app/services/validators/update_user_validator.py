from .base_user_validator import BaseUserValidator
from typing import Optional

class UpdateUserValidator(BaseUserValidator):
    @staticmethod
    def validate(data: dict) -> Optional[str]:
        first_name_error = BaseUserValidator.validate_first_name(data.get('first_name', ''))
        if first_name_error:
            return first_name_error
        
        last_name_error = BaseUserValidator.validate_last_name(data.get('last_name', ''))
        if last_name_error:
            return last_name_error

        username_error = BaseUserValidator.validate_username(data.get('username', ''))
        if username_error:
            return username_error

        email_error = BaseUserValidator.validate_email(data.get('email', ''))
        if email_error:
            return email_error

        birth_date_error = BaseUserValidator.validate_birth_date(data.get('birth_date', ''))    
        if birth_date_error:
            return birth_date_error

        return None