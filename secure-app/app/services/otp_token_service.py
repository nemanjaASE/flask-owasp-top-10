from itsdangerous import SignatureExpired, BadSignature
from app.utils import token_utils
from app.services.exceptions import InvalidInputException, TokenExpiredException, TokenBadSignatureException

class OTPTokenService:
    def __init__(self, s):
        self.s = s

    def verify_otp_token(self, otp_token: str) -> str:
        if not otp_token:
            raise InvalidInputException('otp token', 'Invalid or missing parameter')

        try:
            otp = token_utils.verify_otp_token(otp_token, self.s)
            return otp
        except BadSignature as e:
            raise TokenBadSignatureException(f"Invalid token ({otp_token}) signature.")
        except SignatureExpired as e:
            expired_at = e.date_signed + self.s.max_age
            raise TokenExpiredException(f"Token ({otp_token}) expired at {expired_at}")
        except Exception as e:
            raise e