from app.services import (UserService, ResetTokenService, EmailService)
from app.services.exceptions import *
from app.services.validators.login_user_validator import LoginUserValidator
from app.services.validators.register_user_validator import RegisterUserValidator
from app.services.validators. register_user_validator import BaseUserValidator

from app.utils import password_utils
from app.models.user import User
from app.dto.user_dto import UserRegistrationDTO
from app.dto.reset_password_dto import ResetPasswordDTO
from sqlalchemy.exc import SQLAlchemyError
from app.db import transaction
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
            InvalidInputException: If the email or password is invalid or missing.
            AccountNotVerifiedError: If the user account is not verified
            EntityNotFoundError: If the user is not found by the given email.
            InvalidPasswordException: If the password does not match.
            AccountLockedException: If the account is locked due to multiple failed attempts.
            DatabaseServiceError: If there is a database error.
        """
        msg = LoginUserValidator.validate({
            "email": email,
            "password": password
        })

        if msg:
            raise InvalidInputException("email or password", "Invalid or missing input")

        try:
            user = self.user_service.get_user_by_email(email)
            if not user.is_verified:
                raise AccountNotVerifiedError(email)

            user_id = user.id
            lockout_key = f"lockout:{user_id}"
            failed_attempts_key = f"failed_attempts:{user_id}"

            if self.redis_client.get(lockout_key):
                raise AccountLockedException(email)

            if password_utils.check_password(password, user.password):
                self.redis_client.delete(failed_attempts_key)
                return user
            else:
                failed_attempts = self.redis_client.incr(failed_attempts_key)
                if failed_attempts >= 5:
                    self.redis_client.set(lockout_key, "locked", ex=15*60)
                    raise AccountLockedException(email)
                raise InvalidPasswordException(email, 'Password does not match')

        except (InvalidInputException, EntityNotFoundError, DatabaseServiceError, Exception) as e:
            raise e

    def register(self, user_dto: UserRegistrationDTO) -> User:
        """
        Registers a new user.

        Args:
            user_dto (UserRegistrationDTO): The data transfer object containing user registration information.

        Returns:
            User: The registered user.

        Raises:
            InvalidInputException: If the user_dto or any of its values are invalid or missing.
            DuplicateEmailException: If the email is already in use.
            DatabaseServiceError: If there is a database error.
            EmailAlreadyExistsException: If the user with provided email already exists
            UsernameAlreadyExistsException: If the user with provided username already exists
        """

        msg = RegisterUserValidator.validate(user_dto.__dict__)
        
        if msg:
            raise InvalidInputException("user register", "Invalid or missing input")

        try:
            new_user = self.user_service.create_user(user_dto)

            return new_user
        except (InvalidInputException,UsernameAlreadyExistsException, EmailAlreadyExistsException, DatabaseServiceError, Exception) as e:
            raise e

    def reset_password(self, reset_password_dto: ResetPasswordDTO) -> User:
        """
        Resets the password for a user.

        Args:
            reset_password_dto (ResetPasswordDTO): The data transfer object containing reset password information.

        Returns:
            User: The user with the updated password.

        Raises:
            InvalidInputException: If the reset_password_dto or any of its values are invalid or missing.
            TokenException: If there is an error with the reset token.
            EntityNotFoundError: If the user is not found by the email associated with the token.
            DatabaseServiceError: If there is a database error.
        """
        msg = BaseUserValidator.validate_password(reset_password_dto.password)

        if msg:
            raise InvalidInputException("password", 'Nevalidan ili nedostajući unos.')

        token_str = reset_password_dto.token
        password = reset_password_dto.password

        try:
            with transaction():
                token, email = self.reset_token_service.verify_reset_token(token_str)
                user = self.user_service.get_user_by_email(email)

                updated_user = self.user_service.update_password(user.id, password)
                self.reset_token_service.set_reset_used(token)

            return updated_user

        except (TokenException, InvalidInputException, EntityNotFoundError) as e:
            raise e
        except SQLAlchemyError as e:
            raise DatabaseServiceError("An error occurred while updating the request.") from e