from app.models.reset_token import ResetToken
from app.repositories.base_repository import BaseRepository

from sqlalchemy.exc import SQLAlchemyError
from app.repositories.exceptions import NotFoundError, DatabaseError 


class ResetTokenRepository(BaseRepository[ResetToken]):
    def __init__(self) -> None:
        super().__init__(ResetToken)

    def get_by_name(self, token: str) -> ResetToken:
        try:
            reset_token =  ResetToken.query.filter_by(token=token).first()
            if reset_token is None:
                raise NotFoundError(self.model.__name__, token)
            return reset_token
        except SQLAlchemyError as e:
            raise DatabaseError(e)
