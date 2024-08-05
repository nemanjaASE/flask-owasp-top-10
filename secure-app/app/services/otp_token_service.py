from itsdangerous import SignatureExpired, BadSignature
from app.utils import token_utils

class OTPTokenService:
    def __init__(self, s):
        self.s = s

    def verify_otp_token(self, otp_token: str) -> str:
        try:
            otp = token_utils.verify_otp_token(otp_token, self.s)
            return otp
        except (SignatureExpired, BadSignature, Exception) as e:
            raise e