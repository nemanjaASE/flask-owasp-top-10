from app.services import UserService

from app.models.confirm_token import ConfirmToken
from app.repositories.confirm_token_repository import ConfirmTokenRepository
from app.utils import token_utils
from app.services.exceptions import DatabaseServiceError, InvalidInputException, EntityNotFoundError
from app.repositories.exceptions import *

class ConfirmTokenService:
    def __init__(self, confirm_token_repository: ConfirmTokenRepository, user_service: UserService, s):
        self.confirm_token_repository = confirm_token_repository
        self.user_service = user_service
        self.s = s

    def add_confirm_token(self, confirm_token: str, user_id: str) -> ConfirmToken:
       if not confirm_token:
            raise InvalidInputException("confirm token", "Invalid or missing parameter")
       
       if not user_id:
            raise InvalidInputException("user id", "Invalid or missing parameter")
       
       new_token = ConfirmToken(token=confirm_token, user_id=user_id)

       try:
            return self.confirm_token_repository.create(new_token)
       except DatabaseError as e:
            raise DatabaseServiceError(e) from e
       
    def verify_confirm_token(self, confirm_token: str) -> str:
        if not confirm_token:
            raise InvalidInputException("confirm token", "Invalid or missing parameter")
        
        try:
            token = self.get_confirm_token(confirm_token)
            
            email = token_utils.verify_account_token(token.token, self.s)

            user = self.user_service.get_user_by_email(email)
            self.user_service.verify_user(user.id)

            return token, email
        except EntityNotFoundError as e:
            raise e
        except DatabaseServiceError as e:
            raise e
        
    def get_confirm_token(self, confirm_token: str) -> ConfirmToken:
        if not confirm_token:
            raise InvalidInputException("confirm token", "Invalid or missing parameter")
        
        try:
            token = self.confirm_token_repository.get_by_name(confirm_token)
            return token
        except NotFoundError as e:
            raise EntityNotFoundError("Confirm Token", "name", confirm_token)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e