from .base_user_validator import BaseUserValidator
from typing import Optional

class LoginUserValidator(BaseUserValidator):
    @staticmethod
    def validate(data: dict) -> Optional[str]:
        email_error = BaseUserValidator.validate_email(data.get('email', ''))
        if email_error:
            return email_error
        
        password_error = BaseUserValidator.validate_password(data.get('password', ''))
        if password_error:
            return password_error
        
        return None