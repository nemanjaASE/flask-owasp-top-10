from app.models.reset_token import ResetToken
from app.repositories.reset_token_repository import ResetTokenRepository

from app.utils import token_utils
from app.services.exceptions import *
from app.repositories.exceptions import *

class ResetTokenService:
    def __init__(self, reset_token_repository: ResetTokenRepository, s):
        self.reset_token_repository = reset_token_repository
        self.s = s

    def get_token(self, reset_token: str) -> ResetToken:
        if not reset_token or not isinstance(reset_token, str):
            raise ValueError("Invalid reset token")
        
        try:
            token = self.reset_token_repository.get_by_name(reset_token)
            return token
        except NotFoundError as e:
            raise EntityNotFoundError("Reset Token", "name", reset_token)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    
    def verify_token(self, reset_token: str) -> str:
        try:
            token = self.get_token(reset_token)

            if token.used:
                raise ResetTokenException("The token has already been used.")
            email = token_utils.verify_email_token(token.token, self.s)
            return token, email
        except EntityNotFoundError as e:
            raise e
        except DatabaseServiceError as e:
            raise e

    def add_token(self, reset_token: str, user_id: str) -> ResetToken:
       if not reset_token or not isinstance(reset_token, str):
            raise ValueError("Invalid reset token")
       if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user ID")
       
       new_token = ResetToken(token=reset_token, user_id=user_id)

       try:
            return self.reset_token_repository.create(new_token)
       except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def set_used(self, token: ResetToken) -> ResetToken:
        try:
            return self.reset_token_repository.update(token.id, used=True)
        except NotFoundError as e:
            raise EntityNotFoundError("Reset Token", "ID", token.id)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e
