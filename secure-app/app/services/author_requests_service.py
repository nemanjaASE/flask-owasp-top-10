from app.repositories.author_requests_repository import AuthorRequestsRepository
from app.repositories import UserRepository
from app.models.author_requests import AuthorRequests
from app.services.exceptions import *
from app.repositories.exceptions import *

from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

class AuthorRequestsService:
    def __init__(self, author_requests_repository: AuthorRequestsRepository, user_repository: UserRepository) -> None:
        self.author_requests_repository = author_requests_repository
        self.user_repository = user_repository

    def get_author_request(self, request_id: str) -> Optional[AuthorRequests]:
        """
        Retrieves a author request by their ID.

        Args:
            author_id (str): The ID of the author request to retrieve.

        Returns:
            Optional[AuthorRequests]: The request object if found, otherwise None.

        Raises:
            InvalidInputException: If the request_id is invalid or missing.
            EntityNotFoundError: If the request is not found.
            DatabaseServiceError: If there is a database error.
        """
        try:
            request = self.author_requests_repository.get_by_id(request_id)
            return request
        except NotFoundError as e:
            raise EntityNotFoundError("AuthorRequest", "ID", request_id)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e


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
            raise InvalidInputException("user id", "Invalid or missing parameter")
        
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
        if not user_id:
            raise InvalidInputException("user id", "Invalid or missing parameter")

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

    def update_author_request(self, request_id: str, status: str) -> AuthorRequests:
        """
        Updates the fields of a author requests.

        Args:
             request_id (str): The request ID
             status (str): The status of the transaction

        Returns:
            AuthorRequest: The updated request object.

        Raises:
            InvalidInputException: If the request_id or status is invalid or missing.
            EntityNotFoundError: If the request is not found by the given ID.
            DatabaseServiceError: If there is a database error.
        """
        try:
           
            return self.author_requests_repository.update_request(request_id, status=status)
        except NotFoundError as e:
            raise EntityNotFoundError("AuthorRequest", "ID", request_id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e