from flask import url_for
from flask_mail import Message
from app.services.user_service import UserService
from app.utils import token_utils
from app.services.reset_token_service import ResetTokenService

from app.services.exceptions import *
from app.repositories.exceptions import *

from time import time, sleep

class EmailService:
    def __init__(self, reset_token_service: ResetTokenService, user_service: UserService, mail, s):
        self.reset_token_service = reset_token_service
        self.user_service = user_service
        self.mail = mail
        self.s = s

    def send_reset_email(self, email: str):
        if not email:
            raise InvalidParameterException("email", "Invalid or missing parameter")
        try:
            user = self.user_service.get_user_by_email(email)

            start_time = time()

            token = token_utils.generate_token(email, self.s)
            self.reset_token_service.add_token(token, user.id)

            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'''To reset your password, visit the following link:
            {reset_url}

            If you did not make this request then simply ignore this email and no changes will be made.
            '''
            self.mail.send(msg)

            elapsed_time = time() - start_time
            remaining_time = max(0, 2 - elapsed_time)
            sleep(remaining_time)
        except InvalidParameterException as e:
            raise e
        except EntityNotFoundError as e:
            raise e
        except DatabaseServiceError as e:
            sleep(2)
            raise e
       