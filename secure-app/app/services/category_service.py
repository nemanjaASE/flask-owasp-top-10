from typing import Optional, List

from app.models.post import Category
from app.repositories.category_repository import CategoryRepository
from app.services.exceptions import *
from app.repositories.exceptions import *

class CategoryService:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository

    def get_all_categories(self) -> List[Category]:
        """
        Retrieves all categories.

        Returns:
            List[Category]: A list of all category objects.

        Raises:
            DatabaseServiceError: If there is a database error.
        """
        try:
            return self.category_repository.get_all()
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def get_category_by_id(self, id: str) -> Optional[Category]:
        """
        Retrieves a category by their id.

        Args:
            id (str): The id of the category to retrieve.

        Returns:
            Optional[Category]: The category object if found, otherwise None.

        Raises:
            InvalidParameterException: If the name is invalid or missing.
            EntityNotFoundError: If the category is not found by the given id.
            DatabaseServiceError: If there is a database error.
        """
        if not id or not isinstance(id, str):
            raise InvalidParameterException("id", "Invalid or missing parameter")

        try:
            category = self.category_repository.get_by_id(id)
            if not category:
                raise NotFoundError(f"Category with anme {id} not found.")
            return category
        except NotFoundError as e:
            raise EntityNotFoundError("Category", "id", id) from e
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e