from app.repositories.author_requests_repository import AuthorRequestsRepository
from app.repositories.user_repository import UserRepository
from app.models.author_requests import AuthorRequests
from app.services.exceptions import *
from app.repositories.exceptions import *

from typing import Optional, List

class AuthorRequestsService:
    def __init__(self, author_requests_repository: AuthorRequestsRepository, user_repository: UserRepository) -> None:
        self.author_requests_repository = author_requests_repository
        self.user_repository = user_repository

    def create_author_request(self, user_id: str) -> AuthorRequests:
        """
        Creates an author requests.

        Args:
            user_id (str): The user id.

        Returns:
            AuthorRequests: The created author request object.

        Raises:
            InvalidParameterException: If the user_id is invalid or missing.
            DatabaseServiceError: If there is a database error.
        """
        if not user_id:
            raise InvalidParameterException("user id", "Invalid or missing parameter")
        
        try:
            author_request = AuthorRequests(
                user_id=user_id,
            )

            return self.author_requests_repository.create(author_request)
        
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e
        
    def check_existence(self, user_id: str) -> bool:
        """
        Checks if a user request for author role already exists.

        Args:
            user_id (str): The user ID to check.

        Returns:
            bool: True if the user id exists, False otherwise.

        Raises:
            InvalidParameterException: If the user id is invalid or missing.
            DatabaseServiceError: If there is a database error.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidParameterException("user id", "Invalid or missing parameter")

        try:
            return self.author_requests_repository.check_request(user_id)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e
        
    def get_all_author_requests(self) -> List[AuthorRequests]:
        """
        Retrieves all author requests.

        Returns:
            List[AuthorRequests]: A list of all author requests objects.

        Raises:
            DatabaseServiceError: If there is a database error.
        """
        try:
            return self.author_requests_repository.get_all()
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e
        
    def update_request(self, request_id: str, status: str) -> AuthorRequests:
        """
        Updates the fields of a AuthorRequests.

        Args:
            request_id (str): The request ID.
            status (str): The status of the request

        Returns:
            AuthorRequests: The updated author request object.

        Raises:
            InvalidParameterException: If the user id or status is invalid or missing.
            EntityNotFoundError: If the user is not found by the given ID.
            DatabaseServiceError: If there is a database error.
        """
        if not request_id:
            raise InvalidParameterException("update request id", "Invalid or missing parameter")
        if not status:
            raise InvalidParameterException("update status", "Invalid or missing parameter")

        try:
            return self.author_requests_repository.update_request(request_id, status)
            
        except NotFoundError as e:
            raise EntityNotFoundError("User", "ID", request_id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e
