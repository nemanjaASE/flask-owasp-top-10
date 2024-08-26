import requests

from app.services.exceptions.invalid_input_exception import InvalidInputException

class RecaptchaService():
    def __init__(self):
        self.recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'

    def verify_token(self, recaptcha_token: str, recaptcha_secret: str) -> bool:
        if not recaptcha_token:
            raise InvalidInputException("reacaptcha token", "Invalid or missing parameter")
        
        if not recaptcha_secret:
            raise InvalidInputException("reacaptcha secret", "Invalid or missing parameter")

        response = requests.post(self.recaptcha_url, data={
            'secret': recaptcha_secret,
            'response': recaptcha_token
        })

        result = response.json()
        return False if not result.get('success') else True
