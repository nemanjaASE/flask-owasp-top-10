from itsdangerous import SignatureExpired, BadSignature

def generate_token(email, s):
    return s.dumps(email, salt='email-confirm-salt')

def verify_token(token, s):
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
        return email
    except SignatureExpired:
        raise SignatureExpired("The token has expired.")
    except BadSignature:
        raise BadSignature("The token is invalid.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")