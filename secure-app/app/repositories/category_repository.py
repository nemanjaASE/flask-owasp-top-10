from app.models import Category
from app.repositories.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.exceptions import NotFoundError, DatabaseError

class CategoryRepository(BaseRepository[Category]):
    def __init__(self) -> None:
        super().__init__(Category)

    def get_by_name(self, name: str) -> Category:
        try:
            category = Category.query.filter_by(name=name).first()
            if category is None:
                raise NotFoundError(self.model.__name__, name)
            return category
        except SQLAlchemyError as e:
            raise DatabaseError(e)