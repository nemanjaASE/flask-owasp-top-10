import re
from typing import Optional, List, Any
from datetime import datetime, date

class BaseUserValidator:
     @staticmethod
     def validate_email(email: str) -> Optional[str]:
        if not email or len(email) > 32:
            return 'Email must not be empty and must be less than 32 characters long.'
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return 'Invalid email format.'
        return None
     
     @staticmethod
     def validate_password(password: str) -> Optional[str]:
        if not password or len(password) < 8 or len(password) > 64:
            return 'Password must be between 8 and 64 characters long.'
        if not re.match(r'^[A-Za-z\d@$!%*?&]{8,64}$', password):
            return 'Password can only contain letters, numbers, and special characters @$!%*?&.'
        return None
    
     @staticmethod
     def validate_first_name(first_name: str) -> Optional[str]:
        if not first_name:
            return 'First name cannot be empty.'
        if len(first_name) > 24:
            return 'First name must be 24 characters or less.'
        if not re.match(r'^[A-Za-z\s]+$', first_name):
            return 'First name can only contain letters and spaces.'
        return None
     
     @staticmethod
     def validate_last_name(last_name: str) -> Optional[str]:
        if not last_name:
            return 'Last name cannot be empty.'
        if len(last_name) > 24:
            return 'Last name must be 24 characters or less.'
        if not re.match(r'^[A-Za-z\s]+$', last_name):
            return 'Last name can only contain letters and spaces.'
        return None
     
     @staticmethod
     def validate_username(username: str) -> Optional[str]:
        if not username:
            return 'Username cannot be empty.'
        if len(username) > 24:
            return 'Username must be 24 characters or less.'
        if not re.match(r'^[\w]+$', username):
            return 'Username can only contain letters, numbers, and underscores.'
        return None
     
     @staticmethod
     def validate_confirm_password(password: str, confirm_password: str) -> Optional[str]:
        error = BaseUserValidator.validate_password(confirm_password)
        if error:
            return error
        if password != confirm_password:
            return 'Passwords must match.'
        return None
     
     @staticmethod
     def validate_birth_date(birth_date: date) -> Optional[str]:
        if not birth_date:
            return 'Birth cannot be empty.'
        try:
            datetime.strftime(birth_date, '%Y-%m-%d')
        except ValueError:
            return 'Birth date must be in the format YYYY-MM-DD.'
        return None
     
     @staticmethod
     def validate_title(title: str) -> Optional[str]:
         if not title:
             return 'Title cannot be empty.'
         if len(title) > 128:
            return 'Title must be 128 characters or less.'
         return None
     
     @staticmethod
     def validate_content(body: str) -> Optional[str]:
         if not body:
             return 'Body cannot be empty.'
         return None
     
     from typing import Optional, List, Any

     @staticmethod
     def validate_category(categories: List[Any]) -> Optional[str]:
         if not isinstance(categories, list):
             return 'Categories must be a list.'
         if not categories:
             return 'Category cannot be empty.'
         return None
         
         