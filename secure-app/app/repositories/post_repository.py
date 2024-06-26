from app.models import Post
from app.repositories.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.exceptions import DatabaseError 

class PostRepository(BaseRepository[Post]):
    def __init__(self) -> None:
        super().__init__(Post)

    def count(self) -> int:
        try:
            return Post.query.count()
        except SQLAlchemyError as e:
            raise DatabaseError(e)