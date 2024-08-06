from app.models.author_requests import AuthorRequests
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.exceptions import DatabaseError 
from app.db import db

from app.repositories.exceptions import NotFoundError, DatabaseError 

class AuthorRequestsRepository(BaseRepository[AuthorRequests]):
    def __init__(self) -> None:
        super().__init__(AuthorRequests)

    def check_request(self, user_id: str) -> bool:
        try:
            request = AuthorRequests.query.filter_by(user_id=user_id).first()
            return request is None or request.status != 'InProgress'
        except SQLAlchemyError as e:
            raise DatabaseError(e)
        
    def update_request(self, request_id: str, status: str) -> AuthorRequests:
        try:
            db.session.begin()

            request = AuthorRequests.query.get(request_id)
            if not request:
                db.session.rollback()
                raise NotFoundError(AuthorRequests.__name__, request_id)
            else:
                setattr(request, 'status', status)    

            user_id = request.user_id

            user = User.query.get(user_id)
            if not user:
                db.session.rollback()
                raise NotFoundError(User.__name__, user_id)
            else:
                setattr(user, 'role', 'Author')

            db.session.commit()

            return request
        except DatabaseError as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()