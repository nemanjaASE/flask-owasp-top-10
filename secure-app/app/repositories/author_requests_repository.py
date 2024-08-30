from app.models.author_requests import AuthorRequests
from app.repositories.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.services.exceptions import DatabaseServiceError
from app.repositories.exceptions import DatabaseError, NotFoundError
from app.db import transaction
from sqlalchemy.exc import SQLAlchemyError

class AuthorRequestsRepository(BaseRepository[AuthorRequests]):
    def __init__(self) -> None:
        super().__init__(AuthorRequests)

    def check_request(self, user_id: str) -> bool:
        try:
            request = AuthorRequests.query.filter_by(user_id=user_id).first()
            return request is None or request.status != 'InProgress'
        except SQLAlchemyError as e:
            raise DatabaseError(e)
        
    # def update_request(self, request_id: str, status: str) -> AuthorRequests:
    #     try:
    #         request = AuthorRequests.query.get(request_id)
    #         if not request:
    #             raise NotFoundError(AuthorRequests.__name__, request_id)
        
    #         request.status = status

    #         user_id = request.user_id

    #         user = User.query.get(user_id)
    #         if not user:
    #             raise NotFoundError(User.__name__, user_id)

    #         user.role = 'Author'

    #         db.session.commit()

    #         return request

    #     except DatabaseError as e:
    #         db.session.rollback()
    #         raise e

    def update_request(self, request_id: str, status: str) -> AuthorRequests:
        try:
            with transaction():
                request = AuthorRequests.query.get(request_id)
                if not request:
                    raise NotFoundError(AuthorRequests.__name__, request_id)
            
            # Proverite da li je status validan (opciono, zavisi od konteksta)
            # if status not in VALID_STATUS_LIST:
            #     raise InvalidInputException("Invalid status value")

                request.status = status

                user_id = request.user_id
                user = User.query.get(user_id)
                if not user:
                    raise NotFoundError(User.__name__, user_id)

                user.role = 'Author'

                return request

        except SQLAlchemyError as e:
            raise DatabaseServiceError("An error occurred while updating the request.") from e
        except Exception as e:
            raise e
