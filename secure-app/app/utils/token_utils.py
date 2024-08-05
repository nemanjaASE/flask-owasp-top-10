from itsdangerous import SignatureExpired, BadSignature

def generate_email_token(email, s):
    return s.dumps(email, salt='email-confirm-salt')

def verify_email_token(token, s, expiration=3600):
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=expiration)
        return email
    except SignatureExpired:
        raise SignatureExpired("The email token has expired.")
    except BadSignature:
        raise BadSignature("The email token is invalid.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    
def generate_otp_token(email, s):
    return s.dumps(email, salt='otp-confirm-salt')

def verify_otp_token(token, s, expiration=60):
    try:
        otp = s.loads(token, salt='otp-confirm-salt', max_age=expiration)
        return otp
    except SignatureExpired:
        raise SignatureExpired("The OTP token has expired.")
    except BadSignature:
        raise BadSignature("The OTP token is invalid.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")