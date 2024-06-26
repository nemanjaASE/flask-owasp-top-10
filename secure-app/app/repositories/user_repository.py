from app.models import User
from app.repositories.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.exceptions import NotFoundError, DatabaseError 

class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)
        
    def get_by_email(self, email: str) -> User:
        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                raise NotFoundError(self.model.__name__, email)
            return user
        except SQLAlchemyError as e:
            raise DatabaseError(e)

    def count(self) -> int:
        try:
            return User.query.count()
        except SQLAlchemyError as e:
            raise DatabaseError(e)

    def is_username_unique(self, username: str) -> bool:
        try:
            return User.query.filter_by(username=username).first() is None
        except SQLAlchemyError as e:
            raise DatabaseError(e)

    def is_email_unique(self, email: str) -> bool:
        try:
            return User.query.filter_by(email=email).first() is None
        except SQLAlchemyError as e:
            raise DatabaseError(e)