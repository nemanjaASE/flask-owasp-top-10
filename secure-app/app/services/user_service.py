from typing import Optional, List

from app.models.user import User
from app.dto.user_dto import UserRegistrationDTO
from app.dto.update_user_dto import UpdateUserDTO

from app.utils.password_utils import hash_password
from app.repositories.user_repository import UserRepository
from app.services.exceptions import *
from app.repositories.exceptions import *

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.

        Raises:
            InvalidParameterException: If the user_id is invalid or missing.
            EntityNotFoundError: If the user is not found.
            DatabaseServiceError: If there is a database error.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidParameterException("user ID", "Invalid or missing parameter")

        try:
            user = self.user_repository.get_by_id(user_id)
            return user
        except NotFoundError as e:
            raise EntityNotFoundError("User", "ID", user_id)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.

        Raises:
            InvalidParameterException: If the email is invalid or missing.
            EntityNotFoundError: If the user is not found by the given email.
            DatabaseServiceError: If there is a database error.
        """
        if not email or not isinstance(email, str):
            raise InvalidParameterException("email", "Invalid or missing parameter")

        try:
            user = self.user_repository.get_by_email(email)
            return user
        except NotFoundError as e:
            raise EntityNotFoundError("User", "email", email) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users.

        Returns:
            List[User]: A list of all user objects.

        Raises:
            DatabaseServiceError: If there is a database error.
        """
        try:
            return self.user_repository.get_all()
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def create_user(self, user_dto: UserRegistrationDTO) -> User:
        """
        Creates a new user.

        Args:
            user_dto (UserRegistrationDTO): The data transfer object containing user information.

        Returns:
            User: The created user object.

        Raises:
            InvalidParameterException: If the user_dto is invalid or missing.
            DuplicateEmailException: If the email is already in use.
            DuplicateUsernameException: If the username is already in use.
            DatabaseServiceError: If there is a database error.
        """
        
        try:
            if not self.is_email_unique(user_dto.email):
                raise DuplicateEmailException(f"Email {user_dto.email} is already in use")
            
            if not self.is_username_unique(user_dto.username):
                raise DuplicateUsernameException(f"Username {user_dto.username} is already in use")
            
            hashed_password = hash_password(user_dto.password)
            user = User(
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                username=user_dto.username,
                email=user_dto.email,
                birth_date=user_dto.birth_date,
                password=hashed_password,
            )

            return self.user_repository.create(user)
        
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def update_password(self, user_id: str, new_password: str) -> User:
        """
        Updates the password of a user.

        Args:
            user_id (str): The ID of the user whose password is to be updated.
            new_password (str): The new password to set.

        Returns:
            User: The updated user object.

        Raises:
            InvalidParameterException: If the user_id or new_password is invalid or missing.
            EntityNotFoundError: If the user is not found by the given ID.
            DatabaseServiceError: If there is a database error.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidParameterException("user id", "Invalid or missing parameter")
        
        if not new_password or not isinstance(new_password, str):
            raise InvalidParameterException("password", "Invalid or missing parameter")
        
        if len(new_password) < 8 or len(new_password) > 64:
            raise InvalidParameterException("password", "Password must be between 8 and 64 characters long")
        
        try:
            hashed_password = hash_password(new_password)
            return self.user_repository.update(user_id, password=hashed_password)
        except NotFoundError as e:
            raise EntityNotFoundError("User", "ID", user_id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def verify_user(self, user_id: str) -> User:
        """
        Verifying user.

        Args:
            user_id (str): The user ID

        Returns:
            User: The updated user object.

        Raises:
            InvalidParameterException: If the user ID is invalid or missing.
            EntityNotFoundError: If the user is not found by the given ID.
            DatabaseServiceError: If there is a database error.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidParameterException("user id", "Invalid or missing parameter")
       
        try:
           
            return self.user_repository.update(
                user_id,
                is_verified=True)
        
        except NotFoundError as e:
            raise EntityNotFoundError("User", "ID", user_id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def update_user(self, update_user_dto: UpdateUserDTO) -> User:
        """
        Updates the fields of a user.

        Args:
            update_user_dto (UpdateUserDTO): The data transfer object containing user information.

        Returns:
            User: The updated user object.

        Raises:
            InvalidParameterException: If the user dto is invalid or missing.
            EntityNotFoundError: If the user is not found by the given ID.
            DatabaseServiceError: If there is a database error.
        """
        if not isinstance(update_user_dto, UpdateUserDTO):
            raise InvalidParameterException("update user dto", "Invalid or missing parameter")
        
        user_id = update_user_dto.user_id
       
        try:
           
            return self.user_repository.update(
                user_id,
                first_name=update_user_dto.first_name,
                last_name=update_user_dto.last_name,
                username=update_user_dto.username,
                email=update_user_dto.email,
                birth_date=update_user_dto.birth_date)
        except NotFoundError as e:
            raise EntityNotFoundError("User", "ID", user_id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e


    def delete_user(self, user_id: str) -> User:
        """
        Deletes a user by their ID.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            User: The deleted user object.

        Raises:
            InvalidParameterException: If the user_id is invalid or missing.
            EntityNotFoundError: If the user is not found by the given ID.
            DatabaseServiceError: If there is a database error.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidParameterException("user ID", "Invalid or missing parameter")

        try:
            return self.user_repository.delete(user_id)
        except NotFoundError as e:
            raise EntityNotFoundError("User", "ID", user_id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def user_count(self) -> int:
        """
        Retrieves the total count of users.

        Returns:
            int: The total number of users.

        Raises:
            DatabaseServiceError: If there is a database error.
        """
        try:
            return self.user_repository.count()
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def is_username_unique(self, username: str) -> bool:
        """
        Checks if a username is unique.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username is unique, False otherwise.

        Raises:
            InvalidParameterException: If the username is invalid or missing.
            DatabaseServiceError: If there is a database error.
        """
        if not username or not isinstance(username, str):
            raise InvalidParameterException("username", "Invalid or missing parameter")

        try:
            return self.user_repository.is_username_unique(username)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def is_email_unique(self, email: str) -> bool:
        """
        Checks if an email is unique.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the email is unique, False otherwise.

        Raises:
            InvalidParameterException: If the email is invalid or missing.
            DatabaseServiceError: If there is a database error.
        """
        if not email or not isinstance(email, str):
            raise InvalidParameterException("email", "Invalid or missing parameter")

        try:
            return self.user_repository.is_email_unique(email)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e