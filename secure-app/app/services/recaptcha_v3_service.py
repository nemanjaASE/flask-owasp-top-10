import requests

class RecaptchaService():
    def __init__(self):
        self.recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'

    def verify_token(self, recaptcha_token: str, recaptcha_secret: str) -> bool:
        response = requests.post(self.recaptcha_url, data={
            'secret': recaptcha_secret,
            'response': recaptcha_token
        })

        result = response.json()
        return False if not result.get('success') else True
