from itsdangerous import SignatureExpired, BadSignature
from app.utils import token_utils
from app.services.exceptions.invalid_input_exception import InvalidInputException

class OTPTokenService:
    def __init__(self, s):
        self.s = s

    def verify_otp_token(self, otp_token: str) -> str:
        if not otp_token:
            raise InvalidInputException('otp token', 'Invalid or missing parameter')

        try:
            otp = token_utils.verify_otp_token(otp_token, self.s)
            return otp
        except (SignatureExpired, BadSignature, Exception) as e:
            raise e