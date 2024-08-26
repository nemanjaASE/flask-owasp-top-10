from .base_user_validator import BaseUserValidator
from typing import Optional

class CreatePostValidator(BaseUserValidator):
    @staticmethod
    def validate(data: dict) -> Optional[str]:
        title_error = BaseUserValidator.validate_title(data.get('title', ''))
        if title_error:
            return title_error
        
        body_error = BaseUserValidator.validate_content(data.get('body', ''))
        if body_error:
            return body_error
        
        category_error = BaseUserValidator.validate_category(data.get('categories', ''))
        if category_error:
            return category_error
        
        return None