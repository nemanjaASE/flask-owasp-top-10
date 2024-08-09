from flask import url_for
from flask_mail import Message
from app.services.user_service import UserService
from app.utils import token_utils, otp_utils
from app.services.token_service import TokenService

from app.services.exceptions import *
from app.repositories.exceptions import *

from time import time, sleep
import random

class EmailService:
    def __init__(self, token_service: TokenService, user_service: UserService, mail, s):
        self.token_service = token_service
        self.user_service = user_service
        self.mail = mail
        self.s = s

    def send_reset_email(self, email: str):
        if not email:
            raise InvalidParameterException("email", "Invalid or missing parameter")
        try:
            user = self.user_service.get_user_by_email(email)

            start_time = time()

            token = token_utils.generate_email_token(email, self.s)
            self.token_service.add_reset_token(token, user.id)

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
        
    def send_otp(self, email: str):
       if not email:
            raise InvalidParameterException("email", "Invalid or missing parameter")
       try:
            otp, generated_time = otp_utils.generate_otp()
            otp_token = token_utils.generate_otp_token(otp, self.s)
            msg = Message('Your OTP for Two-Factor Authentication', recipients=[email])
            msg.body = f'Your OTP is: {otp}'
            self.mail.send(msg)
            return otp_token, generated_time
       except InvalidParameterException as e:
            raise e
       
    def send_confrimation_email(self, email: str):
        if not email:
            raise InvalidParameterException("email", "Invalid or missing parameter")
        try:
            user = self.user_service.get_user_by_email(email)

            token = token_utils.generate_email_token(email, self.s)
            self.token_service.add_confirm_token(token, user.id)

            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            msg = Message('Confirm Your Email', recipients=[email])
            msg.body = f'''Please click this link to confirm your email: {confirm_url}

            If you did not make this request then simply ignore this email and no changes will be made.
            '''
            self.mail.send(msg)

        except InvalidParameterException as e:
            raise e
        except EntityNotFoundError as e:
            raise e
        except DatabaseServiceError as e:
            raise e