from app.services.user_service import UserService
from app.services.reset_token_service import ResetTokenService
from app.services.email_service import EmailService

from app.utils import password_utils
from app.models.user import User
from app.dto.user_dto import UserRegistrationDTO
from app.dto.reset_password_dto import ResetPasswordDTO

from app.services.exceptions import *

from typing import Optional

class AuthService:
    def __init__(self, user_service: UserService, reset_token_service: ResetTokenService, email_service: EmailService, redis_client):
        self.user_service = user_service
        self.reset_token_service = reset_token_service
        self.email_service = email_service
        self.redis_client = redis_client

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticates a user using email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            Optional[User]: The authenticated user if the credentials are valid, otherwise None.

        Raises:
            InvalidParameterException: If the email or password is invalid or missing.
            EntityNotFoundError: If the user is not found by the given email.
            InvalidPasswordException: If the password does not match.
            AccountLockedException: If the account is locked due to multiple failed attempts.
            DatabaseServiceError: If there is a database error.
        """
        if not email or not isinstance(email, str):
            raise InvalidParameterException("email", "Invalid or missing parameter")
        
        if not password or not isinstance(password, str):
            raise InvalidParameterException("password", "Invalid or missing parameter")

        try:
            user = self.user_service.get_user_by_email(email)

            user_id = user.id
            lockout_key = f"lockout:{user_id}"
            failed_attempts_key = f"failed_attempts:{user_id}"

            if self.redis_client.get(lockout_key):
                raise AccountLockedException()

            if password_utils.check_password(password, user.password):
                self.redis_client.delete(failed_attempts_key)
                return user
            else:
                failed_attempts = self.redis_client.incr(failed_attempts_key)
                if failed_attempts >= 5:
                    self.redis_client.set(lockout_key, "locked", ex=15*60)
                    raise AccountLockedException()
                raise InvalidPasswordException('Password does not match')

        except (InvalidParameterException, EntityNotFoundError, DatabaseServiceError) as e:
            raise e
        except Exception as e:
            raise e

    def register(self, user_dto: UserRegistrationDTO) -> User:
        """
        Registers a new user.

        Args:
            user_dto (UserRegistrationDTO): The data transfer object containing user registration information.

        Returns:
            User: The registered user.

        Raises:
            InvalidParameterException: If the user_dto or any of its values are invalid or missing.
            InvalidPasswordException: If the password does not meet the required length.
            DuplicateEmailException: If the email is already in use.
            DatabaseServiceError: If there is a database error.
        """
        if user_dto is None:
            raise InvalidParameterException("user dto", "Invalid or missing parameter")
        
        if any(value is None for value in vars(user_dto).values()):
            raise InvalidParameterException("user dto values", "Invalid or missing parameter")
        
        password = user_dto.password

        try:
            if len(password) < 8 or len(password) > 64:
                raise InvalidPasswordException("Password must be between 8 and 64 characters long")
            
            new_user = self.user_service.create_user(user_dto)

            return new_user
        except (InvalidParameterException, DuplicateEmailException, DatabaseServiceError) as e:
            raise e
        except Exception as e:
            raise e

    def reset_password(self, reset_password_dto: ResetPasswordDTO) -> User:
        """
        Resets the password for a user.

        Args:
            reset_password_dto (ResetPasswordDTO): The data transfer object containing reset password information.

        Returns:
            User: The user with the updated password.

        Raises:
            InvalidParameterException: If the reset_password_dto or any of its values are invalid or missing.
            ResetTokenException: If there is an error with the reset token.
            EntityNotFoundError: If the user is not found by the email associated with the token.
            DatabaseServiceError: If there is a database error.
        """
        if not reset_password_dto:
            raise InvalidParameterException("reset password dto", "Invalid or missing parameter")
        
        if any(value is None for value in vars(reset_password_dto).values()):
            raise InvalidParameterException("reset password dto values", "Invalid or missing parameter")
        
        token_str = reset_password_dto.token
        password = reset_password_dto.password

        try:
            token, email = self.reset_token_service.verify_token(token_str)
            user = self.user_service.get_user_by_email(email)
            updated_user = self.user_service.update_password(user.id, password)
            self.reset_token_service.set_used(token)
            return updated_user
        except (InvalidParameterException, ResetTokenException, EntityNotFoundError, DatabaseServiceError) as e:
            raise e
        except Exception as e:
            raise e