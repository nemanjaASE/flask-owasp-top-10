from app.models.confirm_token import ConfirmToken
from app.repositories.base_repository import BaseRepository

from sqlalchemy.exc import SQLAlchemyError
from app.repositories.exceptions import NotFoundError, DatabaseError 

class ConfirmTokenRepository(BaseRepository[ConfirmToken]):
    def __init__(self) -> None:
        super().__init__(ConfirmToken)

    def get_by_name(self, token: str) -> ConfirmToken:
        try:
            confirm_token =  ConfirmToken.query.filter_by(token=token).first()
            if confirm_token is None:
                raise NotFoundError(self.model.__name__, token)
            return confirm_token
        except SQLAlchemyError as e:
            raise DatabaseError(e)
