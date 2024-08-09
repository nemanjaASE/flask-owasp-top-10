from app.models.reset_token import ResetToken
from app.models.confirm_token import ConfirmToken
from app.repositories.reset_token_repository import ResetTokenRepository
from app.repositories.confirm_token_repository import ConfirmTokenRepository
from app.services.user_service import UserService
from app.utils import token_utils
from app.services.exceptions import *
from app.repositories.exceptions import *

class TokenService:
    def __init__(self, reset_token_repository: ResetTokenRepository, confirm_token_repository: ConfirmTokenRepository, user_service: UserService, s):
        self.reset_token_repository = reset_token_repository
        self.confirm_token_repository = confirm_token_repository
        self.user_service = user_service
        self.s = s

    def get_reset_token(self, reset_token: str) -> ResetToken:
        if not reset_token or not isinstance(reset_token, str):
            raise ValueError("Invalid reset token")
        
        try:
            token = self.reset_token_repository.get_by_name(reset_token)
            return token
        except NotFoundError as e:
            raise EntityNotFoundError("Reset Token", "name", reset_token)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    
    def verify_reset_token(self, reset_token: str) -> str:
        try:
            token = self.get_reset_token(reset_token)

            if token.used:
                raise TokenException("The reset token has already been used.")
            email = token_utils.verify_email_token(token.token, self.s)
            return token, email
        except EntityNotFoundError as e:
            raise e
        except DatabaseServiceError as e:
            raise e

    def add_reset_token(self, reset_token: str, user_id: str) -> ResetToken:
       if not reset_token or not isinstance(reset_token, str):
            raise ValueError("Invalid reset token")
       if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user ID")
       
       new_token = ResetToken(token=reset_token, user_id=user_id)

       try:
            return self.reset_token_repository.create(new_token)
       except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def set_reset_used(self, token: ResetToken) -> ResetToken:
        try:
            return self.reset_token_repository.update(token.id, used=True)
        except NotFoundError as e:
            raise EntityNotFoundError("Reset Token", "ID", token.id)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e
        
    def add_confirm_token(self, confirm_token: str, user_id: str) -> ConfirmToken:
       if not confirm_token or not isinstance(confirm_token, str):
            raise ValueError("Invalid confirm token")
       if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user ID")
       
       new_token = ConfirmToken(token=confirm_token, user_id=user_id)

       try:
            return self.confirm_token_repository.create(new_token)
       except DatabaseError as e:
            raise DatabaseServiceError(e) from e
       
    def verify_confirm_token(self, confirm_token: str) -> str:
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
        if not confirm_token or not isinstance(confirm_token, str):
            raise ValueError("Invalid confirm token")
        
        try:
            token = self.confirm_token_repository.get_by_name(confirm_token)
            return token
        except NotFoundError as e:
            raise EntityNotFoundError("Confirm Token", "name", confirm_token)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

